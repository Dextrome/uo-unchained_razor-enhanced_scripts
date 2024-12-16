#Spellbook Crafter by SekZ 

#### IMPORTANT!! PLEASE READ INSTRUCTIONS ####
############### Instructions: ################

# Have plenty of Scribes Pens and Scrolls/Reags in a storage container.

# Specify if you want to check for fails in the settings below.

# Set the manareq in the settings below, I recommend 75 if you have it.

# Have your full spellbook in your hand.  Have a blank spellbook (or several if looping script) in your backpack.

# You can fill spellbooks in your backpack from scrolls in the storage container (useful if you have partial books or lots of duplicates)

# Click Inspect Gumps button in the top right of this window, and then confirm the buttons on your server match the lists in the make____Circle functions
# for gumpNo(the first number is always selecting the spell circle/category on left side of the inscribe menu. Each number after that is a spell in that circle) 

# Having Meditation and/or a Mana Regen suit is recommended for any server with it, but not necessary. 

# This is not set to loop.  It will make one spellbook per run unless you set it to loop. 


from System.Collections.Generic import List

global pen, gumpID, player, lisignorescroll, storeduplicates, stoCont, manareq, craftspellbook, minresources, minpens, amounttorestock, progress 



#########################
# Adjust settings below #
#########################

manareq = 60 #This is the amount of mana you will meditate to for most spell circles if your mana is lower than spell cost
storeduplicates = True #This will save extra scrolls if you already have that spell in your current spellbook
fillspellbook = False     #This will attempt to fill a spellbook with the scrolls you crafted

craftspellbooks = False #I dont play any server where this is enabled, so please set to True and adjust it as needed in checkSpellbook

minresources = 5 #When your reags or scrolls fall below this amount, it will grab the amount of each missing supply that you choose on next line
amounttorestock = 20 #You can keep this low if there is a risk you may be PKed while crafting

minpens = 2 #How many pens you want to have on you at all times. Keep at least 2 just in case one breaks, but up to you.
minrune = 1 #How many blank runes to carry (for Runebook crafting)

craft = 'fillFromContainer' #This sets the crafting mode. Options (case sensitive): fullSpellBook, grindScroll, fillFromContainer, runebook. 
                        #If you want to make one circle, just comment out the fullSpellBook circles at the bottom of script that you dont need 
                        
loopmode = False         #Set this to True if you want it to keep making spell books

placeOnVendor = False   #NOT WORKING YET -- keep it set to False, it is broken on most servers and Im looking for an easy fix
price = 7000            #NOT WORKING YET -- price to place on vendor once I have time to fix the placeOnVendor Option

#########################

if placeOnVendor == True:
    vendorBackPack = Target.PromptTarget('Select the vendor backpack')

stoCont = Target.PromptTarget('Target your Storage Container')
Items.UseItem(stoCont)
Misc.Pause(2000)

regsList = [0x0F86,0x0F7B,0x0F8C,0x0F88,0x0F7A,0x0F8D,0x0F85]#,0x0F84]

lisTupSupplies = [
('mandrakeroot', 0x0F86),
('bloodmoss', 0x0F7B),
('sulphurousash', 0x0F8C),
('nightshade', 0x0F88),
('blackpearl', 0x0F7A),
('spidersilk', 0x0F86),
('ginseng', 0x0F85),
#('garlic', 0x0F84),
('pen and ink', 0x0FBF)
]

dSupplies = dict(lisTupSupplies)


player = Mobiles.FindBySerial(Player.Serial)    

def getSupplies(reagAmount = minresources):
    needsupplies = False
    outofstock = True
    lisNeedResupply = []
    
    for i in regsList:
        if Items.BackpackCount(i,-1) < reagAmount:
            needsupplies = True
            try:
                reg = Items.FindByID(i,-1,stoCont)
                Misc.SendMessage('Taking %s' %(reg.Name))
                Misc.Pause(500)
                Items.Move(reg,Player.Backpack.Serial,amounttorestock)
                Misc.Pause(1100)
            except:
                outofstock = True
                lisNeedResupply.append(i)   
                
    if Items.BackpackCount(0x0FBF,-1) < minpens:
        needsupplies = True
        try:
            takepen = Items.FindByID(0x0FBF,-1,stoCont)
            Misc.SendMessage('Taking %s' %(takepen.Name))
            Misc.Pause(500)
            Items.Move(takepen,Player.Backpack.Serial, 1)
            Misc.Pause(1100)
        except:
            outofstock = True
            lisNeedResupply.append(i)
    
    if craft == 'runebook':
        if Items.BackpackCount(0x1F14,-1) < minrune:
            needsupplies = True
            try:
                takerune = Items.FindByID(0x1F14,-1,stoCont)
                Misc.SendMessage('Taking %s' %(takerune.Name))
                Misc.Pause(500)
                Items.Move(takerune,Player.Backpack.Serial, 1)
                Misc.Pause(1100)
            except:
                outofstock = True
                lisNeedResupply.append(i)
            
    if outofstock:
        for i in lisNeedResupply:
            lisNeededItem = []
            lisNeededItemName = [k for k, v in dSupplies.items() if v == i]

        while len(lisNeedResupply) >= 1:
            Mobiles.Message(player, 92, 'Out of supplies: %s' %(lisNeededItemName))
            Misc.Pause(500)
            iterationCount = 0
            for i in lisNeedResupply:
                try:
                    item = Items.FindByID(i, -1, stoCont)
                    Misc.Pause(500)
                    Items.Move(item,Player.Backpack.Serial,amounttorestock)
                    lisNeedResupply.remove(i)
                    Misc.Pause(1100)
                except:
                    Mobiles.Message(player, 35, 'Unable to find: %s' %(lisNeededItemName[iterationCount]))
                iterationCount += 1
            Misc.Pause(3500)
            
#            
#    if upplies:needs
#        #Misc.SendMessage('Confirming if more supplies needed')
#        getSupplies()
        
            
def checkSpellbook():
    global pen

    spellbook = Items.FindByID(0x0EFA,0x0000,Player.Backpack.Serial)
    equippedbook = Player.GetItemOnLayer('RightHand')
    if not equippedbook:
        Mobiles.Message(player,92, 'You must equip a full spellbook for this script to work, and please have an incomplete spellbook in backpack.')
        return
        
    if not spellbook and craftspellbooks:
        Misc.SendMessage('No spellbooks detected, crafting a spell book')
        #getSupplies()
        
        pen = checkPen()
        if pen:
            Items.UseItem(pen)
            
            Gumps.WaitForGump(gumpID, 1500)
            Gumps.SendAction(gumpID, 202)
            Misc.Pause(3000)
        else:
            Misc.SendMessage('Error no pens detected')
        
        spellbook = Items.FindByID(0x0EFA,0x0000,Player.Backpack.Serial)
        
    if spellbook:
        return spellbook
    else:
        Mobiles.Message(player, 35, 'No spell books found in backpack')
    
      
def checkPen():
    global pen
    
    try:
        pen = Items.FindByID(0x0FBF,-1,Player.Backpack.Serial)
        if not pen:
            Mobiles.Message(player, 35, 'No Pens Found', True)
        
    except:
        Misc.SendMessage('Error in checkPen()', 35)
        Misc.Pause(4000)

def checkMana(desiredMana):
    while Player.Mana < desiredMana:
        if not Timer.Check('SkillDelay'):
            Player.UseSkill('Meditation')
            Timer.Create('SkillDelay',11500)
        else:
            Mobiles.Message(player, 92, 'Meditating to %s mana' %(desiredMana))
            Misc.Pause(1000)
    
def makeFirstCircle(spellbook, craft = True):
    circle = 1
    manacost = 10
    checkfail = False
    
    gumpNo = [1,2,9,16,23,30,37,44,51]
    lisscrolls = [0x1F2E,0x1F2F,0x1F30,0x1F31,0x1F32,0x1F33,0x1F2D,0x1F34]
    
    if not craft:
        return lisscrolls
    else:
        makeScrolls(gumpNo, lisscrolls, circle, manacost, spellbook, checkfail)
    
def makeSecondCircle(spellbook, craft = True):
    circle = 2
    manacost = 10
    checkfail = False
    
    gumpNo = [1,58,65,72,79,86,93,100,107]
    lisscrolls = [0x1F35,0x1F36,0x1F37,0x1F38,0x1F39,0x1F3A,0x1F3B,0x1F3C]
    
    if not craft:
        return lisscrolls
    else:
        makeScrolls(gumpNo, lisscrolls, circle, manacost, spellbook, checkfail)
    
            
def makeThirdCircle(spellbook, craft = True):
    circle = 3
    manacost = 10
    checkfail = False
    
    gumpNo = [8,2,9,16,23,30,37,44,51]
    lisscrolls = [0x1F3D,0x1F3E,0x1F3F,0x1F40,0x1F41,0x1F42,0x1F43,0x1F44]
    if not craft:
        return lisscrolls
    else:
        makeScrolls(gumpNo, lisscrolls, circle, manacost, spellbook, checkfail)
            
def makeFourthCircle(spellbook, craft = True):
    circle = 4
    manacost = 11
    checkfail = False
    
    gumpNo = [8,58,65,72,79,86,93,100,107]
    lisscrolls = [0x1F45,0x1F46,0x1F47,0x1F48,0x1F49,0x1F4A,0x1F4B,0x1F4C]
    
    if not craft:
        return lisscrolls
    else:    
        makeScrolls(gumpNo, lisscrolls, circle, manacost, spellbook, checkfail)
    
def makeFifthCircle(spellbook, craft = True): 
    circle = 5
    manacost = 14
    checkfail = False
    
    gumpNo = [15,2,9,16,23,30,37,44,51]
    lisscrolls = [0x1F4D,0x1F4E,0x1F4F,0x1F50,0x1F51,0x1F52,0x1F53,0x1F54,]
    
    if not craft:
        return lisscrolls
    else:
        makeScrolls(gumpNo, lisscrolls, circle, manacost, spellbook, checkfail)

def makeSixthCircle(spellbook, craft = True):
    circle = 6
    manacost = 20
    checkfail = False
    
    gumpNo = [15,58,65,72,79,86,93,100,107]
    lisscrolls = [0x1F55,0x1F56,0x1F57,0x1F58,0x1F59,0x1F5A,0x1F5B,0x1F5C]
    
    if not craft:
        return lisscrolls
    else:
        makeScrolls(gumpNo, lisscrolls, circle, manacost, spellbook, checkfail)
            
def makeSeventhCircle(spellbook, craft = True):
    circle = 7
    manacost = 40
    checkfail = True
    
    gumpNo = [22,2,9,16,23,30,37,44,51]
    lisscrolls = [0x1F5D,0x1F5E,0x1F5F,0x1F60,0x1F61,0x1F62,0x1F63,0x1F64]
    
    if not craft:
        return lisscrolls
    else:
        makeScrolls(gumpNo, lisscrolls, circle, manacost, spellbook, checkfail)
    

def makeEighthCircle(spellbook, craft = True):
    circle = 8
    manacost = 50
    checkfail = True
    
    gumpNo = [22,58,65,72,79,86,93,100,107]
    lisscrolls = [0x1F65,0x1F66,0x1F67,0x1F68,0x1F69,0x1F6A,0x1F6B,0x1F6C]
    
    if not craft:
        return lisscrolls
    else:
        makeScrolls(gumpNo, lisscrolls, circle, manacost, spellbook, checkfail)
    
def makeScrolls(gumpNo, lisscrolls, circle, manacost, spellbook, checkfail):
    global pen
    
    for i in gumpNo:
        #Med to full if you are out of mana
        if Player.Mana < manacost:
            checkMana(Player.ManaMax)
            
        
        while True:
            #Check supplies and pens    
            #getSupplies()
            #checkPen()
            Misc.Pause(500)
            #Use pen if gump is not open and select the spell circle
            
            if not Gumps.IsValid(gumpID):
                Items.UseItem(pen)
                Gumps.WaitForGump(gumpID, 1500)
                Misc.Pause(1100)
            
            if i == gumpNo[0]:
                Misc.SendMessage('Selected spell circle')
                Gumps.SendAction(gumpID, gumpNo[0])
                Gumps.WaitForGump(gumpID, 1500)
                Misc.Pause(500)
                break
                
                
            #Craft the spell
            else:
                mana = Player.Mana
                Gumps.SendAction(gumpID, i)
                Gumps.WaitForGump(gumpID, 1500)
                Misc.Pause(350)
            
                if Player.Mana < mana and checkfail:
                    if not craft == 'runebook': moveScrolls(lisscrolls)
                    break
                elif checkfail:
                    Misc.NoOperation()
                else:
                    if not craft == 'runebook': moveScrolls(lisscrolls)
                    break
                
def moveScrolls(lisscrolls, container = Player.Backpack.Serial):
    global progress
    
    #moveScrolls to SpellBook and store any duplicates if storeduplicates = True in settings
    for i in lisscrolls:
        scroll = Items.FindByID(i,-1,container)
        if scroll and fillspellbook:
            Misc.SendMessage("Adding %s to spellbook" %(scroll.Name))
            progress += 1
            Mobiles.Message(player, 35, '%d/64 spells completed' %(progress))
            Items.Move(scroll,spellbook,1)
            Misc.Pause(1100)
            if Journal.Search('That spell is already'):
                Journal.Clear()
                if storeduplicates:
                    Misc.SendMessage('Storing %s' %(scroll.Name))
                    Items.Move(scroll,stoCont,-1)
                    Misc.Pause(750)
        elif scroll and not fillspellbook:
            Misc.SendMessage('Storing %s' %(scroll.Name))
            Items.Move(scroll,stoCont,-1)
            Misc.Pause(750)
                    
def fillFromContainer(spellbook, lisScrolls, stoContContents):
    for i in stoContContents:
        if i.ItemID in lisScrolls:
            Misc.SendMessage("Adding %s to spellbook" %(i.Name))
            Items.Move(i,spellbook,1)
            Misc.Pause(900)
            
def Initiate(): 
    global pen, gumpID, progress
    
    progress = 0 
    
    while True:
        runebook = Items.FindByID(0x0EFA, 0x0461, Player.Backpack.Serial, -1, True)
        if runebook:
            Misc.IgnoreObject(runebook)
        else:
            break
    
    #getSupplies()
    pen = Items.FindByID(0x0FBF,-1,Player.Backpack.Serial)

    if pen:
        Items.UseItem(pen)
        maxloop = 0
        while not Gumps.HasGump() and maxloop <= 3:
            Misc.Pause(1000)
            maxloop += 1
        if Gumps.HasGump():
            Mobiles.Message(player, 92, 'Inscribe gump set successfully')
            gumpID = Gumps.CurrentGump()
        else:
            Mobiles.Message(player, 92, 'No gumpID detected set to default of  949095101')
            gumpID =  949095101
    else:
        Mobiles.Message(player, 92, 'No Pens found in backpack')

while True:
    
    
    Initiate() #Ensures you have the minimum resources and fetches your gumpID (for servers where the scribe gump ID changes)
        
    if not craft == 'runebook': #Finds a spellbook in your pack to try filling, or skips it if you are making runebooks
        spellbook = checkSpellbook()
        if spellbook: 
            Items.Message(spellbook, 35, 'Filling this spellbook')
        else:
            Mobiles.Message(Player.Serial,35,"No spellbooks left",1)
        Misc.Pause(500)
        
    if craft == 'grindScroll':
        icount = 1
        
        while True:
            icount = icount + 1
            
            ## Make a recall scroll ##
            circle = 4
            manacost = 11
            checkfail = False
            
            gumpNo = [107]
            lisscrolls = [0x1F4C]
            makeScrolls(gumpNo, lisscrolls, circle, manacost, spellbook, checkfail)
                
            ## Gate Scroll ##
#            circle = 7
#            manacost = 40
#            checkfail = True
#            
#            gumpNo = [23]
#            lisscrolls = [0x1F60]
#            makeScrolls(gumpNo, lisscrolls, circle, manacost, spellbook, checkfail)
                
            if icount >= 20:
                moveScrolls(lisscrolls)
                icount = 1

    if craft == 'fullSpellBook': 
        Restock.ChangeList('inscription')
        Misc.Pause( 250 )
        Restock.FStart()
        Misc.Pause( 1200 )
        Restock.FStop()
        Misc.Pause( 250 )
        makeFirstCircle(spellbook) #Comment out any of these functions to skip a spell circle
        makeSecondCircle(spellbook)
        makeThirdCircle(spellbook)
        makeFourthCircle(spellbook)
        makeFifthCircle(spellbook)
        makeSixthCircle(spellbook)
        makeSeventhCircle(spellbook)
        makeEighthCircle(spellbook)
        
    elif craft == 'fillFromContainer': #This mode will fill spellbooks from the scrolls sitting in your storage container
        stoContItem = Items.FindBySerial(stoCont)
        stoContContents = stoContItem.Contains
        lisScrolls = makeFirstCircle(spellbook, False)
        fillFromContainer(spellbook, lisScrolls,stoContContents)
        lisScrolls = makeSecondCircle(spellbook, False)
        fillFromContainer(spellbook, lisScrolls,stoContContents)
        lisScrolls = makeThirdCircle(spellbook, False)
        fillFromContainer(spellbook, lisScrolls,stoContContents)
        lisScrolls = makeFourthCircle(spellbook, False)
        fillFromContainer(spellbook, lisScrolls,stoContContents)
        lisScrolls = makeFifthCircle(spellbook, False)
        fillFromContainer(spellbook, lisScrolls,stoContContents)
        lisScrolls = makeSixthCircle(spellbook, False)
        fillFromContainer(spellbook, lisScrolls,stoContContents)
        lisScrolls = makeSeventhCircle(spellbook, False)
        fillFromContainer(spellbook, lisScrolls,stoContContents)
        lisScrolls = makeEighthCircle(spellbook, False)
        fillFromContainer(spellbook, lisScrolls,stoContContents)
        
    if craft == 'runebook':
        lisTupSupplies.append(('blank rune', 0x1F14))
        if minresources < 8: minresources = 8 #Number of scrolls required to make a rune book
        
        ## Make a recall scroll ##  
        gumpNo = [22,51]
        makeScrolls(gumpNo, [], 4, 11, False, False)#Doesn't check for craft failure
        
        ## Make a gate scroll ##
        gumpNo = [43,23]
        makeScrolls(gumpNo, [], 7, 40, False, True) #Checks for craft failure
        
        ## Make runebook ##
        gumpNo = [57,2]
        makeScrolls(gumpNo, [], 1, 0, False, False)#Doesn't check for craft failure
        Misc.Pause(650)
        
    if craft == 'runebook':
        spellbook = Items.FindByID(0x0EFA, 0x0461, Player.Backpack.Serial, -1, True)

    if placeOnVendor:
        Misc.Pause(650)
        Items.Move(spellbook,vendorBackPack,1,0,0)
        Misc.Pause(2400)
        Player.ChatSay(1, price)
    else:
        try:
            Items.Move(spellbook,stoCont,0)  
        except:
            Mobiles.Message(player, 35, 'No spellbook or runebook found in backpack')

    if not loopmode: break
    
    Misc.Pause(900)

    
    