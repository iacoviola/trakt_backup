# Trakt Backup

> Backup user data from Trakt into JSON/CSV/XML format

Warning, you need to have a **public account** in order to use the API.

## Online Version (No API key required)
You can use this script without having to create your own API key.

Simply go to:

> https://iacoviola.pythonanywhere.com/backup

Enjoy 😃.

## Setup

Clone the project and create the .env file

```bash
cd trakt_backup
cp .env.example .env
```

### Trakt API key

- Create an API key here: https://trakt.tv/oauth/applications/new
  - Fill in the required fields <b>(Name, Description and Redirect URI)</b> and then press <b>SAVE APP</b> at the bottom of the page
- Copy the **Client ID** field inside the .env file
- Fill other fields in the .env file if you don't need to specify it when running the script

## Requirements

Setup a venv and install requirements:


```bash
python3.9 -m venv ./venv

# If you use bash
source venv/bin/activate
# If you use fish
source venv/bin/activate.fish

pip install -r requirements.txt 
```

## Usage

Interactive mode:

```bash 
python ./trakt_backup.py -i
```

You can specify the username and format using the options:

```bash
python ./trakt_backup.py -u user -f csv
```

```
usage: trakt_backup.py [-h] [-i] [-u USERNAME] [-f FORMAT]

Backup your Trakt data

options:
  -h, --help            show this help message and exit
  -i, --interactive
  -u USERNAME, --username USERNAME
                        Your Trakt username
  -f FORMAT, --format FORMAT
                        File type to save your data in (json, csv, xml)
```

## Cron

Want to backup periodically ? Simply setup a cron:

```
30 12 * * * root /<path>/trakt_backup/venv/bin/python /<path>/trakt_backup/trakt_backup.py
```

Every day at 12:30 (https://crontab.guru/)
