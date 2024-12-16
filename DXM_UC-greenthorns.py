from System.Collections.Generic import List
from System import Byte, Int32
from Scripts.glossary.enemies import GetEnemyNotorieties
from Scripts.glossary.colors import colors
from Scripts.utilities.items import FindItem


pet1Serial = 0x000199DE # 3slot
pet2Serial = 0x00023275 # 2slot
petsToCheck = List[Int32]([
        pet1Serial, 
        pet2Serial, 
    ])

def WaitForBandagesToApply():
    while TestBandagesApplying():
        Misc.Pause( 1000 )
        pet1 = Mobiles.FindBySerial( pet1Serial )
        if Player.DistanceTo( pet1 ) > 1:
            FollowMobile( pet1, 1, True )
        Survive()
    return


def HealPets():
    global petsToCheck
    Misc.Pause( 420 )
    bandages = FindItem( 0x0E21, Player.Backpack )
    
    if bandages == None:
        Misc.SendMessage( 'Out of bandages!', colors[ 'red' ] )
        return
    

    for petSerial in petsToCheck:
        pet = Mobiles.FindBySerial( petSerial )
        if pet == None:
            continue
        maxDistance = 2
        
        if ( float( pet.Hits ) / float( pet.HitsMax ) * 100 ) < 88 or pet.Poisoned:
            if Player.DistanceTo( pet ) > maxDistance:
                if not Timer.Check( 'distanceTimer%s' % petSerial ):
                    Misc.SendMessage( 'Too far away from %s to apply bandages' % ( pet.Name ), colors[ 'red' ] )
                    Timer.Create( 'distanceTimer%s' % petSerial, 1000 )
                continue
                
            Items.UseItem( bandages )
            Target.WaitForTarget( 10000, False )
            Target.TargetExecute( pet )
            Player.HeadMessage( colors[ 'cyan' ], 'Applying bandage on %s (currently %i%% health)' % ( pet.Name, ( float( pet.Hits ) / float( pet.HitsMax ) * 100 ) ) )
            Misc.Pause( 150 )
            WaitForBandagesToApply()


while (True):
    mobFilter = Mobiles.Filter()
    mobFilter.RangeMin = 0
    mobFilter.RangeMax = 14
    mobFilter.IsHuman = 0
    mobFilter.IsGhost = 0
    mobFilter.Friend = 0
    mobFilter.Notorieties = GetEnemyNotorieties()
    enemies = Mobiles.ApplyFilter( mobFilter )
    Player.HeadMessage(colors[ 'cyan' ], "checking for enemies")
    Misc.Pause(50)
    
    if len( enemies ) == 0:
        Player.HeadMessage(138, "No enemies found")
        #Look For Corpses
        filCorpse = Items.Filter()
        filCorpse.Enabled = True
        filCorpse.Movable = False
        filCorpse.OnGround = True
        filCorpse.RangeMin = 0
        filCorpse.RangeMax = 2
        filCorpse.Graphics = List[Int32]([0x2006]) 
        filCorpse.IsCorpse = True
        filCorpse.CheckIgnoreObject = False
        lisCorpses = Items.ApplyFilter(filCorpse)

        if len(lisCorpses) >= 1: #loot
            for corpse in lisCorpses:
                Items.UseItem(corpse)
                Misc.Pause(650)
                
                for i in corpse.Contains: 
                    if i.ItemID == "0x0E43": #paragon chest
                        Items.DropItemGroundSelf(i.Serial, 1)
                        
        #else: #plant thorn
        Player.HeadMessage(138, "planting thorn")
        thorns = Items.FindByID(0x0F42,0x0042,Player.Backpack.Serial,False)
        if thorns:
            Items.UseItem(thorns)
            PathFinding.PathFindTo(2065,907, 0)
            Target.WaitForTarget(1500,False)
            Target.TargetExecute(2065, 908 ,0)
        #else: #get thorns from bank
        HealPets()
        Misc.Pause(10000)
    else:
        Misc.Pause(10000)
        
        
        
       
Items.DropItemGroundSelf(0x40819716, 1)