"""Read at most a bounded request body before routing or parsing it."""

import asyncio
from uuid import uuid4

from starlette.responses import JSONResponse
from starlette.types import ASGIApp, Receive, Scope, Send

MAX_REQUEST_BYTES = 131_072


class BodyLimitMiddleware:
    def __init__(self, app: ASGIApp) -> None:
        self.app = app

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        if scope["type"] != "http":
            await self.app(scope, receive, send)
            return
        headers = dict(scope.get("headers", []))
        try:
            declared = int(headers.get(b"content-length", b"0"))
        except ValueError:
            declared = MAX_REQUEST_BYTES + 1
        if declared < 0 or declared > MAX_REQUEST_BYTES:
            await self._reject(scope, receive, send)
            return
        chunks = []
        size = 0
        try:
            async with asyncio.timeout(10):
                while True:
                    message = await receive()
                    if message["type"] == "http.disconnect":
                        return
                    chunk = message.get("body", b"")
                    size += len(chunk)
                    if size > MAX_REQUEST_BYTES:
                        await self._reject(scope, receive, send)
                        return
                    chunks.append(chunk)
                    if not message.get("more_body", False):
                        break
        except TimeoutError:
            await self._reject(scope, receive, send, status=408)
            return
        body = b"".join(chunks)
        consumed = False

        async def bounded_receive() -> dict:
            nonlocal consumed
            if not consumed:
                consumed = True
                return {"type": "http.request", "body": body, "more_body": False}
            return await receive()

        await self.app(scope, bounded_receive, send)

    @staticmethod
    async def _reject(scope: Scope, receive: Receive, send: Send, status: int = 413) -> None:
        request_id = scope.get("state", {}).get("request_id", uuid4().hex)
        response = JSONResponse(
            status_code=status,
            headers={"X-Request-ID": request_id, "X-Content-Type-Options": "nosniff"},
            content={
                "error": {
                    "code": "REQUEST_TOO_LARGE" if status == 413 else "REQUEST_TIMEOUT",
                    "message": "The request body exceeds the size limit."
                    if status == 413
                    else "The request body took too long to arrive.",
                },
                "request_id": request_id,
            },
        )
        await response(scope, receive, send)
