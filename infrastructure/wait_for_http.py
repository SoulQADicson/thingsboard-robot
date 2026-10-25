"""Wait for HTTP 200 with a bounded deadline; does not prove authentication."""

import argparse
import time
from urllib.error import URLError
from urllib.parse import urlsplit
from urllib.request import urlopen


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--url", required=True)
    parser.add_argument("--timeout", type=float, default=240)
    parser.add_argument("--interval", type=float, default=2)
    args = parser.parse_args()
    parsed = urlsplit(args.url)
    if parsed.scheme not in ("http", "https") or not parsed.netloc:
        parser.error("--url must be an HTTP(S) URL")
    if parsed.username or parsed.password:
        parser.error("--url must not contain credentials")
    if args.timeout <= 0 or args.interval <= 0:
        parser.error("--timeout and --interval must be positive")
    deadline = time.monotonic() + args.timeout
    last_error = "No response"
    while (remaining := deadline - time.monotonic()) > 0:
        try:
            with urlopen(args.url, timeout=min(5, remaining)) as response:
                if response.status == 200:
                    print("HTTP ready: status 200")
                    return 0
                last_error = f"HTTP {response.status}"
        except (URLError, TimeoutError, OSError) as error:
            last_error = str(error)
        remaining = deadline - time.monotonic()
        if remaining > 0:
            time.sleep(min(args.interval, remaining))
    print(f"HTTP readiness failed after {args.timeout:g}s: {last_error}")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
