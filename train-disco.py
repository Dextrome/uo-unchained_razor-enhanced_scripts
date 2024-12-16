from Scripts.utilities.items import FindItem
from Scripts.glossary.colors import colors
from System.Collections.Generic import List
from System import Byte, Int32

class Notoriety:
    byte = Byte( 0 )
    color = ''
    description = ''

    def __init__ ( self, byte, color, description ):
        self.byte = byte
        self.color = color
        self.description = description

notorieties = {
    'innocent': Notoriety( Byte( 1 ), 'blue', 'innocent' ),
    'ally': Notoriety( Byte( 2 ), 'green', 'guilded/ally' ),
    'attackable': Notoriety( Byte( 3 ), 'gray', 'attackable but not criminal' ),
    'criminal': Notoriety( Byte( 4 ), 'gray', 'criminal' ),
    'enemy': Notoriety( Byte( 5 ), 'orange', 'enemy' ),
    'murderer': Notoriety( Byte( 6 ), 'red', 'murderer' ),
    'npc': Notoriety( Byte( 7 ), '', 'npc' )
}

def GetNotorietyList ( notorieties ):
    '''
    Returns a byte list of the selected notorieties
    '''
    notorietyList = []
    for notoriety in notorieties:
        notorietyList.append( notoriety.byte )

    return List[Byte]( notorietyList )

def GetEnemyNotorieties( minRange = 0, maxRange = 12 ):
    '''
    Returns a list of the common enemy notorieties
    '''
    global notorieties

    return GetNotorietyList( [
        notorieties[ 'attackable' ],
        notorieties[ 'criminal' ],
        notorieties[ 'enemy' ],
        notorieties[ 'murderer' ]
    ] )


def GetEnemies( Mobiles, minRange = 0, maxRange = 12, notorieties = GetEnemyNotorieties(), IgnorePartyMembers = False ):
    '''
    Returns a list of the nearby enemies with the specified notorieties
    '''

    if Mobiles == None:
        raise ValueError( 'Mobiles was not passed to GetEnemies' )

    enemyFilter = Mobiles.Filter()
    enemyFilter.Enabled = True
    enemyFilter.RangeMin = minRange
    enemyFilter.RangeMax = maxRange
    enemyFilter.Notorieties = notorieties
    enemyFilter.CheckIgnoreObject = True
    enemyFilter.Friend = False
    enemies = Mobiles.ApplyFilter( enemyFilter )

    if IgnorePartyMembers:
        partyMembers = [ enemy for enemy in enemies if enemy.InParty ]
        for partyMember in partyMembers:
            enemies.Remove( partyMember )

    return enemies

    
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
        Player.HeadMessage(138, "Targets found")
        drums = Items.FindByID(0x0E9C,-1,Player.Backpack.Serial)
        if not drums:
            drums = Items.FindByID(0x0EB3,-1,Player.Backpack.Serial)
            if not drums:
                drums = Items.FindByID(0x0E9D,-1,Player.Backpack.Serial)

        if drums:
            Items.UseItem(drums)
            
            for enemy in enemies:
                Mobiles.Message(enemy,170,"> DISCO TARGET <",1000)
                Journal.Clear()
                Misc.Pause(100)
                Player.UseSkill("Discordance")
                Target.WaitForTarget(1000, False)
                Target.TargetExecute(enemy)
                Misc.Pause(200)
                if Journal.Search("You play poorly, and there is no effect."): 
                    Player.HeadMessage(colors[ 'cyan' ], "play poorly")
                    Misc.Pause(10250)
                elif Journal.Search("You play jarring music"): 
                    Player.HeadMessage(colors[ 'cyan' ], "play jarring music")
                    Misc.Pause(10250)
                elif Journal.Search("You attempt to disrupt your target, but fail."): 
                    Player.HeadMessage(colors[ 'cyan' ], "fail to disrupt")
                    Misc.Pause(5000)
                elif Journal.Search("Target cannot be seen."): 
                    Misc.Pause(1500)
                elif Journal.Search("That creature is already in discord."): 
                    Misc.Pause(1500)
                elif Journal.Search("That is too far away."): 
                    Misc.Pause(1500)
                else:
                    Misc.Pause(10250)   
            else:
                Player.HeadMessage(colors[ 'cyan' ], "no instrument found")
                    
                    

    
while not Player.IsGhost and Player.GetSkillValue('Discordance') < 121:
#    PathFinding.PathFindTo(1459,1668,3)
#    PathFinding.PathFindTo(1468,1653,10)
#    PathFinding.PathFindTo(1482,1659,10)

#    #Misc.ScriptRun('heal_lowest-hp_pet.py')
    
    Disco()
    Misc.Pause(2000)
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