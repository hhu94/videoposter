# oaux is an OAuth auxiliary tool for PRAW that helps you setup,
# login and refresh the OAuth for your bot/script/app.
# Made with Python 3.4.0 by /u/twistitup

import praw, time

# Fill in APP_ID and SECRET first. They can be found on the Reddit app settings.
USER_AGENT = "Youtube and website poster:1.0 (by /u/MorrisCasper and /u/twistitup)"
APP_ID = ""
SECRET = ""
URI = "https://127.0.0.1:65010/authorize_callback"

SCOPES = (
    "identity edit flair history modconfig modflair modlog modposts "
    "modwiki mysubreddits privatemessages read report save submit subscribe "
    "vote wikiedit wikiread")

# Run firstSetup() from the python console to retrieve a REFRESH_TOKEN.
REFRESH_TOKEN = ""

# Make sure you're logged into your bot Reddit account on your browser first.
def firstSetup():
    r = praw.Reddit(USER_AGENT)
    r.set_oauth_app_info(APP_ID, SECRET, URI)
    url = r.get_authorize_url("access_code", SCOPES, True)
    import webbrowser
    webbrowser.open(url)
    access_code = input(
        "Please enter access code obtained from browser url, it is after "
        "\"code=\": ")
    access_information = r.get_access_information(access_code)
    r.set_access_credentials(**access_information)
    print(access_information)
    print(
        "Copy the refresh_token above and paste it into the REFRESH_TOKEN "
        "field in your oaux.py. Then you are good to go!")
    return r

# Use r = oaux.login() in your bot file and you'll be logged in!
def login():
    r = praw.Reddit(USER_AGENT)
    r.set_oauth_app_info(APP_ID, SECRET, URI)
    r.refresh_access_information(REFRESH_TOKEN)
    print("Starting time:", time.strftime("%a, %d %b %Y %H:%M:%S",
            time.localtime()))
    return r

# Check if 50 minutes have passed since last refresh time.
# If so, then refreshes the token and updates the last refresh time.
def checkRefresh(r, last_refresh_time):
    if last_refresh_time + 3000 < time.time():
        r.refresh_access_information(REFRESH_TOKEN)
        print("Refresh time:", time.strftime("%a, %d %b %Y %H:%M:%S",
                time.localtime()))
        last_refresh_time = time.time()
    return last_refresh_time
