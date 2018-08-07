import couchdb #Libreria de CouchDB (requiere ser instalada primero)
from tweepy import Stream #tweepy es la libreria que trae tweets desde la API de Twitter (requiere ser instalada primero)
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener
import json #Libreria para manejar archivos JSON


###Credenciales de la cuenta de Twitter########################
#Poner aqui las credenciales de su cuenta privada, caso contrario la API bloqueara esta cuenta de ejemplo
ckey = "xoUZMGGfFyHG4HYTnvYIbtz55"
csecret = "raYqPyiGwMwLKdNg9enl7ZbNetNnQjiuuGV40D4DnnT3ypx4P9"
atoken = "958164408689184768-wBgRQaUgK0PaVzRbT1ojQlxP9HP1Esd"
asecret = "TQPmcHvFchLRpKkcEBvUWOdjy867K30Ujt2mqeVKGhNZt"
#####################################

class listener(StreamListener):
    
    def on_data(self, data):
        dictTweet = json.loads(data)
        try:
            dictTweet["_id"] = str(dictTweet['id'])
            #Antes de guardar el documento puedes realizar parseo, limpieza y cierto analisis o filtrado de datos previo
            #a guardar en documento en la base de datos
            doc = db.save(dictTweet) #Aqui se guarda el tweet en la base de couchDB
            print ("Guardado " + "=> " + dictTweet["_id"])
        except:
            print ("Documento ya existe")
            pass
        return True
    
    def on_error(self, status):
        print (status)
        
#Autenticaciones       
auth = OAuthHandler(ckey, csecret)
auth.set_access_token(atoken, asecret)
twitterStream = Stream(auth, listener())

#Setear la URL del servidor de couchDB
server = couchdb.Server('http://localhost:5984/')
try:
    #Si no existe la Base de datos la crea
    db = server.create('guayaquil')
except:
    #Caso contrario solo conectarse a la base existente
    db = server['guayaquil']
    
#Aqui se define el bounding box con los limites geograficos donde recolectar los tweets
##twitterStream.filter(track=["DilesNo","PorLaPatriaDilesNo","VotaTodoSí","7VecesSí"])
#track arreglo de streams
#location con gps
twitterStream.filter(locations=[-79.95752,-2.238571,-79.864136,-2.056909])
