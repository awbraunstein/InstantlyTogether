from google.appengine.ext import db
from google.appengine.ext import webapp
from google.appengine.ext.webapp import util
from google.appengine.ext.webapp import template
from google.appengine.ext import webapp

from django.utils import simplejson
import wsgiref.handlers

import logging, datetime, re
import os
import os.path

import facebook, dateandtime, users

class User(db.Model):
    user_id = db.StringProperty(required=True)
    access_token = db.StringProperty(required=True)

    user_timezone = db.StringProperty()
    user_created = db.DateTimeProperty(auto_now_add=True)
    
    user_name = db.StringProperty(required=True)
    user_picture = db.StringProperty(required=True)
    
    user_email = db.EmailProperty() # This can be used to help verify a person's location
    user_phone = db.PhoneNumberProperty() # This can be used to verify a person's location
    
    user_college_id = db.StringProperty()
    user_college = db.StringProperty()
    
    user_friends = db.StringListProperty()
    
    last_time = db.DateTimeProperty()
    last_location = db.GeoPtProperty()
    last_category = db.StringProperty(choices=set(['anything', 'food', 'play', 'work', 'none']))
    last_suggestion = db.StringProperty() 
    
def get_user(input_user_id):
    logging.debug("Trying to get a user")
    user_id_query = User.all().filter('user_id =', input_user_id)
    user_id_result = user_id_query.fetch(1)
    logging.debug("")
    if user_id_result == []:
        logging.debug("The user does not exist, return None")
        return None
        
    else:
        logging.debug("The user exists" + str(user_id_result[0].user_name))
        return user_id_result[0]
        
    
def new_user(input_access_token):
    
    logging.debug("Trying to create a new user.")
    
    graph = facebook.GraphAPI(input_access_token)
    user = graph.get_object("me")
    
    user_id = str(user["id"])
    access_token = input_access_token
    
    user_timezone = str(user["timezone"])
    
    user_name = str(user["name"])
    user_picture = "https://graph.facebook.com/me/picture?access_token=%s" % (input_access_token)
#    education_dic = user["education"] #one more level needed + need permission
    
    #Note that this does not work for older students
#    for school in education_dic:
#        if school["type"] == 'College':
#            user_college_id = school["school"]["id"]
#            user_college = school["school"]["name"]
    
    friend_dic = graph.get_connections("me", "friends")
    user_friends = []
    for friend in friend_dic["data"]:
         user_friends.append(friend["id"])
    
         
    new_user = User(
                user_id = user_id, 
                access_token = access_token, 
                
                user_timezone = user_timezone, 
                
                user_name = user_name, 
                user_picture = user_picture,
#                user_college_id = user_college_id,
#                user_college = user_college,
                
                user_friends = user_friends)
    new_user.put()
    
    return new_user

def update_user(input_access_token):
        
    graph = facebook.GraphAPI(input_access_token)
    user = graph.get_object("me")
    user_id = str(user["id"])
    access_token = input_access_token
    user_timezone = str(user["timezone"])
    user_name = str(user["name"])
    user_picture = "https://graph.facebook.com/me/picture?access_token=%s" % (input_access_token)
   
    friend_dic = graph.get_connections("me", "friends")
    user_friends = []
    for friend in friend_dic["data"]:
         user_friends.append(friend["id"])
    
    updated_user = get_user(user_id)
    updated_user.access_token = access_token
    
    updated_user.user_timezone = user_timezone 
    
    updated_user.user_name = user_name
    updated_user.user_picture = user_picture

    updated_user.user_friends = user_friends
    logging.debug("his friends are" + str(user_friends))
    updated_user.put()
    

def message_friends(input_user_id):
    pass

def check_in(user_id, access_token):
    user = get_user(user_id)
    if user == None:
        logging.debug("tring to create a new user")
        user = new_user(access_token)
        logging.debug("created a new user")
    else:
        update_user(access_token)
        
    user.last_time = datetime.datetime.now()
    user.put()
    logging.debug("set datetime: " + str(user.last_time))

def phone_in(phone_number = "+6107610083"): #+15165265739 #14842380812
    user_id_query = User.all().filter('user_phone =', phone_number)
    user_id_result = user_id_query.fetch(1)
    if user_id_result != []:
        user = user_id_result[0]
        user.last_time = datetime.datetime.now()
    
def get_free_friends(input_user_id): # make faster by not finding again
    
    output = ""
    
    logging.debug("start get_free_friends")
    user = get_user(input_user_id)
    
    output+=user.user_name
    
    user_id_query = User.all()
    user_id_result = user_id_query.fetch(5000)
    
    output+="are in the database {"
    person_list = []
    for person in user_id_result:
        person_list.append(person.user_id)
        output+=str(person.user_id)+" "
    output+="}"
    
    logging.debug("Converting to set to get intersection")
    
    ppl_in_database = set(person_list)
    friends = set(user.user_friends)
    out_ppl_in_database = str(ppl_in_database)
    out_friends = str(friends)
    output+="         ppl_in_database:\n"+out_ppl_in_database+"             friends"+out_friends
    potential = ppl_in_database.intersection(friends)
    potential = list(potential)    
    logging.debug("After converting to set")
    logging.debug(str(potential))
    
    free_list = []
    
    for person in potential:
        person = get_user(person)
        if dateandtime.within(datetime.datetime.now(), person.last_time):
            free_list.append(person.user_id)
    
    return free_list
    
def get_user_id(input_access_token):
   
    try:
        graph = facebook.GraphAPI(input_access_token)
        user = graph.get_object("me")
    except:
        return "NONE" 
    
    
    user_id = str(user["id"])
    return user_id

def get_json_ready_dic(free_people_id):
    the_list = []
    for id in free_people_id:
        user = get_user(id)
        item = {"id":str(id),
         "name":str(user.user_name),
         "user_picture":user.user_picture, # change back
         "last_time":str(user.last_time)} # change back
        the_list.append(item)
        
    newlist = sorted(the_list, key=lambda k: k['last_time'])
    newlist = newlist.reverse()
    
    return {"data": the_list}