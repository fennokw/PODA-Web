# PODA Web

Run PODA on your computer and open it in a browser. This repository owns the application UI, API, memory, connectors, and browser launchers. The desktop repositories package an exact revision of the shared application.

## Start locally

| Platform | Setup | Start |
| --- | --- | --- |
| macOS Apple Silicon | Install Python 3.11 or newer and run `./setup_poda.command` | Run `./start_poda.command` |
| Windows x64 | Install x64 Python 3.12 with the Python Launcher and run `Setup-PODA.cmd` | Run `Start-PODA.cmd` |

Open [PODA Web on loopback](http://127.0.0.1:8787). Keep the server running for scheduled automations. On Windows use Ctrl+C in the server window to stop it. On macOS run `./STOP_PODA.command` from the same checkout. Set `PODA_PORT` before starting to use another port.

Install Ollama for local chat and embeddings. Pull the starter models with `ollama pull llama3.2:3b` and `ollama pull nomic-embed-text`.

## Data and integrations

PODA Web uses `~/Library/Application Support/PODA-Web` on macOS and `%LOCALAPPDATA%\PODA-Web` on Windows, with separate OS credentials. Create encrypted backups from Privacy. Browser hosting and desktop each keep their own data and connector setup by default.

Mail supports Gmail and the platform's native connector, Apple Mail or Classic Outlook. Notion, graph memory, workflow approvals, projects, and Daily Automation are available from the browser.

For installed apps, see [PODA for Mac](https://github.com/fennokw/PODA) and [PODA for Windows](https://github.com/fennokw/PODA-Windows).

The upstream PODA source is distributed under [LICENSE-PODA](LICENSE-PODA). This repository's license is in [LICENSE](LICENSE).

Daily Automation resolves email event dates against the original send time, then verifies authorized Notion additions. To use the same read-only scheduling tools from an MCP client, run `python -m poda_app.scheduling.mcp` over stdio from the source folder with the PODA Python environment.
