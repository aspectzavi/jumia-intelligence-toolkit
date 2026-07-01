from __future__ import annotations

from jit.core.enums import RequestType
from jit.discovery.request_classifier import RequestClassifier
from jit.entities.http_request import HttpRequest


def make_request(
    url: str,
    resource_type: str = "xhr",
) -> HttpRequest:
    return HttpRequest(
        url=url,
        resource_type=resource_type,
    )


def test_classifies_rest_api():
    request = make_request(
        "https://example.com/api/products",
    )

    assert (
        RequestClassifier.classify(request)
        == RequestType.API
    )


def test_classifies_v1_api():
    request = make_request(
        "https://example.com/v1/users",
    )

    assert (
        RequestClassifier.classify(request)
        == RequestType.API
    )


def test_classifies_v2_api():
    request = make_request(
        "https://example.com/v2/orders",
    )

    assert (
        RequestClassifier.classify(request)
        == RequestType.API
    )


def test_classifies_graphql():
    request = make_request(
        "https://example.com/graphql",
    )

    assert (
        RequestClassifier.classify(request)
        == RequestType.GRAPHQL
    )


def test_graphql_has_priority_over_api():
    request = make_request(
        "https://example.com/graphql/api",
    )

    assert (
        RequestClassifier.classify(request)
        == RequestType.GRAPHQL
    )


def test_classifies_document():
    request = make_request(
        "https://example.com",
        "document",
    )

    assert (
        RequestClassifier.classify(request)
        == RequestType.DOCUMENT
    )


def test_classifies_image():
    request = make_request(
        "https://example.com/logo.png",
        "image",
    )

    assert (
        RequestClassifier.classify(request)
        == RequestType.IMAGE
    )


def test_classifies_script():
    request = make_request(
        "https://example.com/app.js",
        "script",
    )

    assert (
        RequestClassifier.classify(request)
        == RequestType.SCRIPT
    )


def test_classifies_stylesheet():
    request = make_request(
        "https://example.com/site.css",
        "stylesheet",
    )

    assert (
        RequestClassifier.classify(request)
        == RequestType.STYLESHEET
    )


def test_classifies_font():
    request = make_request(
        "https://example.com/font.woff2",
        "font",
    )

    assert (
        RequestClassifier.classify(request)
        == RequestType.FONT
    )


def test_classifies_media():
    request = make_request(
        "https://example.com/video.mp4",
        "media",
    )

    assert (
        RequestClassifier.classify(request)
        == RequestType.MEDIA
    )


def test_google_analytics_is_tracking():
    request = make_request(
        "https://www.google-analytics.com/g/collect",
    )

    assert (
        RequestClassifier.classify(request)
        == RequestType.TRACKING
    )


def test_googletagmanager_is_tracking():
    request = make_request(
        "https://www.googletagmanager.com/gtm.js",
    )

    assert (
        RequestClassifier.classify(request)
        == RequestType.TRACKING
    )


def test_doubleclick_is_tracking():
    request = make_request(
        "https://doubleclick.net/collect",
    )

    assert (
        RequestClassifier.classify(request)
        == RequestType.TRACKING
    )


def test_facebook_tracking():
    request = make_request(
        "https://facebook.com/tr",
    )

    assert (
        RequestClassifier.classify(request)
        == RequestType.TRACKING
    )


def test_segment_tracking():
    request = make_request(
        "https://api.segment.io/v1/batch",
    )

    assert (
        RequestClassifier.classify(request)
        == RequestType.TRACKING
    )


def test_mixpanel_tracking():
    request = make_request(
        "https://api.mixpanel.com/track",
    )

    assert (
        RequestClassifier.classify(request)
        == RequestType.TRACKING
    )


def test_hotjar_tracking():
    request = make_request(
        "https://script.hotjar.com/modules.js",
    )

    assert (
        RequestClassifier.classify(request)
        == RequestType.TRACKING
    )


def test_clarity_tracking():
    request = make_request(
        "https://clarity.ms/tag",
    )

    assert (
        RequestClassifier.classify(request)
        == RequestType.TRACKING
    )


def test_unknown_resource_returns_other():
    request = make_request(
        "https://example.com/file.bin",
        "unknown",
    )

    assert (
        RequestClassifier.classify(request)
        == RequestType.OTHER
    )


def test_resource_type_is_case_insensitive():
    request = make_request(
        "https://example.com",
        "IMAGE",
    )

    assert (
        RequestClassifier.classify(request)
        == RequestType.IMAGE
    )


def test_api_has_priority_over_resource_type():
    request = make_request(
        "https://example.com/api/products",
        "document",
    )

    assert (
        RequestClassifier.classify(request)
        == RequestType.API
    )


def test_tracking_has_priority_over_document():
    request = make_request(
        "https://google-analytics.com/page",
        "document",
    )

    assert (
        RequestClassifier.classify(request)
        == RequestType.TRACKING
    )
