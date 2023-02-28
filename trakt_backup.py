import datetime
import os
import sys
import subprocess
import converters.json_to_csv as jtc
import converters.json_to_xml as jtx
import argparse
from dotenv import load_dotenv

from trakt_request import TraktRequest

load_dotenv()

TRAKT_API_KEY = os.getenv("TRAKT_API_KEY")
TRAKT_USERNAME = os.getenv("TRAKT_USERNAME") if os.getenv("TRAKT_USERNAME") else ""
BACKUP_ROOT_PATH = os.getenv("BACKUP_ROOT_PATH") if os.getenv("BACKUP_ROOT_PATH") else ""
TRAKT_URL = os.getenv("TRAKT_URL") if os.getenv("TRAKT_URL") else "https://api.trakt.tv/users"
FILE_TYPE = os.getenv("FILE_TYPE") if os.getenv("FILE_TYPE") else "json"

if not TRAKT_API_KEY:
    print("Please, add your Trakt API key in the .env file")
    sys.exit()

accepted_file_types = ["json", "csv", "xml"]


def launch_file(filepath):
    if sys.platform.startswith("darwin"):
        subprocess.call(("open", filepath))
    elif os.name == "nt":
        os.startfile(filepath)
    elif os.name == "posix":
        subprocess.call(("xdg-open", filepath))


def convert(file_type, path):
    for file in os.listdir(path):
        if file_type == "csv":
            dataframe = jtc.get_dataframe_csv(path, file)
            if dataframe is not None:
                dataframe.to_csv(os.path.join(path, file.replace(".json", ".csv")), index=False)
        elif file_type == "xml":
            tree = jtx.get_tree_xml(path, file)
            if tree is not None:
                with open(os.path.join(path, file.replace(".json", ".xml")), "wb") as f:
                    f.write(tree)
        if not file.startswith("stats"):
            os.remove(os.path.join(path, file))


# Check if the API key is valid
if len(TRAKT_API_KEY) != 64:
    print("Invalid Trakt API key, please check your trakt_request.py file")
    sys.exit()

argparser = argparse.ArgumentParser(description="Backup your Trakt data")
argparser.add_argument("-i", "--interactive", action="store_true")
argparser.add_argument("-u", "--username", action="store", help="Your Trakt username")
argparser.add_argument(
    "-f", "--format", action="store", default="json", help="File type to save your data in (json, csv, xml)"
)
args = argparser.parse_args()

if args.interactive:
    # -Y or --yes to save files in the current working directory (optional)
    argparser.add_argument(
        "-Y", "--yes", action="store_true", help="Save files in the current working directory", required=False
    )
    # Positional argument for the username (optional)
    argparser.add_argument("username", nargs="?", help="Your Trakt username")
    # Positional argument for the file type (optional)
    argparser.add_argument("filetype", nargs="?", help="File type to save your data in (json, csv, xml)")
    args = argparser.parse_args()

    # Ask the user if they want to save the files in the current working directory
    if not args.yes:
        folder = input(
            f"Save files here (shell current working directory) ? [Y/n]\n(files will otherwise be saved in {os.path.expanduser('~')}): "
        )
    else:
        folder = "Y"

    if folder.upper() == "Y":
        root = os.getcwd()
        BACKUP_ROOT_PATH = os.path.join(root, "trakt_backup")
    else:
        root = os.path.expanduser("~")
        BACKUP_ROOT_PATH = os.path.join(root, "trakt_backup")
    if args.username:
        TRAKT_USERNAME = args.username
    else:
        TRAKT_USERNAME = input("Enter your Trakt username: ")
    if args.filetype and args.filetype in accepted_file_types:
        file_type = args.filetype.lower()
    else:
        print("Unsupported or no file type specified, defaulting to json")
else:
    if args.username:
        TRAKT_USERNAME = args.username
    FILE_TYPE = args.format


print(f"Files will be saved in: {BACKUP_ROOT_PATH}")

if not os.path.exists(BACKUP_ROOT_PATH):
    os.makedirs(BACKUP_ROOT_PATH)

timestamp = os.path.getmtime(BACKUP_ROOT_PATH)
backup_folder_name = os.path.join(BACKUP_ROOT_PATH, datetime.datetime.now().strftime("%Y-%m-%d--%H:%M:%S"))
os.makedirs(backup_folder_name)
trakt_request = TraktRequest(TRAKT_API_KEY, TRAKT_USERNAME, TRAKT_URL, backup_folder_name)

try:
    trakt_request.create_data_files()
except Exception as e:
    print(e)
    os.rmdir(backup_folder_name)
    sys.exit()

if FILE_TYPE != "json":
    convert(FILE_TYPE, backup_folder_name)

new_backup_folder_name = f"{backup_folder_name}--{FILE_TYPE}"
os.rename(backup_folder_name, new_backup_folder_name)

print(f"Backup folder name: {new_backup_folder_name}")

if args.interactive:
    launch_file(new_backup_folder_name)
print("Done.")
