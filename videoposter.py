# videoposter.py is reddit bot that scrapes a website to find
# the last video posted on it and creates a reddit submission
# with a link to the video, then it posts the youtube channel
# mirror as a comment in the submission.

# Made in Python 3.4.3, by /u/MorrisCasper and /u/twistitup.

import requests, time, praw, oaux, traceback
# install with "pip install beautifulsoup4"
from bs4 import BeautifulSoup
# install with "pip install --upgrade google-api-python-client"
from apiclient.discovery import build
from difflib import SequenceMatcher

### USER CONFIGURATION ###

SLEEP_TIME = 300 # Time to sleep between requesting the website in seconds
SUBREDDIT = "TwoBestFriendsPlay" # Without /r/
YOUTUBE_API_KEY = ""
HIGH_SIMILARITY = 0.99
LOW_SIMILARITY = 0.95

### END USER CONFIGURATION ###

# Returns the link and title of the lastest video on the SBFP website.
def get_latest_video():
    r = requests.get("http://superbestfriendsplay.com/category/videos/", "lxml")
    soup = BeautifulSoup(r.content, "html.parser")
    latest_list_item = soup.find("li", {"class": "archiveitem"})
    link = latest_list_item.find("div", {"class": "archivetitle"}).find("a").get("href")
    title = latest_list_item.find("div", {"class": "archivetitle"}).find("a").text
    return link, title

# Compares two strings and returns a float from 0.0 to 1.0 depending on
# the similarity of the strings.
def similar(a, b):
    return SequenceMatcher(None, a, b).ratio()

# Returns whether or not the youtube video is found and the comment is posted.
def postYoutubeComment(title_ws, submission_posted, similarity):
    service = build("youtube", "v3", developerKey=YOUTUBE_API_KEY)
    playlistItems = service.playlistItems()
    results = 50 # Maximum allowed number of requested videos
    request = playlistItems.list(
        part="snippet", playlistId="UU84X0epDRFdTrybxEX8ZWkA",
        maxResults=results)
    uploads = request.execute()
    for i in range(0, results):
        iterationTitle = uploads["items"][i]["snippet"]["title"]
        # Compare how similar the two titles are. If it's almost
        # certain that they are the same video, post the comment
        if similar(iterationTitle, title_ws) > similarity:
            print("Video title on youtube channel: " + iterationTitle)
            print("Posting youtube url comment")
            videoId = (uploads["items"][i]["snippet"]["resourceId"]["videoId"])
            videoURL = "https://www.youtube.com/watch?v=" + videoId
            submission_posted.add_comment(
                "Here is the video on Youtube! " + videoURL)
            print(
                "Submission and comment posted. Sleeping",
                SLEEP_TIME, "seconds.")
            return True
    return False

if __name__ == "__main__":
    r = oaux.login()
    subreddit = r.get_subreddit(SUBREDDIT)
    latest_link_posted = ""
    while True:
        try:
            link_ws, title_ws = get_latest_video() # Latest link and title from website
            print("Latest video on website: " + title_ws)
            if link_ws != latest_link_posted: # If link_ws not already posted
                latest_link = link_ws
                print("Posting latest video")
                submission_posted = subreddit.submit(title_ws, url = link_ws)
                # submission for testing purposes
                # r.get_submission(submission_id = '3h5hzr')
                if postYoutubeComment(
                        title_ws, submission_posted, HIGH_SIMILARITY) == False:
                    print(
                        "Submission posted but not comment.",
                        "Could not find appropriate youtube video.",
                        "Trying again with a lower similarity ratio.")
                    if postYoutubeComment(
                            title_ws, submission_posted,
                            LOW_SIMILARITY) == False:
                        print(
                            "Still couldn't find youtube video,",
                            "please find it and comment manually.",
                            "Sleeping", SLEEP_TIME, "seconds")
            else:
                print(
                    "Not posting because I already posted. Sleeping",
                    SLEEP_TIME, seconds)
            time.sleep(SLEEP_TIME)
        except KeyboardInterrupt:
            print("Shutting down.")
            break
        except Exception as e:
            print("Something bad happened!", e)
            traceback.print_exc()
            print("Waiting", SLEEP_TIME, "seconds.")
            time.sleep(SLEEP_TIME)
