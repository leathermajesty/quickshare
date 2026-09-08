#!/usr/bin/env python3

import http.server
import os
import shutil
import subprocess
import tempfile
import threading


# Optional QR code support
try:
    import qrcode
    HAS_QRCODE = True
except ImportError:
    HAS_QRCODE = False


# ─────────────────────────────────────────────
# Terminal colors
# ─────────────────────────────────────────────

RESET = "\033[0m"
BOLD = "\033[1m"
CYAN = "\033[36m"
GREEN = "\033[32m"
YELLOW = "\033[33m"
RED = "\033[31m"
DIM = "\033[2m"


def get_en0_ip():
    return subprocess.check_output(
        ["ipconfig", "getifaddr", "en0"],
        text=True
    ).strip()


def format_size(size):
    """Convert bytes to a readable size."""
    units = ["B", "KB", "MB", "GB"]

    for unit in units:
        if size < 1024:
            return f"{size:.1f} {unit}"

        size /= 1024

    return f"{size:.1f} TB"


# ─────────────────────────────────────────────
# Header
# ─────────────────────────────────────────────

print(f"""
{CYAN}{BOLD}╭──────────────────────────────────────────╮
│                 QuickShare               │
│          Fast LAN File Sharing           │
╰──────────────────────────────────────────╯{RESET}
""")


# ─────────────────────────────────────────────
# Get files
# ─────────────────────────────────────────────

files = [
    f for f in os.listdir(".")
    if os.path.isfile(f)
]

if not files:
    print(f"{RED}✗ No files found.{RESET}")
    exit()


print(f"{BOLD}Available Files{RESET}")
print(f"{DIM}────────────────────────────────────────────{RESET}")

for i, f in enumerate(files, start=1):
    size = format_size(os.path.getsize(f))
    print(f"  {CYAN}[{i}]{RESET} {f:<35} {DIM}{size}{RESET}")

print(f"{DIM}────────────────────────────────────────────{RESET}")


# ─────────────────────────────────────────────
# Select file
# ─────────────────────────────────────────────

while True:
    try:
        choice = int(input("\nSelect file: "))

        if 1 <= choice <= len(files):
            break

        print(f"{YELLOW}Invalid choice.{RESET}")

    except ValueError:
        print(f"{YELLOW}Enter a valid number.{RESET}")


selected_file = files[choice - 1]
file_size = format_size(os.path.getsize(selected_file))


# ─────────────────────────────────────────────
# Network information
# ─────────────────────────────────────────────

PORT = 1234
ip = get_en0_ip()

url = f"http://{ip}:{PORT}/{selected_file}"
command = f"wget {url}"


# ─────────────────────────────────────────────
# Temporary directory
# ─────────────────────────────────────────────

tmpdir = tempfile.mkdtemp()

shutil.copy2(selected_file, tmpdir)

os.chdir(tmpdir)


# ─────────────────────────────────────────────
# Copy command to clipboard
# ─────────────────────────────────────────────

subprocess.run(
    ["pbcopy"],
    input=command,
    text=True
)


# ─────────────────────────────────────────────
# Sharing information
# ─────────────────────────────────────────────

print(f"""
{GREEN}{BOLD}✓ File ready to share{RESET}

  File      : {BOLD}{selected_file}{RESET}
  Size      : {file_size}
  IP        : {ip}
  Port      : {PORT}
""")


# ─────────────────────────────────────────────
# VM section
# ─────────────────────────────────────────────

print(f"{BOLD}VM / Linux{RESET}")
print(f"{DIM}────────────────────────────────────────────{RESET}")

print(f"  {YELLOW}{command}{RESET}")
print(f"  {GREEN}✓ Command copied to clipboard{RESET}")


# ─────────────────────────────────────────────
# Android section
# ─────────────────────────────────────────────

print(f"\n{BOLD}Android{RESET}")
print(f"{DIM}────────────────────────────────────────────{RESET}")

if HAS_QRCODE:

    print("  Scan the QR code to download:\n")

    qr = qrcode.QRCode(border=1)
    qr.add_data(url)
    qr.make(fit=True)

    qr.print_ascii(invert=True)

else:

    print(
        f"  {DIM}QR code unavailable "
        f"(optional 'qrcode' package not installed){RESET}"
    )


# ─────────────────────────────────────────────
# Server
# ─────────────────────────────────────────────

print(f"\n{BOLD}Server{RESET}")
print(f"{DIM}────────────────────────────────────────────{RESET}")

print(f"  {GREEN}● Running{RESET}")
print(f"  Listening on {ip}:{PORT}")
print(f"\n  {DIM}Waiting for one download...{RESET}\n")


# ─────────────────────────────────────────────
# HTTP server
# ─────────────────────────────────────────────

class OneShotHandler(http.server.SimpleHTTPRequestHandler):

    def do_GET(self):

        super().do_GET()

        threading.Thread(
            target=self.server.shutdown,
            daemon=True
        ).start()

    def log_message(self, format, *args):

        print(
            f"{GREEN}  ✓ Download request received "
            f"from {self.address_string()}{RESET}"
        )


server = http.server.HTTPServer(
    ("0.0.0.0", PORT),
    OneShotHandler
)


# ─────────────────────────────────────────────
# Start server
# ─────────────────────────────────────────────

try:

    server.serve_forever()

finally:

    server.server_close()

    shutil.rmtree(tmpdir)

    print(f"""
{GREEN}{BOLD}✓ Download complete{RESET}

  Temporary files removed
  Server stopped

{DIM}QuickShare finished.{RESET}
""")