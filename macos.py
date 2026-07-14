#!/usr/bin/env python3

import http.server
import os
import shutil
import subprocess
import tempfile
import threading


def get_en0_ip():
    return subprocess.check_output(
        ["ipconfig", "getifaddr", "en0"],
        text=True
    ).strip()


# Get all files in current directory
files = [f for f in os.listdir(".") if os.path.isfile(f)]

if not files:
    print("No files found.")
    exit()

print("\nAvailable Files:\n")

for i, f in enumerate(files, start=1):
    print(f"[{i}] {f}")

# Select file
while True:
    try:
        choice = int(input("\nSelect file number: "))
        if 1 <= choice <= len(files):
            break
        print("Invalid choice.")
    except ValueError:
        print("Enter a valid number.")

selected_file = files[choice - 1]

PORT = 1234
ip = get_en0_ip()

# Create a temporary directory containing only the selected file
tmpdir = tempfile.mkdtemp()
shutil.copy2(selected_file, tmpdir)
os.chdir(tmpdir)

url = f"http://{ip}:{PORT}/{selected_file}"
command = f"wget {url}"

# Copy command to clipboard (macOS)
subprocess.run(["pbcopy"], input=command, text=True)

print(f"\nSharing: {selected_file}\n")
print("Download command (also copied to clipboard):\n")
print(command)
print("\nWaiting for one download...\n")


class OneShotHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        super().do_GET()
        threading.Thread(target=self.server.shutdown, daemon=True).start()

    def log_message(self, format, *args):
        print(f"[+] {self.address_string()} downloaded {selected_file}")


server = http.server.HTTPServer(
    ("0.0.0.0", PORT),
    OneShotHandler
)

try:
    server.serve_forever()
finally:
    server.server_close()
    shutil.rmtree(tmpdir)
    print("\n✅ Download complete. Server stopped.")
