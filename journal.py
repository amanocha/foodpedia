import server
import datetime
import re

db = server.get_db()

def write_emotions(username, food, emotions, notes):
    date = get_date(datetime.date.today())
    entry = {"food":food.upper(), "emotions": emotions, "notes": notes}
    print entry
    print(db.users.find({"username": username, date:{"$exists": True}}).count())
    if (db.users.find({"username": username, date:{"$exists": True}}).count() > 0):
        #print(db.users.find({"username":username})[0][date])
        entries = db.users.find({"username":username})[0][date]
        print entries
    else:
        entries = []
    entries.append(entry)
    #print entries
    db.users.update(
        {"username":username},
        {"$set": {date: entries}}
    )

def get_date(entry):
    return entry.strftime("%B %d, %Y")

'''
key: date
value: [{"food": food, "emotions": (array of words), "notes": notes}, {"food2": food, "emotions2": (array of words), "notes2": notes}]
'''
def get_calendar(username):
    doc = db.users.find({"username":username})[0]
    entries = {}
    for key in doc:
        if (re.match("[A-Za-z]+\s+[0-9]+,\s+[0-9]+", key)):
            entries[key] = doc[key]
    print entries
    return entries

write_emotions("amanocha", "broccoli", ["happy"], "")
get_calendar("amanocha")