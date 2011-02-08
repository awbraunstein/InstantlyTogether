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


  
def remove_www(handler):
    if handler.request.url.startswith('http://www.'):
        handler.redirect(handler.request.url.replace('http://www.', 'http://'))

def makeStatic(template_name, context={}):
    class Static(webapp.RequestHandler):
        def get(self):
            remove_www(self)
            self.response.headers['Content-Type'] = 'text/html'
            self.response.out.write(
                render(template_name, context)
            )
    return Static

class WhoseFree(webapp.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/javascript'
        
        access_token = self.request.get('access_token', default_value = "NONE")
        
        user_id = users.get_user_id(access_token)
        if user_id == "NONE":
            self.response.out.write("Error: Invalid access token")
        users.check_in(user_id, access_token)
        json = "filler text"
        available_peeps_id_list = users.get_free_friends(user_id)
        #try:
        
        json = simplejson.dumps(users.get_json_ready_dic(available_peeps_id_list))
        #json = users.get_json_ready_dic(available_peeps_id_list)
        #json = str(available_peeps_id_list)
        
        #except:
        #json = "{'Oops. Something went wrong...'}"
        
        self.response.out.write(json)

class Http404Page(webapp.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/html'
        self.error(404)
        self.response.out.write(render('404.html', {
            'path': self.request.path,
        }))

class ListOfStrings(db.Model):
    incomming_string = db.StringProperty() 
       
class Voice(webapp.RequestHandler):
    def get(self):        
        self.response.headers['Content-Type'] = 'text/xml'
        phone = self.request.get('From', default_value = "NONE")
        json = "<Response><Say>Your record has been updated</Say></Response>"
        users.phone_in()
#        if phone != "NONE":
#            phone_in()
        self.response.out.write(json)

def main():
    logging.getLogger().setLevel(logging.DEBUG)
    from wsgiref.handlers import CGIHandler
    application = webapp.WSGIApplication([
        ('/', makeStatic('index.html')),
        ('/Voice', Voice),
        ('/whose_free.json', WhoseFree),
        ('/.*$', Http404Page),
    ], debug=True)
    CGIHandler().run(application)

template_dir = os.path.join(os.path.dirname(__file__), 'templates')
from google.appengine.ext.webapp import template
def render(template_name, context={}):
    path = os.path.join(template_dir, template_name)
    return template.render(path, context)

if __name__ == "__main__":
    main()
