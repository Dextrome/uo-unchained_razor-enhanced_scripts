from Scripts.utilities.items import FindItem
from Scripts.glossary.colors import colors
from System.Collections.Generic import List
from Scripts.glossary.enemies import GetEnemyNotorieties
from System import Byte, Int32

def Tame():
    mobFilter = Mobiles.Filter()
    mobFilter.RangeMin = 0
    mobFilter.RangeMax = 16
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
        for enemy in enemies:
            PathFinding.PathFindTo(enemy.Position)
            Journal.Clear()
            Misc.Pause(100)
            Player.UseSkill("Animal Tarming")
            Target.WaitForTarget(1000, False)
            Target.TargetExecute(enemy)
            
            Misc.Pause(200)
            
            if Journal.Search("That is too far away."):
                PathFinding.PathFindTo(enemy.Position)
            
            Journal.Clear()
            Misc.Pause(100)
            Player.UseSkill("Animal Tarming")
            Target.WaitForTarget(1000, False)
            Target.TargetExecute(enemy)
            Misc.Pause(200)
            if Journal.Search("That is too far away."):
                break
            Misc.Pause(13000)
            Misc.WaitForContext(enemy.Serial, 10000)
            Misc.ContextReply(enemy.Serial, 7)
            Gumps.WaitForGump(2426193729, 10000)
            Gumps.SendAction(2426193729, 2)
            Misc.Pause(650)
            Player.ChatSay("Dextrome Kill")
            Target.WaitForTarget(1000, False)
            Target.TargetExecute(enemy)
            Misc.Pause(8000)
            Player.ChatSay("Dextrome Follow Me")
            
            
            
            
            
while not Player.IsGhost:
    Tame()    
    Misc.Pause(5000)
    PathFinding.PathFindTo(2006,2770,20)
    Tame()    
    Misc.Pause(5000)
    PathFinding.PathFindTo(1989,2733,25)
    Player.ChatSay("Dextrome Guard Me")
    Misc.Pause(15000)