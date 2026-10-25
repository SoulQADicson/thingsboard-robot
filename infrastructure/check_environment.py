"""Check local Python dependencies without contacting ThingsBoard."""

import argparse
import importlib
import sys
from importlib.metadata import version
from pathlib import Path


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--browser", action="store_true", help="Launch headless Chromium")
    args = parser.parse_args()
    print(f"Python: {sys.version.split()[0]}")
    print(f"Interpreter: {sys.executable}")
    modules = {
        "robotframework": "robot",
        "robotframework-browser": "Browser",
        "robotframework-requests": "RequestsLibrary",
        "psycopg": "psycopg",
    }
    failures = 0
    requirements = Path(__file__).resolve().parents[1] / "requirements.txt"
    for line in requirements.read_text(encoding="utf-8").splitlines():
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        # This project's requirements file contains only exact direct pins.
        requirement, expected = line.split("==", 1)
        package = requirement.split("[", 1)[0]
        try:
            installed = version(package)
            importlib.import_module(modules[package])
            if installed != expected:
                raise RuntimeError(f"expected {expected}, installed {installed}")
            print(f"OK: {package}=={installed} (import successful)")
        except Exception as error:
            failures += 1
            print(f"FAIL: {package}: {error}")

    if args.browser:
        browser = None
        try:
            from Browser import Browser

            browser = Browser()
            browser.new_browser(browser="chromium", headless=True)
            print("OK: Chromium headless launched")
        except Exception as error:
            failures += 1
            print(f"FAIL: Chromium: {error}")
        finally:
            if browser is not None:
                try:
                    browser.close_browser()
                except Exception as error:
                    failures += 1
                    print(f"FAIL: browser cleanup: {error}")

    print(f"Environment checks: {failures} failure(s)")
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
