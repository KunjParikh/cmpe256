#! /usr/bin/env python

from mongo import Redditdb
import dataset
from pprint import pprint
import inspect
import pandas as pd
from sklearn.neighbors import NearestNeighbors

def createDataframe():
    db = Redditdb()
    users = db.allUsers()
    data = {}
    
    for user in users: 
        subs = {x : 1 for x in user['subreddits']}
        data[user['username']] = subs
    
    df = pd.DataFrame.from_dict(data, orient='index')
    df = df.fillna(0)
    return df

def findNeighbors(df, username):
    neigh = NearestNeighbors(n_neighbors=10, metric = 'cosine')
    neigh.fit(df)
    dist, ind = neigh.kneighbors(df.loc[username].values.reshape(1,-1))
    names = [df.iloc[i].index for i in ind]
    return names[0][1:], 1/(dist[0][1:])

def getRecommendedSubreddit(df, names, similarities, username):
    result = pd.Series()
    for name, sim in zip(names, similarities):
        s = df.loc[name]
        s =  s * sim
        result = result.add(s, fill_value=0.0)
    
    result = result.sort_values(ascending=False)
    result = result[result > 0.0]
    result = result.index

    alreadySub = df.loc[username]
    alreadySub = alreadySub[alreadySub > 0.0]
    alreadySub = alreadySub.index

    result = [x for x in result if x not in alreadySub]

    return result

if __name__ == "__main__":
    #username = input()
    username = Redditdb().getUser()['username']
    dataset.getComments(username)

    df = createDataframe()
    names, sim = findNeighbors(df, username)
    rec = getRecommendedSubreddit(df, names, sim, username)
    print("Recommended subreddit for user {} is {}".format(username, rec[0]))



