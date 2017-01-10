from pymongo import MongoClient

def get_db():
    client = MongoClient('mongodb://amanocha:food@ds159237.mlab.com:59237/heroku_rfsb5xrr')
    db = client.heroku_rfsb5xrr
    return db