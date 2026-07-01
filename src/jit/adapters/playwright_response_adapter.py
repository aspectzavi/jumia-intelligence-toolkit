from __future__ import annotations

from playwright.async_api import Response

from jit.adapters.header_adapter import HeaderAdapter
from jit.entities.header_collection import HeaderCollection
from jit.entities.http_response import HttpResponse
from jit.entities.request_timing import RequestTiming


class PlaywrightResponseAdapter:
    """
    Converts Playwright Response objects into HttpResponse entities.
    """

    @classmethod
    async def from_playwright(
        cls,
        response: Response,
        request_id: str,
    ) -> HttpResponse:
        """
        Convert a Playwright Response into a HttpResponse.
        """

        headers = await cls._extract_headers(response)
        body = await cls._extract_body(response)

        return HttpResponse(
            request_id=request_id,
            status=response.status,
            status_text=response.status_text,
            url=response.url,
            mime_type=headers.content_type,
            content_length=headers.content_length,
            body=body,
            headers=headers,
            timing=RequestTiming.start_now(),
        )

    @staticmethod
    async def _extract_headers(
        response: Response,
    ) -> HeaderCollection:
        """
        Convert Playwright headers.
        """

        raw_headers = await response.all_headers()

        return HeaderAdapter.from_mapping(raw_headers)

    @staticmethod
    async def _extract_body(
        response: Response,
    ) -> bytes | None:
        """
        Safely obtain the response body.
        """

        try:
            return await response.body()
        except Exception:
            return None
