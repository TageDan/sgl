import json


class Generator:

    def __init__(self, path):
        self.path = path
        self.functionbody = ""
        self.configbody = ""
        self.mainbody = ""
        self.configvars = {"SCREEN_HEIGHT": 100, "SCREEN_WIDTH": 100, "SCREEN_BG": [0,0,0], "SCREEN_CLEAR_DELAY":0, "SCREEN_GRIDSIZE": 5}
        self.section = "none"
        self.buffer = ""
        self.footer = "</script>\n</body>\n</html>\n"

    def set_section(self, section):
        self.section = section

    def write_to_buffer(self, stri):
        self.buffer += stri

    def buffer_to_body(self):
        if self.section == "CONFIG":
            buf = self.buffer
            try:
                self.configvars[buf.split("=")[0]] = float(buf.split("=")[1])
            except:
                self.configvars[buf.split("=")[0]] = json.loads(buf.split("=")[1])
        elif self.section == "FUNCTIONS":
            self.functionbody += self.buffer
        elif self.section == "MAIN":
            self.mainbody += self.buffer
        self.buffer = ""

    def write_to_file(self):
        self.configbody = f"""
        <!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Document</title>
    <style>
        body {'{'}
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh; /* This ensures the content is centered vertically on the page */
            margin: 0; /* Removes default margin */
            background-color: #f5f5dc;
        {'}'}

        /* Add additional styles for your content here */
    </style>
</head>
<body >
    <canvas id = "CANVASIDHOPFULLYNOONEUSESTHISASVARIABLEORFUNCTIONNAME" width= "{int(self.configvars["SCREEN_GRIDSIZE"]*self.configvars["SCREEN_WIDTH"])}" height = "{int(self.configvars["SCREEN_HEIGHT"]*self.configvars["SCREEN_GRIDSIZE"])}"></canvas>

    <script>
    SCREEN_HEIGHT = {self.configvars["SCREEN_HEIGHT"]}
    SCREEN_GRIDSIZE = {self.configvars["SCREEN_GRIDSIZE"]}
    SCREEN_WIDTH = {self.configvars["SCREEN_WIDTH"]}
    SCREEN_BG = {self.configvars["SCREEN_BG"]}
    SCREEN_CLEAR_DELAY = {self.configvars["SCREEN_CLEAR_DELAY"]}

    CANVASIDHOPFULLYNOONEUSESTHISASVARIABLEORFUNCTIONNAME = document.getElementById('CANVASIDHOPFULLYNOONEUSESTHISASVARIABLEORFUNCTIONNAME').getContext('2d');

    const sleep = (delay) => new Promise((resolve) => setTimeout(resolve, delay))

    function draw(x, y, col){'{'}
        DRAWXVARHOPEFULLYNOONEUSESTHISNAME = Math.floor(x)
        DRAWYVARHOPEFULLYNOONEUSESTHISNAME = Math.floor(y)
        CANVASIDHOPFULLYNOONEUSESTHISASVARIABLEORFUNCTIONNAME.fillStyle = 'rgb('+col[0]+','+col[1]+','+col[2]+')'
        CANVASIDHOPFULLYNOONEUSESTHISASVARIABLEORFUNCTIONNAME.fillRect(DRAWXVARHOPEFULLYNOONEUSESTHISNAME*SCREEN_GRIDSIZE,DRAWYVARHOPEFULLYNOONEUSESTHISNAME*SCREEN_GRIDSIZE,SCREEN_GRIDSIZE,SCREEN_GRIDSIZE)
    {'}'}

    async function clear(){'{'}
        await sleep(SCREEN_CLEAR_DELAY*1000)
        CANVASIDHOPFULLYNOONEUSESTHISASVARIABLEORFUNCTIONNAME.fillStyle = 'rgb('+SCREEN_BG[0]+','+SCREEN_BG[1]+','+SCREEN_BG[2]+')'
        CANVASIDHOPFULLYNOONEUSESTHISASVARIABLEORFUNCTIONNAME.fillRect(0,0,SCREEN_WIDTH*SCREEN_GRIDSIZE,SCREEN_HEIGHT*SCREEN_GRIDSIZE)
    {'}'}
"""

        with open(self.path, "w+") as f:
            f.write(self.configbody + self.functionbody + "\n const THISISTHEMAINFUNCTION = async () => {\n await clear() \n"+self.mainbody+"} \n THISISTHEMAINFUNCTION()" + self.footer)

