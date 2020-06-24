import socket
from _thread import *
from player import Player
from game import Game
import pickle
import sys

# server info
server = "192.168.1.10"
port = 5555

# socket info
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# bind server and port to the socket
try:
    s.bind((server, port))
except socket.error as e:
    str(e)

# opens up to the port to allow clients to connect
# leaving empty allows for any number of connections
s.listen()
print("Waiting for a connection, Server Started")

# Variables
connected = set()
games = {}
idCount = 0

# define a threaded function


def threaded_client(connection, p, gameId):
    global idCount
    connection.send(str.encode(str(p)))

    reply = ""
    while True:
        try:
            data = connection.recv(4096*2).decode()

            if gameId in games:
                game = games[gameId]

                if not data:
                    break
                else:
                    if data == "reset":
                        game.resetWent()
                    elif data != "get":
                        game.play(p, data)

                    reply = game
                    connection.sendall(pickle.dumps(reply))
            else:
                break
        except:
            break

    print("Lost connection")

    try:
        del games[gameId]
        print("Closing Game: ", gameId)
    except:
        pass
    idCount -= 1
    connection.close()


while True:
    connection, addr = s.accept()
    print("connected to: ", addr)

    idCount += 1
    p = 0
    gameId = (idCount - 1)//2
    if idCount % 2 == 1:
        games[gameId] = Game(gameId)
        print("Creating a new game...")
    else:
        games[gameId].ready = True
        p = 1

    start_new_thread(threaded_client, (connection, p , gameId))

