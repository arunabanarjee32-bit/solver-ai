"""Exercise real JWT signatures and fail-closed fixed-JWKS identity validation."""

import asyncio
import time

import httpx
import jwt
import pytest
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey
from starlette.requests import Request

from solver_api.features.identity import verification as auth
from solver_api.http.errors import APIError


def request(headers=None):
    return Request(
        {
            "type": "http",
            "method": "GET",
            "path": "/private",
            "headers": [
                (name.lower().encode(), value.encode()) for name, value in (headers or {}).items()
            ],
        }
    )


def public_jwk(key, kid="test-key"):
    return {
        "kty": "OKP",
        "crv": "Ed25519",
        "kid": kid,
        "alg": "EdDSA",
        "use": "sig",
        "x": jwt.utils.base64url_encode(
            key.public_key().public_bytes(
                serialization.Encoding.Raw, serialization.PublicFormat.Raw
            )
        ).decode(),
    }


@pytest.fixture(autouse=True)
def reset_cache(monkeypatch):
    auth.clear_auth_cache()
    monkeypatch.setenv("AUTH_ISSUER", "http://127.0.0.1:3000")
    monkeypatch.setenv("AUTH_JWKS_URL", "http://127.0.0.1:3000/api/auth/jwks")
    yield
    auth.clear_auth_cache()


@pytest.fixture
def issuer(monkeypatch):
    key = Ed25519PrivateKey.generate()
    fetched_urls = []

    async def fetch(url):
        fetched_urls.append(url)
        return {"keys": [public_jwk(key)]}

    monkeypatch.setattr(auth, "_fetch_jwks", fetch)

    def token(changes=None, remove=(), headers=None, signing_key=None):
        now = int(time.time())
        claims = {
            "sub": "user_123",
            "iss": "http://127.0.0.1:3000",
            "aud": "solver-api",
            "iat": now,
            "exp": now + 300,
            "token_use": "solver_api",
            **(changes or {}),
        }
        for name in remove:
            claims.pop(name, None)
        return jwt.encode(
            claims,
            signing_key or key,
            algorithm="EdDSA",
            headers={"kid": "test-key", **(headers or {})},
        )

    return token, key, fetched_urls


def authenticate(token):
    return asyncio.run(auth.require_user(request({"Authorization": f"Bearer {token}"})))


def assert_unauthorized(token):
    with pytest.raises(APIError) as error:
        authenticate(token)
    assert error.value.status == 401
    assert error.value.code == "UNAUTHORIZED"
    assert error.value.headers == {"WWW-Authenticate": "Bearer"}


def test_valid_signature_resolves_immutable_id_and_reuses_fixed_jwks(issuer):
    token, _, urls = issuer
    assert authenticate(token()) == "user_123"
    assert authenticate(token()) == "user_123"
    assert urls == ["http://127.0.0.1:3000/api/auth/jwks"]


@pytest.mark.parametrize(
    "headers",
    [
        {},
        {"Cookie": "session=user_123", "X-User-ID": "user_123"},
        {"Authorization": "Basic user_123"},
        {"Authorization": "Bearer "},
        {"Authorization": "Bearer one two"},
        {"Authorization": "Bearer " + "a" * 8193},
    ],
)
def test_identity_does_not_come_from_unverified_headers(headers):
    with pytest.raises(APIError) as error:
        asyncio.run(auth.require_user(request(headers)))
    assert error.value.status == 401


def test_duplicate_authorization_header_is_rejected(issuer):
    token, _, urls = issuer
    incoming = request({"Authorization": f"Bearer {token()}"})
    incoming.scope["headers"].append((b"authorization", f"Bearer {token()}".encode()))
    with pytest.raises(APIError) as error:
        asyncio.run(auth.require_user(incoming))
    assert error.value.status == 401
    assert not urls


@pytest.mark.parametrize(
    "changes",
    [
        {"iss": "https://attacker.invalid"},
        {"aud": "another-service"},
        {"aud": ["solver-api", "another-service"]},
        {"exp": int(time.time()) - 10},
        {"iat": int(time.time()) + 20},
        {"sub": "user with spaces"},
        {"sub": 123},
        {"sub": ""},
        {"token_use": "session"},
        {"exp": int(time.time()) + 3600},
        {"iat": str(int(time.time()))},
        {"exp": float(int(time.time()) + 300)},
    ],
)
def test_invalid_claims_are_rejected(issuer, changes):
    token, _, _ = issuer
    assert_unauthorized(token(changes=changes))


@pytest.mark.parametrize("claim", ["exp", "iat", "sub", "iss", "aud", "token_use"])
def test_required_claims_cannot_be_missing(issuer, claim):
    token, _, _ = issuer
    assert_unauthorized(token(remove=(claim,)))


def test_forged_signature_cannot_impersonate_account(issuer):
    token, _, _ = issuer
    assert_unauthorized(token(signing_key=Ed25519PrivateKey.generate()))


def test_algorithm_is_fixed_before_any_key_fetch(issuer):
    _, _, urls = issuer
    forged = jwt.encode(
        {"sub": "user_123"},
        "attacker-controlled-long-enough-key!",
        "HS256",
        headers={"kid": "test-key"},
    )
    assert_unauthorized(forged)
    assert not urls


@pytest.mark.parametrize(
    "header",
    [
        {"kid": None},
        {"kid": "x" * 129},
        {"jku": "https://attacker.invalid/jwks"},
        {"x5u": "https://attacker.invalid/cert"},
        {"crit": ["custom"]},
    ],
)
def test_token_headers_cannot_change_key_source_or_verification(issuer, header):
    token, _, urls = issuer
    if header.get("kid", "") is None:
        # PyJWT prevents malformed headers during signing, so omit kid manually.
        encoded = jwt.encode({"sub": "user_123"}, issuer[1], algorithm="EdDSA", headers={})
    else:
        encoded = token(headers=header)
    assert_unauthorized(encoded)
    assert not urls


def test_unknown_key_ids_are_throttled_and_refresh_for_rotation(issuer, monkeypatch):
    token, key, urls = issuer
    assert authenticate(token()) == "user_123"
    for _ in range(4):
        assert_unauthorized(token(headers={"kid": "unknown-key"}))
    assert len(urls) == 1
    state = next(iter(auth._caches.values()))
    state.next_refresh_at = 0

    async def rotated_fetch(url):
        urls.append(url)
        return {"keys": [public_jwk(key), public_jwk(key, "rotated-key")]}

    monkeypatch.setattr(auth, "_fetch_jwks", rotated_fetch)
    assert authenticate(token(headers={"kid": "rotated-key"})) == "user_123"
    assert len(urls) == 2


def test_stale_keys_refresh_before_accepting_valid_signature(issuer):
    token, _, urls = issuer
    assert authenticate(token()) == "user_123"
    state = next(iter(auth._caches.values()))
    # A runner may have uptime under 60 seconds; zero is not necessarily stale.
    state.fetched_at = time.monotonic() - auth._CACHE_SECONDS - 1
    state.next_refresh_at = 0
    assert authenticate(token()) == "user_123"
    assert len(urls) == 2


def test_unreachable_jwks_fails_closed_with_retry_cooldown(issuer, monkeypatch):
    token, _, _ = issuer
    calls = []

    async def broken_fetch(url):
        calls.append(url)
        raise httpx.ConnectError("sensitive remote detail")

    monkeypatch.setattr(auth, "_fetch_jwks", broken_fetch)
    for _ in range(3):
        with pytest.raises(APIError) as error:
            authenticate(token())
        assert error.value.status == 503
        assert error.value.code == "AUTH_UNAVAILABLE"
        assert "sensitive" not in error.value.message
    assert len(calls) == 1


@pytest.mark.parametrize(
    "data", [{}, {"keys": []}, {"keys": "invalid"}, {"keys": [None]}, {"keys": [{"kty": "RSA"}]}]
)
def test_invalid_or_unsupported_jwks_is_not_used(issuer, monkeypatch, data):
    token, _, _ = issuer

    async def fetch(_url):
        return data

    monkeypatch.setattr(auth, "_fetch_jwks", fetch)
    with pytest.raises(APIError) as error:
        authenticate(token())
    assert error.value.status == 503


def test_concurrent_authentication_shares_one_key_fetch(issuer, monkeypatch):
    token, key, urls = issuer

    async def slow_fetch(url):
        urls.append(url)
        await asyncio.sleep(0.01)
        return {"keys": [public_jwk(key)]}

    monkeypatch.setattr(auth, "_fetch_jwks", slow_fetch)

    async def requests():
        return await asyncio.gather(
            *[auth.require_user(request({"Authorization": f"Bearer {token()}"})) for _ in range(8)]
        )

    assert asyncio.run(requests()) == ["user_123"] * 8
    assert len(urls) == 1
