from collections.abc import Iterator
from pathlib import Path
import subprocess
import sys
import time
from urllib.error import URLError
from urllib.request import urlopen

import pytest


APP_URL = "http://127.0.0.1:8000/"
STARTUP_TIMEOUT_SECONDS = 15


def _app_is_available() -> bool:
    try:
        with urlopen(APP_URL, timeout=1):
            return True
    except URLError:
        return False


@pytest.fixture(scope="session", autouse=True)
def demo_app() -> Iterator[None]:
    process = None
    if not _app_is_available():
        project_root = Path(__file__).resolve().parents[1]
        process = subprocess.Popen(
            [sys.executable, "-m", "app.server"],
            cwd=project_root,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.STDOUT,
        )
        deadline = time.monotonic() + STARTUP_TIMEOUT_SECONDS
        while time.monotonic() < deadline:
            if process.poll() is not None:
                pytest.fail(
                    "The demo server exited during startup "
                    f"(exit code {process.returncode}); check whether port 8000 is available."
                )
            if _app_is_available():
                break
            time.sleep(0.1)
        else:
            process.terminate()
            process.wait(timeout=5)
            pytest.fail(
                f"The demo server did not become available at {APP_URL} "
                f"within {STARTUP_TIMEOUT_SECONDS} seconds."
            )

    yield

    if process is not None:
        process.terminate()
        try:
            process.wait(timeout=5)
        except subprocess.TimeoutExpired:
            process.kill()
            process.wait()
