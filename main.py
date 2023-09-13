import constants  
from network import Network
import logging
import generators
import json

#odczytanie pliku zawierającego seedy 
with open("seeds.json", 'r') as file_json:
    all_seeds = json.load(file_json)


# plik tworzący logi z działania programu
logfile = 'logfile.log'
logging.basicConfig(handlers=[logging.FileHandler(filename=logfile, encoding='utf-8', mode='a+')], level=logging.INFO)


def main():
    #pętla przechodząca przez zestawy seedów
    for set_seeds in all_seeds:
        gaussianGenerator1 = generators.GaussianGenerator(seed = set_seeds[0])
        gaussianGenerator2 = generators.GaussianGenerator(seed = set_seeds[1])
        exponentialGenerator = generators.ExponentialGenerator(seed = set_seeds[2], lambd=constants.LAMBD)
        uniformGenerator = generators.UniformGenerator(seed = set_seeds[3])

        # zmienne do przechowywania statystyk
        counterCreated = 0 
        counterDeleteFromPosition = 0
        counterDeleteFromDisconnection = 0
        counterChangeStation = 0

        clock = 0
        activeRaport = False
        raportUser = None
        network = Network(capacity=constants.N)
        usr = network.createUser(uniformGenerator.uniformGenerator(), clock, gaussianGenerator1.gaussianGenerator(), gaussianGenerator2.gaussianGenerator()) # tworzenie pierwszego użytkownika
        logging.debug('TIME: %s | Tworze usera o ID %s' % (clock, usr.id))
        timeCreateNextUser = exponentialGenerator.exponentialGenerator() # czas tworzenia nowego użytkownika
        timeRaportUser = min(network.usersList, key = lambda user: user.timeRaport).timeRaport # czas tworzenia raportu użytkownika
        
        while True:
            #ustawienie czasu systemu
            clock = timeCreateNextUser if timeCreateNextUser <= timeRaportUser else timeRaportUser

            #Zdarzenie czasowe - tworzenie nowego użytkownika
            if clock == timeCreateNextUser:
                usr = network.createUser(uniformGenerator.uniformGenerator(), clock, gaussianGenerator1.gaussianGenerator(), gaussianGenerator2.gaussianGenerator()) 
                timeCreateNextUser = clock + exponentialGenerator.exponentialGenerator()
                counterCreated += 1
                logging.debug('TIME: %s | Tworze usera o ID %s' % (clock, usr.id))

            #Zdarzenie czasowe - raport użytkownika
            if clock == timeRaportUser:
                raportUser = min(network.usersList, key = lambda user: user.timeRaport)
                raportUser.updatePosition()
                raportUser.updatePower(gaussianGenerator1.gaussianGenerator(), gaussianGenerator2.gaussianGenerator())
                activeRaport = True

            #Zdarzenie warunkowe - usunięcie użytkownika przez dystans
            if activeRaport and raportUser.checkDeleteUser():
                logging.debug('TIME: %s | Usuwam przez dystans usera o ID: %s' % (clock, raportUser.id))  
                network.deleteUser(raportUser)
                counterDeleteFromPosition += 1
                activeRaport = False

            #Zdarzenie warunkowe - rozłączenie użytkownika  
            if activeRaport and raportUser.checkDisconnectUser():
                logging.debug('TIME: %s | Rozłączenie usera o ID: %s' % (clock, raportUser.id))   
                network.deleteUser(raportUser)
                counterDeleteFromDisconnection += 1
                activeRaport = False

            #Zdarzenie warunkowe - przełączenie stacji
            if activeRaport and raportUser.checkSwitchStation():
                raportUser.handoverTime += 20
                if raportUser.handoverTime == constants.TTT:
                    raportUser.station = 'BS2' if raportUser.station == 'BS1' else 'BS1'   
                    logging.debug('Przełączam usera o ID: %s' % raportUser.id)                    
                    raportUser.handoverTime = 0
                    counterChangeStation += 1
            elif activeRaport and not raportUser.checkSwitchStation() and raportUser.handoverTime != 0:
                raportUser.handoverTime = 0

            if activeRaport:
                raportUser.updateRaportTime()
                timeRaportUser = min(network.usersList, key = lambda user: user.timeRaport).timeRaport
                activeRaport = False

            if (counterDeleteFromDisconnection + counterDeleteFromPosition == 500):
                logging.info('Liczba stworzonych użytkowników: %s' % counterCreated) 
                logging.info('Liczba przełączeń: %s' % counterChangeStation) 
                logging.info('Liczba usuniętych użytkowników przez dystans: %s' % counterDeleteFromPosition) 
                logging.info('Liczba usuniętych użytkowników przez rozłączenie: %s' % counterDeleteFromDisconnection) 
                logging.error('TIME: %s | KONIEC SYMULACJI') 
                print("KONIEC")
                break

main()
        




























        #if clock == timeCreateNextUser:
            
            
            



        

        # if clock == minTimeRaport.timeRaport:
        #     minTimeRaport.updatePosition()
        #     if minTimeRaport.position > constants.L - constants.X:
        #         print('usuwam usera')
        #         network.deleteUser(minTimeRaport)
        #         break
        #     else:
        #         minTimeRaport.updatePower()
        #         minTimeRaport.updateRaportTime()
        #         if minTimeRaport.station == 'BS1' and minTimeRaport.powerBS1 < minTimeRaport.powerBS2:
        #             minTimeRaport.handoverState = True
        #             minTimeRaport.handoverTime = clock
        #             minTimeRaport.activeRaport = True

        #         if minTimeRaport.id == 1:
        #             print (f'ID {minTimeRaport.id}, speed {minTimeRaport.speed}, station {minTimeRaport.station}, position {minTimeRaport.position}, powerBS1 {minTimeRaport.powerBS1}, powerBS2 {minTimeRaport.powerBS2}, handoverState {minTimeRaport.handoverState}, timeRaport {minTimeRaport.timeRaport}')
            
            #print ('robie raport')
            #if minTimeRaport.userRaport(clock) == False:
            #    print('usuwam usera')
            #    network.deleteUser(minTimeRaport)
            #    break
        # if clock == timeCreateNextUser:
        #     print ('tworze nowego usera')
        #     counterCreated += 1
        #     network.createUser(clock) 
        #     timeCreateNextUser = clock + int(constants.TAU)


        #print('Global Time:', clock)
        
        #cnt += 1
        #if counterCreated > 100:
        #    break
        #if cnt == 1000:
        #   break
    # while True:


    
    
