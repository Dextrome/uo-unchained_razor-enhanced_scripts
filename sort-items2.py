from System.Collections.Generic import List
from System import Byte, Int32

def MoveItem( Items, Misc, item, destinationBag, amount = 0 ):
    Items.Move( item, destinationBag, amount )
    Misc.Pause( 700 )

gold_ID = 0x0EED
tmap = 0x14EC
arcanedust = 0x5745
arcanescroll = 0x0EF3
scrolloftrans = 0x0E34
biggem1 = 0x3193
biggem2 = 0x3194
biggem3 = 0x3195
biggem4 = 0x3196
biggem5 = 0x3197
biggem6 = 0x3198
biggem7 = 0x3199
ingot = 0x1BF2
arrow = 0x0F3F
bolt = 0x1BFB
deed = 0x14F0
dye1 = 0x0E2A
dye2 = 0x0E2B
dye3 = 0x0EFF
dye4 = 0x0EFE

reglist = [0x0F84,0x0F8D,0x0F7B,0x0F88,0x0F7A,0x0F86,0x0F85,0x0F8C]

exceptionlist = [gold_ID,tmap,arcanedust,arcanescroll,scrolloftrans,biggem1,biggem2,biggem3,biggem4,biggem5,biggem6,biggem7,ingot,arrow,bolt,deed,dye1,dye2,dye3,dye4]

sourceBox = Target.PromptTarget( 'Select container to move items out of' )
sourceBoxItem = Items.FindBySerial( sourceBox )
if sourceBoxItem == None:
    sourceBox = Mobiles.FindBySerial( sourceBox ).Backpack
else:
    sourceBox = sourceBoxItem

if sourceBox == Player.Backpack:
    sourceBox = None

targetBox = Target.PromptTarget( 'Select trash container' )
targetBoxItem = Items.FindBySerial( targetBox )
if targetBoxItem == None:
    targetBox = Mobiles.FindBySerial( targetBox ).Backpack
else:
    targetBox = targetBoxItem
    
scavengerBox = Target.PromptTarget( 'Select scavenger chest' )
scavengerBoxItem = Items.FindBySerial( scavengerBox )
if scavengerBox == None:
    scavengerBox = Mobiles.FindBySerial( targetBox ).Backpack
else:
    scavengerBox = scavengerBoxItem
    
exceptionBox = Target.PromptTarget( 'Select where to move other items' )
exceptionBoxItem = Items.FindBySerial( exceptionBox )
if exceptionBox == None:
    exceptionBox = Mobiles.FindBySerial( targetBox ).Backpack
else:
    exceptionBox = exceptionBoxItem  

#targetBox = 0x400540E4
#scavengerBox = 0x401A433A
#exceptionBox = 0x400539E4

Items.UseItem( sourceBox )
Misc.Pause( 700 )

Items.UseItem( targetBox )
Misc.Pause( 700 )

Items.UseItem( scavengerBox )
Misc.Pause( 700 )

for item in sourceBox.Contains:
    if item.ItemID not in exceptionlist and item.ItemID not in reglist:
        if item.Layer == 'Invalid':
            MoveItem( Items, Misc, item, targetBox )
        else:
            MoveItem( Items, Misc, item, scavengerBox )
    else:
        if exceptionBox == None:
            MoveItem( Items, Misc, item, Player.Backpack )
        else:
            MoveItem( Items, Misc, item, exceptionBox )