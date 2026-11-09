"""Run PODA Web in a browser on this computer."""
from __future__ import annotations

import argparse
import os
import socket


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--port", type=int, default=int(os.getenv("PODA_PORT", "8787")))
    args = parser.parse_args()
    if not 0 <= args.port <= 65535:
        parser.error("port must be between 0 and 65535")

    with socket.socket() as listener:
        if os.name == "nt":
            listener.setsockopt(socket.SOL_SOCKET, socket.SO_EXCLUSIVEADDRUSE, 1)
        else:
            listener.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        listener.bind(("127.0.0.1", args.port))
        listener.listen()
        port = listener.getsockname()[1]
        os.environ["PODA_PORT"] = str(port)

        import uvicorn
        from .main import app
        from .runtime.instance import claim_data_directory

        server = uvicorn.Server(uvicorn.Config(
            app, host="127.0.0.1", port=port, access_log=False, proxy_headers=False,
            server_header=False, timeout_graceful_shutdown=8,
        ))
        with claim_data_directory():
            print(f"PODA Web listening on http://127.0.0.1:{port}", flush=True)
            server.run(sockets=[listener])
        if not server.started:
            raise SystemExit(1)


if __name__ == "__main__":
    main()
