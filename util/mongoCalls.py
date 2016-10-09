from pymongo import MongoClient

def checkUser(collection, userName):
    x = list(collection.find({'emails.address':userName}, {'emails':1, 'profile.name':1, 'profile.school':1, 'profile.travel.zipcode':1}))
    if len(x) > 0:
        return (True,x[0])
    else:
        return (False, None)

def updateInfo(collection, id, data):
    #Todo update id with data
