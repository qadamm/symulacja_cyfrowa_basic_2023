import queue
from user import User

class Network:
    def __init__(self, capacity):
        self.usersList = []
        self.waitQueue = queue.Queue()
        self.capacity = capacity
           
    # funkcja dodająca użytkownika
    def createUser(self, speed, clock, generator1, generator2):
        user = User(speed, clock, generator1, generator2)   
        if len(self.usersList) < self.capacity: #dodanie do odpowiedniej struktury danych 
            self.usersList.append(user)
            return user
        else:
            self.waitQueue.put(user)
            return user
        
    #funkcja usuwająca użytkownika z systemu       
    def deleteUser(self, User):
        self.usersList.remove(User)
        if (self.waitQueue.qsize() > 0 and len(self.usersList) < self.capacity): # sprawdzenie czy nie ma użytkownika w drugiej kolejce
            self.usersList.append(self.waitQueue.get())
             


    
    
        
        
    
