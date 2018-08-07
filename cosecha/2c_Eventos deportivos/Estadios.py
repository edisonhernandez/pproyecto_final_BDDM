import couchdb #Libreria de CouchDB (requiere ser instalada primero)
from tweepy import Stream #tweepy es la libreria que trae tweets desde la
#API de Twitter (requiere ser instalada primero)
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener
import json #Libreria para manejar archivos JSON


###Credenciales de la cuenta de Twitter########################
#Poner aqui las credenciales de su cuenta privada, caso contrario
#la API bloqueara esta cuenta de ejemplo
ckey = "UvrUEQZpfYHaUtU2cmw1somPl"
csecret = "Ql34YqGNCwdnd7DG1hv3CgRuayYjC46ItKUuu0WEtw5AiCgBBV"
atoken = "375942730-51BEzcTtIq5UdQ7kdlHf8W5u4LnkVyXGQl45eSLi"
asecret = "gn73ZudvSeXrjEneD1dl9gdDr1JCjXLe8guoYRDdvJjL3"
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
        
auth = OAuthHandler(ckey, csecret)
auth.set_access_token(atoken, asecret)
twitterStream = Stream(auth, listener())

#Setear la URL del servidor de couchDB
server = couchdb.Server('http://localhost:5984/')
try:
    #Si no existe la Base de datos la crea
    db = server.create('estadios')
except:
    #Caso contrario solo conectarse a la base existente
    db = server['estadios']
    
#Aqui se define el bounding box con los limites geograficos donde recolectar los tweets
twitterStream.filter(locations=[-78.4785483997,-0.1793371263,-78.4746484678,-0.1759790167])
twitterStream.filter(locations=[-79.9273135233,-2.1879918428,-79.9224962759,-2.183478289])
twitterStream.filter(locations=[-78.4909271665,-0.1091603768,-78.4877489197,-0.1063308197])
twitterStream.filter(locations=[-79.8951401803,-2.2080647803,-79.8924422197,-2.2053668197])
twitterStream.filter(locations=[-79.8961293803,-2.1802633803,-79.8928599383,-2.1775654197])

##twitterStream.filter(track=["Monumental Isidro Romero Carbo","Modelo Alberto Spencer","Rodrigo Paz Delgado",
                           # "George Capwell","Olímpico Atahualpa"])
