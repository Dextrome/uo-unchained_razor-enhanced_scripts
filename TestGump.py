from datetime import datetime
Timer.Create('healPet', 10000)
from System.Collections.Generic import List
#


def updateClockGump():
    now_msg = "{}".format( datetime.now())
    timeRemaining = Timer.Remaining('healPet')/1000
    test = "{:.0f}".format(timeRemaining)
    gumpLen = int(test)
    
    gd = Gumps.CreateGump('movable')
    Gumps.AddPage(gd, 0);
    Gumps.AddBackground(gd, 0, 0, gumpLen*10, 35, 30512)
    #Gumps.AddBackground(gd, 0, 0, gumpLen*10, 35, 0)
    
    
    
    Gumps.AddLabel(gd, 10, 10, 1166, 'HealPet ' + test)
    
    
    
    #Gumps.AddButton(gd, 10, 30, 247, 248, 1, 1, 0)
    #Gumps.AddButton(gd, 10, 50, 247, 248, 2, 1, 0)
    #Gumps.AddButton(gd, 10, 70, 246, 247, 3, 2, 0)
    
    
    Gumps.SendGump(123456, Player.Serial, 120, 120, gd.gumpDefinition, gd.gumpStrings)
    
    
    

def main():
    
    while True: # if program running. Replaces having to loop it and keeps from returning to top if variables that change are set.
        updateClockGump()#go to start sendgump method.
        Misc.Pause(100) #pause for 750ms
        gd = Gumps.GetGumpData(123456)
        
        if (gd.buttonid != -1):
            Misc.SendMessage("DONE button ID: {}".format(gd.buttonid ))
        else:
            Gumps.SendAction(123456,0)
main()