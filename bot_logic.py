import socket
import sys
import threading
import re

class Socket (threading.Thread):

    def __init__(self, host, port):
        threading.Thread.__init__(self)
        self.host = host
        self.port = port
        self.nick = "TargeBot"
        self.IDENT = "targebot"
        self.REALNM = "TargeBot"
        self.read_buffer = ""
        self.channel = "#testtarge"

        self.my_socket = socket.socket()

    def connect(self):
        self.my_socket.connect((self.host, self.port))
        self.my_socket.send(bytes("nick %s\r\n" % self.nick, "UTF-8"))
        self.my_socket.send(bytes("USER %s %s place_text :%s\r\n" % (self.IDENT, self.host, self.REALNM), "UTF-8"))

    def run(self):
        while 1:
            self.read_buffer = self.read_buffer + self.my_socket.recv(1024).decode("UTF-8")
            temp_string = str.split(self.read_buffer, "\n")
            temp_string = re.split('\r|\n', self.read_buffer)
            #self.read_buffer = temp_string.pop()
			
            #print(temp_string)

            while len(temp_string)>0:
                server_message = temp_string.pop(0)
                print(server_message)
                if "PING :" in server_message:
                    #pong_int = string.replace(server_message, "PING :", "")
                    pong_int = server_message.replace("PING :", "")
                    self.pong_send(int(pong_int))
    
    def set_host(self, new_host):
        self.host = new_host

    def set_port(self, new_port):
        self.port = new_port

    def set_nick(self, new_nick):
        self.nick = new_nick

    def set_ident(self, new_ident):
        self.IDENT = new_ident

    def set_name(self, new_name):
        self.REALNM = new_name

    def get_host(self):
        return self.host

    def get_port(self):
        return self.port

    def get_nick(self):
        return self.nick

    def get_ident(self):
        return self.IDENT

    def get_name(self):
        return self.REALNM
    
    def send_message(self, message):
        self.my_socket.send(bytes("PRIVMSG %s :%s \r\n" % (self.channel, message), "UTF-8"))
        
    def join_channel(self):
        self.my_socket.send(bytes("JOIN %s\r\n" % self.channel, "UTF-8"))
		
    def pong_send(self, pong_int):
        self.my_socket.send(bytes("PONG %s\r\n" % pong_int, "UTF-8"))
        
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
