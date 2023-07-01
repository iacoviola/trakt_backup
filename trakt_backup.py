import datetime
import os
import sys
import converters.json_to_csv as jtc
import converters.json_to_xml as jtx
import zipfile

from flask import Flask, request, send_file, render_template

from trakt_request import TraktRequest

app = Flask(__name__)

# We load the necessary infos from the env file
TRAKT_API_KEY = "MY_API_KEY"
TRAKT_USERNAME = "" #get from request
TRAKT_URL = "https://api.trakt.tv/users"
BACKUP_ROOT_PATH = os.path.join(os.getcwd(), "backups")

accepted_file_types = ["json", "csv", "xml"]

# Check if the API key is valid
if len(TRAKT_API_KEY) != 64:
    print("Invalid Trakt API key, please check your trakt_request.py file")
    sys.exit()

if not os.path.exists(BACKUP_ROOT_PATH):
    os.makedirs(BACKUP_ROOT_PATH)

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

def clear_folder(path):
    #recursively delete all files in folder
    for root, dirs, files in os.walk(path):
        for file in files:
            os.remove(os.path.join(root, file))
        for dir in dirs:
            clear_folder(os.path.join(root, dir))
            os.rmdir(os.path.join(root, dir))


@app.route("/backup", methods=["GET"])
def get_backup():
    if request.method == "GET":
        TRAKT_USERNAME = request.args.get("username")
        tmp_file_type = request.args.get("filetype")
        if TRAKT_USERNAME is not None and TRAKT_USERNAME != "":
            if tmp_file_type in accepted_file_types or tmp_file_type is not None:
                FILE_TYPE = tmp_file_type
            else:
                FILE_TYPE = "json"

            backup_folder_name = f"{TRAKT_USERNAME}--{datetime.datetime.now().strftime('%Y-%m-%d--%H:%M:%S')}"
            backup_folder_path = os.path.join(BACKUP_ROOT_PATH, backup_folder_name)
            print(f"Backup folder name: {BACKUP_ROOT_PATH}")
            os.makedirs(backup_folder_path)

            trakt_request = TraktRequest(TRAKT_API_KEY, TRAKT_USERNAME, TRAKT_URL, backup_folder_path)

            try:
                trakt_request.create_data_files()
            except Exception as e:
                os.rmdir(backup_folder_path)
                sys.exit()


            if FILE_TYPE != "json":
                convert(FILE_TYPE, backup_folder_path)

            new_backup_folder_name = f"{backup_folder_path}--{FILE_TYPE}"
            os.rename(backup_folder_path, new_backup_folder_name)

            print(f"Backup folder name: {new_backup_folder_name}")

            #zip the folder
            zip_name = f"{new_backup_folder_name}.zip"
            with zipfile.ZipFile(zip_name, "w", zipfile.ZIP_DEFLATED) as zip:
                for root, dirs, files in os.walk(new_backup_folder_name):
                    for file in files:
                        zip.write(os.path.join(root, file), os.path.relpath(os.path.join(root, file), os.path.join(new_backup_folder_name, "..")))

            return send_file(zip_name, mimetype="application/zip")
        
        else:
            if request.args.get("username") == "":
                return render_template("form.html", error="Please enter a username")
            return render_template("form.html")
        

app.run(host="127.0.0.1", port=8080, debug=True)

get_backup()

print("Done.")
