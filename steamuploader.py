#-------------------------
# Steam Uploader Menu v1.1
#-------------------------

import os
import sys
import subprocess
import tkinter as tk
from tkinter import filedialog

# ANSI Colors
RESET = "\033[0m"
CYAN = "\033[96m"
GREEN = "\033[92m"
RED = "\033[91m"
YELLOW = "\033[93m"

# Config files
SETTINGS_FILE = 'settings.txt'
COMMANDS_FILE = 'commands.txt'
MODS_FILE = 'mods.txt'

# Script directory
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

# Main data structures
SETTINGS = {
    'DEFAULT_BASE_PATH': '',
    'DEFAULT_DESCRIPTION_PATH': '',
    'DEFAULT_MOD_NAME': '',
    'DEFAULT_DESCRIPTION_FILE_NAME': '',
    'DEFAULT_TITLE': '',
    'DEFAULT_VISIBILITY': '0',
    'DEFAULT_TAGS': '',
    'DEFAULT_PREVIEW_PATH': '',
}

# Visibility options mapping
VISIBILITY_MAP = {
    '0': "Public (default)",
    '1': "Friends-only",
    '2': "Private (hidden)",
    '3': "Unlisted"
}

# Mods dictionary and command templates
MODS = {}
COMMAND_TEMPLATES = []

# -----------------
# Utility Functions
# -----------------

def clear_screen():
    """Clear console screen across CMD, PowerShell, Windows Terminal, Linux/macOS."""
    try:
        if os.name == "nt":
            parent_process = os.environ.get("ComSpec", "").lower()
            if "powershell" in parent_process:
                os.system("powershell -Command Clear-Host")
            else:
                os.system("cls")
        else:
            os.system("clear")

        sys.stdout.write("\033[2J\033[3J\033[H")
        sys.stdout.flush()
    except Exception:
        print("\n" * 100)


def save_all_mods_to_file():
    try:
        with open(MODS_FILE, 'w') as f:
            f.write("# Lines starting with '#' are comments.\n")
            f.write("# The user can manually edit this file to add/remove mods or use the \"Manage Mods\" option in the script main menu.\n")
            f.write("# Format: ModName=WorkshopID\n\n")
            for mod_name, mod_id in MODS.items():
                f.write(f'{mod_name}={mod_id}\n')
    except Exception as e:
        print(f"{RED}ERROR writing to {MODS_FILE}: {e}{RESET}")


def update_mods_file(mod_name, new_id):
    MODS[mod_name.strip()] = new_id.strip()
    save_all_mods_to_file()


def load_settings():
    if not os.path.exists(SETTINGS_FILE):
        SETTINGS['DEFAULT_DESCRIPTION_PATH'] = SCRIPT_DIR
        save_settings(SETTINGS['DEFAULT_MOD_NAME'], SETTINGS['DEFAULT_DESCRIPTION_FILE_NAME'])
        return

    try:
        with open(SETTINGS_FILE, 'r', encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith("#"):
                    continue
                if "=" in line:
                    var_name, var_value = line.split("=", 1)
                    var_name, var_value = var_name.strip(), var_value.strip()
                    if var_name in SETTINGS:
                        SETTINGS[var_name] = var_value

        if not SETTINGS['DEFAULT_DESCRIPTION_PATH']:
            SETTINGS['DEFAULT_DESCRIPTION_PATH'] = SCRIPT_DIR
            save_settings(SETTINGS['DEFAULT_MOD_NAME'], SETTINGS['DEFAULT_DESCRIPTION_FILE_NAME'])

    except Exception as e:
        print(f"{RED}ERROR reading {SETTINGS_FILE}: {e}{RESET}")


def load_mods():
    if not os.path.exists(MODS_FILE):
        return
    try:
        with open(MODS_FILE, 'r') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    mod_name, mod_id = line.split('=', 1)
                    MODS[mod_name.strip()] = mod_id.strip().lstrip('+')
    except Exception as e:
        print(f"{RED}ERROR reading {MODS_FILE}: {e}{RESET}")


def load_commands():
    if not os.path.exists(COMMANDS_FILE):
        print(f"{RED}ERROR: {COMMANDS_FILE} not found.{RESET}")
        sys.exit(1)
    try:
        with open(COMMANDS_FILE, 'r') as f:
            global COMMAND_TEMPLATES
            COMMAND_TEMPLATES = [line.strip() for line in f if line.strip()]
        if len(COMMAND_TEMPLATES) < 2:
            print(f"{RED}ERROR: {COMMANDS_FILE} must contain at least two templates.{RESET}")
            sys.exit(1)
    except Exception as e:
        print(f"{RED}ERROR reading {COMMANDS_FILE}: {e}{RESET}")
        sys.exit(1)


def save_settings(mod_name, description_file_name):
    if not all([SETTINGS['DEFAULT_BASE_PATH'], SETTINGS['DEFAULT_DESCRIPTION_PATH']]):
        return

    SETTINGS['DEFAULT_MOD_NAME'] = mod_name
    SETTINGS['DEFAULT_DESCRIPTION_FILE_NAME'] = description_file_name

    try:
        with open(SETTINGS_FILE, 'w', encoding="utf-8") as f:
            f.write("# Lines starting with '#' are comments.\n")
            f.write("# settings.txt stores last used values.\n")
            f.write("# The user can manually edit this file to change the values or let the script handle it.\n")
            f.write("# DEFAULT_BASE_PATH points to the directory where mods are located (not recommended to change).\n\n")
            for key, value in SETTINGS.items():
                f.write(f"{key}={value}\n")

    except Exception as e:
        print(f"{RED}ERROR writing to {SETTINGS_FILE}: {e}{RESET}")


# ---------------
# Input Functions
# ---------------

def get_description():
    while True:
        if SETTINGS.get('DEFAULT_DESCRIPTION_PATH'):
            initial_dir = SETTINGS['DEFAULT_DESCRIPTION_PATH']
        else:
            initial_dir = os.path.expanduser("~")

        root = tk.Tk()
        root.withdraw()
        root.attributes("-topmost", True)

        file_path = filedialog.askopenfilename(
            title="Select Description file",
            filetypes=[("Text Files", "*.txt")],
            initialdir=initial_dir
        )

        root.destroy()

        if file_path:
            file_path = file_path.strip()

        if not file_path:
            print(f"{RED}No description file was selected.{RESET}")
            input("Press Enter to continue...")
            clear_screen()
            return None

        if not os.path.isfile(file_path):
            print(f"{RED}File not found: {file_path}{RESET}")
            continue

        filename = os.path.basename(file_path)
        if not filename.lower().endswith(".txt"):
            print(f"{RED}Invalid file selected. Must be a .txt file.{RESET}")
            continue

        print(f"Selected description file: {YELLOW}{filename}{RESET} ({file_path})")

        SETTINGS['DEFAULT_DESCRIPTION_PATH'] = os.path.dirname(file_path)
        SETTINGS['DEFAULT_DESCRIPTION_FILE_NAME'] = os.path.splitext(filename)[0]
        save_settings(SETTINGS['DEFAULT_MOD_NAME'], SETTINGS['DEFAULT_DESCRIPTION_FILE_NAME'])

        while True:
            choice = input("Proceed with Description upload? (y/n or c to select a new file): ").strip().lower()
            if choice == 'y':
                clear_screen()
                return file_path
            elif choice == 'n':
                clear_screen()
                return None
            elif choice == 'c':
                clear_screen()
                break
            else:
                print(f"{RED}Invalid input. Please enter y, n, or c.{RESET}")


def get_description_file():
    if SETTINGS.get('DEFAULT_DESCRIPTION_PATH'):
        initial_dir = SETTINGS['DEFAULT_DESCRIPTION_PATH']
    else:
        initial_dir = os.path.expanduser("~")

    root = tk.Tk()
    root.withdraw()
    root.attributes("-topmost", True)

    file_path = filedialog.askopenfilename(
        title="Select Description file",
        filetypes=[("Text Files", "*.txt")],
        initialdir=initial_dir
    )

    root.destroy()

    if file_path:
        file_path = file_path.strip()

    if not file_path:
        print(f"{RED}No description file was selected.{RESET}")
        return None

    if not os.path.isfile(file_path):
        print(f"{RED}File not found: {file_path}{RESET}")
        return None

    filename = os.path.basename(file_path)
    if not filename.lower().endswith(".txt"):
        print(f"{RED}Invalid file selected. Must be a .txt file.{RESET}")
        return None

    SETTINGS['DEFAULT_DESCRIPTION_PATH'] = os.path.dirname(file_path)
    SETTINGS['DEFAULT_DESCRIPTION_FILE_NAME'] = os.path.splitext(filename)[0]
    save_settings(SETTINGS['DEFAULT_MOD_NAME'], SETTINGS['DEFAULT_DESCRIPTION_FILE_NAME'])

    return file_path


def get_title():
    default = SETTINGS.get('DEFAULT_TITLE', '')
    title = input(f"Enter the Title [{default}]: ").strip()
    clear_screen()
    if not title:
        title = default
    if not title:
        print(f"{RED}Title cannot be empty.{RESET}")
        return get_title()
    return title


def get_visibility():
    default = SETTINGS.get('DEFAULT_VISIBILITY', '0')

    while True:
        print(f"{CYAN}=== VISIBILITY OPTIONS ==={RESET}")
        print("0) Public (default)")
        print("1) Friends-only")
        print("2) Private (hidden)")
        print("3) Unlisted")
        print("Q) Go back\n")

        vis = input(f"Select (0,1,2,3,Q) [{default}]: ").strip().upper()

        if not vis:
            vis = default
        if vis in ('0', '1', '2', '3'):
            clear_screen()
            return vis
        elif vis == 'Q':
            clear_screen()
            return None
        else:
            print(f"{RED}Invalid choice. Please enter 0,1,2,3 or Q.{RESET}")


def get_tags():
    default = SETTINGS.get('DEFAULT_TAGS', '')
    tags = input(f"Enter Tags (comma-separated) [{default}]: ").strip()
    clear_screen()
    if not tags:
        tags = default
    if not tags:
        print(f"{RED}Tags cannot be empty.{RESET}")
        return get_tags()
    tag_list = [tag.strip() for tag in tags.split(',')]
    if all(tag_list):
        cleaned = ",".join(tag_list)
        SETTINGS['DEFAULT_TAGS'] = cleaned
        return cleaned
    print(f"{RED}Invalid format. Tags must be separated by commas without empty values.{RESET}")
    return get_tags()


def get_preview():
    while True:
        if SETTINGS.get('DEFAULT_PREVIEW_PATH'):
            initial_dir = SETTINGS['DEFAULT_PREVIEW_PATH']
        else:
            initial_dir = os.path.expanduser("~")

        root = tk.Tk()
        root.withdraw()
        root.attributes("-topmost", True)

        file_path = filedialog.askopenfilename(
            title="Select Preview image",
            filetypes=[("Image Files", "*.jpg *.png *.gif")],
            initialdir=initial_dir
        )

        root.destroy()

        if file_path:
            file_path = file_path.strip()

        if not file_path:
            print(f"{RED}No image was selected.{RESET}")
            input("Press Enter to continue...")
            clear_screen()
            return None

        if not os.path.isfile(file_path):
            print(f"{RED}File not found: {file_path}{RESET}")
            continue
        if os.path.getsize(file_path) > 1 * 1024 * 1024:
            print(f"{RED}File too large (>1MB): {file_path}{RESET}")
            continue

        filename = os.path.basename(file_path)
        if not filename:
            print(f"{RED}Invalid file selected (no filename).{RESET}")
            continue

        print(f"Selected image: {YELLOW}{filename}{RESET} ({file_path})")

        SETTINGS['DEFAULT_PREVIEW_PATH'] = os.path.dirname(file_path)
        save_settings(SETTINGS['DEFAULT_MOD_NAME'], SETTINGS['DEFAULT_DESCRIPTION_FILE_NAME'])

        while True:
            choice = input("Proceed with Preview upload? (y/n or c to select a new image): ").strip().lower()
            if choice == 'y':
                clear_screen()
                return file_path
            elif choice == 'n':
                clear_screen()
                return None
            elif choice == 'c':
                clear_screen()
                break
            else:
                print(f"{RED}Invalid input. Please enter y, n, or c.{RESET}")


def get_preview_file():
    if SETTINGS.get('DEFAULT_PREVIEW_PATH'):
        initial_dir = SETTINGS['DEFAULT_PREVIEW_PATH']
    else:
        initial_dir = os.path.expanduser("~")

    root = tk.Tk()
    root.withdraw()
    root.attributes("-topmost", True)

    file_path = filedialog.askopenfilename(
        title="Select Preview image",
        filetypes=[("Image Files", "*.jpg *.png *.gif")],
        initialdir=initial_dir
    )

    root.destroy()

    if file_path:
        file_path = file_path.strip()

    if not file_path:
        print(f"{RED}No image was selected.{RESET}")
        input("Press Enter to continue...")
        clear_screen()
        return None

    if not os.path.isfile(file_path):
        print(f"{RED}File not found: {file_path}{RESET}")
        return None
    if os.path.getsize(file_path) > 1 * 1024 * 1024:
        print(f"{RED}File too large (>1MB): {file_path}{RESET}")
        return None

    filename = os.path.basename(file_path)
    if not filename:
        print(f"{RED}Invalid file selected (no filename).{RESET}")
        return None

    SETTINGS['DEFAULT_PREVIEW_PATH'] = os.path.dirname(file_path)
    save_settings(SETTINGS['DEFAULT_MOD_NAME'], SETTINGS['DEFAULT_DESCRIPTION_FILE_NAME'])

    return file_path


def get_workshop_id(mod_name):
    if mod_name in MODS and MODS[mod_name]:
        return MODS[mod_name]
    while True:
        wid = input(f"Enter the Workshop ID for {YELLOW}{mod_name}{RESET}: ").strip()
        if wid.isdigit() and len(wid) == 10:
            update_mods_file(mod_name, wid)
            return wid
        print(f"{RED}Workshop ID must be a 10-digit numeric value.{RESET}")


# ------------------
# Mod Selection Menu
# ------------------

def select_mod_from_menu():
    if not MODS:
        print(f"{YELLOW}No mods found in mods.txt{RESET}")
        input("Press Enter to continue...")
        clear_screen()
        return None, None

    clear_screen()
    print(f"{CYAN}=== SELECT MOD FOR UPLOAD ==={RESET}")
    for i, name in enumerate(MODS.keys()):
        mod_id_display = MODS[name] if MODS[name] else "MISSING ID"
        print(f"{i+1}) {name} [{mod_id_display}]")
    print("Q) Go back\n")

    while True:
        choice = input("Select Mod number: ").strip().upper()
        if choice == 'Q':
            clear_screen()
            return None, None
        if choice.isdigit():
            idx = int(choice) - 1
            if 0 <= idx < len(MODS):
                mod_name = list(MODS.keys())[idx]
                wid = get_workshop_id(mod_name)
                clear_screen()
                return wid, mod_name
        print(f"{RED}Invalid choice.{RESET}")


# -------------------
# Confirmation Prompt
# -------------------

def confirm_action(action_type):
    while True:
        choice = input(f"Proceed with {action_type}? (y/n): ").strip().lower()
        if choice in ('y', 'n'):
            clear_screen()
            return choice == 'y'
        print(f"{RED}Invalid input.{RESET}")


# ---------------
# Execution Logic
# ---------------

def execute_upload(command_template, workshop_id, content_path=None, desc_path=None, title=None, visibility=None, tags=None, preview=None):
    """
    Handles commands with placeholders:
    Replaces {WORKSHOP_ID} with workshop_id
    Replaces {CONTENT}, {DESC}, {TITLE}, {VISIBILITY}, {TAGS}, {PREVIEW} with given values or strips them out if not provided.
    """
    if not workshop_id:
        return False, f"{RED}ERROR: missing Workshop ID{RESET}"

    cmd = command_template.replace('{WORKSHOP_ID}', workshop_id)

    resolved_content   = os.path.expandvars(content_path) if content_path else None
    resolved_desc      = os.path.expandvars(desc_path) if desc_path else None
    resolved_title     = title if title else None
    resolved_visibility= visibility if visibility is not None else None
    resolved_tags      = tags if tags else None
    resolved_preview   = os.path.expandvars(preview) if preview else None

    replacements = {
        '{CONTENT}':    (resolved_content,   '-c {CONTENT}'),
        '{DESC}':       (resolved_desc,      '-d {DESC}'),
        '{TITLE}':      (resolved_title,     '-t {TITLE}'),
        '{VISIBILITY}': (resolved_visibility,'-v {VISIBILITY}'),
        '{TAGS}':       (resolved_tags,      '-T {TAGS}'),
        '{PREVIEW}':    (resolved_preview,   '-p {PREVIEW}')
    }

    for placeholder, (value, flag_pattern) in replacements.items():
        if placeholder in cmd:
            if value:
                cmd = cmd.replace(placeholder, f'"{value}"')
            else:
                cmd = cmd.replace(flag_pattern, '')

    if '{' in cmd and '}' in cmd:
        return False, f"{RED}ERROR: Unresolved placeholder in command{RESET}\nTemplate: {command_template}\nFinal: {cmd}"

    try:
        result = subprocess.run(
            cmd,
            shell=True,
            check=True,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL
        )
        out = result.stdout or ""
        return True, f"{CYAN}[Command]{RESET}\n{cmd}\n\n{YELLOW}[Logs]{RESET}\n{out}"
    except subprocess.CalledProcessError as e:
        return False, (
            f"{RED}Failed with code {e.returncode}{RESET}\n"
            f"{CYAN}[Command]{RESET} {cmd}\n\n"
            f"{YELLOW}[Logs]{RESET}\n{e.stdout or ''}"
        )
    except FileNotFoundError:
        return False, f"{RED}ERROR: app.exe not found.{RESET}"


def show_execution_results(execution_logs, success, canceled=False):
    if execution_logs:
        print("\n".join(execution_logs))
    if canceled:
        print(f"{YELLOW}=== ACTION CANCELED ==={RESET}")
    elif success:
        save_settings(SETTINGS['DEFAULT_MOD_NAME'], SETTINGS['DEFAULT_DESCRIPTION_FILE_NAME'])
        print(f"{GREEN}=== ACTION COMPLETE ==={RESET}")
    else:
        print(f"{RED}=== ACTION FAILED ==={RESET}")
    input("Press Enter to continue...")
    clear_screen()


# --------------
# Mod Management
# --------------

def add_mod():
    clear_screen()
    print(f"{CYAN}=== ADD / UPDATE MOD ==={RESET}")
    mod_name = input("Enter Mod name: ").strip()
    if not mod_name:
        print(f"{RED}Mod name cannot be empty.{RESET}")
        input("Press Enter to continue...")
        clear_screen()
        return
    while True:
        clear_screen()
        mod_id = input(f"Enter Workshop ID for {YELLOW}{mod_name}{RESET} (or blank to clear): ").strip()
        if not mod_id:
            break
        if mod_id.isdigit() and len(mod_id) == 10:
            break
        print(f"{RED}Workshop ID must be a 10-digit numeric value or blank.{RESET}")
    clear_screen()
    print(f"Added/Updated mod: {YELLOW}{mod_name}{RESET} with ID ({YELLOW}{mod_id or 'MISSING ID'}{RESET})")
    update_mods_file(mod_name, mod_id)
    input("Press Enter to go back...")
    clear_screen()


def remove_mod():
    if not MODS:
        print(f"{YELLOW}No mods to remove.{RESET}")
        input("Press Enter to continue...")
        clear_screen()
        return
    while True:
        clear_screen()
        print(f"{CYAN}=== REMOVE MOD ==={RESET}")
        for i, name in enumerate(MODS.keys()):
            print(f"{i+1}) {name} [{MODS[name] or 'MISSING ID'}]")
        print("Q) Go back\n")
        choice = input("Select Mod to remove: ").strip().upper()
        if choice == 'Q':
            clear_screen()
            return
        if choice.isdigit():
            clear_screen()
            idx = int(choice) - 1
            if 0 <= idx < len(MODS):
                mod_to_remove = list(MODS.keys())[idx]
                confirm = input(f"Selected mod: {YELLOW}{mod_to_remove}{RESET}\nRemove mod? (y/n): ").strip().lower()
                if confirm == 'y':
                    clear_screen()
                    print(f"Removed mod: {YELLOW}{mod_to_remove}{RESET}")
                    del MODS[mod_to_remove]
                    save_all_mods_to_file()
                    input("Press Enter to go back...")
                    clear_screen()
                    return


def show_mod_list():
    clear_screen()
    print(f"{CYAN}=== CURRENT MODS ==={RESET}")
    if not MODS:
        print(f"{YELLOW}No mods loaded.{RESET}")
    else:
        mod_name_width = max(len("MOD_NAME"), max((len(name) for name in MODS.keys()), default=0))
        wid_width = max(len("WORKSHOP_ID"), max((len(wid or 'MISSING ID') for wid in MODS.values()), default=0))

        header = f"{'MOD_NAME'.ljust(mod_name_width)} | {'WORKSHOP_ID'.ljust(wid_width)}"
        print(header)
        print("-" * (len(header)))

        for name, wid in MODS.items():
            display_id = wid or 'MISSING ID'
            print(f"{name.ljust(mod_name_width)} | {display_id.ljust(wid_width)}")

    input("\nPress Enter to go back...")
    clear_screen()


def mod_management_menu():
    while True:
        clear_screen()
        print(f"{CYAN}=== MOD MANAGEMENT ==={RESET}")
        print("1) Add / Update Mod")
        print("2) Remove Mod")
        print("3) Show Mod List")
        print("Q) Go Back\n")
        choice = input("Select (1,2,3,Q): ").strip().upper()
        if choice == '1':
            add_mod()
        elif choice == '2':
            remove_mod()
        elif choice == '3':
            show_mod_list()
        elif choice == 'Q':
            clear_screen()
            return
        else:
            input("Press Enter to continue...")
            clear_screen()

# ---------------------
# Multiple Options Flow
# ---------------------

def multiple_options_flow(base_path, desc_base_path):
    while True:
        workshop_id, mod_name = select_mod_from_menu()
        if not workshop_id:
            return [], False, None
        SETTINGS['DEFAULT_MOD_NAME'] = mod_name

        while True:
            clear_screen()
            print(f"{CYAN}=== MULTIPLE OPTIONS ==={RESET}")
            print("1) Content")
            print("2) Description")
            print("3) Title")
            print("4) Visibility")
            print("5) Tags")
            print("6) Preview")
            print("7) All")
            print("Q) Go back\n")

            default = "7"
            raw = input(f"Single, multiple (comma-separated) or all.\nSelect Options [{default}]: ").strip()
            if not raw:
                raw = default
            raw = raw.upper()

            if raw == 'Q':
                break

            if raw in ('7', 'ALL'):
                selected = ['1', '2', '3', '4', '5', '6']
            else:
                parts = [p.strip() for p in raw.split(',')]
                selected = [p for p in parts if p.isdigit() and 1 <= int(p) <= 6]

            if not selected:
                input(f"{RED}No valid option selected. Press Enter to try again...{RESET}")
                continue

            content_path = desc_path = title = visibility = tags = preview_path = None

            if '1' in selected:
                content_path = os.path.join(base_path, mod_name, 'Contents')
            if '2' in selected:
                desc_path = get_description_file()
                if not desc_path:
                    break
            if '3' in selected:
                title = get_title()
                SETTINGS['DEFAULT_TITLE'] = title
            if '4' in selected:
                visibility = get_visibility()
                if visibility is None:
                    break
                SETTINGS['DEFAULT_VISIBILITY'] = visibility
            if '5' in selected:
                tags = get_tags()
            if '6' in selected:
                preview_path = get_preview_file()
                if not preview_path:
                    break

            clear_screen()
            print(f"{CYAN}=== SUMMARY ==={RESET}")
            if content_path:
                print(f"Content path: {YELLOW}{content_path}{RESET}")
            if desc_path:
                print(f"Description file: {YELLOW}{os.path.basename(desc_path)}{RESET} ({desc_path})")
            if title:
                print(f"Title: {YELLOW}{title}{RESET}")
            if visibility is not None:
                print(f"Visibility: {YELLOW}{VISIBILITY_MAP.get(visibility, visibility)}{RESET}")
            if tags:
                print(f"Tags: {YELLOW}{tags}{RESET}")
            if preview_path:
                print(f"Preview image: {YELLOW}{os.path.basename(preview_path)}{RESET} ({preview_path})")

            if not confirm_action("multiple options upload"):
                return [], False, True

            execution_logs = []
            if len(selected) == 1:
                opt = selected[0]
                if opt == '1':
                    ok, out = execute_upload(COMMAND_TEMPLATES[0], workshop_id, content_path=content_path)
                elif opt == '2':
                    ok, out = execute_upload(COMMAND_TEMPLATES[1], workshop_id, desc_path=desc_path)
                elif opt == '3':
                    ok, out = execute_upload(COMMAND_TEMPLATES[2], workshop_id, title=title)
                elif opt == '4':
                    ok, out = execute_upload(COMMAND_TEMPLATES[3], workshop_id, visibility=visibility)
                elif opt == '5':
                    ok, out = execute_upload(COMMAND_TEMPLATES[4], workshop_id, tags=tags)
                elif opt == '6':
                    ok, out = execute_upload(COMMAND_TEMPLATES[5], workshop_id, preview=preview_path)
                else:
                    ok, out = False, f"{RED}ERROR: Unsupported option {opt}{RESET}"
                execution_logs.append(out)
                return execution_logs, ok, False

            if len(selected) > 1 and len(COMMAND_TEMPLATES) >= 7:
                ok, out = execute_upload(
                    COMMAND_TEMPLATES[6],
                    workshop_id,
                    content_path=content_path,
                    desc_path=desc_path,
                    title=title,
                    visibility=visibility,
                    tags=tags,
                    preview=preview_path
                )
                execution_logs.append(out)
                return execution_logs, ok, False

            execution_logs.append(f"{RED}ERROR: No combined template available in {COMMANDS_FILE}{RESET}")
            return execution_logs, False, False

# ---------
# Main Menu
# ---------

def main():
    load_settings()
    load_mods()
    load_commands()
    base_path = SETTINGS.get('DEFAULT_BASE_PATH')
    desc_base_path = SETTINGS.get('DEFAULT_DESCRIPTION_PATH')
    if not base_path or not desc_base_path:
        print(f"{RED}FATAL: Missing base paths in settings.txt{RESET}")
        sys.exit(1)

    while True:
        clear_screen()
        print(f"{CYAN}=== STEAM UPLOADER MENU ==={RESET}")
        print("1) Content (-c)")
        print("2) Description (-d)")
        print("3) Title (-t)")
        print("4) Visibility (-v)")
        print("5) Tags (-T)")
        print("6) Preview (-p)")
        print("7) Multiple Options")
        print("8) Manage Mods")
        print("Q) Quit\n")

        choice = input("Select (1,2,3,4,5,6,7,8,Q): ").strip().upper()
        if choice == 'Q':
            save_settings(SETTINGS['DEFAULT_MOD_NAME'], SETTINGS['DEFAULT_DESCRIPTION_FILE_NAME'])
            print(f"{CYAN}\n█▀▀ █▀█ █▀█ █▀▄ █▀▄ █ █ █▀▀ █{RESET}")
            print(f"{CYAN}█ █ █ █ █ █ █ █ █▀▄  █  █▀▀ ▀{RESET}")
            print(f"{CYAN}▀▀▀ ▀▀▀ ▀▀▀ ▀▀  ▀▀   ▀  ▀▀▀ ▀{RESET}")
            sys.exit(0)
        elif choice == '8':
            mod_management_menu()
            continue

        execution_logs, success = [], True
        workshop_id, mod_name = None, None
        content_path, desc_path, title, visibility, tags = None, None, None, None, None

        if choice == '1':
            workshop_id, mod_name = select_mod_from_menu()
            if not workshop_id:
                continue
            SETTINGS['DEFAULT_MOD_NAME'] = mod_name
            content_path = os.path.join(base_path, mod_name, 'Contents')
            if confirm_action("content upload"):
                ok, out = execute_upload(COMMAND_TEMPLATES[0], workshop_id, content_path=content_path)
                execution_logs.append(out)
                show_execution_results(execution_logs, ok)
            else:
                show_execution_results([], False, canceled=True)
            continue

        elif choice == '2':
            workshop_id, mod_name = select_mod_from_menu()
            if not workshop_id:
                continue
            SETTINGS['DEFAULT_MOD_NAME'] = mod_name
            desc_path = get_description()
            if not desc_path:
                show_execution_results([], False, canceled=True)
                continue
            ok, out = execute_upload(COMMAND_TEMPLATES[1], workshop_id, desc_path=desc_path)
            execution_logs.append(out)
            show_execution_results(execution_logs, ok)
            continue

        elif choice == '3':
            workshop_id, mod_name = select_mod_from_menu()
            if not workshop_id:
                continue
            SETTINGS['DEFAULT_MOD_NAME'] = mod_name
            title = get_title()
            SETTINGS['DEFAULT_TITLE'] = title
            print(f"Title: {YELLOW}{title}{RESET}")
            if confirm_action("title update"):
                ok, out = execute_upload(COMMAND_TEMPLATES[2], workshop_id, title=title)
                execution_logs.append(out)
                show_execution_results(execution_logs, ok)
            else:
                show_execution_results([], False, canceled=True)
            continue

        elif choice == '4':
            while True:
                workshop_id, mod_name = select_mod_from_menu()
                if not workshop_id:
                    break
                SETTINGS['DEFAULT_MOD_NAME'] = mod_name
                visibility = get_visibility()
                if visibility is None:
                    continue
                SETTINGS['DEFAULT_VISIBILITY'] = visibility
                print(f"Selected visibility: {YELLOW}{VISIBILITY_MAP.get(visibility, visibility)}{RESET}")
                if confirm_action("visibility update"):
                    ok, out = execute_upload(COMMAND_TEMPLATES[3], workshop_id, visibility=visibility)
                    execution_logs.append(out)
                    show_execution_results(execution_logs, ok)
                else:
                    show_execution_results([], False, canceled=True)
                break
            continue

        elif choice == '5':
            workshop_id, mod_name = select_mod_from_menu()
            if not workshop_id:
                continue
            SETTINGS['DEFAULT_MOD_NAME'] = mod_name
            tags = get_tags()
            print(f"Tags: {YELLOW}{tags}{RESET}")
            if confirm_action("tags update"):
                ok, out = execute_upload(COMMAND_TEMPLATES[4], workshop_id, tags=tags)
                execution_logs.append(out)
                show_execution_results(execution_logs, ok)
            else:
                show_execution_results([], False, canceled=True)
            continue

        elif choice == '6':
            workshop_id, mod_name = select_mod_from_menu()
            if not workshop_id:
                continue
            SETTINGS['DEFAULT_MOD_NAME'] = mod_name
            preview_path = get_preview()
            if not preview_path:
                show_execution_results([], False, canceled=True)
                continue
            ok, out = execute_upload(COMMAND_TEMPLATES[5], workshop_id, preview=preview_path)
            execution_logs.append(out)
            show_execution_results(execution_logs, ok)
            continue

        elif choice == '7':
            execution_logs, success, canceled = multiple_options_flow(base_path, desc_base_path)
            if canceled is None:
                continue
            show_execution_results(execution_logs, success, canceled=canceled)
            continue

        if choice in ('1','2','3','4','5','6'):
            show_execution_results(execution_logs, success)


if __name__ == "__main__":
    main()