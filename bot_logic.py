import command
import re
import socket
import sys
import threading

class Socket (threading.Thread):

    def __init__(self, host, port): #initialises Socket object
        threading.Thread.__init__(self)
        self.host = host
        self.port = port
        self.nick = "TargeBot"
        self.IDENT = "targebot"
        self.REALNM = "TargeBot"
        self.read_buffer = ""
        self.channel = "#testtarge"

        self.my_socket = socket.socket()

    def connect(self): #connects to irc server
        self.my_socket.connect((self.host, self.port))
        self.my_socket.send(bytes("nick %s\r\n" % self.nick, "UTF-8"))
        self.my_socket.send(bytes("USER %s %s place_text :%s\r\n" % (self.IDENT, self.host, self.REALNM), "UTF-8"))

    def run(self): #endless loop that prints incoming messages, replies to PING : and parses messages
        while 1:
            self.read_buffer = self.read_buffer + self.my_socket.recv(1024).decode("UTF-8")
            #temp_string = str.split(self.read_buffer, "\n")
            temp_string = re.split('\r|\n', self.read_buffer)
            self.read_buffer = temp_string.pop()
            while len(temp_string) > 0:
                server_message = temp_string.pop(0)
                if server_message is not "":
                    print(server_message)
                    if "PING :" in server_message:
                        pong_int = server_message.replace("PING :", "")
                        self.pong_send(int(pong_int))
                    elif "PRIVMSG" in server_message:
                        print("PARSING: "+server_message)
                        self.message_parse(server_message)

    def message_parse(self, message): #takes message (string) from server, calls subsequent parsing functions
        sub_message = self.meta_parse(message) #either calls functions to add new command or replies to channel
        command = ""                           #with command "message"

        command_value = ""
        flag = 2

        if self.set_parse(sub_message) == 0:    #SET
            flag = 0
            command = self.command_parse(sub_message, 0)
            command_value = self.command_parse(sub_message, 3)
            map_list.add_command(command, self.value_parse(sub_message))

        elif "PRIVMSG" in message: #REQUEST
            flag = 1
            command = self.command_parse(sub_message, 1)
            command_value = map_list.get_command(command)
            if command_value is None:
                return
            channel = self.channel_parse(message)
            self.send_to_channel(channel, command_value)

    def command_parse(self, message, flag): #takes message (string) and flag (int), flag determines what it is parsing for 
        command_pattern = " "               #flag 0 -> !set "!command", flag 1 -> "!command", flag 3 -> !set !command "message"
        command_object = re.split(command_pattern, message) #returns (string) according to above key
        if flag == 0:
            return command_object[1]
        elif flag == 1:
            return command_object[0]
        elif flag == 3:
            return command_object[2]

    def set_parse(self, message): #takes message (string), returns (int) 0 if "!set !command", otherwise returns (int) 1
        set_pattern = "(!\w*) (!\w*)"
        command_value = re.sub(set_pattern, '', message)
        set_object = re.match(set_pattern, message)
        if set_object is not None:
            return 0
        else:
            return 1

    def value_parse(self, message): #takes message (string), returns (string) command_value 
        set_pattern = "(!\w*) (!\w*)" #command_value is !set !command "command_value"
        command_value = re.sub(set_pattern, '', message)
        command_value = command_value[1:]
        return command_value

    def meta_parse(self, message): #takes message (string), returns (string) meta_string 
        meta_pattern = "(:.*:)"    #meta_string is server message stripped to just message sent
        meta_string = re.sub(meta_pattern, '', message)
        return meta_string

    def channel_parse(self, message): #takes message (string), returns channel[1] (string)
        channel_pattern = "(PRIVMSG #\w*)" #returned value is channel name
        channel = re.search(channel_pattern, message)
        if channel is None:
            return
        channel = re.split(" ", channel.group(0))
        return channel[1]

    def user_parse(self, message):
        user_pattern = "(:\w*!~)"

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

    def send_to_channel(self, channel, message):
        self.my_socket.send(bytes("PRIVMSG %s :%s \r\n" % (channel, message), "UTF-8"))

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

map_list = command.Map_list()

socket = Socket("irc.quakenet.org", 6667)
socket.connect()
socket.start()

user_reader = User_reader(socket)
user_reader.start()

socket.channel_parse(":Targe!~Targe@cpc1-bath5-2-0-cust421.aztw.cable.virginm.net PRIVMSG #testtarge :!set !new_command_test testtesttest")
