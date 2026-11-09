# PODA Web security

The supported launcher binds to `127.0.0.1`. Browser sessions use an HTTP-only same-site cookie and protected routes validate origin. SQLCipher is required by default. Browser-hosted PODA uses a separate data directory and OS credential namespace, with macOS Keychain on macOS and Credential Manager on Windows.

Live connectors and file tools require their existing per-account or folder permissions. The service is intended for the signed-in user on this computer. Keep it on loopback.

Report a suspected vulnerability privately through this repository's Security tab.
