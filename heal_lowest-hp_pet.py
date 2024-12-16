from Scripts.utilities.items import FindItem
from Scripts.glossary.colors import colors
import System.Collections.Generic
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
def HealLowestHpPet():
    global petsToCheck
    
    bandages = FindItem( 0x0E21, Player.Backpack )
    
    if bandages == None:
        Misc.SendMessage( 'Out of bandages!', colors[ 'red' ] )
        return
    #Misc.SendMessage( 'healing pets' )
    
    lowesthppercentage = 100
    
    pettoheal = None

    #for petSerial in petsToCheck:
    for pet in myPets:
        #pet = Mobiles.FindBySerial( petSerial )
        if pet == None:
            continue
        
        if pet.Hits > 0:    
            hppercentage = ( float( pet.Hits ) / float( pet.HitsMax ) * 100 )
#            Player.HeadMessage( colors[ 'cyan' ], '%s (currently %i%% health)' % ( pet.Name, ( float( pet.Hits ) / float( pet.HitsMax ) * 100 ) ) )
            
            if hppercentage < lowesthppercentage:
                pettoheal = pet
                lowesthppercentage = hppercentage
    
    if pettoheal:
        if Target.HasTarget(): 
            Target.Cancel()
            Target.ClearQueue()
        Player.HeadMessage(colors[ 'green' ],pettoheal.Name)  
        Items.UseItem( bandages )
        Target.WaitForTarget(1000)
        if Target.HasTarget():
            Player.HeadMessage( colors[ 'cyan' ], '(currently %i%% health)' % ( ( float( pettoheal.Hits ) / float( pettoheal.HitsMax ) * 100 ) ) )
            Target.TargetExecute( pettoheal )
            Misc.Pause(150)
        else:
            Misc.SendMessage('No bandaid target')
        
#Misc.SendMessage( 'Start Healing Lowest HP Pet', colors[ 'green' ])
            
#while not Player.IsGhost:
#    HealPets()
#    Misc.Pause(150)
HealLowestHpPet()
    