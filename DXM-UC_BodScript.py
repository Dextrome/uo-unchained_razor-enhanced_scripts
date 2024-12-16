### Config / Mapping ###
########################

resourceStorageSerial = 0x402DD22C
resourceStorageGumpId = 111922706
bodGumpId = 1526454082
bodStoreGumpId = 2511202189

class CraftItem:
  def __init__(self, itemId, gumpCategory, gumpSelection):
    self.itemId = itemId
    self.gumpCategory = gumpCategory
    self.gumpSelection = gumpSelection
    
    
def getItemMapping(itemname,skill):
    if skill == 'Blacksmithing':
        #Metal Armor
        if itemname == 'ringmail gloves':
            return CraftItem(0x13EB,8,2)
        elif itemname == 'ringmail leggings':
            return CraftItem(0x13F0,8,9)
        elif itemname == 'ringmail sleeves':
            return CraftItem(0x13EE,8,16)  
        elif itemname == 'ringmail tunic':
            return CraftItem(0x13EC,8,23)
        elif itemname == 'chainmail coif':
            return CraftItem(0x13BB,8,30)
        elif itemname == 'chainmail leggings':
            return CraftItem(0x13BE,8,37)
        elif itemname == 'chainmail tunic':
            return CraftItem(0x13BF,8,44)
        elif itemname == 'platemail arms':
            return CraftItem(0x1410,8,51)
        elif itemname == 'platemail gloves':
            return CraftItem(0x1414,8,58)
        elif itemname == 'platemail gorget':
            return CraftItem(0x1413,8,65)
        elif itemname == 'platemail legs':
            return CraftItem(0x1411,8,72)
        elif itemname == 'platemail tunic':
            return CraftItem(0x1415,8,79)
        elif itemname == 'female plate':
            return CraftItem(0x1C04,8,86)
        #Helmets
        elif itemname == 'bascinet':
            return CraftItem(0x140C,15,2)
        elif itemname == 'close helmet':
            return CraftItem(0x1408,15,9)
        elif itemname == 'helmet':
            return CraftItem(0x140A,15,16)
        elif itemname == 'norse helm':
            return CraftItem(0x140E,15,23)
        elif itemname == 'plate helm':
            return CraftItem(0x1412,15,30)
        #Shields
        elif 'buck' in itemname:
            return CraftItem(0x1B73,22,2)
        elif itemname == 'bronze shield':
            return CraftItem(0x1B72,22,9)
        elif itemname == 'heater shield':
            return CraftItem(0x1B76,22,16)
        elif itemname == 'metal shield':
            return CraftItem(0x1B7B,22,23)
        elif itemname == 'metal kite shield':
            return CraftItem(0x1B74,22,30)
        elif itemname == 'tear kite shield':
            return CraftItem(0x1B78,22,37)
        #Bladed
        elif itemname == 'bone harvester':
            return CraftItem(0x26BB,29,2)
        elif itemname == 'broadsword':
            return CraftItem(0x0F5E,29,9)
        elif itemname == 'cutlass':
            return CraftItem(0x1441,29,16)
        elif itemname == 'dagger':
            return CraftItem(0x0F52,29,23)
        elif itemname == 'katana':
            return CraftItem(0x13FF,29,30)
        elif itemname == 'kryss':
            return CraftItem(0x1401,29,37)
        elif itemname == 'longsword':
            return CraftItem(0x0F61,29,44)
        elif itemname == 'scimitar':
            return CraftItem(0x13B6,29,51)
        elif itemname == 'viking sword':
            return CraftItem(0x13B9,29,58)
        #Axes
        elif itemname == 'axe':
            return CraftItem(0x0F49,36,2)
        elif itemname == 'battle axe':
            return CraftItem(0x0F47,36,9)
        elif itemname == 'double axe':
            return CraftItem(0x0F4B,36,16)
        elif 'executioner' in itemname:
            return CraftItem(0x0F45,36,23)
        elif itemname == 'large battle axe':
            return CraftItem(0x13FB,36,30)
        elif itemname == 'two handed axe':
            return CraftItem(0x1443,36,37)
        elif itemname == 'war axe':
            return CraftItem(0x13B0,36,44)
        #Polearms
        elif itemname == 'bardiche':
            return CraftItem(0x0F4D,43,2)
        elif itemname == 'bladed staff':
            return CraftItem(0x26BD,43,9)
        elif itemname == 'double bladed staff':
            return CraftItem(0x26BF,43,16)
        elif itemname == 'halberd':
            return CraftItem(0x143E,43,23)
        elif itemname == 'pike':
            return CraftItem(0x26BE,43,30)
        elif itemname == 'short spear':
            return CraftItem(0x1403,43,37)
        elif itemname == 'scythe':
            return CraftItem(0x26BA,43,44)
        elif itemname == 'spear':
            return CraftItem(0x0F62,43,51)
        elif itemname == 'war fork':
            return CraftItem(0x1405,43,58)
        #Bashing
        elif itemname == 'hammer pick':
            return CraftItem(0x143D,50,2)
        elif itemname == 'mace':
            return CraftItem(0x0F5C,50,9)
        elif itemname == 'maul':
            return CraftItem(0x143B,50,16)
        elif itemname == 'war mace':
            return CraftItem(0x1407,50,23)
        elif itemname == 'war hammer':
            return CraftItem(0x1439,50,30)
        else:
            Misc.SendMessage('Gump Responses for %s have not been mapped' % (item))
            return None
    elif skill == 'Tailoring':
        #Miscellaneous
        if itemname == 'body sash':
            return CraftItem(0x1541,1,16)
        elif itemname == 'half apron':
            return CraftItem(0x153B,1,23)
        elif itemname == 'full apron':
            return CraftItem(0x153D,1,30)   
        #Hats
        elif itemname == 'skullcap':
            return CraftItem(0x1544,8,2)    
        elif itemname == 'bandana':
            return CraftItem(0x1540,8,9)   
        elif itemname == 'floppy hat':
            return CraftItem(0x1713,8,16)   
        elif itemname == 'cap':
            return CraftItem(0x1715,8,23)   
        elif itemname == 'wide-brim hat':
            return CraftItem(0x1714,8,30)   
        elif itemname == 'straw hat':
            return CraftItem(0x1717,8,37)   
        elif itemname == 'tall straw hat':
            return CraftItem(0x1716,8,44)
        elif 'wizard' in itemname:
            return CraftItem(0x1718,8,51)
        elif itemname == 'bonnet':
            return CraftItem(0x1719,8,58)
        elif itemname == 'feathered hat':
            return CraftItem(0x171A,8,65)   
        elif itemname == 'tricorne hat':
            return CraftItem(0x171B,8,72)
        elif itemname == 'jester hat':
            return CraftItem(0x171C,8,79)
        #Shirts & Pants
        elif itemname == 'doublet':
            return CraftItem(0x1F7B,29,2)
        elif itemname == 'shirt':
            return CraftItem(0x1517,29,9)
        elif itemname == 'fancy shirt':
            return CraftItem(0x1EFD,29,16) 
        elif itemname == 'tunic':
            return CraftItem(0x1FA1,29,23)    
        elif itemname == 'surcoat':
            return CraftItem(0x1FFD,29,30)
        elif itemname == 'plain dress':
            return CraftItem(0x1F01,29,37)
        elif itemname == 'cloak':
            return CraftItem(0x1515,29,44)
        elif itemname == 'robe':
            return CraftItem(0x1F03,29,51)
        elif itemname == 'jester suit':
            return CraftItem(0x1F9F,29,58)
        elif itemname == 'short pants':
            return CraftItem(0x152E,29,65)
        elif itemname == 'long pants':
            return CraftItem(0x1539,29,72)
        elif itemname == 'kilt':
            return CraftItem(0x1537,29,79)
        elif itemname == 'skirt':
            return CraftItem(0x1516,29,86)            
        #Footwear
        elif itemname == 'sandals':
            return CraftItem(0x170D,36,2)
        elif itemname == 'shoes':
            return CraftItem(0x170F,36,9)
        elif itemname == 'boots':
            return CraftItem(0x170B,36,16)
        elif itemname == 'thigh boots':
            return CraftItem(0x1711,36,23)
        #Leather Armor
        elif itemname == 'leather gorget':
            return CraftItem(0x13C7,43,2)
        elif itemname == 'leather cap':
            return CraftItem(0x1DB9,43,9)
        elif itemname == 'leather gloves':
            return CraftItem(0x13C6,43,16)
        elif itemname == 'leather sleeves':
            return CraftItem(0x13C7,43,23)
        elif itemname == 'leather leggings':
            return CraftItem(0x13CB,43,30)
        elif itemname == 'leather tunic':
            return CraftItem(0x13CC,43,37)
        #Studded Armor
        elif itemname == 'studded gorget':
            return CraftItem(0x13D6,50,2)
        elif itemname == 'studded gloves':
            return CraftItem(0x13D5,50,9)
        elif itemname == 'studded sleeves':
            return CraftItem(0x13DC,50,16)
        elif itemname == 'studded leggings':
            return CraftItem(0x13DA,50,23)    
        elif itemname == 'studded tunic':
            return CraftItem(0x13DB,50,30)
        #Female Armor
        elif itemname == 'leather shorts':
            return CraftItem(0x1C00,57,2)
        #Bone Armor
        else:
            Misc.SendMessage('Gump Responses for %s have not been mapped' % (item))
            return None
    else:
        Misc.SendMessage('Gump Responses for %s have not been mapped' % (skill))
        return None


def GetMats(skill, material):
    Items.UseItem(resourceStorageSerial)
    Misc.Pause(250)
    Gumps.WaitForGump(111922706, 10000)
    if skill == 'Blacksmithing':   
        if material == 'iron':
            Gumps.SendAction(resourceStorageGumpId, 1)
        elif material == 'dull':
            Gumps.SendAction(resourceStorageGumpId, 2)
        elif material == 'shadow':
            Gumps.SendAction(resourceStorageGumpId, 3)
        elif material == 'copper':
            Gumps.SendAction(resourceStorageGumpId, 4)
        elif material == 'bronze':
            Gumps.SendAction(resourceStorageGumpId, 5)
        elif material == 'gold':
            Gumps.SendAction(resourceStorageGumpId, 6)
        elif material == 'agapite':
            Gumps.SendAction(resourceStorageGumpId, 7)
        elif material == 'verite':
            Gumps.SendAction(resourceStorageGumpId, 8)
        elif material == 'valorite':
            Gumps.SendAction(resourceStorageGumpId, 9)
    elif skill == 'Tailoring':
        if material == 'cloth':
            Gumps.SendAction(resourceStorageGumpId, 125) #next page
            Gumps.WaitForGump(resourceStorageGumpId, 10000)
            Gumps.SendAction(resourceStorageGumpId, 125) #next page
            Gumps.WaitForGump(resourceStorageGumpId, 10000)
            Gumps.SendAction(resourceStorageGumpId, 48) #cloth
        elif material == 'leather':
            Gumps.SendAction(resourceStorageGumpId, 18) #leather
        elif material == 'spined':
            Gumps.SendAction(resourceStorageGumpId, 19) #spined leather
        elif material == 'horned':
            Gumps.SendAction(resourceStorageGumpId, 20) #horned leather
        elif material == 'barbed':
            Gumps.SendAction(resourceStorageGumpId, 125) #next page
            Gumps.WaitForGump(resourceStorageGumpId, 10000)
            Gumps.SendAction(resourceStorageGumpId, 21) #barbed leather
            
    Misc.Pause(250)
    Gumps.WaitForGump(111922706, 10000)
    Gumps.SendAction(111922706, 0) #close gump
    Misc.Pause(250)
        
    
        
### Complete BODs in backpack and turn them in ###
##################################################

BODs = Items.FindAllByID(0xA614,-1,Player.Backpack.Serial,-1,False)
countItem = 1

for bod in BODs:
    Misc.SendMessage('BOD %i' % (countItem), 10)
    countItem += 1

 ### Determine Crafting Skill & Prop Indices
    if bod.Hue == 0x0a41:
        skill = 'Blacksmithing'
        toolId = 0x13E3
        toolResourceShelfButton = 52
        toolGumpId = 949095101
    elif bod.Hue == 0x0a4b:
        skill = 'Tailoring'
        toolId = 0x0F9D
        toolResourceShelfButton = 53
        toolGumpId = 949095101
    else:
        Misc.SendMessage('Unknown BOD type')
        break
        
    Misc.SendMessage('Skill: %s' % (skill), 15)
 
    if len(bod.Properties) == 9:
        matProp = 6
        amountProp = 7
        itemProp = 8
    else:
        matProp = 5
        amountProp = 6
        itemProp = 7
        
 ### Determine Item & Amount already added to the BOD
    item = bod.Properties[itemProp].ToString().split(": ")[0]
    Misc.SendMessage('Item: %s' % (item),40)
    amountAddedToBod = int(bod.Properties[itemProp].ToString().split(": ")[1])
    
 ### Determine Material
    if skill == 'Blacksmithing':
        if 'dull copper' in bod.Properties[matProp].ToString():
            material = 'dull'
            Misc.SendMessage('Material: Dull Copper', 20)
        elif 'shadow' in bod.Properties[matProp].ToString():
            material = 'shadow'
            Misc.SendMessage('Material: Shadow', 20)
        elif 'copper' in bod.Properties[matProp].ToString():
            material = 'copper'
            Misc.SendMessage('Material: Copper', 20)
        elif 'bronze' in bod.Properties[matProp].ToString():
            material = 'bronze'
            Misc.SendMessage('Material: Bronze', 20)
        elif 'gold' in bod.Properties[matProp].ToString():
            material = 'gold'
            Misc.SendMessage('Material: Gold', 20)
        elif 'agapite' in bod.Properties[matProp].ToString():
            material = 'agapite'
            Misc.SendMessage('Material: Agapite', 20)
        elif 'verite' in bod.Properties[matProp].ToString():
            material = 'verite'
            Misc.SendMessage('Material: Verite', 20)
        elif 'valorite' in bod.Properties[matProp].ToString():
            material = 'valorite'
            Misc.SendMessage('Material: Valorite', 20)
        else:
            material = 'iron'
            Misc.SendMessage('Material: Iron', 20)
    elif skill == 'Tailoring':
        if 'leather' in item or 'studded' in item:
            material = 'leather'
            #Misc.SendMessage('Material: Leather', 20)
        else:
            material = 'cloth'
            #Misc.SendMessage('Material: Cloth', 20)
            
        if 'spined' in bod.Properties[matProp].ToString():
            material = 'spined'
            #Misc.SendMessage('Material: Spined Leather', 20)
        if 'horned' in bod.Properties[matProp].ToString():
            material = 'horned'
            #Misc.SendMessage('Material: Horned Leather', 20)
        if 'barbed' in bod.Properties[matProp].ToString():
            material = 'barbed'
            #Misc.SendMessage('Material: Barbed Leather', 20)
        if 'scaled' in bod.Properties[matProp].ToString():
            material = 'scaled'
            #Misc.SendMessage('SKIP BOD! Not doing Scaled Leather', 20)
            break
            
        Misc.SendMessage('Material: %s' % (material), 20)
            
    else:
        break
         
 ### Determine Amount
    amount = [int(s) for s in bod.Properties[amountProp].ToString().split() if s.isdigit()][0]
    Misc.SendMessage('Amount: %i' % (amount),30)
    
 ### Get Crafting Tool
    tool = Items.FindByID(toolId,-1,Player.Backpack.Serial,-1,False)

    if not tool: # Get Tool
        Items.UseItem(resourceStorageSerial) # Opening Resource Storage
        Misc.Pause(250)
        Gumps.WaitForGump(resourceStorageGumpId, 10000)
        Gumps.SendAction(resourceStorageGumpId, 125) # next page
        Gumps.WaitForGump(resourceStorageGumpId, 10000)
        Gumps.SendAction(resourceStorageGumpId, 125) # next page
        Gumps.WaitForGump(resourceStorageGumpId, 10000)
        Misc.Pause(250)
        Gumps.SendAction(resourceStorageGumpId, toolResourceShelfButton) # getting tool
        Gumps.WaitForGump(resourceStorageGumpId, 10000)
        Gumps.SendAction(resourceStorageGumpId, 0) # close gump
        Misc.Pause(250)
        tool = Items.FindByID(toolId,-1,Player.Backpack.Serial,-1,False)    
    
 ### Switch to Material 
    if material != 'cloth':
        Items.UseItem(tool)
        Misc.Pause(250)
        Gumps.WaitForGump(toolGumpId, 10000)
        Gumps.SendAction(toolGumpId, 7)
        Misc.Pause(250)
        Gumps.WaitForGump(toolGumpId, 10000)
        
        if skill == 'Blacksmithing':
            if material == 'iron':
                Gumps.SendAction(toolGumpId, 6) #iron ingots
            elif material == 'dull':
                Gumps.SendAction(toolGumpId, 13) #dull copper ingots
            elif material == 'shadow':
                Gumps.SendAction(toolGumpId, 20) #shadow iron ingots
            elif material == 'copper':
                Gumps.SendAction(toolGumpId, 27) #copper ingots
            elif material == 'bronze':
                Gumps.SendAction(toolGumpId, 34) #bronze ingots
            elif material == 'gold':
                Gumps.SendAction(toolGumpId, 41) #gold ingots
            elif material == 'agapite':
                Gumps.SendAction(toolGumpId, 48) #agapite ingots
            elif material == 'verite':
                Gumps.SendAction(toolGumpId, 55) #verite ingots
            elif material == 'valorite':
                Gumps.SendAction(toolGumpId, 62) #valorite ingots
            else:
                break #todo: implement other materials
        elif skill == 'Tailoring':
            if material == 'leather':
                Gumps.SendAction(toolGumpId, 6) #leather
            elif material == 'spined':
                Gumps.SendAction(toolGumpId, 13) #spined leather
            elif material == 'horned':
                Gumps.SendAction(toolGumpId, 20) #horned leather
            elif material == 'barbed':
                Gumps.SendAction(toolGumpId, 13) #barbed leather
            else:
                break #todo: implement other materials
        Misc.Pause(250)
        Gumps.WaitForGump(toolGumpId, 10000)
        Gumps.SendAction(toolGumpId, 0) #close gump
        Misc.Pause(250)
        
 ### Get Mats from Resource Storage
    GetMats(skill, material)
    
 ### Craft Item
    craftItem = getItemMapping(item,skill)
    
    if craftItem:
        #Crafting
        countItemsMade = len(Items.FindAllByID(craftItem.itemId,-1,Player.Backpack.Serial,-1,False))
        amountAddedToBod = int(bod.Properties[itemProp].ToString().split(": ")[1])
        
        while amountAddedToBod + countItemsMade < amount:
            Items.UseItem(tool)        
            Misc.Pause(200)
            Gumps.WaitForGump(toolGumpId, 10000)
            Gumps.SendAction(toolGumpId, craftItem.gumpCategory)
            Misc.Pause(200)
            Gumps.WaitForGump(toolGumpId, 10000)
            Gumps.SendAction(toolGumpId, craftItem.gumpSelection)
            Misc.Pause(2500)
            
            if countItemsMade == len(Items.FindAllByID(craftItem.itemId,-1,Player.Backpack.Serial,-1,False)):
                GetMats(skill, material)
            
            countItemsMade = len(Items.FindAllByID(craftItem.itemId,-1,Player.Backpack.Serial,-1,False))
            amountAddedToBod = int(bod.Properties[itemProp].ToString().split(": ")[1])
            Misc.SendMessage('%s left to make: %i' % (item, amount - (amountAddedToBod + countItemsMade)))
            
            if Player.Weight > Player.MaxWeight - 75 or (amountAddedToBod < amount and countItemsMade > 0 and (Player.Weight > Player.MaxWeight - 75 or countItemsMade > 50)): #ADD ITEMS TO BOD
                Items.UseItem(bod.Serial)
                Misc.Pause(200)
                Gumps.WaitForGump(bodGumpId, 10000)
                Gumps.SendAction(bodGumpId, 4)
                Target.WaitForTarget(10000, False)
                Target.TargetExecute(Player.Backpack.Serial)
                Misc.Pause(1500)
                if Target.HasTarget():
                    Target.Cancel()
                Misc.Pause(1500)
                Gumps.SendAction(bodGumpId, 0) # close gump
                Misc.Pause(200)
                
            
            
        #Add items to BOD 
        Items.UseItem(bod.Serial)
        Misc.Pause(200)
        Gumps.WaitForGump(bodGumpId, 10000)
        Gumps.SendAction(bodGumpId, 4)
        Target.WaitForTarget(10000, False)
        Target.TargetExecute(Player.Backpack.Serial)
        Target.WaitForTarget(10000, False)
        Misc.Pause(500)
        if Target.HasTarget():
            Target.Cancel()
        Gumps.WaitForGump(bodGumpId, 5000)
        Gumps.SendAction(bodGumpId, 0) # close gump
        Misc.Pause(200)
        
        #Turn in BOD
#        Player.ChatSay(45, "[bod")
#        Misc.Pause(200)
#        Gumps.WaitForGump(bodStoreGumpId, 10000)
#        Gumps.SendAction(bodStoreGumpId, 200) 
#        Misc.Pause(200)
#        Target.WaitForTarget(10000, False)
#        Target.TargetExecute(bod.Serial)
#        Misc.Pause(200)
#        Gumps.WaitForGump(bodStoreGumpId, 5000)
#        Gumps.SendAction(bodStoreGumpId, 0) # close gump
        
        #Deposit tool & resources to shelf
        Items.UseItem(resourceStorageSerial)
        Misc.Pause(250)
        Gumps.WaitForGump(resourceStorageGumpId, 10000)
        Gumps.SendAction(resourceStorageGumpId, 123) # fill all from backpack
        Misc.Pause(250)
        Gumps.WaitForGump(resourceStorageGumpId, 10000)
        Gumps.SendAction(resourceStorageGumpId, 0) # close gump
        Misc.Pause(250)

