#AlchBot v1.0 by Monero
#Requirements: Have a container with reagents and bottles and mortar and pestles.
#You can set your 3 continers as the same one if youd like.  Otherwise you can choose 3 separate containers.
#Containers are: Reagent/Bottle Restock, Output container (For finished potions), Tools Container (Mortal and Pestles)
#restocks all reagents no matter what, you need to have all in stock and restock all 8 to your backpack.
#This only makes greater potions, some regular poison, and deadly poison, so you can sell what you make or use it.

mode = 'train' #[train,heal,cure,refresh,str,dex,explode,invis,resist] #only mode right now is train [future updates on Patreon]
regsList = [0x0F86,0x0F7B,0x0F8C,0x0F88,0x0F7A,0x0F8D,0x0F85,0x0F84,0x0F0E] #plus bottles
potsList = [0x0F0B,0x0F0A,0x0F08,0x0F09,0x0F07,0x0F0C,0x0F0A,0x0F0D]
toolsList = [0x0E9B]  #only mortar n pestle
pestle = 0x0E9B
emptybot = 0x0F0E
regAmount = 15#(How many minimum reagents to have)
toolsAmount = 1
regsamounttorestock = 45#(How many to restock)
toolsamounttorestock = 1#(How many to restock)
pottype = '' #this will be set and called for each level of skill
pottomake = '' #this will be set and called for each level of skill
delay = 1250 #(Wait after attempting to make a potion)
stoCont = Target.PromptTarget('Target your Reagent and Empty Bottle Restock Container')
outCont = Target.PromptTarget('Target your Output Container')
toolsCont = Target.PromptTarget('Target your tools [mortal and pestles] Container [if its different]')

def refreshPots():
    pottype = 1 #Current pot type heal/restore
    pottomake = 9 #Current pot to make greater refreshment
    Items.UseItemByID(pestle,0)
    Gumps.WaitForGump(949095101, 10000)
    Gumps.SendAction(949095101, pottype)
    Gumps.WaitForGump(949095101, 10000)
    Gumps.SendAction(949095101, pottomake)
    Misc.Pause(delay)
    
def strPots():
    pottype = 8 #Current pot type enhancement
    pottomake = 30 #Current pot to make greater strength
    Items.UseItemByID(pestle,0)
    Gumps.WaitForGump(949095101, 10000)
    Gumps.SendAction(949095101, pottype)
    Gumps.WaitForGump(949095101, 10000)
    Gumps.SendAction(949095101, pottomake)
    Misc.Pause(delay)

def dexPots():
    pottype = 8 #Current pot type enhancement
    pottomake = 9 #Current pot to make greater agility
    Items.UseItemByID(pestle,0)
    Gumps.WaitForGump(949095101, 10000)
    Gumps.SendAction(949095101, pottype)
    Gumps.WaitForGump(949095101, 10000)
    Gumps.SendAction(949095101, pottomake)
    Misc.Pause(delay)
    
def explodePots():
    pottype = 22 #Current pot type explosive
    pottomake = 16 #Current pot to make greater explosion
    Items.UseItemByID(pestle,0)
    Gumps.WaitForGump(949095101, 10000)
    Gumps.SendAction(949095101, pottype)
    Gumps.WaitForGump(949095101, 10000)
    Gumps.SendAction(949095101, pottomake)
    Misc.Pause(delay)

def healPots():
    pottype = 1 #Current pot type healing and curative
    pottomake = 30 #Current pot to make greater heal
    Items.UseItemByID(pestle,0)
    Gumps.WaitForGump(949095101, 10000)
    Gumps.SendAction(949095101, pottype)
    Gumps.WaitForGump(949095101, 10000)
    Gumps.SendAction(949095101, pottomake)
    Misc.Pause(delay)
    
def curePots():
    pottype = 1 #Current pot type healing and curative
    pottomake = 51 #Current pot to make greater cure
    Items.UseItemByID(pestle,0)
    Gumps.WaitForGump(949095101, 10000)
    Gumps.SendAction(949095101, pottype)
    Gumps.WaitForGump(949095101, 10000)
    Gumps.SendAction(949095101, pottomake)
    Misc.Pause(delay)
    
def trainAlchemy():
    #This mode trains Alchemy from 42-100  
    if Player.GetRealSkillValue('Alchemy') > 99.9:
        Player.ChatSay(45,'[e yea')
        Player.ChatSay(45,'GM Alchemy')
        Misc.Pause(10000)

    if Player.GetSkillValue('Alchemy') > 97.9:
        if Player.GetSkillValue('Alchemy') < 100:
            Misc.SendMessage('Making Deadly Poison')
            pottype = 15 #Current pot type toxic
            pottomake = 23 #Current pot to make deadly poison
            Items.UseItemByID(pestle,0)
            Gumps.WaitForGump(949095101, 10000)
            Gumps.SendAction(949095101, pottype)
            Gumps.WaitForGump(949095101, 10000)
            Gumps.SendAction(949095101, pottomake)
            Misc.Pause(delay)

    if Player.GetSkillValue('Alchemy') > 94.9:
        if Player.GetSkillValue('Alchemy') < 98:
            pottype = 1 #Current pot type healing and curative
            pottomake = 51 #Current pot to make greater cure
            Items.UseItemByID(pestle,0)
            Gumps.WaitForGump(949095101, 10000)
            Gumps.SendAction(949095101, pottype)
            Gumps.WaitForGump(949095101, 10000)
            Gumps.SendAction(949095101, pottomake)
            Misc.Pause(delay)

    if Player.GetSkillValue('Alchemy') > 86.9:
        if Player.GetSkillValue('Alchemy') < 95:
            pottype = 1 #Current pot type healing and curative
            pottomake = 30 #Current pot to make greater heal
            Items.UseItemByID(pestle,0)
            Gumps.WaitForGump(949095101, 10000)
            Gumps.SendAction(949095101, pottype)
            Gumps.WaitForGump(949095101, 10000)
            Gumps.SendAction(949095101, pottomake)
            Misc.Pause(delay)

    if Player.GetSkillValue('Alchemy') > 79.9:
        if Player.GetSkillValue('Alchemy') < 87:
            pottype = 8 #Current pot type enhancement
            pottomake = 30 #Current pot to make greater strength
            Items.UseItemByID(pestle,0)
            Gumps.WaitForGump(949095101, 10000)
            Gumps.SendAction(949095101, pottype)
            Gumps.WaitForGump(949095101, 10000)
            Gumps.SendAction(949095101, pottomake)
            Misc.Pause(delay)

    if Player.GetSkillValue('Alchemy') > 66.9:
        if Player.GetSkillValue('Alchemy') < 80:
            pottype = 8 #Current pot type enhancement
            pottomake = 9 #Current pot to make greater agility
            Items.UseItemByID(pestle,0)
            Gumps.WaitForGump(949095101, 10000)
            Gumps.SendAction(949095101, pottype)
            Gumps.WaitForGump(949095101, 10000)
            Gumps.SendAction(949095101, pottomake)
            Misc.Pause(delay)

    if Player.GetRealSkillValue('Alchemy') > 59.9:
        if Player.GetRealSkillValue('Alchemy') < 67:
            pottype = 1 #Current pot type heal/restore
            pottomake = 9 #Current pot to make greater refreshment
            Items.UseItemByID(pestle,0)
            Gumps.WaitForGump(949095101, 10000)
            Gumps.SendAction(949095101, pottype)
            Gumps.WaitForGump(949095101, 10000)
            Gumps.SendAction(949095101, pottomake)
            Misc.Pause(delay)

    if Player.GetRealSkillValue('Alchemy') > 42:
        if Player.GetRealSkillValue('Alchemy') < 60: 
            pottype = 15 #Current pot type toxic
            pottomake = 9 #Current pot to make regular poison
            Items.UseItemByID(pestle,0)
            Gumps.WaitForGump(949095101, 10000)
            Gumps.SendAction(949095101, pottype)
            Gumps.WaitForGump(949095101, 10000)
            Gumps.SendAction(949095101, pottomake)
            Misc.Pause(delay)
            
    if Player.GetRealSkillValue('Alchemy') < 42:
        Misc.SendMessage('YOU FORGOT TO TRAIN - MACRO EXITING')
        Player.ChatSay(45,'[e no')
        Player.ChatSay(45,'Go train to 42.0 Alchemy at the NPC')
        exit()

def restockDumpstock():
    for i in toolsList:
        #tool restock
        if Items.BackpackCount(pestle,-1) < toolsAmount:
            movepestle = Items.FindByID(pestle,-1,toolsCont)
            Misc.SendMessage('Restocking Tools')
            Misc.Pause(500)
            Items.Move(movepestle,Player.Backpack.Serial,toolsamounttorestock)
            Misc.Pause(1100)
    for i in regsList:
        #reg and bottle restock
        if Items.BackpackCount(i,-1) < regAmount:
            reg = Items.FindByID(i,-1,stoCont)
            Misc.SendMessage('Restocking Reagents and Bottles')
            Misc.Pause(500)
            Items.Move(reg,Player.Backpack.Serial,regsamounttorestock)
            Misc.Pause(1100)
    for i in potsList:
        if Items.BackpackCount(i,-1) > 10:
            pot = Items.FindByID(i,-1,Player.Backpack.Serial)
            Misc.SendMessage('Moving Finished Potions')
            Misc.Pause(500)
            Items.Move(pot,outCont,999)
            Misc.Pause(1100)

while not Player.IsGhost:
    restockDumpstock()
    if mode == 'train':
        trainAlchemy()
    if mode == 'heal':
        healPots()
    if mode == 'cure':
        curePots()
    if mode == 'refresh':
        refreshPots()
    if mode == 'str':
        strPots()
    if mode == 'dex':
        dexPots()
    if mode == 'explode':
        explodePots()
