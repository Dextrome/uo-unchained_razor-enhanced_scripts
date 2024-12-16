from System.Collections.Generic import List
from System import Byte

def UseDisco():
    Player.UseSkill("Discordance")
    Target.WaitForTarget(500, False)
    Target.PerformTargetFromList('closest mob')
    Timer.Create("DiscoTimer", 500)
    if Target.HasTarget():
        Target.Cancel()
        
def UsePeace():
    Player.UseSkill("Peacemaking")
    Target.WaitForTarget(500, False)
    Target.PerformTargetFromList('closest mob')
    Timer.Create("PeaceTimer", 5500)
    if Target.HasTarget():
        Target.Cancel()

def Kill(petname):
    if Target.HasTarget(): 
        Target.Cancel()
        Target.ClearQueue()
        
    if petname is None:
        crook =  Items.FindByID(0x0E81, -1, Player.Backpack.Serial,True,False) 
        
        filter = Mobiles.Filter()
        filter.Enabled = True
        filter.Friend = False
        filter.Notorieties = List[Byte](bytes([3,4,5,6])) #1:cyan 2:green 3:gray 4:criminal 5:orange 6:red 7:yellow
        filter.CheckLineOfSight = True
        filter.RangeMax = 8
        Mobs = Mobiles.ApplyFilter(filter)
        
        #if len(Mobs) > 0 and Player.GetSkillValue('Herding') >= 70 and crook and not Timer.Check("HerdingTimer"):
            #Items.UseItem(crook)
            #Timer.Create("HerdingTimer", 8000)
        #else:
        Player.ChatSay("all kill")
    else:
        #Misc.UseContextMenu(pet.Serial,"Command: Kill",1000)
        Player.ChatSay("%s kill" % (petname))

    if Target.WaitForTarget(500):
        Target.PerformTargetFromList("closest mob")
                            
    if Misc.ScriptStatus('fishing.py') == False:
        if Player.GetSkillValue('Discordance') >= 65 and not Timer.Check("DiscoTimer"):
            Misc.Pause(100)
            if Target.HasTarget():
                Target.Cancel()
                Target.ClearQueue()
                
            instrument =  Items.FindByID(0x0E9D, -1, -1) #tambourine

            if instrument:
                UseDisco()
            else:
                instrument =  Items.FindByID(0x0E9E, -1, -1) #tambourine(tassel)

                if instrument:
                    UseDisco()
                else:
                    instrument =  Items.FindByID(0x0E9C, -1, -1) #drum

                    if instrument:
                        UseDisco()
        elif Player.GetSkillValue('Peacemaking') >= 65 and not Timer.Check("PeaceTimer"):
            Misc.Pause(100)
            if Target.HasTarget():
                Target.Cancel()
                Target.ClearQueue()
                
            instrument =  Items.FindByID(0x0E9D, -1, -1) #tambourine

            if instrument:
                UsePeace()
            else:
                instrument =  Items.FindByID(0x0E9E, -1, -1) #tambourine(tassel)

                if instrument:
                    UsePeace()
                else:
                    instrument =  Items.FindByID(0x0E9C, -1, -1) #drum

                    if instrument:
                        UsePeace()
Kill(None)
Misc.Pause(100)
if Target.HasTarget():
    Target.Cancel()
Target.ClearQueue()