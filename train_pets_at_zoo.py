from Scripts.utilities.items import FindItem
from Scripts.glossary.colors import colors
from System.Collections.Generic import List
from Scripts.glossary.enemies import GetEnemyNotorieties
from System import Byte, Int32

pet1Serial = 0x0000745B

petsToCheck = List[Int32]([
        0x0000745B, 
        0x00007A2D, 
    ])

#loot Item IDs
corpse_ID = 0x2006
gold_ID = 0x0EED
biggem1 = 0x3193
biggem2 = 0x3194
biggem3 = 0x3195
biggem4 = 0x3196
biggem5 = 0x3197
biggem6 = 0x3198
biggem7 = 0x3199
arcanedust = 0x5745
arcanescroll = 0x0EF3
scrolloftrans = 0x0E34
tmap = 0x14EC
artifact1 = 0x1576
plant = 0x63DF
deed = 0x14F0

loot_list  = [gold_ID,biggem1,biggem2,biggem3,biggem4,biggem5,biggem6,biggem7,arcanedust,arcanescroll,scrolloftrans,tmap,artifact1,plant,deed]

    
# TRAVEL #
##########

def PlayersNearby():
    mobFilter = Mobiles.Filter()
    mobFilter.RangeMin = 0
    mobFilter.RangeMax = 21
    mobFilter.IsHuman = 1
    mobFilter.IsGhost = 0
    
    pets = Mobiles.ApplyFilter( mobFilter )
    
    if len( pets ) == 0:
        return False
    else:
        return True
        
def PlayerWalk( direction ):
    '''
    Moves the player in the specified direction
    '''

    playerPosition = Player.Position
    if Player.Direction == direction:
        Player.Walk( direction )
    else:
        Player.Walk( direction )
        Player.Walk( direction )
    return

def FollowMobile( mobile, maxDistanceToMobile = 2, startPlayerStuckTimer = False ):
    '''
    Uses the X and Y coordinates of the animal and player to follow the animal around the map
    Returns True if player is not stuck, False if player is stuck
    '''

    mobilePosition = mobile.Position
    playerPosition = Player.Position
    directionToWalk = ''
    if mobilePosition.X > playerPosition.X and mobilePosition.Y > playerPosition.Y:
        directionToWalk = 'Down'
    if mobilePosition.X < playerPosition.X and mobilePosition.Y > playerPosition.Y:
        directionToWalk = 'Left'
    if mobilePosition.X > playerPosition.X and mobilePosition.Y < playerPosition.Y:
        directionToWalk = 'Right'
    if mobilePosition.X < playerPosition.X and mobilePosition.Y < playerPosition.Y:
        directionToWalk = 'Up'
    if mobilePosition.X > playerPosition.X and mobilePosition.Y == playerPosition.Y:
        directionToWalk = 'East'
    if mobilePosition.X < playerPosition.X and mobilePosition.Y == playerPosition.Y:
        directionToWalk = 'West'
    if mobilePosition.X == playerPosition.X and mobilePosition.Y > playerPosition.Y:
        directionToWalk = 'South'
    if mobilePosition.X == playerPosition.X and mobilePosition.Y < playerPosition.Y:
        directionToWalk = 'North'

    if startPlayerStuckTimer:
        Timer.Create( 'playerStuckTimer', 1000 )

    playerPosition = Player.Position
    PlayerWalk( directionToWalk )

    newPlayerPosition = Player.Position
    if playerPosition == newPlayerPosition and not Timer.Check( 'playerStuckTimer' ):
        # Player has been stuck in the same position for a while, try to find them a way out of the stuck position
        if Player.Direction == 'Up':
            for i in range ( 5 ):
                Player.Walk( 'Down' )
        elif Player.Direction == 'Down':
            for i in range( 5 ):
                Player.Walk( 'Up' )
        elif Player.Direction == 'Right':
            for i in range( 5 ):
                Player.Walk( 'Left' )
        elif Player.Direction == 'Left':
            for i in range( 5 ):
                Player.Walk( 'Right' )
        Timer.Create( 'playerStuckTimer', 1000 )
    elif playerPosition != newPlayerPosition:
        Timer.Create( 'playerStuckTimer', 1000 )

    if Player.DistanceTo( mobile ) > maxDistanceToMobile:
        # This pause may need further tuning
        # Don't want to create a ton of infinite calls if the player is stuck, but also don't want to not be able to catch up to animals
        Misc.Pause( 100 )
        FollowMobile( mobile, maxDistanceToMobile )

    return True
        
    
    
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
    crps_list = findCorpses()

    for current_corpse in crps_list:
        if not tooMuchWeight():
            Items.Message(current_corpse,170,"loot this")
            Items.UseItem(current_corpse)
            Misc.Pause(750)
            lootCorpse(current_corpse)
            
    while TestBandagesApplying():
        Misc.Pause( 750 )
        #pet1 = Mobiles.FindBySerial( pet1Serial )
        #if Player.DistanceTo( pet1 ) > 1:
            #FollowMobile( pet1, 1, True )
    return


def HealPets():
    global petsToCheck
    
    bandages = FindItem( 0x0E21, Player.Backpack )
    
    if bandages == None:
        Misc.SendMessage( 'Out of bandages!', colors[ 'red' ] )
        return
    #Misc.SendMessage( 'healing pets' )
    

    for petSerial in petsToCheck:
        pet = Mobiles.FindBySerial( petSerial )
        if pet == None:
            continue
        #Misc.SendMessage( 'Checking %s\'s health' % pet.Name )
        maxDistance = 2
        
        if pet.Hits < pet.HitsMax - 5 or pet.Poisoned:
            if Player.DistanceTo( pet ) > maxDistance:
                if not Timer.Check( 'distanceTimer%s' % petSerial ):
                    Misc.SendMessage( 'Too far away from %s to apply bandages' % ( pet.Name ), colors[ 'red' ] )
                    Timer.Create( 'distanceTimer%s' % petSerial, 1000 )
                continue

            Items.UseItem( bandages )
            Target.WaitForTarget( 10000, False )
            Target.TargetExecute( pet )
            Player.HeadMessage( colors[ 'cyan' ], 'Applying bandage on %s (currently %i%% health)' % ( pet.Name, ( float( pet.Hits ) / float( pet.HitsMax ) * 100 ) ) )
            
            Misc.Pause( 200 )
            WaitForBandagesToApply()
            
            
# LOOTING #
###########
def findCorpses():
    corpses_filter = Items.Filter()
    corpses_filter.IsCorpse = True # optional
    corpses_filter.OnGround = True # Questionably optional
    corpses_filter.RangeMin = 0 # optional
    corpses_filter.RangeMax = 2 # optoinal
    corpses_filter.Graphics = List[Int32]([corpse_ID,]) # optional, use item IDs
    corpses_filter.CheckIgnoreObject = True # optioinal, if you use Misc.IgnoreObject(item) the fitler will ignore if true.

    corpse_list = Items.ApplyFilter(corpses_filter) # returns list of items, manipulate list after this as you wish

    return corpse_list

def lootCorpse(corpse):
    for item_to_loot in corpse.Contains:
        Misc.SendMessage("found a {} with ID {}".format(item_to_loot.Name, item_to_loot.ItemID),130)
        Misc.Pause(10)
        shouldLoot = False
        if checkItemByID(item_to_loot, loot_list):
            shouldLoot = True
        if shouldLoot:
            Items.Move(item_to_loot,Player.Backpack,-1 ) # -1 -> all, for stackable items
            Misc.Pause(750)
        
            
def checkItemByID(item_to_check, valid_ids):
    if item_to_check.ItemID in loot_list:
        return True
    return False
    
def checkItemByName(item_to_check, valid_names):
    for name in valid_names:
        if name.lower() in str(item_to_check.Name).lower():
            return True
    return False
    
    
def tooMuchWeight():
    if Player.Weight > Player.MaxWeight - 30:
        Player.HeadMessage(138, "Burp, Feeling full")
        Misc.Pause(2000)


while not Player.IsGhost:
    for i in range(30):
        HealPets()
        crps_list = findCorpses()

        for current_corpse in crps_list:
            if not tooMuchWeight():
                Items.Message(current_corpse,170,"loot this")
                Items.UseItem(current_corpse)
                Misc.Pause(750)
                lootCorpse(current_corpse)
        
        if i == 1:
            Test_Route = PathFinding.Route()
            Test_Route.X = 432
            Test_Route.Y = 1184
            Test_Route.IgnoreMobile = True
            PathFinding.Go(Test_Route)
        elif i == 16:
            Test_Route = PathFinding.Route()
            Test_Route.X = 432
            Test_Route.Y = 1192
            Test_Route.IgnoreMobile = True
            PathFinding.Go(Test_Route)
            

        mobFilter = Mobiles.Filter()
        mobFilter.RangeMin = 0
        mobFilter.RangeMax = 7
        mobFilter.IsHuman = 0   
        mobFilter.IsGhost = 0
        mobFilter.Friend = 0
        mobFilter.Notorieties = GetEnemyNotorieties()
        enemies = Mobiles.ApplyFilter( mobFilter )
        Misc.SendMessage("Looking for enemies")
        
        for enemy in enemies:
            HealPets()
            Mobiles.Message(enemy,170,"> TARGET <",5000)
            Misc.Pause(150)
            Player.ChatSay("All Kill")
            Misc.Pause(250)
            Target.TargetExecute(enemy)
            Misc.Pause(5000)
            pet1 = Mobiles.FindBySerial( pet1Serial )
            if Player.DistanceTo( pet1 ) > 2:
                FollowMobile( pet1, 2, True )
            Misc.Pause(150) 

        Misc.Pause(5000) 
        
        