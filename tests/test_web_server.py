import os
import subprocess
import sys
import time

import httpx
import pytest

from poda_app.runtime import config, instance


def test_directory_lease_releases_on_exit(tmp_path, monkeypatch):
    monkeypatch.setattr(config, "DATA_DIR", tmp_path)
    monkeypatch.setattr(config, "BACKUP_DIR", tmp_path / "backups")
    monkeypatch.setattr(config, "LOG_DIR", tmp_path / "logs")
    with instance.claim_data_directory():
        with pytest.raises(RuntimeError, match="already in use"):
            with instance.claim_data_directory():
                pass
    with instance.claim_data_directory():
        pass


def test_web_start_opens_browser_session_on_loopback(tmp_path):
    env = dict(os.environ, PODA_DATA_DIR=str(tmp_path), PODA_BACKUP_DIR=str(tmp_path / "backups"),
               PODA_DB_ENCRYPTION="off")
    log_path = tmp_path / "server.log"
    with log_path.open("w", encoding="utf-8") as log:
        child = subprocess.Popen([sys.executable, "-m", "poda_app.server", "--port", "0"], env=env,
                                 stdout=log, stderr=log, stdin=subprocess.DEVNULL)
        try:
            deadline = time.monotonic() + 25
            url = None
            while time.monotonic() < deadline and child.poll() is None:
                url = next((line.rsplit(" ", 1)[-1] for line in log_path.read_text(errors="replace").splitlines()
                            if line.startswith("PODA Web listening on ")), None)
                if url:
                    break
                time.sleep(.05)
            assert url and url.startswith("http://127.0.0.1:"), log_path.read_text(errors="replace")
            with httpx.Client(base_url=url, trust_env=False, timeout=1) as client:
                while time.monotonic() < deadline:
                    try:
                        assert client.get("/memory").status_code == 401
                        break
                    except httpx.RequestError:
                        time.sleep(.05)
                else:
                    pytest.fail(log_path.read_text(errors="replace"))
                assert client.get("/").status_code == 200
                assert client.get("/memory").status_code == 200
                assert client.get("/memory", headers={"Origin": "https://example.test"}).status_code == 403
        finally:
            if child.poll() is None:
                child.terminate()
            try:
                child.wait(timeout=12)
            except subprocess.TimeoutExpired:
                child.kill()
                child.wait(timeout=3)
