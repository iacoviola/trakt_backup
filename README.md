# trakt_backup

## Usage
<ul>
<li>Clone the repository to your machine</li>
<li>Open a terminal instance within the cloned folder</li>
<li>Install requirements issuing the following command:</li>
</ul>

```bash 
pip install -r requirements.txt 
```
<ul>
<li>Run trakt_backup.py using the command:</li>
</ul>

```bash 
python ./trakt_backup.py
```
You can also run the script adding command line arguments as follows:
<ul>
<li>The first argument is used to specify the id of the user whose profile needs to be backed up <b>(if left blank the username will be requested by the program)</b></li>
<li>The second argument is used to specify the format used to save the files on your machine <b>(if left blank the program will default to JSON)</b></li>
</ul>

Example:

```bash 
python ./trakt_backup.py user1
```

Begins backing up files for user "user1".

```bash 
python ./trakt_backup.py user1 csv
```

Begins backing up files for user "user1" using "csv" format.

<b>(Supported formats: JSON, csv, XML)</b>
