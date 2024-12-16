import sys
import math
from System.Collections.Generic import List
from System import Byte, Int32
from Scripts.utilities.items import FindItem, FindNumberOfItems, MoveItem
from Scripts.glossary.items.ores import ores
from Scripts.glossary.colors import colors
import clr
clr.AddReference('System.Speech')
from System.Speech.Synthesis import SpeechSynthesizer

if Player.Name == "Shmolas":
    storageShelfSerial = 0x401B271D
    vaultSerial = 0x4028C99B
    petSerial = 0x00013F18
    pet = Mobiles.FindBySerial( petSerial )
    runeBookSerial = 0x4034E9C4
#    targetRunebook = False
#    canCastRecall = False
#    homeRuneIndex = 10
    targetRunebook = True
    canCastRecall = True
    toolbagSerial = 0x4046965F #can be a container in your bank(vault) or just a container within range 
    numberOfRunes = 8
elif Player.Name == "Phill Myke Hunt":
    storageShelfSerial = 0x401B271D
    vaultSerial = 0x4028C99B
    petSerial = 0x0000DFE5
    pet = Mobiles.FindBySerial( petSerial )
    runeBookSerial = 0x401444C6
    targetRunebook = True
    canCastRecall = True
    toolbagSerial = 0x400CBA40 #can be a container in your bank(vault) or just a container within range
    numberOfRunes = 8
    
resourceShelfSerial = 0x402DD22C
homeforgeSerial = 0x401A5010
captchaGumpId = 1565867016
checkForAnyGump = True
oreLandIDs = [0x00F1, 0x00F2, 0x00F3, 0x00F0, 0x023A, 0x0232]
oreStaticIDs = [0x053B, 0x053C, 0x053D, 0x053E, 0x053F]
forgesList = [0x197A, 0x197E, 0x19A2, 0x1982, 0x1992, 0x1996, 0x199A, 0x0FB1]
ScanZone = 24
global miningTool

#generic
self = Player.Serial
self_pack = Player.Backpack.Serial

##types lists
forgesList = List[int]((0x197A, 0x197E, 0x19A2, 0x1982, 0x1992, 0x1996, 0x199A, 0x0FB1))
tinkerTools = [0x1EB8, 0x1EBC]
minerTools = [0x0F39, 0x0E86]

pickaxeID = 0x0F39 #0x0E86 

## msg stubs
smeltSuccess = 'You smelt the ore removing the impurities and put the metal in your backpack.'
smeltFail = 'You burn away the impurities but are left with less useable metal.'

spk = SpeechSynthesizer()


def sayTTS(text):
    spk.Speak(text)
    

def GetGM():
    enemyfil = Mobiles.Filter()
    enemyfil.Enabled = True
    enemyfil.RangeMin = 0
    enemyfil.RangeMax = 8
    enemyfil.ZLevelMin = Player.Position.Z -8
    enemyfil.ZLevelMax = Player.Position.Z +8
    enemyfil.CheckLineOfSight = True
    enemyfil.Friend = False
    #enemyfil.IsHuman = True
    enemyfil.Notorieties = List[Byte](bytes([7]))
    enemyList = Mobiles.ApplyFilter(enemyfil)
    gm = Mobiles.Select(enemyList, 'Nearest')
    return gm
    
    
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

                
    if Player.Name == "Phill Myke Hunt": 
        for item in Player.Backpack.Contains:
            if item.ItemID == 0x1BF2: #ingot
                Misc.SendMessage('Moving %s to %s' % (item.Name, pet.Name))
                Items.Move(item.Serial,Mobiles.FindBySerial( petSerial ).Backpack,0)
                Misc.Pause( 650 )
                    
def GoHome():
    Player.ChatSay("all follow me")
    Misc.Pause(1000)
    
    #while (Gumps.CurrentGump() != 0 and checkForAnyGump) or Gumps.CurrentGump() == captchaGumpId:
    while Gumps.HasGump(captchaGumpId):
        sayTTS("%s Captcha Alert" % (Player.Name))
        Misc.Pause(666)
        
    if Player.Mount == None:
        mount = Mobiles.FindBySerial( petSerial )
        if mount != None:
            Mobiles.UseMobile( mount )

    
    if targetRunebook and canCastRecall:
        Spells.Cast("Recall")
        Target.WaitForTarget(5000)
        Target.TargetExecute(runeBookSerial) #runebook
    elif not targetRunebook:
        if canCastRecall:
            Misc.NoOperation() #TODO: implement going to runeindex page and click the recall button
        else:
            Items.UseItem(runeBookSerial) #runebook
            Gumps.WaitForGump(89, 10000)
            Gumps.SendAction(89, homeRuneIndex) #home location
            Misc.Pause(5000)
    
    Misc.Pause( 650 )
    
    #Player.Walk("Right")
    #if Player.Name == "Shmolas":
#        if Player.Direction == "Left":
#            Player.Walk("Left")
#            Misc.Pause( 50 )
#        else:
#            Player.Walk("Left")
#            Misc.Pause( 50 )
#            Player.Walk("Left")
#            Misc.Pause( 50 )
    Player.Run("North")
    Player.Run("North")
    Player.Run("North")
    Player.Run("North")
    Player.Run("North")
    Player.Run("North")
    Player.Run("North")
    Player.Run("North")
    Player.Run("North")
    Player.Run("North")
    Player.Run("North")
    Player.Run("North")
    Player.Run("North")
    Player.Run("North")
    Player.Run("North")
    Player.Run("North")
    Player.Run("North")
    Player.Run("North")
    
    Mobiles.UseMobile( Player.Serial ) #dismount
    Misc.Pause( 650 )
    Misc.WaitForContext(petSerial, 10000)
    Misc.ContextReply(petSerial, "Open Backpack")   
    Misc.Pause( 650 )
    
#    storageBox = Items.FindBySerial( 0x40018161 )
#    Items.UseItem( storageBox )
#    Misc.Pause( 650 )
    
    #smelt ores into ingots
    for item in Player.Backpack.Contains:
        if item.ItemID == 0x19B9: #ore
            Items.UseItem(item)
            Target.WaitForTarget(5000,False)
            Target.TargetExecute(homeforgeSerial) #forge
            Misc.Pause( 500 )  
            
    pet = Mobiles.FindBySerial( petSerial )
    if not pet:
        Mobiles.UseMobile( Player.Serial ) #dismount
        Misc.Pause( 650 )
        
    for item in pet.Backpack.Contains:
        if item.ItemID == 0x19B9: #ore
            Items.UseItem(item)
            Target.WaitForTarget(5000,False)
            Target.TargetExecute(homeforgeSerial) #forge
            Misc.Pause( 500 )  
        elif item.ItemID == 0x1BF2: #ingot
            Items.Move(item.Serial,Player.Backpack,0)
            Misc.Pause( 650 )
    #move ingots manually
#    pickaxecounter = 0
#    
#    for item in Player.Backpack.Contains:
#        if item.ItemID == 0x1BF2: #ingot
#            MoveItem( Items, Misc, item, storageBox )
#            Misc.Pause( 650 )     
#        elif item.ItemID == 0x0E86:
#            pickaxecounter += 1

    #Use resource shelf for storing ingots and getting pickaxes/shovels
    Items.UseItem(resourceShelfSerial)
    Gumps.WaitForGump(111922706, 10000)
    Misc.Pause(50)
    Gumps.SendAction(111922706, 123) #fill from backpack
    Gumps.WaitForGump(111922706, 10000)
    Misc.Pause(50)
    Gumps.SendAction(111922706, 125) #next page
    Gumps.WaitForGump(111922706, 10000)
    Misc.Pause(50)
    Gumps.SendAction(111922706, 125) #next page
    Gumps.WaitForGump(111922706, 10000)
    Misc.Pause(50)
    Gumps.SendAction(111922706, 60) #get shovel
    Gumps.WaitForGump(111922706, 10000)
    Misc.Pause(50)
    Gumps.SendAction(111922706, 0) #close gump
    Misc.Pause(250)
        
    pet = Mobiles.FindBySerial( petSerial )
    Mobiles.UseMobile( pet ) #remount
    Misc.Pause( 650 )
    
    #open bank vault
    vault = Items.FindBySerial(vaultSerial)
    Items.UseItem( vault )
    Misc.Pause( 650 )
    
    #get pickaxes from bag in bank
#    if pickaxecounter < 2:
#        toolbag = Items.FindBySerial(toolbagSerial)
#        Items.UseItem( toolbag )
#        Misc.Pause( 650 )
#        tooltomove = Items.FindByID(0x0E86,-1,toolbag.Serial)
#        if tooltomove:
#            MoveItem( Items, Misc, tooltomove, Player.Backpack )
#            Misc.Pause( 650 )
#            tooltomove = Items.FindByID(0x0E86,-1,toolbag.Serial)
#            if tooltomove:
#                MoveItem( Items, Misc, tooltomove, Player.Backpack )
#                Misc.Pause( 650 )
    
    #refill recall scrolls from bank to runebook
    if not canCastRecall:
        recallscrolls = Items.FindByID(0x1F4C,-1,Player.Bank.Serial, 2)
        if recallscrolls:
            Items.Move(recallscrolls.Serial, runeBookSerial, 2)
            Misc.Pause( 650 )
    else:
        Items.UseItem(storageShelfSerial)
       # Misc.WaitForContext(storageShelfSerial, 10000)
#        Misc.ContextReply(storageShelfSerial, 3)
#        Target.WaitForTarget(10000, False)
#        Misc.Pause( 750 )
#        Target.Self()
        Misc.Pause( 750 )
        Gumps.SendAction(2834126535, 3637)
        Misc.Pause( 750 )
        Gumps.SendAction(2834126535, 0)
        Misc.Pause( 750 )
       
    #sys.exit(99) #turns script off

#while True:
for iRune in range(0,numberOfRunes):
    Player.HeadMessage(138, "recall to next spot")
    Items.UseItem(runeBookSerial)
    Misc.Pause(600)
    Gumps.WaitForGump( 89, 10000 )
    
    if canCastRecall:
        Gumps.SendAction( 89, 50 + iRune )
        
    else:
        Gumps.SendAction(89, 10 + iRune) 
    
    Misc.Pause(2500)
    
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
                
            while GetGM():
                sayTTS("%s GM Alert" % (Player.Name))
                Misc.Pause(555)
            
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
                    Misc.Pause( 500 )
                    
                    if Journal.SearchByType( 'Target cannot be seen.', 'Regular' ):
                        Journal.Clear()
                        break
                        
                    Misc.Pause( 500 ) # Wait for the mining animation to complete and then call the guards in case an elemental appears
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
    
    