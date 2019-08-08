from multiprocessing import Pool, cpu_count
import praw
#from praw.handlers import MultiprocessHandler
from mongo import Redditdb
import datetime
import sys
import requests
from pprint import pprint
from tqdm import tqdm

def getSubredditUsers(subreddit, limit=250) -> list:
    """
    Get the commentors in a subreddit. Skip users existing in db
    """
    #reddit = praw.Reddit(user_agent="kNN Subreddit Recommendation Engine", handler=MultiprocessHandler())
    db = Redditdb()
    reddit = praw.Reddit(user_agent="kNN Subreddit Recommendation Engine")
    subreddit = reddit.subreddit(subreddit)
    comments = subreddit.comments(limit=limit)
    currentUsers = db.allUsers()
    if currentUsers:
        found = [user['username'] for user in currentUsers]
    else:
        found = []
    users = []
    for comment in comments:
        if comment.author.name not in found:
            users.append(comment.author.name)
    return users

def getComments(username):
    """
    Return the subreddits a user has commented in.
    """
    db = Redditdb()
    try:
        unique_subs = []
        #reddit = praw.Reddit(user_agent="kNN Subreddit Recommendation Engine", handler=MultiprocessHandler())
        reddit = praw.Reddit(user_agent="kNN Subreddit Recommendation Engine")
        user = reddit.redditor(username)
        subs = []

        for comment in user.comments.new(limit=250):
            if comment.subreddit.display_name not in subs:
                subs.append(comment.subreddit.display_name)
            db.insertSub(comment.subreddit.display_name)
        return db.insertUser(username, subs)
    except requests.exceptions.HTTPError as e:
        print(e)
        pass

def cron(user):
    db = Redditdb()
    if abs(datetime.datetime.utcnow() - user['updated']).days >= 1:
        return db.getComments(username)

def main():
    numUsers = 100

    users = getSubredditUsers('all', numUsers)
    try:
        #Can't use class methods in Pool
        pool = Pool(processes=(cpu_count()*6))
        for _ in tqdm(pool.imap(getComments, iter(users)), total=numUsers):
            pass
        pool.close()
        pool.join()
    except KeyboardInterrupt:
        pool.terminate()
        sys.exit()

if __name__ == "__main__":
    main()
