# oaux is an OAuth auxiliary tool for PRAW that helps you setup,
# login and refresh the OAuth for your bot/script/app.
# Made with Python 3.4.0 by /u/twistitup

import praw, configparser, time

# You should have already created a reddit app in your bot's account
# before using this tool.
# Fill in appID and secret in oaux.ini manually.
# These values can be found in your reddit app settings.

# Run setup() from the python console to retrieve a refreshToken.
# It will be automatically written into oaux.ini.
# Make sure you're logged into your bot's reddit account on your browser first.
def setup():
    config = configparser.ConfigParser()
    config.read("oaux.ini")
    r = praw.Reddit(config["DEFAULT"]["userAgent"])
    r.set_oauth_app_info(
        config["DEFAULT"]["appID"], config["DEFAULT"]["secret"],
        config["DEFAULT"]["URI"])
    url = r.get_authorize_url("accessCode", config["DEFAULT"]["scopes"], True)
    import webbrowser
    webbrowser.open(url)
    time.sleep(1)
    accessCode = input(
        "Please click Allow, then find the access code found in the" +
        " resulting URL right after \"code=\". Enter the access code here: ")
    accessInfo = r.get_access_information(accessCode)
    r.set_access_credentials(**accessInfo)
    config["DEFAULT"]["refreshToken"] = accessInfo["refresh_token"]
    with open("oaux.ini", "w") as modifiedConfig:
        config.write(modifiedConfig)
    print(
        "Your OAuth is all set up and ready to go! Use r = oauth.login()",
        "in your bot to obtain a PRAW AuthenticatedReddit instance.")

# Use r = oaux.login() in your bot file and you'll be logged in!
# Returns a PRAW AuthenticatedReddit instance.
def login():
    config = configparser.ConfigParser()
    config.read("oaux.ini")
    r = praw.Reddit(config["DEFAULT"]["userAgent"])
    r.set_oauth_app_info(
        config["DEFAULT"]["appID"], config["DEFAULT"]["secret"],
        config["DEFAULT"]["URI"])
    r.refresh_access_information(config["DEFAULT"]["refreshToken"])
    print("Login time:", time.strftime("%a, %d %b %Y %H:%M:%S",
            time.localtime()))
    print("Logged in as", r.get_me().name)
    return r
