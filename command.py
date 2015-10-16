import json

class Map_list ():
    
    def __init__(self):
        self.command_list = {};

    def enter_command(self, key, value):
        new_command = {key: value};
        self.command_list.update(new_command);
        
    def get_command(self, key):
        command_value = self.command_list.get(key);
        print(command_value);
        
    def save_file(self):
       with open('commands.json', 'w') as f:
           json.dump(self.command_list, f);
    
    def load_file(self):
        with open('commands.json', 'r') as f:
            commands = json.load(f);
        return commands;
    
    def delete_command(self, key):
        self.command_list.pop(key , None);
        
    
