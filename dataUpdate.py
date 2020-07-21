import dataUpdateProcess

option = input('Please enter the operation you want to perform(update or remove) (u/r): ')

if option == 'u' :
    dataUpdateProcess.dataUpdatePlayers()
    
elif option == 'r' :
    dataUpdateProcess.dataUpdateRemoveRowsPlayers()
    
else :
    print('The operation you chose is not valid')