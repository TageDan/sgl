import json


class Lib_Generator:

    def __init__(self, path):
        self.path = path
        self.functionbody = ""
        self.buffer = ""

    def set_section(self, section):
        self.section = section

    def write_to_buffer(self, stri):
        self.buffer += stri

    def buffer_to_body(self):
        self.functionbody += self.buffer
        self.buffer = ""
    
    def write_to_file(self):
        with open(self.path, "w+") as f:
            f.write(self.functionbody)

