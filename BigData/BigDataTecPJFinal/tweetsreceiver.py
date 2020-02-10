
"""
Created on Thu Jan 23 19:23:22 2020

@author: pherrera
"""


import tweepy
from tweepy.auth import OAuthHandler
from tweepy import Stream
from tweepy.streaming import StreamListener
import socket
import json

# credenciales de nuestra app http://developer.twitter.com
consumer_key    = 'VmAdp9Pv0la6yKVtfBqMee8h2'
consumer_secret = 'C9PywUxzyc1elskA30S5jEfY5THbL1RWbfxfrHwymqfPKjBNSy'
access_token    = '1157394439326830592-0ne9R6FGqKM3fDwgT2BcZ2sxMMEkaK'
access_secret   = 'zbCQ1Q17FTcId00Y779jwsgoI8XaKabjkZyVlvxTw7Onx'

#creamos tweepy StreamListener la cual hereda de StreamListener
class TweetsListener(StreamListener):

    def __init__(self, csocket):
        self.client_socket = csocket
    
    #sobreescribimos el metodo on_data() de StreamListener
    def on_data(self, data):
        try:
            message = json.loads( data )
            print( message['text'].encode('utf-8') )
            self.client_socket.send( message['text'].encode('utf-8') )
            return True
        except BaseException as e:
            print("Error on_data: %s" % str(e))
        return True

    def if_error(self, status):
        print(status)
        return True



def send_tweets(c_socket):
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_secret)
    
    twitter_stream = Stream(auth, TweetsListener(c_socket))
    twitter_stream.filter(track=['Iran']) # este es el tema que nos interesa buscar



if __name__ == "__main__":
    #Comando para limpiar nuestro socket 5555
    #$ lsof -i :5555
    #Then kill it:
    #$ sudo kill -9 PID
    
    #inicializamos nuestro objecto socket
    new_skt = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    new_skt.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)   
        
    host = "127.0.0.1"     # direccion de nuestra maquina local
    port = 5555                 # puerto a utilizar para nuestro servicio
    new_skt.bind((host, port))        # referenciamos nuestro host y puerto

    print("Now listening on port: %s" % str(port))

    new_skt.listen(5)                 #  esperamos la coneccion con el cliente
    
    # Establecemos coneccion con el cliente, primero retorna el obejcto socket y despues la direccion relacionada a este socket
    c, addr = new_skt.accept()        

    print("Received request from: " + str(addr))
    # hecho esto podemos enviar los tweets atravez del socket
    send_tweets(c)