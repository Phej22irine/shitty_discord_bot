from discord.ext import tasks
import datetime
import json

class user_data_class:
    def __init__(self, slur_count = 0, goon_count = 0, slur_achievement100 = False, slur_achievement1000 = False):
        self.slur_count = slur_count
        self.goon_count = goon_count
        self.slurs_achievement100 =  slur_achievement100
        self.slurs_achievement1000 =  slur_achievement1000
    
    def to_dict(self):
        return{
            "slur_count": self.slur_count,
            "goon_count": self.goon_count,
            "slur_achievement100": self.slurs_achievement100,
            "slur_achievement1000" :self.slurs_achievement1000
        }
    @classmethod
    def from_dict(cls, data):
        return cls(data["slur_count"], data["goon_count"], data["slur_achievement100"], data["slur_achievement1000"])

nensho_values = ("1210551292531834920", "768102905172983808", "nensho")

# Needed as to make sure "Nensho" and "Nenshon" accounts have the same data as per request.
def nensho_check(user_id):
    if str(user_id) in nensho_values: return "nensho"
    
    return user_id

# Loads data stuff.
def load_data():
    with open("data.json", "r") as file:
        data = json.load(file)
    
    return data

def save_data(data):
    with open("data.json", "w") as file:
        json.dump(data, file, indent=4)

# Adds user variables.
def validate_user(user_id):
    data = load_data()
    user_id = nensho_check(user_id)
    
    if user_id in data["userdata"]: return data
    
    john = user_data_class
    data["userdata"][str(user_id)] = john.to_dict()
    save_data(data)
    
    return data

# Gets user data as a struct.
def get_user_data(data, author):
    return user_data_class.from_dict(data["userdata"][author])

# Updates user data regarding slurs.
def update_slurs(author, count):
    author = nensho_check(author)
    data = load_data()
    achievement_unlocked = False
    
    if data:
        user_data = 0
        data = validate_user(author)
        user_data = get_user_data(data, author)
        user_data.slur_count += count
        
        # Achievement update 
        if user_data.slur_count >= 100 and user_data.slurs_achievement100 == False:
            user_data.slurs_achievement100 = True
            achievement_unlocked = True
    
        data["userdata"][author] = user_data.to_dict()
    
    save_data(data)
    
    return [user_data.slur_count ,achievement_unlocked]

# Updates general user data from previously existing user data.
def update_userdata():
    data = load_data()
    userdata = data["userdata"]

    for x in userdata:
        try:
            userdata[x] = user_data_class(userdata[x])
        except: pass
    
    data["userdata"] = userdata
    save_data(data)

# Counts gooner related shit.
def goon_counter(author):
    author = nensho_check(author)
    data = load_data()
    if data:
        spent = False
        data = validate_user(author)
        user_data = get_user_data(data, author)
    
        if user_data.goon_count > 0:
            spent = True
            user_data.goon_count = user_data.goon_count - 1

        data["userdata"][author] = user_data.to_dict()
    
    with open("data.json", "w") as file:
        json.dump(data, file, indent=4)

    return [spent, user_data.goon_count]

# Checks date and update tokens
def validate_date():
    global data
    data = load_data()
    
    if data:
        date = str(datetime.datetime.now().date())
    
        if data['date'] != date:
            data['date'] = date
    
            for x in data['userdata']:
                data['userdata'][x]['goon_count'] += 10
            
            save_data(data)
    
    print(str(datetime.datetime.now().time()))

# Task loop to log and update data periodically and consistently.
@tasks.loop(minutes = 1)
async def check_date(): validate_date()