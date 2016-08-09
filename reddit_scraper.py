import praw
from time import sleep
import delorean

USER_AGENT = "YasuoPostChecker"

r = praw.Reddit(user_agent = USER_AGENT)

global found_submissions
found_submissions = []

def scrape_subreddit(search_term, search_time, subreddit="leagueoflegends", content="hot"):
    f = open(search_term + "_" + search_time + ".txt" , "a")
    subreddit = r.get_subreddit(subreddit)
    
    if content == "new":
        submissions = subreddit.get_new(limit = 25)
    elif content == "top":
        submissions = subreddit.get_top(limit = 25)
    else:
        submissions = subreddit.get_hot(limit = 25)  
    
    for submission in submissions:
        if submission.id not in found_submissions:
            if search_term.lower() in submission.title.lower() or search_term.lower() in submission.selftext:
                found_submissions.append(submission.id)
                print(submission.title)
                print(submission.url)
                f.write(submission.title + ":\n")
                f.write(submission.url)
                f.write("\n\n")
    f.close()

if __name__ == "__main__":
    time = delorean.now().datetime
    search_time = str(time.year) + str(time.month) + str(time.day) + str(time.hour) + str(time.minute)
    term = input("Enter a search term: ")
    to_be_scraped = []
    subreddit = ""
    print("Enter all the subreddits you want to scrape (or n to stop entering subreddits.")
    while True:
        subreddit = input("Subreddit: ")
        if subreddit == "n":
            break
        else:
            to_be_scraped.append(subreddit)
    
    while True:
        print("Scraping...")
        for sub in to_be_scraped:            
            scrape_subreddit(search_time=search_time, search_term=term)
            scrape_subreddit(search_time=search_time, content="new",search_term=term)
            scrape_subreddit(search_time=search_time, content="top",search_term=term)
        print("Going to sleep.")
        sleep(60)
    
