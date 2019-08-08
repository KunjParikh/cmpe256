from pymongo import MongoClient
import datetime

class Redditdb:

    def __init__(self):
        client = MongoClient()
        db = client.Reddit
        self.users = db.users
        self.subreddits = db.subreddits

    def insertUser(self, username, subreddits):
        user = {
            'username': username,
            'subreddits' : subreddits,
            'updated' : datetime.datetime.utcnow()
        }
        collection = self.users
        userID = collection.update({'username': user['username']}, 
            {'username': user['username'], 
                'subreddits' : user['subreddits'], 
                'updated': user['updated']}, 
            upsert=True)
        return userID

    def insertSub(self, sub):
        sub = {
            'name': sub,
            'updated' : datetime.datetime.utcnow()
        }
        collection = self.subreddits
        subID = collection.update({'name': sub['name']}, 
            {'name':sub['name'], 
                'updated': sub['updated']}, 
            upsert=True)
        return subID

    def queryUser(self, username):
        collection = self.users
        user = collection.find_one({'username': username})
        return user

    def update(self, username, subreddits):
        collection = self.users
        collection.update({'username': username}, {"$set": {'subreddits': subreddits}})

    def getSubreddits(self):
        return self.subreddits.find()

    def allUsersInArray(self, userArray):
        return self.users.find({'username': {"$in": userArray}})

    def allUsers(self):
        return self.users.find()

    #Use aggregate instead of find_one to get random user
    def getUser(self):
        return self.users.aggregate([{ "$sample" : {"size":1}}]).next()

    def tmpList(self):
        return self.tmp.find()

    def tmpInsert(self, items):
        return self.tmp.insert(items)
