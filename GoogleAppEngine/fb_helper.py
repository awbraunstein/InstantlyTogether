from facebook import *

input_access_token = "166577153373466|3b7b38e26bd1fdacbdb6cb5d-845160715|iCm98HpPMJnVIuQLdykfvX16d74x"
        
graph = GraphAPI(input_access_token)
try: 
    user = graph.get_object("me")
except:
    print "failed authentication"
    return

user_id = str(user["id"])
access_token = input_access_token

user_timezone = str(user["timezone"])

user_name = str(user["name"])
user_picture = "https://graph.facebook.com/me/picture?access_token=%s" % (input_access_token)
education_dic = user["education"] #one more level needed + need permission

#Note that this does not work for older students
for school in education_dic:
    if school["type"] == 'College':
        user_college_id = school["school"]["id"]
        user_college = school["school"]["name"]

friend_dic = graph.get_connections("me", "friends")
user_friends = []
for friend in friend_dic["data"]:
     user_friends.append(friend["id"])