# trakt_backup

## Usage

> **Note** <br>
> <b>First you need to generate your own API key on trakt's website. </b><br>
> Instructions:
> <ul>
> <li>Go to <a href="https://trakt.tv">trakt.tv</a></li>
> <li>Login with your account</li>
> <li>From the menu in the top right corner select <a href="https://trakt.tv/settings">Settings</a></li>
> <li>From the menu bar choose <a href="https://trakt.tv/oauth/applications">Your API apps</a></li>
> <li>Press on <a href="https://trakt.tv/oauth/applications/new">NEW APPLICATION</a></li>
> <li>Fill in the required fields <b>(Name, Description and Redirect URI)</b> and then press <b>SAVE APP</b> at the bottom of the page</li>
> <li>In the next section copy the <b>Client ID</b> string and paste it at the bottom of the <b>trakt_request.py</b> file where indicated.</li>
> </ul>
> <img width="433" alt="Screenshot 2023-01-03 at 4 39 58 PM" src="https://user-images.githubusercontent.com/26089090/210390686-14160db7-53e8-4481-a1db-8aca23e9647e.png">


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
