from __future__ import annotations

import asyncio

from jit.capture import CaptureRunner


async def main() -> None:
    runner = CaptureRunner()

    capture = await runner.capture(
        "https://www.jumia.co.ke/",
    )

    print(f"Requests : {capture.request_count}")
    print(f"Responses: {capture.response_count}")
    print(f"Endpoints: {capture.endpoint_count}")

    print()

    for endpoint in capture.endpoints:
        print(endpoint)


if __name__ == "__main__":
    asyncio.run(main())
