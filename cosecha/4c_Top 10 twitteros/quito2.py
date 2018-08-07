import couchdb #Libreria de CouchDB (requiere ser instalada primero)
from tweepy import Stream #tweepy es la libreria que trae tweets desde la
#API de Twitter (requiere ser instalada primero)
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener
import json #Libreria para manejar archivos JSON


###Credenciales de la cuenta de Twitter########################
#Poner aqui las credenciales de su cuenta privada, caso contrario
#la API bloqueara esta cuenta de ejemplo
ckey = "et7mSb13N6xJ4BEYEjDAdzEqO"
csecret = "E855g2ROj98sR2h8xMFEGxDR5t9H2aQwYIeUqSvsOCrby94wUr"
atoken = "388324185-Fu6TS5OvtNe9anFMxaKSGUlcdZic6g87Ycb2fBEs"
asecret = "XSTkmXt52oCS6eYi2G4okZh7bsJ0vtTNKds4vYon60oqb"
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
    db = server.create('quito')
except:
    #Caso contrario solo conectarse a la base existente
    db = server['quito']
    
#Aqui se define el bounding box con los limites geograficos donde recolectar los tweets
#twitterStream.filter(track=["mundial","rusia2018","Mundial","Rusia2018"])
twitterStream.filter(locations=[-78.556822,-0.29526,-78.398894,-0.064549])
