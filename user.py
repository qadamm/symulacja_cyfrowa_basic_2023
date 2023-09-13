from constants import X, L, ALFA, DELTA 
import math

class User:
    _counter = 0
    def __init__(self, speed, clock, generator1, generator2):
        User._counter += 1
        self.id = User._counter
        self.speed = speed
        self.station = "BS1"
        self.position = X
        self.powerBS1 = generator1
        self.powerBS2 = generator2
        self.handoverTime = 0
        self.timeRaport = clock + 20
        
    def __str__(self):
        return f'User ID: {self.id} z pozycja: {self.position}'

    def updatePower(self, generator1, generator2):
        self.powerBS1 = 4.56 - 22 * math.log10(self.position) + generator1
        self.powerBS2 = 4.56 - 22 * math.log10(L - self.position) + generator2

    def updatePosition(self): 
        self.position += self.speed * 0.02
    
    def updateRaportTime(self):
        self.timeRaport = self.timeRaport + 20

    def checkSwitchStation(self):
        return (self.powerBS2 - self.powerBS1 if self.station == 'BS1' else self.powerBS1 - self.powerBS2) >= ALFA
    
    def checkDeleteUser(self):
        return (self.position > L - X)   

    def checkDisconnectUser(self):
        return (self.powerBS1 - self.powerBS2 if self.station == 'BS1' else self.powerBS2 - self.powerBS1) <= -DELTA      

    
        
        