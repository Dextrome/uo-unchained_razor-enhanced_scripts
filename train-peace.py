from Scripts.utilities.items import FindItem
from Scripts.glossary.colors import colors
from System.Collections.Generic import List
from Scripts.glossary.enemies import GetEnemyNotorieties
from System import Byte, Int32

    
def Disco():
    mobFilter = Mobiles.Filter()
    mobFilter.RangeMin = 0
    mobFilter.RangeMax = 12
    mobFilter.IsHuman = 0
    mobFilter.IsGhost = 0
    mobFilter.Friend = 0
    mobFilter.Notorieties = GetEnemyNotorieties()
    enemies = Mobiles.ApplyFilter( mobFilter )
    Player.HeadMessage(colors[ 'cyan' ], "checking for targets")
    Misc.Pause(50)
    
    if len( enemies ) == 0:
        Player.HeadMessage(138, "No targets found")
    else:
        drums = Items.FindByID(0x0E9C,-1,Player.Backpack.Serial)
        if not drums:
            drums = Items.FindByID(0x0EB3,-1,Player.Backpack.Serial)

        if drums:
            Items.UseItem(drums)
            
            for enemy in enemies:
                Mobiles.Message(enemy,170,"> PEACE TARGET <",1000)
                Journal.Clear()
                Misc.Pause(100)
                Player.UseSkill("Peacemaking")
                Target.WaitForTarget(1000, False)
                Target.TargetExecute(enemy)
                Misc.Pause(200)
                if Journal.Search("You play poorly, and there is no effect."): 
                    Player.HeadMessage(colors[ 'cyan' ], "play poorly")
                    Misc.Pause(10250)
                elif Journal.Search("You play jarring music"): 
                    Player.HeadMessage(colors[ 'cyan' ], "play jarring music")
                    Misc.Pause(10250)
                elif Journal.Search("You attempt to calm your target, but fail."): 
                    Player.HeadMessage(colors[ 'cyan' ], "fail to disrupt")
                    Misc.Pause(5000)
                elif Journal.Search("Target cannot be seen."): 
                    Misc.Pause(1500)
                elif Journal.Search("That creature is already being calmed."): 
                    Misc.Pause(1500)
                elif Journal.Search("That is too far away."): 
                    Misc.Pause(1500)
                else:
                    Misc.Pause(10250)
                    
                    

    
while not Player.IsGhost and Player.GetSkillValue('Peacemaking') < 110:
#    PathFinding.PathFindTo(1459,1668,3)
#    PathFinding.PathFindTo(1468,1653,10)
#    PathFinding.PathFindTo(1482,1659,10)

#    #Misc.ScriptRun('heal_lowest-hp_pet.py')
    
#    Disco()
#    PathFinding.PathFindTo(439,1173,23)
#    Disco()
#    PathFinding.PathFindTo(433,1175,23)
#    Disco()
#    PathFinding.PathFindTo(421,1177,23)
#    Disco()
#    PathFinding.PathFindTo(421,1185,23)
#    PathFinding.PathFindTo(413,1190,23)
#    Disco()
#    PathFinding.PathFindTo(418,1196,23)
#    PathFinding.PathFindTo(431,1195,23)
#    Disco()
#    PathFinding.PathFindTo(443,1193,23)
#    Disco()
#    PathFinding.PathFindTo(445,1177,23)
    Player.UseSkill("Peacemaking")
    Target.WaitForTarget(1000, False)
    Target.Self()
    Misc.Pause(5250)
    