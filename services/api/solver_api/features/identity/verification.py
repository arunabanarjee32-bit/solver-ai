"""Validate short-lived API tokens issued by the configured Better Auth instance.

Only a configured JWKS URL is contacted. Token headers cannot select a URL or an
algorithm, and no cookie or caller-provided user identifier establishes identity.
"""

import asyncio
import json
import os
import re
import time
from dataclasses import dataclass, field
from urllib.parse import urlsplit

import httpx
import jwt
from fastapi import Request

from solver_api.http.errors import APIError

_MAX_TOKEN_BYTES = 8192
_MAX_JWKS_BYTES = 65536
_MAX_JWKS_KEYS = 32
_CACHE_SECONDS = 60
_REFRESH_COOLDOWN_SECONDS = 5
_SUBJECT = re.compile(r"[A-Za-z0-9_-]{1,128}\Z")


@dataclass
class _KeyCache:
    keys: dict[str, jwt.PyJWK] = field(default_factory=dict)
    fetched_at: float = 0
    next_refresh_at: float = 0
    unavailable: bool = False
    lock: asyncio.Lock = field(default_factory=asyncio.Lock)


_caches: dict[str, _KeyCache] = {}


def clear_auth_cache() -> None:
    """Clear cached public keys after configuration changes and between tests."""
    _caches.clear()


def _unauthorized() -> APIError:
    return APIError(
        401,
        "UNAUTHORIZED",
        "Sign in to continue.",
        headers={"WWW-Authenticate": "Bearer"},
    )


def _unavailable() -> APIError:
    return APIError(503, "AUTH_UNAVAILABLE", "Account verification is temporarily unavailable.")


async def _fetch_jwks(url: str) -> dict:
    """Fetch a bounded public key document using inherited proxy and CA trust."""
    async with httpx.AsyncClient(
        timeout=httpx.Timeout(5, connect=2), follow_redirects=False, trust_env=True
    ) as client:
        async with client.stream("GET", url, headers={"Accept": "application/json"}) as response:
            response.raise_for_status()
            if int(response.headers.get("Content-Length", "0")) > _MAX_JWKS_BYTES:
                raise ValueError("Public key document exceeds its size limit")
            body = bytearray()
            async for chunk in response.aiter_bytes():
                body.extend(chunk)
                if len(body) > _MAX_JWKS_BYTES:
                    raise ValueError("Public key document exceeds its size limit")
    data = json.loads(body)
    if not isinstance(data, dict):
        raise ValueError("Invalid public key document")
    return data


def _parse_keys(data: dict) -> dict[str, jwt.PyJWK]:
    entries = data.get("keys")
    if not isinstance(entries, list) or not 1 <= len(entries) <= _MAX_JWKS_KEYS:
        raise ValueError("Invalid public key list")
    keys: dict[str, jwt.PyJWK] = {}
    for entry in entries:
        if not isinstance(entry, dict):
            raise ValueError("Invalid public key")
        # Never allow RSA/HMAC/another curve to select a different verifier.
        if (
            entry.get("kty") != "OKP"
            or entry.get("crv") != "Ed25519"
            or entry.get("alg", "EdDSA") != "EdDSA"
            or entry.get("use", "sig") != "sig"
        ):
            continue
        kid = entry.get("kid")
        if not isinstance(kid, str) or not 1 <= len(kid) <= 128 or kid in keys or "d" in entry:
            raise ValueError("Invalid public key identifier")
        if "key_ops" in entry and (
            not isinstance(entry["key_ops"], list) or "verify" not in entry["key_ops"]
        ):
            continue
        key = jwt.PyJWK.from_dict(entry, algorithm="EdDSA")
        if key.algorithm_name != "EdDSA":
            raise ValueError("Unexpected key algorithm")
        keys[kid] = key
    if not keys:
        raise ValueError("No supported public keys")
    return keys


async def _signing_key(url: str, kid: str) -> jwt.PyJWK:
    state = _caches.setdefault(url, _KeyCache())
    now = time.monotonic()
    if kid in state.keys and now - state.fetched_at < _CACHE_SECONDS:
        return state.keys[kid]
    async with state.lock:
        now = time.monotonic()
        if kid in state.keys and now - state.fetched_at < _CACHE_SECONDS:
            return state.keys[kid]
        if now < state.next_refresh_at:
            if state.unavailable or now - state.fetched_at >= _CACHE_SECONDS:
                raise _unavailable()
            raise _unauthorized()
        state.next_refresh_at = now + _REFRESH_COOLDOWN_SECONDS
        try:
            state.keys = _parse_keys(await _fetch_jwks(url))
        except (httpx.HTTPError, ValueError, TypeError, jwt.PyJWTError) as exc:
            state.unavailable = True
            raise _unavailable() from exc
        state.fetched_at = time.monotonic()
        state.unavailable = False
        if kid not in state.keys:
            raise _unauthorized()
        return state.keys[kid]


async def require_user(request: Request) -> str:
    """FastAPI dependency returning only the verified, immutable account ID."""
    authorization = request.headers.getlist("authorization")
    if len(authorization) != 1:
        raise _unauthorized()
    scheme, separator, token = authorization[0].partition(" ")
    if (
        not separator
        or scheme.casefold() != "bearer"
        or not token
        or len(token) > _MAX_TOKEN_BYTES
        or any(character.isspace() for character in token)
    ):
        raise _unauthorized()
    try:
        header = jwt.get_unverified_header(token)
    except jwt.PyJWTError as exc:
        raise _unauthorized() from exc
    kid = header.get("kid")
    if (
        header.get("alg") != "EdDSA"
        or not isinstance(kid, str)
        or not 1 <= len(kid) <= 128
        or any(key in header for key in ("jku", "x5u", "crit"))
    ):
        raise _unauthorized()
    issuer = os.environ.get("AUTH_ISSUER", "http://127.0.0.1:3000").rstrip("/")
    url = os.environ.get("AUTH_JWKS_URL", "http://127.0.0.1:3000/api/auth/jwks")
    configured = urlsplit(url)
    if (
        not issuer
        or configured.scheme not in {"http", "https"}
        or not configured.hostname
        or configured.username is not None
        or configured.password is not None
        or configured.fragment
    ):
        raise _unavailable()
    key = await _signing_key(url, kid)
    try:
        claims = jwt.decode(
            token,
            key.key,
            algorithms=["EdDSA"],
            issuer=issuer,
            audience="solver-api",
            options={
                "require": ["exp", "iat", "sub", "iss", "aud"],
                "strict_aud": True,
            },
        )
    except jwt.PyJWTError as exc:
        raise _unauthorized() from exc
    subject = claims.get("sub")
    issued_at, expires_at = claims.get("iat"), claims.get("exp")
    if (
        not isinstance(subject, str)
        or not _SUBJECT.fullmatch(subject)
        or claims.get("token_use") != "solver_api"
        or type(issued_at) is not int
        or type(expires_at) is not int
        or not 0 < expires_at - issued_at <= 300
    ):
        raise _unauthorized()
    return subject
