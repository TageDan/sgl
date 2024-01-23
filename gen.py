


class Generator:

    def __init__(self, path):
        self.path = path
        self.functionbody = ""
        self.configbody = ""
        self.mainbody = ""
        self.configvars = {"SCREEN_HEIGHT": "100", "SCREEN_WIDTH": "100", "SCREEN_BG": "[0,0,0]", "SCREEN_CLEAR_DELAY":"0"}
        self.section = "none"
        self.buffer = ""

    def set_section(self, section):
        self.section = section

    def write_to_buffer(self, stri):
        if self.section == "CONFIG":
            pass
        else:
            self.buffer += stri

    def buffer_to_body(self):
        if self.section == "CONFIG":
            pass
        elif self.section == "FUNCTIONS":
            self.functionbody += self.buffer
        elif self.section == "MAIN":
            self.mainbody += self.buffer
        buffer = ""

    def write_to_file(self):
        with open(self.path, "w+") as f:
            f.write(self.configbody + self.functionbody + self.mainbody + self.footer)

