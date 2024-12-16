from Scripts.utilities.items import FindItem
from Scripts.glossary.colors import colors
from System.Collections.Generic import List
from Scripts.glossary.enemies import GetEnemyNotorieties
from System import Byte, Int32

# SETTINGS #
############
#loot Item IDs
corpse_ID = 0x2006
gold_ID = 0x0EED
citrine = 0x0F15
amber = 0x0F25
amethyst = 0x0F16
ruby = 0x0F13
emerald = 0x0F10
diamond = 0x0F26
sapphire = 0x0F11
tourmaline = 0x0F18
starsapph = 0x0F0F
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
plant1 = 0x63DF
plant2 = 0x1E0F
plant3 = 0x11C8
plant4 = 0xAC91
plant5 = 0x63D4
plant6 = 0x0C90
plant7 = 0xAC92
plant8 = 0x63D5
plant9 = 0x9FFF
plant10 = 0x1782
plant11 = 0x0D0B
plant12 = 0x4C3A
deed = 0x14F0
dye1 = 0x0E2A
dye2 = 0x0E2B
dye3 = 0x0EFF
dye4 = 0x0EFE
artifact1 = 0x1576
artifact2 = 0x2228
artifact3 = 0x1F14
artifact4 = 0x2D28
artifact5 = 0x14ED
artifact6 = 0x1227
artifact7 = 0x4076
artifact8 = 0x223D
artifact9 = 0x1F18
artifact10 = 0x2B01
artifact11 = 0x15BB
artifact12 = 0x14F4
artifact13 = 0x1B0C
sulphash = 0x0F8C
bloodmoss = 0x0F7B
ginseng = 0x0F85
garlic = 0x0F84
blackpearl = 0x0F7A
nightshade = 0x0F88
mandrake = 0x0F86
spidersilk = 0x0F8D
special1 = 0x234D #rose of trinsic
specialfood1 = 0xB939
specialfood2 = 0xA672

reg_list = [sulphash,bloodmoss,ginseng,garlic,blackpearl,nightshade,mandrake,spidersilk]
loot_list = [gold_ID,biggem1,biggem2,biggem3,biggem4,biggem5,biggem6,biggem7,arcanedust,arcanescroll,scrolloftrans,tmap,artifact1,plant1,plant2,plant3,plant4,deed,dye1,dye2,dye3,plant5,artifact2,artifact3,artifact4,artifact5,artifact6,dye4,artifact7,plant6,artifact8,artifact9,plant7,artifact10,special1,artifact11,specialfood1,specialfood2,artifact12,artifact13,plant8,plant9,plant10,plant11,plant12]

#Player Settings
if Player.Name == "Dextrome":
    pet1Serial = 0x000199DE # mystwyrm
    pet2Serial = 0x00023275 # mystdrak
    pet2Serial = 0x00009315 #mare
    gemorganizer = "gems dextrome"
    regorganizer = "regs dextrome"
    restorganizer = "loot dextrome"
    restockagent = "regs"
    runebookSerial = 0x4016BF11 #Hard Mobs
    homebookorruneSerial = 0x4014447E
    numberOfRunes = 16
    use_petals_str = False
    use_petals_int = False
    use_petals_agi = False
    use_skinnning = False     
elif Player.Name == "Gaga":
    pet1Serial = 0x0000312F #DragonDeezNutz
    pet2Serial = 0x00006291 #DeezButtz
    gemorganizer = "gems gaga"
    regorganizer = "regs gaga"
    restorganizer = "loot gaga"
    restockagent = "regs gaga"
    runebookSerial = 0x4010D85B #EZ Mobs
    numberOfRunes = 10
    use_petals_str = False
    use_petals_int = False
    use_petals_agi = False
    use_skinnning = False
    
runebook = Items.FindBySerial( runebookSerial )
homebookorrune = Items.FindBySerial( homebookorruneSerial )
petsToCheck = List[Int32]([
        pet1Serial, 
        pet2Serial, 
    ])
    
# SURVIVAL #
############
def RearmTrappouch():
    done = False
    trappouch = FindItem( 0x09B0, Player.Backpack )
    
    if trappouch != None:
        while not done:
            Misc.Pause(150)
            Spells.CastMagery("Magic Trap")
            
            Misc.Pause(1000)
            Target.TargetExecute(trappouch)
            
            Items.SingleClick(trappouch.Serial)
            
            regularText = Journal.GetTextByType( 'Label' )
            regularText.Reverse()
            
            for line in regularText[ 0 : 20 ]:
                if line == 'a pouch [Charges 10/10]':
                    Player.ChatSay("woop")
                    done = True
                    Misc.Pause(1000)
                    break
    
def Survive():
    if Player.Paralized:
        trappouch = FindItem( 0x09B0, Player.Backpack )
        if trappouch != None:
            Items.UseItem(trappouch)
            Misc.Pause( 150 )
    
    if Player.Poisoned:
        Spells.Cast("Cure")
        Target.WaitForTarget( 1500, False )
        Target.Self()
        Misc.Pause( 50 )
            
    if Player.Hits < 75:
        Spells.Cast("Greater Heal")
        Misc.Pause( 500 )
        Player.ChatSay("all guard me")
        Target.WaitForTarget( 1500, False )
        Target.Self()
        Misc.Pause( 50 )
        
        
    
def CheckPetalsStr():
    if use_petals_str == True:
        if (Player.BuffsExist('Bless') and Player.Str < 115) or Player.Str < 105:
            petals_str = Items.FindByID(0x1021,0x000e, Player.Backpack.Serial)

            if petals_str:
                Items.UseItem(petals_str.Serial)
                Misc.Pause( 100 )
#            else:
#                Items.UseItem(0x4001298E)
#                Misc.Pause(600)
#                petals_str = Items.FindByID(0x1021,0x000e, Player.Backpack.Serial)
#                if petals_str:
#                    Items.UseItem(petals_str.Serial)
#                    Misc.Pause( 150 )
#        
# DROP LOOT & RESTOCK #
#######################

def DropLoot():
    Organizer.ChangeList(gemorganizer)
    Misc.Pause( 250 )
    Organizer.FStart()
    Misc.Pause( 5000 )
    Organizer.FStop()
    Misc.Pause( 250 )
    if Player.Name == 'Dextrome':
        Organizer.ChangeList(regorganizer)
        Organizer.FStart()
        Misc.Pause( 5000 )
        Organizer.FStop()
        Misc.Pause( 250 )
    Organizer.ChangeList(restorganizer)
    Misc.Pause( 250 )
    Organizer.FStart()
    Misc.Pause( 5000 )
    Organizer.FStop()
    Misc.Pause( 250 )
    Organizer.FStart()
    Misc.Pause( 3000 )
    Organizer.FStop()
    Misc.Pause( 250 )
    
def RestockRegsAndBandages():
    Restock.ChangeList(restockagent)
    Misc.Pause( 150 )
    Restock.FStart()
    Misc.Pause( 6000 )
    Restock.FStop()
    Misc.Pause( 150 )
    Restock.FStart()
    Misc.Pause( 5000 )
    Restock.FStop()
    
# TRAVEL #
##########

def PlayersNearby():
#    mobFilter = Mobiles.Filter()
#    mobFilter.RangeMin = 0
#    mobFilter.RangeMax = 17
#    mobFilter.IsHuman = 1
#    mobFilter.IsGhost = 0
#    
#    pets = Mobiles.ApplyFilter( mobFilter )
#    
#    if len( pets ) == 0:
#        return False
#    else:
#        return True
    return False
        
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
    tooMuchWeight()
    
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
        Timer.Create( 'playerStuckTimer', 5000 )

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
        Timer.Create( 'playerStuckTimer', 5000 )
    elif playerPosition != newPlayerPosition:
        Timer.Create( 'playerStuckTimer', 5000 )

    if Player.DistanceTo( mobile ) > maxDistanceToMobile:
        # This pause may need further tuning
        # Don't want to create a ton of infinite calls if the player is stuck, but also don't want to not be able to catch up to animals
        Misc.Pause( 150 )
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
    #crps_list = findCorpses()

    #for current_corpse in crps_list:
    #    if not tooMuchWeight():
    #        Items.Message(current_corpse,170,"loot this")
    #        Items.UseItem(current_corpse)
    #        Misc.Pause(750)
    #        lootCorpse(current_corpse)
            
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
    #Misc.SendMessage( 'healing pets' )
    

    for petSerial in petsToCheck:
        pet = Mobiles.FindBySerial( petSerial )
        if pet == None:
            continue
        #Misc.SendMessage( 'Checking %s\'s health' % pet.Name )
        maxDistance = 2
        
        #if pet.Hits < pet.HitsMax or pet.Poisoned:
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
    #Items.UseItem(corpse)
    #Misc.Pause(600)
    if use_skinnning == True and scissors:
        Items.UseItem(dagger)
        Target.WaitForTarget(700,0)
        Target.TargetExecute(corpse)
        Misc.Pause(500)
            
    for item_to_loot in corpse.Contains:
        #Misc.SendMessage("found a {} with ID {}".format(item_to_loot.Name, item_to_loot.ItemID),130)
        #Misc.Pause(10)
        shouldLoot = False

        if use_skinnning == True and item_to_loot.ItemID == 0x1079 and scissors:
            Items.UseItem(scissors)
            Target.WaitForTarget(700,0)
            Target.TargetExecute(item_to_loot)
            Misc.Pause(700)
        else:
            if checkItemByID(item_to_loot, loot_list):
                shouldLoot = True
            if shouldLoot:
                Items.Move(item_to_loot,Player.Backpack,-1 ) # -1 -> all, for stackable items
                Misc.Pause(700)
    if use_skinnning == True:                    
        leather = Items.FindByID(0x1081,-1, corpse.Serial)
        if leather: 
            #Player.HeadMessage(50, "Leather Found")
            Misc.Pause(100)
            Items.Move(leather.Serial,Player.Backpack.Serial,-1)
            Misc.Pause(600)   
            
def checkItemByID(item_to_check, valid_ids):
    if item_to_check.ItemID in loot_list:
        return True
    elif Player.Name == "Dextrome" and item_to_check.ItemID in reg_list:
        return True
    return False
    
def checkItemByName(item_to_check, valid_names):
    for name in valid_names:
        if name.lower() in str(item_to_check.Name).lower():
            return True
    return False
    
    
def tooMuchWeight():
    if Player.Weight > Player.MaxWeight - 18:
        if Player.BuffsExist('Bless'):
            Player.HeadMessage(138, "Burp, Feeling full")
            return True
        else:
            Spells.CastMagery('Bless')
            Target.WaitForTarget(1500)
            Target.Self()
            Misc.Pause(1500)


# MAIN #
########

#def main(): # define the function
#    while not Player.IsGhost:
#        HealPets()
#        Misc.Pause( 150 )

def CheckForEnemies(waitTimeIfNoEnemies):
    CheckPetalsStr()
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
        HealPets()
        Misc.Pause(waitTimeIfNoEnemies)
    else:
        #Player.ChatSay("all kill")
        #Target.WaitForTarget( 250, False )
        #Target.PerformTargetFromList('closest mob')
        #Misc.Pause(100)
        Player.ChatSay("all guard")
        crook = Items.FindByID(0x0E81,-1,Player.Backpack.Serial)
        if crook:
            #equip crook#
            Items.UseItem(crook)
            Misc.Pause(250)
            Target.Cancel()
        
        for enemy in enemies:
            Mobiles.Message(enemy,170,"Enemy Here",1000)
            Player.ChatSay("all kill")
            Target.WaitForTarget( 250, False )
            Target.TargetExecute(enemy)
            Misc.Pause(50)
            regularText = Journal.GetTextByType( 'System' )

            # Reverse the Journal entries so that we read from newest to oldest
            regularText.Reverse()

            # Read back until the bandages were started to see if they have finished applying
            for line in regularText[ 0 : len( regularText ) ]:
                if line == 'Target cannot be seen.':
                    break
                
         #   crps_list = findCorpses()
#
#            for current_corpse in crps_list:
#                if not tooMuchWeight():
#                    Items.Message(current_corpse,170,"loot this")
#                    Items.UseItem(current_corpse)
#                    Misc.Pause(620)
#                    lootCorpse(current_corpse)
#           
            Player.ChatSay("all guard")
            Misc.Pause(50)
            Player.Attack(enemy.Serial)
            while Mobiles.FindBySerial(enemy.Serial) != None:
                #Player.HeadMessage(138, "Enemy is alive")
                #Follow Pet
                pet1 = Mobiles.FindBySerial( pet1Serial )
                if Player.DistanceTo( pet1 ) > 1:
                    FollowMobile( pet1, 1, True )
                    
                #Heal Pets
                HealPets()
                Survive()
                Misc.Pause(150)
                
            #enemy is dead - check for loot
            Player.ChatSay("all guard")
            HealPets()
            Misc.Pause( 150 )
            crps_list = findCorpses()

 #           for current_corpse in crps_list:
#                if not tooMuchWeight():
#                    Items.Message(current_corpse,170,"loot this")
#                    Items.UseItem(current_corpse)
#                    Misc.Pause(620)
#                    lootCorpse(current_corpse)
            
            Misc.Pause(50)
    



while not Player.IsGhost:
    dagger = Items.FindByID(0x0F52,-1,Player.Backpack.Serial)
    if use_skinnning == True and not dagger:
        Player.HeadMessage(50,"No dagger found")
        sys.exit()
    scissors = Items.FindByID(0x0F9F,-1,Player.Backpack.Serial)
        
    for i in range(1,numberOfRunes):
        Survive()
        Misc.Pause( 650 )
        Player.HeadMessage(138, "recall to next spot")
        Items.UseItem( runebook )
        Gumps.WaitForGump( 89, 5000 )
        Gumps.SendAction( 89, 50 + i )
        Misc.Pause(4000)
        
        if i == 0:
            #Bank
            
            #RearmTrappouch()
#            Misc.Pause(150)
#            Player.ChatSay("bank")
#            Misc.Pause(150)
#            DropLoot()
#            Misc.Pause(150)
#            RestockRegsAndBandages()
            Misc.Pause(500)
        else:
            if PlayersNearby() == False:
                Player.HeadMessage(170, "no players nearby")
                Player.ChatSay("all kill")
                Target.WaitForTarget( 250, False )
                Target.PerformTargetFromList('closest mob')
                Misc.Pause(1500)
                Player.ChatSay("all guard me")
                Target.Cancel()
                HealPets()
                Player.ChatSay("all guard")
                pet2 = Mobiles.FindBySerial( pet2Serial )
                if Player.DistanceTo( pet2 ) > 1:
                    FollowMobile( pet2, 1, True )
                CheckForEnemies(4750)
                Player.ChatSay("all guard")
                pet1 = Mobiles.FindBySerial( pet1Serial )
                if Player.DistanceTo( pet1 ) > 1:
                    FollowMobile( pet1, 1, True )
                Player.ChatSay("all guard")
                CheckForEnemies(50)
                Survive()
                Player.ChatSay("all follow me")
                #crps_list = findCorpses()
#
#                for current_corpse in crps_list:
#                    if not tooMuchWeight():
#                        Items.Message(current_corpse,170,"loot this")
#                        Items.UseItem(current_corpse)
#                        Misc.Pause(700)
#                        lootCorpse(current_corpse)
                Misc.Pause(150)
            else:
                Player.HeadMessage(138,"Players nearby, recalling to next in 7 seconds")
                Misc.Pause(1500)
                Player.Run("North")
                Player.Run("Right")
                Player.Run("Down")
                Player.Run("Left")
                Player.Run("North")
                Player.Run("Right")
                Player.Run("Down")
                Player.Run("Left")
                Player.Run("West")
                Player.Run("Right")
                Player.Run("East")
                Player.Run("Left")
                Player.Run("Up")
                Player.Run("North")
                Player.Run("East")
                Player.Run("South")
                Misc.Pause(1000)
                Player.ChatSay("all follow me")
                Misc.Pause(2800)
        
        CheckPetalsStr()
        bandages = FindItem( 0x0E21, Player.Backpack )
        if bandages == None:
            break
        elif Player.Weight > Player.MaxWeight - 20:
            if Player.BuffsExist('Bless'):
                break
            else:
                Spells.CastMagery('Bless')
                Target.WaitForTarget(1500)
                Target.Self()
                
    Survive()
    i = 1     
                
# RUN       
#main()