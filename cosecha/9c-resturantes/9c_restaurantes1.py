
import couchdb #Libreria de CouchDB (requiere ser instalada primero)
from tweepy import Stream #tweepy es la libreria que trae tweets desde la API de Twitter (requiere ser instalada primero)
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener
import json #Libreria para manejar archivos JSON

print("restaurante")
ckey = "tt9hxmB4nXMPkGM2X2sZB2QZi"
csecret = "qVnKRRWLoL6t4hiw1uVEOAHtI4CMbfLJJautW9EpCyAUbHJKwT"
atoken = "999027968683978753-UrAz3OQBtu0Wl3HG9o6AheDqHjGQSKM"
asecret = "tzzT8ZLItqlIds3ygvWEgIWagOe4EppnE6On8dmN2Z2K0"
class listener(StreamListener):
    
    def on_data(self, data):
        dictTweet = json.loads(data)
        try:
            dictTweet["_id"] = str(dictTweet['id'])
           
            doc = db.save(dictTweet) #Aqui se guarda el tweet en la base de couchDB
            print ("Guardado " + "=> " + dictTweet["_id"])
        except:
            print ("Documento ya existe")
            pass
        return True
    
    def on_error(self, status):
        print (status)
        
auth = OAuthHandler(ckey, csecret)
auth.set_access_token(atoken, asecret)
twitterStream = Stream(auth, listener())

#Setear la URL del servidor de couchDB
server = couchdb.Server('http://localhost:5984/')
try:
    #Si no existe la Base de datos la crea
    db = server.create('restaurantes_citioss')
except:
    #Caso contrario solo conectarse a la base existente
    db = server['restaurantes_citioss']
    
#Aqui se define el bounding box con los limites geograficos donde recolectar los tweets
#twitterStream.filter(locations=[-78.512329,-0.220164,-78.512329,-0.220164])
twitterStream.filter(track=['Restaurante','Restaurantes'])
