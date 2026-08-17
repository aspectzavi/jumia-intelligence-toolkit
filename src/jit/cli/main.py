from __future__ import annotations

import argparse
import asyncio
import sys

from jit.cli.discover import run_discover


def build_parser() -> argparse.ArgumentParser:
    """
    Build the top-level `jit` argument parser.
    """

    parser = argparse.ArgumentParser(
        prog="jit",
        description=(
            "Jumia Intelligence Toolkit - browser/API discovery toolkit."
        ),
    )

    subparsers = parser.add_subparsers(dest="command", required=True)

    discover_parser = subparsers.add_parser(
        "discover",
        help="Capture a website's network traffic and discover its API surface.",
    )
    discover_parser.add_argument("url", help="Target URL to visit and capture.")
    discover_parser.add_argument(
        "--export",
        dest="export_path",
        default=None,
        help="Export the discovered API as OpenAPI (.json, .yaml, or .yml).",
    )
    discover_parser.add_argument(
        "--title",
        default="Discovered API",
        help="Title used in the generated OpenAPI document.",
    )
    discover_parser.add_argument(
        "--api-version",
        dest="version",
        default="1.0.0",
        help="Version used in the generated OpenAPI document.",
    )

    return parser


def main(argv: list[str] | None = None) -> int:
    """
    CLI entry point registered as the `jit` console script.
    """

    parser = build_parser()
    args = parser.parse_args(argv)

    if args.command == "discover":
        return asyncio.run(
            run_discover(
                args.url,
                export_path=args.export_path,
                title=args.title,
                version=args.version,
            )
        )

    parser.print_help()
    return 1


if __name__ == "__main__":
    sys.exit(main())
