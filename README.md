# PODA Web

Run PODA on your computer and open it in a browser. This repository owns the application UI, API, memory, connectors, and browser launchers. The desktop repositories package an exact revision of the shared application.

## Start locally

| Platform | Setup | Start |
| --- | --- | --- |
| macOS Apple Silicon | Install Python 3.11 or newer and run `./setup_poda.command` | Run `./start_poda.command` |
| Windows x64 | Install x64 Python 3.12 with the Python Launcher and run `Setup-PODA.cmd` | Run `Start-PODA.cmd` |

Open [PODA Web on loopback](http://127.0.0.1:8787). Keep the server running for scheduled automations. On Windows use Ctrl+C in the server window to stop it. On macOS run `./STOP_PODA.command` from the same checkout. Set `PODA_PORT` before starting to use another port.

Install Ollama for local chat and embeddings. Pull the starter models with `ollama pull llama3.2:3b` and `ollama pull nomic-embed-text`.

The launch scripts install the pinned chat preview assets on first use. After that, diagrams, equations, code highlighting, and sandbox image previews work offline. For a manual server launch, run `python -m poda_app.runtime.chat_renderers` once in the PODA environment.

## Data and integrations

PODA Web uses `~/Library/Application Support/PODA-Web` on macOS and `%LOCALAPPDATA%\PODA-Web` on Windows, with separate OS credentials. Create encrypted backups from Privacy. Browser hosting and desktop each keep their own data and connector setup by default.

Mail supports Gmail and the platform's native connector, Apple Mail or Classic Outlook. Notion, graph memory, workflow approvals, projects, and Daily Automation are available from the browser.

For installed apps, see [PODA for Mac](https://github.com/fennokw/PODA) and [PODA for Windows](https://github.com/fennokw/PODA-Windows).

The upstream PODA source is distributed under [LICENSE-PODA](LICENSE-PODA). This repository's license is in [LICENSE](LICENSE).

Daily Automation resolves email event dates against the original send time, then verifies authorized Notion additions. To use the same read-only scheduling tools from an MCP client, run `python -m poda_app.scheduling.mcp` over stdio from the source folder with the PODA Python environment.

Use **Personalize → Memory search with Hindsight** to install and enable the local search engine. Setup uses an installed Ollama chat model and the PODA embedding model. Hindsight keeps a derived index in the app's data folder. **Add-ons** contains the downloadable program catalog and saved skills. Program tools require a separate trust opt-in and per-tool enable switch. **Developer mode** in the toolbar reveals technical diagnostics.

In Chat, choose **Attach files**, drop files into the chat, or paste a screenshot. Files are shared with that message only. PODA can inspect source ZIPs and text-based PDFs and return edited copies. A revised PDF uses PODA’s document layout. To read images, install a local vision model such as `qwen3-vl:4b` from **System → Model installer and profile selection**.
