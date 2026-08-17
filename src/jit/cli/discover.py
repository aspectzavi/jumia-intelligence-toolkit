from __future__ import annotations

from collections import Counter
from pathlib import Path

from rich.console import Console

from jit.cli.export import export_openapi
from jit.discovery.discovery_pipeline import DiscoveryPipeline
from jit.discovery.request_classifier import RequestClassifier
from jit.openapi.openapi_generator import OpenApiGenerator

console = Console()


async def run_discover(
    url: str,
    *,
    export_path: str | None,
    title: str,
    version: str,
) -> int:
    """
    Run API discovery against a URL and print a summary.

    Returns a process exit code (0 on success, 1 on failure).
    """

    console.print("[bold]Jumia Intelligence Toolkit[/bold]")
    console.print()
    console.print(f"Target:\n{url}")
    console.print()

    pipeline = DiscoveryPipeline()

    try:
        await pipeline.discover(url)
    except Exception as error:  # noqa: BLE001 - surfaced to the user
        console.print(f"[bold red]Discovery failed:[/bold red] {error}")
        return 1

    classification = Counter(
        RequestClassifier.classify(request).value
        for request in pipeline.last_requests
    )

    api_count = classification.get("api", 0) + classification.get("graphql", 0)
    tracking_count = classification.get("tracking", 0)
    asset_count = sum(classification.values()) - api_count - tracking_count

    console.print("[bold]Capture[/bold]")
    console.print("-" * 7)
    console.print(f"Requests:   {pipeline.last_request_count}")
    console.print(f"Responses:  {pipeline.last_response_count}")
    console.print()

    console.print("[bold]Discovery[/bold]")
    console.print("-" * 9)
    console.print(f"Endpoints:  {len(pipeline)}")
    console.print(f"API:        {api_count}")
    console.print(f"Assets:     {asset_count}")
    console.print(f"Tracking:   {tracking_count}")
    console.print()

    schema_count = sum(
        1 for endpoint in pipeline.endpoints if endpoint.response_schema is not None
    )
    example_count = sum(len(endpoint.examples) for endpoint in pipeline.endpoints)

    console.print("[bold]Analysis[/bold]")
    console.print("-" * 8)
    console.print(f"Schemas:    {schema_count}")
    console.print(f"Examples:   {example_count}")
    console.print()

    if export_path is not None:
        # Build OpenAPI directly from the already-populated mapper so we
        # don't trigger a second, redundant browser capture.
        document = OpenApiGenerator.generate(
            pipeline.mapper,
            title=title,
            version=version,
        )
        output = export_openapi(document, export_path)

        console.print("[bold]Export[/bold]")
        console.print("-" * 6)
        console.print(f"Format:     OpenAPI {document.openapi}")
        console.print(f"Output:     {Path(output).as_posix()}")
        console.print()

    console.print("[green]Discovery completed successfully.[/green]")
    return 0
