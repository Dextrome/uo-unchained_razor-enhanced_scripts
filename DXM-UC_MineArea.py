import sys
import math
from System.Collections.Generic import List
from System import Byte, Int32


###CONFIG SETTINGS###

petSerial = 0x0001E8A9

###---------------###


colors = {
    'green': 65,
    'cyan': 90,
    'orange': 43,
    'red': 1100,
    'yellow': 52
}

pet = Mobiles.FindBySerial( petSerial )
captchaGumpId = 1565867016
checkForAnyGump = True
oreLandIDs = [0x00F1, 0x00F2, 0x00F3, 0x00F0, 0x023A]
oreStaticIDs = [0x053B, 0x053C, 0x053D, 0x053E, 0x053F]
forgesList = [0x197A, 0x197E, 0x19A2, 0x1982, 0x1992, 0x1996, 0x199A, 0x0FB1]
oreposx = []
oreposy = []
oreposz = []
ScanZone = 24
global miningTool
self = Player.Serial
self_pack = Player.Backpack.Serial
forgesList = List[int]((0x197A, 0x197E, 0x19A2, 0x1982, 0x1992, 0x1996, 0x199A, 0x0FB1))
tinkerTools = [0x1EB8, 0x1EBC]
minerTools = [0x0F39, 0x0E86]
pickaxeID = 0x0F39 #0x0E86 
journalEntryDelayMilliseconds = 200
targetClearDelayMilliseconds = 200
dragDelayMilliseconds = 700

class myItem:
    name = None
    itemID = None
    color = None
    category = None
    weight = None

    def __init__ ( self, name, itemID, color, category, weight ):
        self.name = name
        self.itemID = itemID
        self.color = color
        self.category = category
        self.weight = weight

        
def FindItem( itemID, container, color = -1, ignoreContainer = [] ):
    '''
    Searches through the container for the item IDs specified and returns the first one found
    Also searches through any subcontainers, which Misc.FindByID() does not
    '''

    ignoreColor = False
    if color == -1:
        ignoreColor = True

    if isinstance( itemID, int ):
        foundItem = next( ( item for item in container.Contains if ( item.ItemID == itemID and ( ignoreColor or item.Hue == color ) ) ), None )
    elif isinstance( itemID, list ):
        foundItem = next( ( item for item in container.Contains if ( item.ItemID in itemID and ( ignoreColor or item.Hue == color ) ) ), None )
    else:
        raise ValueError( 'Unknown argument type for itemID passed to FindItem().', itemID, container )

    if foundItem != None:
        return foundItem

    subcontainers = [ item for item in container.Contains if ( item.IsContainer and not item.Serial in ignoreContainer ) ]
    for subcontainer in subcontainers:
        foundItem = FindItem( itemID, subcontainer, color, ignoreContainer )
        if foundItem != None:
            return foundItem


def FindNumberOfItems( itemID, container, color = -1 ):
    '''
    Recursively looks through a container for any items in the provided list
    Returns the a dictionary with the number of items found from the list
    '''
    
    ignoreColor = False
    if color == -1:
        ignoreColor = True

    # Create the dictionary
    numberOfItems = {}

    if isinstance( itemID, int ):
        # Initialize numberOfItems
        numberOfItems[ itemID ] = 0

        # Populate numberOfItems
        for item in container.Contains:
            if item.ItemID == itemID and ( ignoreColor or item.Hue == color ):
                numberOfItems[ itemID ] += item.Amount
    elif isinstance( itemID, list ):
        # Initialize numberOfItems
        for ID in itemID:
            numberOfItems[ ID ] = 0

        # Populate numberOfItems
        for item in container.Contains:
            if item.ItemID in itemID and ( ignoreColor or item.Hue == color ):
                numberOfItems[ item.ItemID ] += item.Amount
    else:
        raise ValueError( 'Unknown argument type for itemID passed to FindItem().', itemID, container )

    subcontainers = [ item for item in container.Contains if item.IsContainer ]

    # Iterate through each item in the given list
    for subcontainer in subcontainers:
        numberOfItemsInSubcontainer = FindNumberOfItems( itemID, subcontainer )
        for ID in numberOfItems:
            numberOfItems[ ID ] += numberOfItemsInSubcontainer[ ID ]

    return numberOfItems


def MoveItem( Items, Misc, item, destinationBag, amount = 0 ):
    Items.Move( item, destinationBag, amount )
    Misc.Pause( config.dragDelayMilliseconds )

    
def ScanLandForOre( ): 
    global oreposcoords
    Misc.SendMessage("--> Scanning Tiles in ScanZone", 77)
    minx = Player.Position.X - ScanZone
    maxx = Player.Position.X + ScanZone + 2
    miny = Player.Position.Y - ScanZone
    maxy = Player.Position.Y + ScanZone + 4
    tmporeposcoords = []

    while miny <= maxy:
        while minx <= maxx: 
            tileLandID = Statics.GetLandID(minx, miny, Player.Map)
            tileZ = Statics.GetLandZ(minx,minx, Player.Map)
            
            if tileLandID != None:
                for landID in oreLandIDs:
                    if landID == tileLandID:
                        tileinfo = Statics.GetStaticsTileInfo(minx, miny, Player.Map)
                        validTile = True
                        if tileinfo.Count > 0:
                            for tile in tileinfo:
                                if tile.StaticID != 0x0000 or tileLandID == None:
                                    validTile = False
                        if validTile:
                            Misc.SendMessage('-> Ore found at X: %i - Y: %i - Z: %i' % (minx, miny, tileZ), 66)
                            tmporeposcoords.Add([minx,miny,tileZ])
            else:
                Misc.NoOperation()
            minx = minx + 1
        minx = Player.Position.X - ScanZone            
        miny = miny + 1
    
    oreposcoords = sorted(tmporeposcoords , key=lambda k: [k[1], k[0], k[2]])
    
    Misc.SendMessage(oreposcoords.Count)
        
    
def MoveToOre(i):
    if abs(Player.Position.X - oreposcoords [i][0]) > 5 or abs(Player.Position.Y - oreposcoords [i][1]) > 5:
        if Player.Mount == None:
            Mobiles.UseMobile( pet ) #remount
            Misc.Pause( 650 )
    
    staticOnTile = False
    tileLandID = Statics.GetLandID(oreposcoords[i][0], oreposcoords[i][1], Player.Map)
    tileinfo = Statics.GetStaticsTileInfo(oreposcoords[i][0], oreposcoords[i][1], Player.Map)
    landFlag_Impassable = Statics.GetLandFlag(tileLandID, "Impassable")
    if landFlag_Impassable == True:
        staticOnTile = True
    elif tileinfo.Count > 0:
        for tile in tileinfo:
            if tile.StaticID != 0x0000 or tileLandID == None:
                staticOnTile = True
                    
    if staticOnTile == True:
        tileLandID = Statics.GetLandID(oreposcoords[i][0], oreposcoords[i][1]-1, Player.Map)
        tileinfo = Statics.GetStaticsTileInfo(oreposcoords[i][0], oreposcoords[i][1]-1, Player.Map)
        landFlag_Impassable = Statics.GetLandFlag(tileLandID, "Impassable")
        if landFlag_Impassable == True:
            staticOnTile = True
        elif tileinfo.Count > 0:
            for tile in tileinfo:
                if tile.StaticID != 0x0000 or tileLandID == None:
                    staticOnTile = True
                        
        if staticOnTile == True:
            staticOnTile = False
            tileLandID = Statics.GetLandID(oreposcoords[i][0], oreposcoords[i][1]+1, Player.Map)
            tileinfo = Statics.GetStaticsTileInfo(oreposcoords[i][0], oreposcoords[i][1]+1, Player.Map)
            landFlag_Impassable = Statics.GetLandFlag(tileLandID, "Impassable")
            if landFlag_Impassable == True:
                staticOnTile = True
            elif tileinfo.Count > 0:
                for tile in tileinfo:
                    if tile.StaticID != 0x0000 or tileLandID == None or landFlag_Impassable == True:
                        staticOnTile = True
                        
            if staticOnTile == True:
                staticOnTile = False
                tileLandID = Statics.GetLandID(oreposcoords[i][0]-1, oreposcoords[i][1]-1, Player.Map)
                tileinfo = Statics.GetStaticsTileInfo(oreposcoords[i][0]-1, oreposcoords[i][1]-1, Player.Map)
                landFlag_Impassable = Statics.GetLandFlag(tileLandID, "Impassable")
                if landFlag_Impassable == True:
                    staticOnTile = True
                elif tileinfo.Count > 0:
                    for tile in tileinfo:
                        if tile.StaticID != 0x0000 or tileLandID == None:
                            staticOnTile = True
                            
                if staticOnTile == True:
                    staticOnTile = False
                    tileLandID = Statics.GetLandID(oreposcoords[i][0]+1, oreposcoords[i][1]-1, Player.Map)
                    tileinfo = Statics.GetStaticsTileInfo(oreposcoords[i][0]+1, oreposcoords[i][1]-1, Player.Map)
                    landFlag_Impassable = Statics.GetLandFlag(tileLandID, "Impassable")
                    if landFlag_Impassable == True:
                        staticOnTile = True
                    elif tileinfo.Count > 0:
                        for tile in tileinfo:
                            if tile.StaticID != 0x0000 or tileLandID == None:
                                staticOnTile = True
                                
                    if staticOnTile == True:
                        staticOnTile = False
                        tileinfo = Statics.GetStaticsTileInfo(oreposcoords[i][0]-1, oreposcoords[i][1]-1, Player.Map)
                        landFlag_Impassable = Statics.GetLandFlag(tileLandID, "Impassable")
                        if landFlag_Impassable == True:
                            staticOnTile = True
                        elif tileinfo.Count > 0:
                            for tile in tileinfo:
                                if tile.StaticID != 0x0000 or tileLandID == None:
                                    staticOnTile = True
                        if staticOnTile == True:
                            Misc.NoOperation()
                            Misc.SendMessage('cant move to target', 56)
                        else:
                            Misc.SendMessage('Moving to X: %i - Y: %i - Z: %i' % (oreposcoords[i][0]+1, oreposcoords[i][1]+1, oreposcoords[i][2]), 76)
                            PathFinding.PathFindTo(oreposcoords[i][0]+1, oreposcoords[i][1]+1, oreposcoords[i][2])  
                    else:
                        Misc.SendMessage('Moving to X: %i - Y: %i - Z: %i' % (oreposcoords[i][0]+1, oreposcoords[i][1]-1, oreposcoords[i][2]), 76)    
                        PathFinding.PathFindTo(oreposcoords[i][0]+1, oreposcoords[i][1]-1, oreposcoords[i][2])   
                else:
                    Misc.SendMessage('Moving to X: %i - Y: %i - Z: %i' % (oreposcoords[i][0]-1, oreposcoords[i][1]-1, oreposcoords[i][2]), 76)
                    PathFinding.PathFindTo(oreposcoords[i][0]-1, oreposcoords[i][1]-1, oreposcoords[i][2])
            else:
                Misc.SendMessage('Moving to X: %i - Y: %i - Z: %i' % (oreposcoords[i][0], oreposcoords[i][1]+1, oreposcoords[i][2]), 76)
                PathFinding.PathFindTo(oreposcoords[i][0], oreposcoords[i][1]+1, oreposcoords[i][2])
        else:
            Misc.SendMessage('Moving to X: %i - Y: %i - Z: %i' % (oreposcoords[i][0], oreposcoords[i][1]-1, oreposcoords[i][2]), 76)
            PathFinding.PathFindTo(oreposcoords[i][0], oreposcoords[i][1]-1, oreposcoords[i][2])
    else:
        Misc.SendMessage('Moving to X: %i - Y: %i - Z: %i' % (oreposcoords[i][0], oreposcoords[i][1], oreposcoords[i][2]), 76)
        PathFinding.PathFindTo(oreposcoords[i][0], oreposcoords[i][1], oreposcoords[i][2])
        

def MoveOreToPet():
    pet = Mobiles.FindBySerial( petSerial )
    if pet == None:
        Player.HeadMessage( colors[ 'red' ], 'Could not find storage pet!' )

#    Mobiles.UseMobile( Player.Serial ) #dismount
#    Misc.Pause( 650 )
    Misc.WaitForContext(pet, 10000)
    Misc.ContextReply(pet, "Open Backpack")   
    Misc.Pause( 650 )
    
    
    for item in Player.Backpack.Contains:
        if item.ItemID == 0x19B9: #ore
            Journal.Clear()
            Misc.Pause(200)
            
            if Player.Name == "Phill Myke Hunt":
                Items.UseItem(item)
                Target.WaitForTarget(5000,False)
                Target.TargetExecute(0x00001CE2) #firebeetle
                Misc.Pause( 500 )  
            else:
                Misc.SendMessage('Moving %s to %s' % (item.Name, pet.Name))
                Items.Move(item.Serial,Mobiles.FindBySerial( petSerial ).Backpack,0)
                Misc.Pause( 650 )

def GoHome():
    Player.HeadMessage( colors[ 'green' ], "DONE MINING")
    sys.exit(99) #turns script off

#while True:
if not Player.IsGhost:
    oreposcoords = []
    ScanLandForOre()
    i = 0
    wentHome = False
    
    Misc.SendMessage("---")
    Misc.SendMessage(oreposcoords.Count)

    while i < oreposcoords.Count and wentHome == False:
        pet = Mobiles.FindBySerial( petSerial )
        if pet == None and Player.Mount == None:
            Player.HeadMessage( colors[ 'red' ], 'Could not find storage pet!' )
            
        #Misc.SendMessage('Target = X: %i - Y: %i - Z: %i' % (oreposcoords[i][0], oreposcoords[i][1], oreposcoords[i][2]), 66)
        MoveToOre(i)
        
        if Player.Mount != None:
            Mobiles.UseMobile( Player.Serial ) #dismount
            Misc.Pause( 650 )
            Misc.UseContextMenu(petSerial,"Command: Guard",1000)
            
        Journal.Clear()
        Misc.Pause(200)
        
#        iteminhand = Player.GetItemOnLayer("RightHand")
#        if not iteminhand: 
#            pickaxe = Items.FindByID(pickaxeID, -1, Player.Backpack.Serial)
#            Misc.Pause(200)
#            if pickaxe:
#                Misc.SendMessage("equipping pickaxe")
#                Player.EquipItem(pickaxe)
#                Misc.Pause( 650 )
        pickaxe = Items.FindByID(pickaxeID, -1, Player.Backpack.Serial)
        
        while ( not Journal.SearchByName( 'There is no metal here to mine.', 'System' ) and
                not Journal.SearchByName( 'Target cannot be seen.', 'System' ) and
                not Journal.SearchByName( 'You can\'t mine there.', 'System' ) and 
                not Journal.SearchByName( 'That is too far away.', 'System' ) and 
                not Journal.SearchByName( 'You have worn out your tool!', 'System' ) ):
                
            while Gumps.HasGump(captchaGumpId):
                sayTTS("%s Captcha Alert" % (Player.Name))
                Misc.Pause(666)
            
            if Player.Weight <= Player.MaxWeight - 20:
                #Player.HeadMessage(99,"mining")
#                iteminhand = Player.GetItemOnLayer("RightHand")
#                if not iteminhand: 
#                    pickaxe = Items.FindByID(pickaxeID, -1, Player.Backpack.Serial)
#                else:
#                    pickaxe = iteminhand
                pickaxe = Items.FindByID(pickaxeID, -1, Player.Backpack.Serial)
                    
                if pickaxe:
                    #Misc.SendMessage("using pickaxe")
                    Items.UseItem(pickaxe)
                    Target.WaitForTarget(2500,False)
                    tileinfo = Statics.GetStaticsTileInfo(oreposcoords[i][0], oreposcoords[i][1], Player.Map)
                    Target.TargetExecute(oreposcoords[i][0], oreposcoords[i][1], oreposcoords[i][2])
                    Misc.Pause( 2000 ) # Wait for the mining animation to complete
                else:
                    #GoHome()
                    wentHome = True
                    break
            else:
                Player.HeadMessage(99,"overweight")
                MoveOreToPet()
                if Journal.Search("You are overloaded") or Player.Weight >= Player.MaxWeight - 20:
                    Misc.SendMessage('Overloaded time to go home')
                    #GoHome()
                    wentHome = True
                    break
                
            Misc.Pause( 50 )
                
        i+=2
    
    GoHome()