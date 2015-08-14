# Made in Python 3.4.3, by /u/MorrisCasper.
# TODO: Oauth, replying to submission_posted with the Youtube URL. 
# I don't know anything about the Youtube API and I don't want to scrape youtube.com because I don't want to get banned.
import requests
from bs4 import BeautifulSoup
import time
import praw

### USER CONFIGURATION ###

SLEEP_TIME = 300 # Time to sleep between requesting the website in seconds
SUBREDDIT = "TwoBestFriendsPlay" # Without /r/
USER_AGENT = "Youtube and website poster v0.1" # A short description about the bot visible to Reddit
USERNAME = ""
PASSWORD = ""

### END USER CONFIGURATION ###

def get_latest_video():
    r = requests.get("http://superbestfriendsplay.com/category/videos/", "lxml")
    soup = BeautifulSoup(r.content)
    latest_list_item = soup.find("li", {"class": "archiveitem"})

    link = latest_list_item.find("div", {"class": "archivetitle"}).find("a").get("href")
    title = latest_list_item.find("div", {"class": "archivetitle"}).find("a").text

    return link, title

if __name__ == "__main__":
    r = praw.Reddit(USER_AGENT)
    # TODO: Oauth 2
    r.login(USERNAME, PASSWORD)
    subreddit = r.get_subreddit(SUBREDDIT)
    latest_link_posted = ""
    while True:
        link_ws, title_ws = get_latest_video() # Latest link and title from website
        print("Latest video on website: " + title_ws)
        if link_ws != latest_link_posted: # If link_ws not already posted
            latest_link = link_ws
            print("Posting latest video")
            submission_posted = subreddit.submit(title_ws, url = link_ws)
            # TODO: Reply to submission_posted with the Youtube URL
        else:
            print("Not posting because I already posted")
        time.sleep(SLEEP_TIME)