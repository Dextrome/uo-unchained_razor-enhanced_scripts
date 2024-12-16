import sys
from System.Collections.Generic import List
from Scripts.utilities.items import MoveItem
from Scripts import config
import clr
clr.AddReference('System.Speech')
from System.Speech.Synthesis import SpeechSynthesizer

###CONFIG
beetle = 0x0000DFE5
homeRuneSerial = 0x401444C6
vaultSerial = 0x4028C99B
####


spk = SpeechSynthesizer()
tileinfo = List[Statics.TileInfo]
treeposx = []
treeposy = []
treeposz = []
treegfx = []
treenumber = 0
toolid = 0x0F43 #set chopping tool graphic id defaulted as hatchet
maxweight = 375
TreeStaticID = [3221, 3222, 3225, 3227, 3228, 3229, 3210, 3238, 3240, 3242, 3243, 3267, 3268, 3272, 3273, 3274, 3275, 3276, 3277, 3280, 3283, 3286, 3288, 3290, 3293, 3296, 3299, 3302, 3320, 3323, 3326, 3329, 3365, 3367, 3381, 3383, 3384, 3394, 3395, 3417, 3440, 3461, 3476, 3478, 3480, 3482, 3484, 3486, 3488, 3490, 3492, 3496]
RaggioScansione = 18
boardID = 0x1BD7


compendium = 0x4007AC82
captchaGumpId = 1565867016
checkForAnyGump = True
resourceShelfSerial = 0x402DD22C
harvestAttemptsSinceLastCaptcha = 0

def sayTTS(text):
    spk.Speak(text)


def ScanStatic( ): 
    global treenumber
    Misc.SendMessage("--> Inizio Scansione Tile", 77)
    minx = Player.Position.X - RaggioScansione
    maxx = Player.Position.X + RaggioScansione
    miny = Player.Position.Y - RaggioScansione
    maxy = Player.Position.Y + RaggioScansione

    while miny <= maxy:
        while minx <= maxx:
            tileinfo = Statics.GetStaticsTileInfo(minx, miny, Player.Map)
            if tileinfo.Count > 0:
                for tile in tileinfo:
                    for staticid in TreeStaticID:
                        if staticid == tile.StaticID:
                            Misc.SendMessage('--> Albero X: %i - Y: %i - Z: %i' % (minx, miny, tile.StaticZ), 66)
                            treeposx.Add(minx)
                            treeposy.Add(miny)
                            treeposz.Add(tile.StaticZ)
                            treegfx.Add(tile.StaticID)
            else:
                Misc.NoOperation()
            minx = minx + 1
        minx = Player.Position.X - RaggioScansione            
        miny = miny + 1
    treenumber = treeposx.Count    
    Misc.SendMessage('--> Totale Alberi: %i' % (treenumber), 77)
#
#while not Player.IsGhost:    
#    Player.HeadMessage(90, "PathFinding")
#    
#    PathFinding.PathFindTo(975,1608,0)
#    PathFinding.PathFindTo(965,1604,0)
#    PathFinding.PathFindTo(973,1596,0)


def MoveToTree(i):
    staticOnTile = False
    tileinfo = Statics.GetStaticsTileInfo(treeposx[i], treeposy[i]-1, Player.Map)
    if tileinfo.Count > 0:
        for tile in tileinfo:
            if tile.StaticID != 0x0000:
                staticOnTile = True
                    
    if staticOnTile == True:
        staticOnTile = False
        tileinfo = Statics.GetStaticsTileInfo(treeposx[i], treeposy[i]+1, Player.Map)
        if tileinfo.Count > 0:
            for tile in tileinfo:
                if tile.StaticID != 0x0000:
                    staticOnTile = True
                    
        if staticOnTile == True:
            staticOnTile = False
            tileinfo = Statics.GetStaticsTileInfo(treeposx[i]-1, treeposy[i]-1, Player.Map)
            if tileinfo.Count > 0:
                for tile in tileinfo:
                    if tile.StaticID != 0x0000:
                        staticOnTile = True
                        
            if staticOnTile == True:
                staticOnTile = False
                tileinfo = Statics.GetStaticsTileInfo(treeposx[i]+1, treeposy[i]-1, Player.Map)
                if tileinfo.Count > 0:
                    for tile in tileinfo:
                        if tile.StaticID != 0x0000:
                            staticOnTile = True
                            
                if staticOnTile == True:
                    #staticOnTile = False
#                    tileinfo = Statics.GetStaticsTileInfo(treeposx[i]-1, treeposy[i]-1, Player.Map)
#                    if tileinfo.Count > 0:
#                        for tile in tileinfo:
#                            if tile.StaticID != 0x0000:
#                                staticOnTile = True
                    PathFinding.PathFindTo(treeposx[i]+1, treeposy[i]+1, treeposz[i])  
                else:
                    PathFinding.PathFindTo(treeposx[i]+1, treeposy[i]-1, treeposz[i])       
            else:
                PathFinding.PathFindTo(treeposx[i]-1, treeposy[i]-1, treeposz[i])
        else:
            PathFinding.PathFindTo(treeposx[i], treeposy[i]+1, treeposz[i])
    else:
        PathFinding.PathFindTo(treeposx[i], treeposy[i]-1, treeposz[i])
        
       
def MoveBoardsToBeetle():
    Mobiles.UseMobile( Player.Serial ) #dismount
    Misc.Pause( 650 )
    Misc.WaitForContext(beetle, 10000)
    Misc.ContextReply(beetle, "Open Backpack")   
    Misc.Pause( 650 )
    
    for item in Player.Backpack.Contains:
        if item.ItemID == boardID:
            MoveItem( Items, Misc, item, Mobiles.FindBySerial( beetle ).Backpack )
            Misc.Pause( 650 )
            
    Mobiles.UseMobile( beetle ) #remount
    Misc.Pause( 650 )
        
    if Player.Weight >= maxweight: 
        for item in Player.Backpack.Contains:
            if item.ItemID == 0x1BDD: #log
                Items.UseItem(hatchet) #use hatchet
                Target.WaitForTarget(2500,False) #wait for the target to appear on screen.
                Target.TargetExecute(item)
                Misc.Pause(750)
        sys.exit(99)
       
        


while not Player.IsGhost:
    ScanStatic()
    i = 0
    
    while i < treenumber:
        MoveToTree(i)
        Misc.Pause(500) 
        Journal.Clear() #Make sure journal is not reading ahead of when this started.
        woodFound = True
        
        while woodFound:
            Journal.Clear() #clear message as to not get confused.
            Player.HeadMessage(67, "Start Chopping Wood")
            #hatchet = Items.FindByID(toolid, -1, Player.Backpack.Serial) #find hatchet in pack.
            hatchet = Items.FindByID(toolid, -1, -1)
            if hatchet: #if hatchet exists
                Items.UseItem(hatchet) #use hatchet
                Target.WaitForTarget(2500,False) #wait for the target to appear on screen.
                harvestAttemptsSinceLastCaptcha += 1
                tiles = Statics.GetStaticsTileInfo(treeposx[i], treeposy[i], Player.Map) #read map files to find target as static
                if len(tiles) != 0 and tiles[0].StaticID != 0: #if tile is not id 0
                    Target.TargetExecute(treeposx[i], treeposy[i], tiles[0].StaticZ, tiles[0].StaticID) #target tile
                    Misc.Pause(1000)#pause
                    if Journal.Search("That is too far away.") == True: #if string is read in journal
                        Player.HeadMessage(1100, "Too Far Away")
                        break #go to next location
                    if Player.Weight >= maxweight: 
                        Player.HeadMessage(1100, "Overweight!") 
                        MoveBoardsToBeetle()
                    Misc.Pause(1000) #pause
                else: #if tile does not exist
                    Target.Cancel() #cancel target
                    sys.exit(99) #turns script off
            else: #if hatchet does not exist
                Player.HeadMessage(90, "No Hatchet")
                sys.exit(99) #turns script off
            
            captchaCheck = True
            countWaitTime = 0
            
            while captchaCheck:
                Misc.Pause(666)
                countWaitTime += 666
                if Journal.Search("There's not enough wood here to harvest.") == True or Journal.Search("You can't use an axe on that.") == True:
                       
                    Player.HeadMessage(90, ">>> TREE IS DONE <<<")
                    Misc.Pause(666)  
                    for item in Player.Backpack.Contains:
                        if item.ItemID == 0x1BDD: #log
                            Items.UseItem(hatchet) #use hatchet
                            Target.WaitForTarget(2500,False) #wait for the target to appear on screen.
                            Target.TargetExecute(item)
                            Misc.Pause(2000)
                    
                    woodFound = False
                    captchaCheck = False
                elif Journal.Search("You chop some") == True or Journal.Search("You hack at the tree for a while") or Journal.Search("You must wait to perform another action") == True:
                    Misc.Pause(250)
                    captchaCheck = False
                else:
                    Player.HeadMessage(90, "WAITING")
                    
                    if (Gumps.CurrentGump() != 0 and checkForAnyGump) or Gumps.CurrentGump() == captchaGumpId:
                        Misc.SendMessage("%s Mining Attempt Since Last Captcha" % (harvestAttemptsSinceLastCaptcha))
                        sayTTS("%s Captcha Alert" % (Player.Name))
                        harvestAttemptsSinceLastCaptcha = 0
                    if countWaitTime > 5000:
                        if Gumps.CurrentGump() == 0:
                            captchaCheck = False
        
        i = i + 1
        
    treeposx = []
    treeposy = []
    treeposz = []
    treegfx = []
    treenumber = 0    