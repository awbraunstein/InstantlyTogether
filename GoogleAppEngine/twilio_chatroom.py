import json

entry1 = {"id" : "123", "name" : "Jonathan", "last_status" : "Say Hi"}
entry2 = {"id" : "456", "name" : "Leung", "last_status" : "Say Bye"}
print json.dumps({"data" : [entry1,entry2]})
