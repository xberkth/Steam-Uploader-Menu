# Steam Uploader Menu
[![Python](https://img.shields.io/badge/Python-v3.13.7-3776AB.svg?logo=python&logoColor=F2F2F2)](https://www.python.org/downloads/)
[![SteamUploader](https://img.shields.io/badge/SteamUploader-v0.6.0-16376D.svg?logo=steam&logoColor=F2F2F2)](https://github.com/SirDoggyJvla/Steam-Uploader/releases/tag/v0.6.0)
[![GPLv3 License](https://img.shields.io/badge/License-GPL%20v3-green.svg?logo=googledocs&logoColor=F2F2F2)](https://www.gnu.org/licenses/gpl-3.0.html)

> [!NOTE]
> This script is a work in progress, currently designed to work with the Project Zomboid workshop. It will later be compatible with any game's workshop.

**Steam Uploader Menu** is a Python script that provides a simple, navigable menu for uploading and updating mods on the **Steam Workshop**.
It acts as a user-friendly wrapper around the **Steam Uploader CLI**, so you don’t need to remember or type complex commands.

## Features
- 🚀 **Upload / update mods** directly to Steam Workshop
- 📂 **Content upload** – push your mod files easily
- 📝 **Description update** – pick a `.txt | .bbcode` file with a file dialog
- 🏷️ **Title, tags, and visibility settings** – update with menu prompts
- 🖼️ **Preview image support** – select an image `.jpg | .png | .gif` with a file dialog
- ⚡ **Multiple options flow** – update several fields at once in a single run
- 🛠️ **Mod management** – add, update or remove mods from the mod list in `mods.txt`
- 💾 **Persistent settings** – remembers your last used values in `settings.txt`

## How it works
- You choose what to upload / update through a simple text menu.
- File selections (description, preview image) are made via the file explorer.
- It builds the correct CLI command with the chosen options and runs it automatically.
- Results and logs are shown directly in the console.

## Quick Start
### 1. **Requirements**
  - **Python 3.13+**
  - Steam Uploader executable (CLI tool)
  - Windows, Linux, or macOS console

### 2. **Setup**
  1. Clone this project or download the last release [here](https://github.com/xberkth/Steam-Uploader-Menu/releases/latest).
  2. Make sure these files are present in the script folder:
     - `steamuploader.py` → main script
     - `settings.txt` → stores default paths & last used values (auto-created if missing)
     - `commands.txt` → command templates with placeholders like `{CONTENT}`, `{DESC}`, `{TITLE}`, `{VISIBILITY}`, `{TAGS}`, `{PREVIEW}`
     - `mods.txt` → stores your mods list in the format ModName=WorkshopID

### 3. **Run the script**
> [!NOTE]
> Steam needs to be open (even in the background) for the CLI tool to work.
```shell
python steamuploader.py
```

### 4. **Use the menu**
- You’ll see a text-based menu with numbered options:

    ![Steam Uploader Menu](https://raw.githubusercontent.com/xberkth/xberkth-stuff/refs/heads/main/steam-uploader-menu.png)
- For Description and Preview uploads, a file explorer dialog will pop up so you can select the file instead of typing the path.

### 5. **Example workflow**
  - Add your Mod and Workshop ID via **Manage Mods**.
  - Pick **Description** → select a `.txt | .bbcode` file.
  - Confirm and the script will run the correct upload command.
  - Done ✅

## Configuration Files
- `settings.txt`
  Stores last used values such as base paths, default description file, last chosen preview path, etc.
  → This file is created automatically on first run and updated whenever you make changes.

- `mods.txt`
  Contains the list of mods you manage with the script. Each line follows the format:
  ```
  ModName=WorkshopID
  ```
  You can add/remove mods either manually or via the **Manage Mods** menu.

- `commands.txt`
  Defines the CLI templates used for uploads/updates.
  Placeholders such as `{CONTENT}`, `{DESC}`, `{TITLE}`, `{VISIBILITY}`, `{TAGS}`, and `{PREVIEW}` are replaced by the script when building commands.

## Known Limitations
- Preview images must be **1 MB or smaller**.
- Only `.txt | .bbcode` files are supported for descriptions.
- Only `.jpg | .png | .gif` files are supported for preview images.

## Troubleshooting
- **Script can’t find files**
  - → Check the paths stored in settings.txt. The script updates this automatically, but you can edit it manually if needed.
- **Upload fails immediately**
  - → Verify that the Workshop ID is correct in mods.txt.
- **On first run, paths are missing**
  - → The script will create settings.txt and default paths automatically. Simply run it again and select files when prompted.

## Credits
Thanks to [@SirDoggyJvla](https://github.com/SirDoggyJvla) for creating [Steam Uploader](https://github.com/SirDoggyJvla/Steam-Uploader/) 🤘
