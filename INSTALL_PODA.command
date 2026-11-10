#!/bin/bash
set -euo pipefail
cd "$(dirname "$0")"
printf 'PODA %s — clean public Mac installation\n' "$(cat PODA_VERSION.txt)"
chmod +x ./*.command
printf '\n1/2: Python, local inference engine and encryption verification\n'
./setup_poda.command
printf '\n2/2: source and isolated smoke verification\n'
./VERIFY_PODA.command
printf '\nInstall complete. Run ./start_poda.command, then download GGUF models in System.\n'
