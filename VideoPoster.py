# Made in Python 3.4.3, by /u/MorrisCasper and /u/twistitup.
import requests, time, praw, oaux, traceback
from bs4 import BeautifulSoup
from apiclient.discovery import build
from difflib import SequenceMatcher

### USER CONFIGURATION ###

SLEEP_TIME = 300 # Time to sleep between requesting the website in seconds
SUBREDDIT = "TwoBestFriendsPlay" # Without /r/
YOUTUBE_API_KEY = ""

### END USER CONFIGURATION ###

def get_latest_video():
    r = requests.get("http://superbestfriendsplay.com/category/videos/", "lxml")
    soup = BeautifulSoup(r.content, "html.parser")
    latest_list_item = soup.find("li", {"class": "archiveitem"})

    link = latest_list_item.find("div", {"class": "archivetitle"}).find("a").get("href")
    title = latest_list_item.find("div", {"class": "archivetitle"}).find("a").text

    return link, title

def similar(a, b):
    return SequenceMatcher(None, a, b).ratio()

def postYoutubeComment(title_ws, submission_posted):
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
        if similar(iterationTitle, title_ws) > 0.99:
            print("Posting youtube url comment")
            videoId = (uploads["items"][i]["snippet"]["resourceId"]["videoId"])
            videoURL = "https://www.youtube.com/watch?v=" + videoId
            submission_posted.add_comment(
                "Here is the video on Youtube! " + videoURL)
            return

if __name__ == "__main__":
    r = oaux.login()
    last_refresh_time = time.time()
    subreddit = r.get_subreddit(SUBREDDIT)
    latest_link_posted = ""
    while True:
        try:
            last_refresh_time = oaux.checkRefresh(r, last_refresh_time)
            link_ws, title_ws = get_latest_video() # Latest link and title from website
            print("Latest video on website: " + title_ws)
            if link_ws != latest_link_posted: # If link_ws not already posted
                latest_link = link_ws
                print("Posting latest video")
                submission_posted = subreddit.submit(title_ws, url = link_ws)
                # submission for testing purposes
                # r.get_submission(submission_id = '3h5hzr')
                postYoutubeComment(title_ws, submission_posted)
            else:
                print("Not posting because I already posted")
            time.sleep(SLEEP_TIME)
        except KeyboardInterrupt:
            print("Shutting down.")
            break
        except praw.errors.HTTPException as e:
            exc = e._raw
            print("Something bad happened! HTTPError", exc.status_code)
            if exc.status_code == 503:
                print("Let's wait til reddit comes back! Sleeping 60 seconds.")
                time.sleep(60)
        except Exception as e:
            print("Something bad happened!", e)
            traceback.print_exc()
