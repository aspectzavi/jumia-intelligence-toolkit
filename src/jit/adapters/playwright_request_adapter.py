from __future__ import annotations

from playwright.async_api import Request

from jit.adapters.cookie_adapter import CookieAdapter
from jit.adapters.header_adapter import HeaderAdapter
from jit.entities.header_collection import HeaderCollection
from jit.entities.http_cookie import HttpCookie
from jit.entities.http_request import HttpRequest
from jit.entities.request_timing import RequestTiming


class PlaywrightRequestAdapter:
    """
    Converts Playwright Request objects into HttpRequest entities.
    """

    @classmethod
    async def from_playwright(
        cls,
        request: Request,
    ) -> HttpRequest:
        """
        Convert a Playwright Request into a HttpRequest.
        """

        headers = await cls._extract_headers(request)

        cookies = cls._extract_cookies(headers)

        return HttpRequest(
            url=request.url,
            method=request.method,
            resource_type=request.resource_type,
            frame_url=cls._extract_frame_url(request),
            is_navigation=request.is_navigation_request(),
            post_data=cls._extract_post_data(request),
            headers=headers,
            cookies=cookies,
            timing=RequestTiming.start_now(),
        )

    @staticmethod
    async def _extract_headers(
        request: Request,
    ) -> HeaderCollection:
        """
        Convert Playwright headers.
        """

        raw_headers = await request.all_headers()

        return HeaderAdapter.from_mapping(raw_headers)

    @staticmethod
    def _extract_cookies(
        headers: HeaderCollection,
    ) -> list[HttpCookie]:
        """
        Extract cookies from the Cookie header.
        """

        cookie_header = headers.get("cookie")

        if cookie_header is None:
            return []

        return CookieAdapter.from_cookie_header(cookie_header)

    @staticmethod
    def _extract_frame_url(
        request: Request,
    ) -> str | None:
        """
        Safely obtain the frame URL.
        """

        try:
            return request.frame.url
        except Exception:
            return None

    @staticmethod
    def _extract_post_data(
        request: Request,
    ) -> str | None:
        """
        Safely obtain POST data.
        """

        try:
            return request.post_data
        except Exception:
            return None
