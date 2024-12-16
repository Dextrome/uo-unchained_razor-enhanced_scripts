from Scripts.utilities.items import FindItem
from Scripts.glossary.colors import colors
from System.Collections.Generic import List
from Scripts.glossary.enemies import GetEnemyNotorieties
from System import Byte, Int32

    
filMobs = Mobiles.Filter()
filMobs.Enabled = True
filMobs.Friend = True
filMobs.IsHuman = False
filMobs.RangeMax = 15            
myPets = Mobiles.ApplyFilter(filMobs)
    
    
    
# PET HEALING #
###############
def TestBandagesApplying():
    # Fetch the Journal entries (oldest to newest)
    regularText = Journal.GetTextByType( 'System' )

    # Reverse the Journal entries so that we read from newest to oldest
    regularText.Reverse()

    # Read back until the bandages were started to see if they have finished applying
    for line in regularText[ 0 : len( regularText ) ]:
        if line == 'You begin applying the bandages.':
            break
        if ( line == 'You finish applying the bandages.' or
                line == 'You heal what little damage your patient had.' or
                line == 'You did not stay close enough to heal your patient!' or
                line == 'You apply the bandages, but they barely help.' or
                line == 'That being is not damaged!' or
                line == 'You fail to resurrect the creature.' or
                line == 'You are able to resurrect your patient.' or
                line == 'You have cured the target of all poisons!' or
                line == 'That is too far away.' ):
            return False
    return True

def WaitForBandagesToApply():
    bandageDone = False
    secondsCounter = 0.15
    while TestBandagesApplying():
        Misc.Pause( 1617 )
        secondsCounter += 1.617
        msgcolor = colors[ 'cyan' ]
        if secondsCounter > 4:
            msgcolor = colors[ 'yellow' ]
        elif secondsCounter > 3:
            msgcolor = colors[ 'green' ]
            
        if secondsCounter < 6:    
            Misc.SendMessage( '%i seconds since bandage started' % ( secondsCounter ), msgcolor )
    return

def HealPets():
    global myPets
    
    bandages = FindItem( 0x0E21, Player.Backpack )
    
    if bandages == None:
        Misc.SendMessage( 'Out of bandages!', colors[ 'red' ] )
        return
    #Misc.SendMessage( 'healing pets' )
    

    #for petSerial in petsToCheck:
    for pet in myPets:
        #pet = Mobiles.FindBySerial( petSerial )
        if pet == None:
            continue
        #Misc.SendMessage( 'Checking %s\'s health' % pet.Name )
        maxDistance = 3
        
        #if pet.Hits == 0:
        if pet.Hits == 0 or ( float( pet.Hits ) / float( pet.HitsMax ) * 100 ) < 88 or pet.Poisoned:
            if Player.DistanceTo( pet ) > maxDistance:
                if not Timer.Check( 'distanceTimer%s' % petSerial ):
                    Misc.SendMessage( 'Too far away from %s to apply bandages' % ( pet.Name ), colors[ 'red' ] )
                    Timer.Create( 'distanceTimer%s' % petSerial, 1000 )
                continue

            if Target.HasTarget(): 
                Target.Cancel()
                Target.ClearQueue()
            Items.UseItem( bandages )
            Target.WaitForTarget(1000)
            if Target.HasTarget():
                Target.TargetExecute( pet )
                Player.HeadMessage( colors[ 'cyan' ], 'Applying bandage on %s (currently %i%% health)' % ( pet.Name, ( float( pet.Hits ) / float( pet.HitsMax ) * 100 ) ) )
                Misc.Pause( 150 )
            WaitForBandagesToApply()
#        elif ( float( pet.Hits ) / float( pet.HitsMax ) * 100 ) < 88 or pet.Poisoned:
#            if Player.DistanceTo( pet ) > maxDistance:
#                if not Timer.Check( 'distanceTimer%s' % petSerial ):
#                    Misc.SendMessage( 'Too far away from %s to apply bandages' % ( pet.Name ), colors[ 'red' ] )
#                    Timer.Create( 'distanceTimer%s' % petSerial, 1000 )
#                continue
#
#            Items.UseItem( bandages )
#            Target.WaitForTarget( 10000, False )
#            Target.TargetExecute( pet )
#            Player.HeadMessage( colors[ 'cyan' ], 'Applying bandage on %s (currently %i%% health)' % ( pet.Name, ( float( pet.Hits ) / float( pet.HitsMax ) * 100 ) ) )
#            Misc.Pause( 150 )
#            WaitForBandagesToApply()
    

Misc.SendMessage( 'Starting Heal Pets Script', colors[ 'green' ])
            
while not Player.IsGhost:
    HealPets()
    Misc.Pause(150)
    