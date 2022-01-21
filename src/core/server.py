###15.01.2020###

from http import client, server
import json
import socket

class server():
    #pref's
    json_str = json.load(open('src/core/GenesisBlock.json'))
    s_ip = json_str['ip']
    i_port = json_str['port']
    i_maxListeners = json_str['maxlisteners']

    #Responce header
    HDRS = 'HTTP/1.1 200 OK\r\nContent-Type: text/html; charset=utf-8\r\n\r\n'.encode('utf-8')

    #thread
    def start():
        #starting messages

        #create server
        #Socket server
        serv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        serv.bind((server.s_ip, server.i_port))
        serv.listen(server.i_maxListeners)

        #waiting requests

        #sending requests

        #network talker
        print('Server working...')
        while True:
            client_socket, address = serv.accept()

            #Get request data
            data = client_socket.recv(1024).decode('utf-8')
            print(data)

            #Responce
            content = 'Request page'.encode('utf-8')
            client_socket.send(server.HDRS + content)
            print('Next')

        #network listener

    def send(content):
        print('send message')
        
