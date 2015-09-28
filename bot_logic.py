import socket
import sys
import threading

class Socket (threading.Thread):

    def __init__(self, HOST, PORT):
        threading.Thread.__init__(self)
        self.HOST = HOST
        self.PORT = PORT
        self.NICK = "TargeBot"
        self.IDENT = "targebot"
        self.REALNM = "TargeBot"
        self.read_buffer = ""
        self.channel = "#tl.dota"

        self.my_socket = socket.socket()

    def connect(self):
        self.my_socket.connect((self.HOST, self.PORT))
        self.my_socket.send(bytes("NICK %s\r\n" % self.NICK, "UTF-8"))
        self.my_socket.send(bytes("USER %s %s place_text :%s\r\n" % (self.IDENT, self.HOST, self.REALNM), "UTF-8"))

    def run(self):
        while 1:
            self.read_buffer = self.read_buffer + self.my_socket.recv(1024).decode("UTF-8")
            temp_string = str.split(self.read_buffer, "\n")
            self.read_buffer = temp_string.pop()
            print(temp_string)

            for ln in temp_string:
                ln = str.rstrip(ln)
                ln = str.split(ln)
                if(ln[0] == "PING"):
                    self.my_socket.send(bytes("PONG %s\r\n" % ln[1], "UTF-8"))
    
    def set_host(self, new_host):
        self.HOST = new_host

    def set_port(self, new_port):
        self.PORT = new_port

    def set_nick(self, new_nick):
        self.NICK = new_nick

    def set_ident(self, new_ident):
        self.IDENT = new_ident

    def set_name(self, new_name):
        self.REALNM = new_name

    def get_host(self):
        return self.HOST

    def get_port(self):
        return self.PORT

    def get_nick(self):
        return self.NICK

    def get_ident(self):
        return self.IDENT

    def get_name(self):
        return self.REALNM
    
    def send_message(self, message):
        self.my_socket.send(bytes("PRIVMSG %s :%s \r\n" % (self.channel, message), "UTF-8"))
        
    def join_channel(self):
        self.my_socket.send(bytes("JOIN %s\r\n" % self.channel, "UTF-8"))
        
class User_reader(threading.Thread):
    
    def __init__(self, irc_socket):
        self.irc_socket = irc_socket
        threading.Thread.__init__(self)
    
    def run(self):
        while 1:
            message = input()
            if message == "START":
                self.irc_socket.join_channel()
            self.irc_socket.send_message(message)

socket = Socket("irc.quakenet.org", 6667)
socket.connect()
socket.start()

user_reader = User_reader(socket)
user_reader.start()