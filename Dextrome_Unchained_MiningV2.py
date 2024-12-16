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
from operator import length_hint
from os.path import exists
from os import makedirs
import pickle

#miningModes: "Normal" or "GuildTreasury"
storageShelfSerial = 0x4002D26E
#Character Specific Config
if Player.Name == "Generic Player":
    miningMode = "GuildTreasury"
    vaultSerial = 0x4028C99B
    petSerial = 0x00018E40 #fire beetle
    pet = Mobiles.FindBySerial( petSerial )
    firebeetleSerial = 0x00018E40
    runeBookSerial = 0x40014E65
    targetRunebook = True
    canCastRecall = True
    #toolbagSerial = 0x4046965F #can be a container in your bank(vault) or just a container within range 
    numberOfRunes = 6
    summonPetContextReply = 4
    shieldSerial = 0x401607D2
if Player.Name == "DXM":
    miningMode = "GuildTreasury"
    vaultSerial = 0x4028C99B
    #petSerial = 0x0001E8A9 #regular beetle
    petSerial = 0x00001CE2 #fire beetle
    pet = Mobiles.FindBySerial( petSerial )
    firebeetleSerial = 0x00001CE2
    runeBookSerial = 0x4034E9C4
    targetRunebook = True
    canCastRecall = True
    #toolbagSerial = 0x4046965F #can be a container in your bank(vault) or just a container within range 
    numberOfRunes = 7
    summonPetContextReply = 5
    shieldSerial = 0x4008E8AA
elif Player.Name == "Phill Myke Hunt":
    miningMode = "Normal"
    vaultSerial = 0x4028C99B
    petSerial = 0x0000DFE5 #Blood Beetle
    #petSerial = 0x00004B80 #Fire Beetle
    pet = Mobiles.FindBySerial( petSerial )
    firebeetleSerial = 0x00004B80
    runeBookSerial = 0x401444C6
    targetRunebook = True
    canCastRecall = True
    #toolbagSerial = 0x400CBA40 #can be a container in your bank(vault) or just a container within range
    numberOfRunes = 7
    summonPetContextReply = 4
    shieldSerial = 0x400E85D8

#Other Config
miningAttemptsSinceLastCaptcha = 0
totalHarvestCount = 0
totalDoubleHarvestCount = 0
resourceShelfSerial = 0x402DD22C
homeforgeSerial = 0x4002B6CE
captchaGumpId = 1565867016
checkForAnyGump = True
oreLandIDs = [0x00F1, 0x00F2, 0x00F3, 0x00F0, 0x023A, 0x0232]
oreStaticIDs = [0x053B, 0x053C, 0x053D, 0x053E, 0x053F]
forgesList = [0x197A, 0x197E, 0x19A2, 0x1982, 0x1992, 0x1996, 0x199A, 0x0FB1]
ScanZone = 24
global miningTool

##types lists
forgesList = List[int]((0x197A, 0x197E, 0x19A2, 0x1982, 0x1992, 0x1996, 0x199A, 0x0FB1))
tinkerTools = [0x1EB8, 0x1EBC]
minerTools = [0x0F39, 0x0E86]
miningToolID = 0x0F39 #=Shovel / 0x0E86=Pickaxe

#tts
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
    
#    for enemy in enemyList:
#        if not enemy.Name.Contains('Animal Trainer') and not enemy.Name.Contains('Animal Trainer'):
#            gm = enemy
#            
    gm = Mobiles.Select(enemyList, 'Nearest')
    return gm
    
    
def ScanLandForOre( ): 
    global oreposcoords
    Misc.SendMessage("--> Scanning Tiles in ScanZone", 77)
    minx = Player.Position.X - ScanZone - 4
    maxx = Player.Position.X + ScanZone + 4
    miny = Player.Position.Y - ScanZone
    maxy = Player.Position.Y + ScanZone + 12
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
                            
                            addToList = True
                            
                            for coord in tmporeposcoords:
                                if ((coord[0] == minx  and (coord[1] == miny or coord[1] == miny - 1 or coord[1] == miny + 1 )) or
                                    (coord[0] == minx + 1 and (coord[1] == miny or coord[1] == miny - 1 or coord[1] == miny + 1 )) or
                                    (coord[0] == minx - 1 and (coord[1] == miny or coord[1] == miny - 1 or coord[1] == miny + 1 ))):
                                        addToList = False
                            
                            if addToList:
                                tmporeposcoords.Add([minx,miny,tileZ])
                            
            else:
                Misc.NoOperation()
                
            minx = minx + 1
        minx = Player.Position.X - ScanZone            
        miny = miny + 1
    
    oreposcoords = sorted(tmporeposcoords , key=lambda k: [k[1], k[0], k[2]])
    
    Misc.SendMessage(oreposcoords.Count)
    
    
def MoveToOre(i):
    if abs(Player.Position.X - oreposcoords [i][0]) > 7 or abs(Player.Position.Y - oreposcoords [i][1]) > 7:
        if Player.Mount == None:
            pet = Mobiles.FindBySerial( petSerial )
            if pet:
                Mobiles.UseMobile( pet ) #remount
                Misc.Pause( 600 )
    
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
        Player.HeadMessage( colors[ 'red' ], 'Could not find pet!' )

    if miningMode == "Normal":
        Mobiles.UseMobile( Player.Serial ) #dismount
        Misc.Pause( 650 )
        Misc.WaitForContext(pet, 10000)
        Misc.ContextReply(pet, "Open Backpack")   
        Misc.Pause( 650 )
    
    for item in Player.Backpack.Contains:
        if item.ItemID == 0x19B9: #ore  
            Journal.Clear()
            Misc.Pause(200)
            
            if firebeetleSerial:
                Items.UseItem(item)
                Target.WaitForTarget(5000,False)
                Target.TargetExecute(firebeetleSerial) #firebeetle
                Misc.Pause( 500 )  
            else:
                Misc.SendMessage('Moving %s to %s' % (item.Name, pet.Name))
                Items.Move(item.Serial,Mobiles.FindBySerial( petSerial ).Backpack,0)
                Misc.Pause( 650 )
        elif item.ItemID == 0x1779: #stone
            Misc.SendMessage('Moving %s to %s' % (item.Name, pet.Name))
            Items.Move(item.Serial,Mobiles.FindBySerial( petSerial ).Backpack,0)
            Misc.Pause( 650 )
            
    if miningMode == "GuildTreasury":            
    #if Player.Name == "DXM": #add everything except valorite ingots to guild treasury
        #Player.ChatSay("guild") #Open Guild Treasure/Buff Gump
        Player.GuildButton()
        Gumps.WaitForGump(516474935, 2500)
        Misc.Pause(120)
        Gumps.SendAction(516474935, 15)
        Gumps.WaitForGump(1478311224, 2500)
        Misc.Pause(120)
        
        for item in Player.Backpack.Contains:
#            if not Gumps.HasGump(1478311224): 
#                Misc.SendMessage("no guild treasury gump found")
#            else:
#                Misc.SendMessage("guild treasury gump found")
            if item.ItemID == 0x1BF2 and not item.Hue == 0x08ab and not item.Hue == 0x0000 and not item.Hue == 0x0973:
                Misc.SendMessage('Moving %s to Guild Treasury' % (item.Name))
                Gumps.SendAction(1478311224, 100) #add to guild buff treasury 
                Target.WaitForTarget(2500, False)
                Misc.Pause(50)
                Target.TargetExecute(item)
                Misc.Pause(100)
    else:
    #if Player.Name == "Phill Myke Hunt": 
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
    
    #smelt ores into ingots
    for item in Player.Backpack.Contains:
        if item.ItemID == 0x19B9: #ore
            Items.UseItem(item)
            Target.WaitForTarget(5000,False)
            Target.TargetExecute(homeforgeSerial) #forge
            Misc.Pause( 500 )  
        elif item.ItemID == 0x1779: #stone
            Items.Move(item.Serial,0x403C0EAC,0)
            Misc.Pause( 650 )
    
    if miningMode == "Normal":        
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
            elif item.ItemID == 0x1779: #stone
                Items.Move(item.Serial,0x403C0EAC,0)
                Misc.Pause( 650 )

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
        Misc.Pause( 750 )
        Gumps.SendAction(2834126535, 3662)
        Misc.Pause( 750 )
        Gumps.SendAction(2834126535, 0)
        Misc.Pause( 750 )
    #sys.exit(99) #turns script off
    
    
def Mine():
    global oreposcoords
    global miningAttemptsSinceLastCaptcha
    global totalHarvestCount
    global totalDoubleHarvestCount
    skipPreAlert = False
    oreposcoords = []
    ScanLandForOre()
    i = 0
    wentHome = False
    
    Misc.SendMessage("---")
    Misc.SendMessage(oreposcoords.Count)
    Player.ChatSay("all guard")

    while i < oreposcoords.Count and wentHome == False:
        SaveVariables()
        
        if Player.WarMode:
                Misc.SendMessage("exiting script",30)
                break
                
        pet = Mobiles.FindBySerial( petSerial )
        if pet == None and Player.Mount == None:
            Player.HeadMessage( colors[ 'red' ], 'Summoning pet!' )
            Misc.WaitForContext(Player.Serial, 2500)
            Misc.ContextReply(Player.Serial, 5)
            
        #Misc.SendMessage('Target = X: %i - Y: %i - Z: %i' % (oreposcoords[i][0], oreposcoords[i][1], oreposcoords[i][2]), 66)
        MoveToOre(i)
        
        if Player.Mount != None:
            Mobiles.UseMobile( Player.Serial ) #dismount
            Misc.Pause( 600 )
            #Misc.UseContextMenu(petSerial,"Command: Guard",1000)
            Player.ChatSay("all guard")
            
        Journal.Clear()
        miningTool = Items.FindByID(miningToolID, -1, Player.Backpack.Serial)
        
        #count ore to track double harvest
        ores = Items.FindAllByID(0x19B9,-1,Player.Backpack.Serial,-1,False)
        countIronOreBefore = 0
        
        if len(ores):
            for ore in ores:
                countIronOreBefore += ore.Amount
            
        #Mine
        while ( not Journal.SearchByName( 'There is no metal here to mine.', 'System' ) and
                not Journal.SearchByName( 'Target cannot be seen.', 'System' ) and
                not Journal.SearchByName( 'You can\'t mine there.', 'System' ) and 
                not Journal.SearchByName( 'That is too far away.', 'System' ) and 
                not Journal.SearchByName( 'You have worn out your tool!', 'System' ) ):
                
            if Player.WarMode:
                Misc.SendMessage("exiting script",30)
                break
                
            if miningAttemptsSinceLastCaptcha > 496 and skipPreAlert == False:
                sayTTS("Incoming Captcha for %s" % (Player.Name))
                Misc.SendMessage('Mining Script Paused')
                Target.PromptTarget('Target Anything')
                skipPreAlert = True
                
            while Gumps.HasGump(captchaGumpId):
                sayTTS("%s Captcha Alert" % (Player.Name))
                Misc.SendMessage("%s Mining actions since last Captcha alert" % (miningAttemptsSinceLastCaptcha),25)
                miningAttemptsSinceLastCaptcha = 0
                Misc.Pause(1500)
                skipPreAlert = False
                
            while GetGM():
                sayTTS("%s GM Alert" % (Player.Name))
                Misc.Pause(999)
                
            #display harvest stats
            if miningAttemptsSinceLastCaptcha > 0 and miningAttemptsSinceLastCaptcha % 100 == 0:
                Misc.SendMessage('>> Total Harvest: %i' % (totalHarvestCount+totalDoubleHarvestCount), 10)
                Misc.SendMessage('>> Total Double Harvest: %i' % (totalDoubleHarvestCount), 10)
                Misc.SendMessage('>>> Double Harvest Rate: %i%%' % ((totalDoubleHarvestCount/(totalHarvestCount+totalDoubleHarvestCount))*100), 11)
            
            #check for double harvest
            ores = Items.FindAllByID(0x19B9,-1,Player.Backpack.Serial,-1,False)
            countIronOreAfter = 0
            
            if len(ores):
                for ore in ores:
                    countIronOreAfter += ore.Amount
            
            if countIronOreAfter > countIronOreBefore + 1:
                Misc.SendMessage('> Double Harvest!', 11)
                totalDoubleHarvestCount += 1
            elif countIronOreAfter == countIronOreBefore + 1:
                totalHarvestCount += 1
            
            ores = Items.FindAllByID(0x19B9,-1,Player.Backpack.Serial,-1,False)
            countIronOreBefore = 0
            
            if len(ores):
                for ore in ores:
                    countIronOreBefore += ore.Amount
            
            if Player.Weight <= Player.MaxWeight - 20:
                #Player.HeadMessage(99,"mining")
#                iteminhand = Player.GetItemOnLayer("RightHand")
#                if not iteminhand: 
#                    pickaxe = Items.FindByID(miningToolID, -1, Player.Backpack.Serial)
#                else:
#                    pickaxe = iteminhand
                miningTool = Items.FindByID(miningToolID, -1, Player.Backpack.Serial)
                    
                if miningTool:
                    Items.UseItem(miningTool)
                    Target.WaitForTarget(2500,False)
                    tileinfo = Statics.GetStaticsTileInfo(oreposcoords[i][0], oreposcoords[i][1], Player.Map)
                    Target.TargetExecute(oreposcoords[i][0], oreposcoords[i][1], oreposcoords[i][2])
                    miningAttemptsSinceLastCaptcha += 1
                    Misc.SendMessage('Actions: %i' % (miningAttemptsSinceLastCaptcha), 20)
                    Misc.Pause( 2000 ) # Wait for the mining animation to complete   
                else:
                    GoHome()
                    wentHome = True
                    break
            else:
                Player.HeadMessage(99,"overweight")
                Player.ChatSay("all follow me")
                Misc.Pause(500)
                MoveOreToPet()
                Player.ChatSay("all guard")
                
                if Journal.Search("You are overloaded") or Player.Weight >= Player.MaxWeight - 100:
                    Misc.SendMessage('Overloaded time to go home')
                    
                    if miningMode == "Normal":
                        GoHome()
                        
                    wentHome = True
                    break
                
        i+=1
        Player.ChatSay("all follow me")

        
def InitializeStart():
    global miningAttemptsSinceLastCaptcha
    global totalHarvestCount
    global totalDoubleHarvestCount
    Misc.SendMessage("Loading variables")
    save_folder = Misc.ScriptDirectory() + "\\saved-variables\\"
    save_file = save_folder + Player.Name + "_PersistentVariables.pickle"
    save_file_exists = exists(save_file)

    if not exists(save_folder):
        makedirs(save_folder)
        
    if save_file_exists:
        Misc.SendMessage("Save File Found")
        
        with open(save_file, 'rb') as f2 :
            save_data = pickle.load(f2)
            
        miningAttemptsSinceLastCaptcha = save_data['MiningActionsSinceLastCaptcha']   
        totalHarvestCount = save_data['totalHarvestCount']
        totalDoubleHarvestCount = save_data['totalDoubleHarvestCount']
        Misc.SendMessage("Loaded miningAttemptsSinceLastCaptcha:" + miningAttemptsSinceLastCaptcha.ToString())
        Misc.SendMessage("Loaded totalHarvestCount:" + totalHarvestCount.ToString())
        Misc.SendMessage("Loaded totalDoubleHarvestCount:" + totalDoubleHarvestCount.ToString())
    else:
        Misc.SendMessage("No Save File Found")
        miningAttemptsSinceLastCaptcha = 0
    
    
def InitializeExit():
    global miningAttemptsSinceLastCaptcha
    global totalHarvestCount
    global totalDoubleHarvestCount
    SaveVariables()

def SaveVariables():
    global miningAttemptsSinceLastCaptcha
    global totalHarvestCount
    global totalDoubleHarvestCount
    Misc.SendMessage("Saving variables")
    save_folder = Misc.ScriptDirectory() + "\\saved-variables\\"
    save_file = save_folder + Player.Name + "_PersistentVariables.pickle"
    save_file_exists = exists(save_file)

    if not exists(save_folder):
        makedirs(save_folder)
        
    save_data = { 'MiningActionsSinceLastCaptcha': miningAttemptsSinceLastCaptcha, 'totalHarvestCount': totalHarvestCount, 'totalDoubleHarvestCount': totalDoubleHarvestCount}
    with open(save_file, 'wb') as f1:        
        pickle.dump(save_data, f1)    
        
    
            
InitializeStart()

try: 
    for iRune in range(0,numberOfRunes):
        #Recall To Next Spot
        Player.HeadMessage(138, "recall to next spot")
        Items.UseItem(runeBookSerial)
        Misc.Pause(800)
        Gumps.WaitForGump( 89, 10000 )
        
        if canCastRecall:
            Gumps.SendAction( 89, 50 + iRune )
        else:
            Gumps.SendAction(89, 10 + iRune) 
        
        Misc.Pause(4000)
        
        #Equip Shield
        if not shieldSerial == None: 
            Player.EquipItem(shieldSerial)
            Misc.Pause(600)
            
        Mine()
                
        #Go home to resupply if low on regs        
        if Items.FindByID(0x0F86,-1,Player.Backpack.Serial,-1,False).Amount <= 2:
            GoHome()
            
        if Player.WarMode:
                Misc.SendMessage("exiting script",30)
                break
except Exception:
        print('Error!')

InitializeExit()     
GoHome()