class Colour:
    def __init__(self):
        self.black = (0,0,0)
        self.white = (255,255,255)
        self.red = (255,0,0)
        self.green = (0,255,0)
        self.blue = (0,0,255)
        self.yellow = (255,255,0)
        self.aqua = (0,255,255)
        self.purple = (127.5,0,255)
        self.pink = (255,0,255)
        
    def randomiser(self):
        import random
        colourList = [self.red,self.green,self.blue,self.yellow,self.aqua,self.purple,self.pink]
        return colourList[random.randint(0,len(colourList))]

