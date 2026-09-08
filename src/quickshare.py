#!/usr/bin/env python3

import http.server
import os
import platform
import shutil
import socket
import subprocess
import tempfile
import threading
import urllib.parse
import zipfile


# ─────────────────────────────────────────────
# Optional QR code support
# ─────────────────────────────────────────────

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


def setup_colors():

    if not os.isatty(1):

        return (
            "",
            "",
            "",
            "",
            "",
            "",
            "",
        )

    return (
        RESET,
        BOLD,
        CYAN,
        GREEN,
        YELLOW,
        RED,
        DIM,
    )


(
    RESET,
    BOLD,
    CYAN,
    GREEN,
    YELLOW,
    RED,
    DIM,
) = setup_colors()


# ─────────────────────────────────────────────
# Get local IP
# ─────────────────────────────────────────────

def get_local_ip():

    system = platform.system()

    # macOS
    if system == "Darwin":

        try:

            ip = subprocess.check_output(
                [
                    "ipconfig",
                    "getifaddr",
                    "en0",
                ],
                text=True,
                stderr=subprocess.DEVNULL,
            ).strip()

            if ip:

                return ip

        except (
            subprocess.CalledProcessError,
            FileNotFoundError,
        ):

            pass

    # Windows / Linux fallback
    sock = socket.socket(
        socket.AF_INET,
        socket.SOCK_DGRAM,
    )

    try:

        # No data is actually sent.
        sock.connect(
            (
                "8.8.8.8",
                80,
            )
        )

        return sock.getsockname()[0]

    finally:

        sock.close()


# ─────────────────────────────────────────────
# Clipboard
# ─────────────────────────────────────────────

def copy_to_clipboard(text):

    system = platform.system()

    try:

        # macOS
        if system == "Darwin":

            subprocess.run(
                ["pbcopy"],
                input=text,
                text=True,
                check=True,
            )

            return True

        # Windows
        if system == "Windows":

            subprocess.run(
                ["clip.exe"],
                input=text,
                text=True,
                check=True,
            )

            return True

    except (
        FileNotFoundError,
        subprocess.CalledProcessError,
    ):

        pass

    return False


# ─────────────────────────────────────────────
# File size
# ─────────────────────────────────────────────

def get_size(path):

    if os.path.isfile(path):

        return os.path.getsize(path)

    total = 0

    for root, _, filenames in os.walk(path):

        for filename in filenames:

            full_path = os.path.join(
                root,
                filename,
            )

            try:

                total += os.path.getsize(
                    full_path
                )

            except OSError:

                pass

    return total


def format_size(size):

    units = [
        "B",
        "KB",
        "MB",
        "GB",
        "TB",
    ]

    for unit in units:

        if size < 1024:

            return f"{size:.1f} {unit}"

        size /= 1024

    return f"{size:.1f} PB"


# ─────────────────────────────────────────────
# Create ZIP from directory
# ─────────────────────────────────────────────

def zip_directory(
    source_directory,
    destination_directory,
):

    source_directory = os.path.abspath(
        source_directory
    )

    directory_name = os.path.basename(
        source_directory
    )

    archive_name = (
        directory_name + ".zip"
    )

    archive_path = os.path.join(
        destination_directory,
        archive_name,
    )

    with zipfile.ZipFile(
        archive_path,
        "w",
        compression=zipfile.ZIP_DEFLATED,
    ) as archive:

        parent_directory = os.path.dirname(
            source_directory
        )

        for root, _, filenames in os.walk(
            source_directory
        ):

            for filename in filenames:

                full_path = os.path.join(
                    root,
                    filename,
                )

                archive_name_inside_zip = (
                    os.path.relpath(
                        full_path,
                        parent_directory,
                    )
                )

                archive.write(
                    full_path,
                    archive_name_inside_zip,
                )

    return archive_path


# ─────────────────────────────────────────────
# Header
# ─────────────────────────────────────────────

print(
    f"""
{CYAN}{BOLD}╭──────────────────────────────────────────╮
│                 QuickShare               │
│          Fast LAN File Sharing           │
╰──────────────────────────────────────────╯{RESET}
"""
)


# ─────────────────────────────────────────────
# Get files and directories
# ─────────────────────────────────────────────

entries = []

for entry in os.scandir("."):

    # Ignore hidden files/directories
    if entry.name.startswith("."):

        continue

    if entry.is_file() or entry.is_dir():

        entries.append(entry)


if not entries:

    print(
        f"{RED}✗ No files or directories found.{RESET}"
    )

    raise SystemExit(1)


print(
    f"{BOLD}Available Files & Directories{RESET}"
)

print(
    f"{DIM}────────────────────────────────────────────{RESET}"
)


for number, entry in enumerate(
    entries,
    start=1,
):

    if entry.is_dir():

        item_type = "DIR"

    else:

        item_type = "FILE"

    size = format_size(
        get_size(entry.path)
    )

    print(
        f"  {CYAN}[{number}]{RESET} "
        f"{item_type:<4} "
        f"{entry.name:<30} "
        f"{DIM}{size}{RESET}"
    )


print(
    f"{DIM}────────────────────────────────────────────{RESET}"
)


# ─────────────────────────────────────────────
# Select item
# ─────────────────────────────────────────────

while True:

    try:

        choice = int(
            input("\nSelect item: ")
        )

        if 1 <= choice <= len(entries):

            break

        print(
            f"{YELLOW}Invalid choice.{RESET}"
        )

    except ValueError:

        print(
            f"{YELLOW}Enter a valid number.{RESET}"
        )


selected_entry = entries[
    choice - 1
]

selected_path = selected_entry.path

selected_name = selected_entry.name

selected_is_directory = (
    selected_entry.is_dir()
)


# ─────────────────────────────────────────────
# Network
# ─────────────────────────────────────────────

PORT = 1234

ip = get_local_ip()


# ─────────────────────────────────────────────
# Temporary directory
# ─────────────────────────────────────────────

tmpdir = tempfile.mkdtemp()


try:

    # ─────────────────────────────────────────
    # Prepare file to share
    # ─────────────────────────────────────────

    if selected_is_directory:

        shared_file = zip_directory(
            selected_path,
            tmpdir,
        )

        shared_name = os.path.basename(
            shared_file
        )

        share_type = "Directory (ZIP)"

    else:

        shared_file = os.path.join(
            tmpdir,
            selected_name,
        )

        shutil.copy2(
            selected_path,
            shared_file,
        )

        shared_name = selected_name

        share_type = "File"


    # ─────────────────────────────────────────
    # Number-based URL
    #
    # Example:
    #
    # [6] tools/
    #
    # becomes:
    #
    # http://192.168.1.10:1234/6
    # ─────────────────────────────────────────

    url = (
        f"http://{ip}:{PORT}/{choice}"
    )


    # wget uses the filename supplied by
    # Content-Disposition.
    command = f"wget {url}"

    # ─────────────────────────────────────────
    # Copy command
    # ─────────────────────────────────────────

    clipboard_ok = copy_to_clipboard(
        command
    )


    # ─────────────────────────────────────────
    # Sharing information
    # ─────────────────────────────────────────

    print(
        f"""
{GREEN}{BOLD}✓ Ready to share{RESET}

  Type      : {share_type}
  Name      : {BOLD}{shared_name}{RESET}
  Size      : {format_size(os.path.getsize(shared_file))}
  IP        : {ip}
  Port      : {PORT}
  Share ID  : {choice}
"""
    )


    # ─────────────────────────────────────────
    # VM / Linux
    # ─────────────────────────────────────────

    print(
        f"{BOLD}VM / Linux{RESET}"
    )

    print(
        f"{DIM}────────────────────────────────────────────{RESET}"
    )

    print(
        f"  {YELLOW}{command}{RESET}"
    )

    if clipboard_ok:

        print(
            f"  {GREEN}✓ Command copied to clipboard{RESET}"
        )

    else:

        print(
            f"  {DIM}Clipboard copy unavailable{RESET}"
        )


    # ─────────────────────────────────────────
    # Android
    # ─────────────────────────────────────────

    print(
        f"\n{BOLD}Android{RESET}"
    )

    print(
        f"{DIM}────────────────────────────────────────────{RESET}"
    )


    if HAS_QRCODE:

        print(
            "  Scan the QR code to download:\n"
        )

        qr = qrcode.QRCode(
            border=1
        )

        qr.add_data(url)

        qr.make(
            fit=True
        )

        qr.print_ascii(
            invert=True
        )

    else:

        print(
            f"  {DIM}QR unavailable.{RESET}"
        )

        print(
            f"  {DIM}Install optional support:{RESET}"
        )

        print(
            f"  {DIM}pip install qrcode{RESET}"
        )


    # ─────────────────────────────────────────
    # Server information
    # ─────────────────────────────────────────

    print(
        f"\n{BOLD}Server{RESET}"
    )

    print(
        f"{DIM}────────────────────────────────────────────{RESET}"
    )

    print(
        f"  {GREEN}● Running{RESET}"
    )

    print(
        f"  Listening on {ip}:{PORT}"
    )

    print(
        f"  Share URL: {url}"
    )

    print(
        f"\n  {DIM}Waiting for one download...{RESET}\n"
    )


    # ─────────────────────────────────────────
    # HTTP Server
    # ─────────────────────────────────────────

    class QuickShareHandler(
        http.server.BaseHTTPRequestHandler
    ):

        def do_GET(self):

            # Extract path and remove query string
            requested_path = (
                urllib.parse.urlsplit(
                    self.path
                ).path
            )

            # Remove leading slash
            requested_id = (
                requested_path.lstrip("/")
            )


            # ─────────────────────────────────
            # Validate Share ID
            # ─────────────────────────────────

            if requested_id != str(choice):

                self.send_error(
                    404,
                    "Share not found"
                )

                return


            # ─────────────────────────────────
            # Make sure shared file exists
            # ─────────────────────────────────

            if not os.path.isfile(
                shared_file
            ):

                self.send_error(
                    404,
                    "File not found"
                )

                return


            # ─────────────────────────────────
            # File information
            # ─────────────────────────────────

            file_size = os.path.getsize(
                shared_file
            )


            # ─────────────────────────────────
            # Send HTTP response
            # ─────────────────────────────────

            self.send_response(200)

            self.send_header(
                "Content-Type",
                "application/octet-stream",
            )

            self.send_header(
                "Content-Length",
                str(file_size),
            )

            # Tell browser/wget the original
            # filename.
            encoded_filename = (
                urllib.parse.quote(
                    shared_name
                )
            )

            self.send_header(
                "Content-Disposition",
                (
                    f'attachment; '
                    f'filename="{shared_name}"; '
                    f"filename*=UTF-8''"
                    f"{encoded_filename}"
                ),
            )

            self.send_header(
                "Cache-Control",
                "no-store",
            )

            self.end_headers()


            # ─────────────────────────────────
            # Send file
            # ─────────────────────────────────

            try:

                with open(
                    shared_file,
                    "rb",
                ) as file:

                    while True:

                        data = file.read(
                            64 * 1024
                        )

                        if not data:

                            break

                        self.wfile.write(
                            data
                        )


                # Download completed
                print(
                    f"{GREEN}"
                    f"  ✓ Download completed "
                    f"from "
                    f"{self.client_address[0]}"
                    f"{RESET}"
                )


                # Stop server
                threading.Thread(
                    target=self.server.shutdown,
                    daemon=True,
                ).start()


            except (
                BrokenPipeError,
                ConnectionResetError,
            ):

                print(
                    f"{YELLOW}"
                    f"  ! Client disconnected "
                    f"before completion"
                    f"{RESET}"
                )


        def log_message(
            self,
            format,
            *args,
        ):

            # Disable default HTTP logs
            pass


    # ─────────────────────────────────────────
    # Start server
    # ─────────────────────────────────────────

    server = http.server.HTTPServer(
        (
            "0.0.0.0",
            PORT,
        ),
        QuickShareHandler,
    )


    try:

        server.serve_forever()

    finally:

        server.server_close()


    # ─────────────────────────────────────────
    # Finished
    # ─────────────────────────────────────────

    print(
        f"""
{GREEN}{BOLD}✓ Download complete{RESET}

  Temporary files removed
  Server stopped

{DIM}QuickShare finished.{RESET}
"""
    )


except KeyboardInterrupt:

    print(
        f"\n{YELLOW}Server stopped by user.{RESET}"
    )


finally:

    # Always clean temporary directory
    shutil.rmtree(
        tmpdir,
        ignore_errors=True,
    )