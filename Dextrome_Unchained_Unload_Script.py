from operator import length_hint
from os.path import exists
from os import makedirs
from sys import exit
import pickle


#Settings
#########
items_to_ignore = [0x0EFA , 0x09B0, 0x0E79, 0x0F52, 0x0FC1, 0x1034, 0x0F9F, 0x0E9E,0x0E76]
storageShelfSerial = 0x4002D26E
orbBoxSerial = 0x4007D779
tinctureBoxSerial = 0x400FB8A6
greenThornBoxSerial = 0x400CAA4A
psTome = 0x40086A84
psBox = 0x404FF6E3
transTome = 0x400747CE
spellbookDyeTome = 0x4003F9FA
armamentDyeTome = 0x400B1D4C
runebookDyeTome = 0x40093AA3
clothTome = 0x4003FAFB
beardDyeTome = 0x400E341F
hairDyeTome = 0x400E3450
furnitureDyeTome = 0x400E34BF


#Item Functions
###############
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

    # Wait for the move to complete
    Misc.Pause( 650 )
    
    
#Load or Create save_data for variables    
#######################################
#save_folder = Misc.ScriptDirectory() + "\\saved-variables\\"
#save_file = save_folder + "Dextrome_Unload_Script_Variables.pickle"
#save_file_exists = exists(save_file)
#
#if not exists(save_folder):
#    makedirs(save_folder)
#    
#if save_file_exists:
#    Misc.SendMessage("Save File Found")
#    
#    with open(save_file, 'rb') as f2 :
#        save_data = pickle.load(f2)
#        
#    storageShelfSerial = save_data['StorageShelf']
#    storageShelfItem = Items.FindBySerial( storageShelfSerial )
#    if storageShelfItem == None:
#        Misc.SendMessage('Cant find storage shelf')
#        exit(99)
#    else:
#        Misc.SendMessage("Loaded serial %s for Storage Shelf" % (storageShelfSerial))
# 
#    unloadBoxSerial = save_data['UnloadBox']
#    unloadBoxItem = Items.FindBySerial( unloadBoxSerial )
#    if unloadBoxItem == None:
#        Misc.SendMessage("Invalid Target")
#        exit(99)     
#    else:
#        Misc.SendMessage("Loaded serial %s for Unload Container" % (unloadBoxSerial))
#else:
#    Misc.SendMessage("No Save File Found")
#    #No save file - ask for player for serials to save
#    storageShelfSerial = Target.PromptTarget( 'Target storage shelf' )
#    storageShelfItem = Items.FindBySerial( storageShelfSerial )
#    if storageShelfItem == None:
#        Misc.SendMessage("Invalid Target")
#        exit(99)
#    
#    orbBoxSerial = Target.PromptTarget( 'Target Mastery Orb Container' )
#    orbBoxItem = Items.FindBySerial( orbBoxSerial )
#    if orbBoxItem == None:
#        Misc.SendMessage("Invalid Target")
#        exit(99)    
#
#    unloadBoxSerial = Target.PromptTarget( 'Target container to unload other items' )
#    unloadBoxItem = Items.FindBySerial( unloadBoxSerial )
#    if unloadBoxItem == None:
#        Misc.SendMessage("Invalid Target")
#        exit(99)    
#        
#    save_data = { 'StorageShelf': storageShelfSerial, 'UnloadBox': unloadBoxSerial }
#    with open(save_file, 'wb') as f1:        
#        pickle.dump(save_data, f1)    
#
    
#Add all from backpack to storage shelf + Resupply
##################################################
Items.UseItem(storageShelfSerial)
Gumps.WaitForGump(2834126535, 10000)
Misc.Pause(250)
Gumps.SendAction(2834126535, 1464)
Misc.Pause(250)
Gumps.WaitForGump(2834126535, 10000)
Misc.Pause(150)
Gumps.SendAction(2834126535, 0)
Misc.Pause(250)
Target.WaitForTarget(10000, False)
Misc.Pause(250)
Target.Self()
Misc.Pause(250)
Gumps.WaitForGump(2834126535, 10000)
Misc.Pause(250)
Gumps.SendAction(2834126535, 3662)
Misc.Pause(150)
Gumps.SendAction(2834126535, 0)

#Move items to containers
#########################
for item in Player.Backpack.Contains:
    if item.ItemID == 0x573E: #mastery orbs
        MoveItem(Items, Misc, item, orbBoxSerial)
        Misc.Pause(300)
    elif item.ItemID == 0x4516: #vials of tincture
        MoveItem(Items, Misc, item, tinctureBoxSerial)
        Misc.Pause(300)
    elif item.ItemID == 0x0F42: #green thorns
        MoveItem(Items, Misc, item, greenThornBoxSerial)
        Misc.Pause(300)
    elif 'power scroll of herding' in item.Name: 
        MoveItem(Items, Misc, item, psBox)
        Misc.Pause(300)
    elif 'power scroll of arms lore' in item.Name: 
        MoveItem(Items, Misc, item, psBox)
        Misc.Pause(300)
        
#Fill PS Tome with PS & arcane scrolls
######################################
Items.UseItem(psTome)
Misc.Pause(200)
Gumps.WaitForGump(191824442, 10000)
Misc.Pause(200)
Gumps.SendAction(191824442, 1)
Misc.Pause(650)

for item in Player.Backpack.Contains:
    if (item.ItemID == 0x14F0 and item.Hue == 0x0b42) or (item.ItemID == 0x0EF3 and (item.Hue == 0x0a44 or item.Hue == 0x06f6 or item.Hue == 0x06fc)):
        Target.TargetExecute(item)
        Misc.Pause(650)

Misc.Pause(100)
Target.Cancel()
Gumps.SendAction(191824442, 0)

#Fill Trans Scroll Tome
#######################
Items.UseItem(transTome)
Misc.Pause(200)
Gumps.WaitForGump(3083091039, 10000)
Misc.Pause(120)
Gumps.SendAction(3083091039, 1)
Misc.Pause(300)

for item in Player.Backpack.Contains:
    if item.ItemID == 0x0E34 and item.Hue == 0x0b42:
        Target.TargetExecute(item)
        Misc.Pause(600)
        
Misc.Pause(100)
Target.Cancel()
Gumps.SendAction(3083091039, 0)


#Fill Spellbook Dye Tome
########################
for item in Player.Backpack.Contains:
    if item.Name == 'Spellbook Dye':
        Items.UseItem(spellbookDyeTome)
        Misc.Pause(200)
        Gumps.WaitForGump(0xdd418d4b, 10000)
        Misc.Pause(120)
        Gumps.SendAction(0xdd418d4b, 1000)
        Misc.Pause(300)
        Target.TargetExecute(item)
        Misc.Pause(600)
        
#Fill Armament Dye Tome
########################
for item in Player.Backpack.Contains:
    if item.Name == 'Armament Dye':
        Items.UseItem(armamentDyeTome)
        Misc.Pause(200)
        Gumps.WaitForGump(0xc512fa6f, 10000)
        Misc.Pause(120)
        Gumps.SendAction(0xc512fa6f, 1000)
        Misc.Pause(300)
        Target.TargetExecute(item)
        Misc.Pause(600)
        
#Fill Runebook Dye Tome
########################
for item in Player.Backpack.Contains:
    if item.Name == 'Runebook Dye':
        Items.UseItem(runebookDyeTome)
        Misc.Pause(200)
        Gumps.WaitForGump(0x5d776aaf, 10000)
        Misc.Pause(120)
        Gumps.SendAction(0x5d776aaf, 1000)
        Misc.Pause(300)
        Target.TargetExecute(item)
        Misc.Pause(600)
        
        
        
#Fill Cloth Tome
################
for item in Player.Backpack.Contains:
    if item.ItemID == 0x1767:
        Items.UseItem(clothTome)
        Misc.Pause(200)
        Gumps.WaitForGump(0x4b60e46f, 10000)
        Misc.Pause(120)
        Gumps.SendAction(0x4b60e46f, 1000)
        Misc.Pause(300)
        Target.TargetExecute(item)
        Misc.Pause(600)
        
        
#Fill Beard Dye Tome
####################
for item in Player.Backpack.Contains:
    if item.Name == 'Rare Beard Dye':
        Items.UseItem(beardDyeTome)
        Misc.Pause(200)
        Gumps.WaitForGump(0xddeae86f, 10000)
        Misc.Pause(120)
        Gumps.SendAction(0xddeae86f, 1000)
        Misc.Pause(300)
        Target.TargetExecute(item)
        Misc.Pause(600)

        
#Fill Hair Dye Tome
###################
for item in Player.Backpack.Contains:
    if item.Name == 'Rare Hair Dye':
        Items.UseItem(hairDyeTome)
        Misc.Pause(200)
        Gumps.WaitForGump(0xb010c72f, 10000)
        Misc.Pause(120)
        Gumps.SendAction(0xb010c72f, 1000)
        Misc.Pause(300)
        Target.TargetExecute(item)
        Misc.Pause(600)
                
#Fill Furniture Dye Tome
###################
for item in Player.Backpack.Contains:
    if item.Name == 'Rare Furniture Dye':
        Items.UseItem(furnitureDyeTome)
        Misc.Pause(200)
        Gumps.WaitForGump(0x673dddaf, 10000)
        Misc.Pause(120)
        Gumps.SendAction(0x673dddaf, 1000)
        Misc.Pause(300)
        Target.TargetExecute(item)
        Misc.Pause(600)

#Move remaining items to dump container
#######################################
#for item in Player.Backpack.Contains:
#    if item.ItemID not in items_to_ignore:
#        MoveItem( Items, Misc, item, unloadBoxSerial )