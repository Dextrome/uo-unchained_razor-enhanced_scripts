from Scripts.utilities.items import MoveItem
from Scripts import config
from System.Collections.Generic import List
from System import Byte, Int32

reglist = [0x0F84,0x0F8D,0x0F7B,0x0F88,0x0F7A,0x0F86,0x0F85,0x0F8C]

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
arrow = 0x0F3F
bolt = 0x1BFB
arcanedust = 0x5745

gemlist = [citrine,amber,amethyst,ruby,emerald,diamond,sapphire,tourmaline,starsapph,biggem1,biggem2,biggem3,biggem4,biggem5,biggem6,biggem7,arrow,bolt,arcanedust]

gold_ID = 0x0EED
tmap = 0x14EC
arcanescroll = 0x0EF3
scrolloftrans = 0x0E34

exceptionlist = [gold_ID,tmap,arcanedust,arcanescroll,scrolloftrans]

ingot = 0x1BF2
log = 0x1BDD

resourcelist = [ingot,log]

spellscrolllist = [0x1F2E,0x1F2F,0x1F30,0x1F31,0x1F32,0x1F33,0x1F2D,0x1F34,0x1F35,0x1F36,0x1F37,0x1F38,0x1F39,0x1F3A,0x1F3B,0x1F3C,0x1F3D,0x1F3E,0x1F3F,0x1F40,0x1F41,0x1F42,0x1F43,0x1F44,0x1F45,0x1F46,0x1F47,0x1F48,0x1F49,0x1F4A,0x1F4B,0x1F4C,0x1F4D,0x1F4E,0x1F4F,0x1F50,0x1F51,0x1F52,0x1F53,0x1F54,0x1F55,0x1F56,0x1F57,0x1F58,0x1F59,0x1F5A,0x1F5B,0x1F5C,0x1F5D,0x1F5E,0x1F5F,0x1F60,0x1F61,0x1F62,0x1F63,0x1F64,0x1F65,0x1F66,0x1F67,0x1F68,0x1F69,0x1F6A,0x1F6B,0x1F6C]





sourceBox = Target.PromptTarget( 'Select container to move items out of' )
sourceBoxItem = Items.FindBySerial( sourceBox )
if sourceBoxItem == None:
    sourceBox = None
else:
    sourceBox = sourceBoxItem

if sourceBox == Player.Backpack:
    sourceBox = None

gemregBox = Target.PromptTarget( 'Select gem/reg container' )
gemregBoxItem = Items.FindBySerial( gemregBox )
if gemregBoxItem == None:
    gemregBox = Mobiles.FindBySerial( gemregBox ).Backpack
else:
    gemregBox = gemregBoxItem
    
#scavengerBox = Target.PromptTarget( 'Select scavenger chest' )
#scavengerBoxItem = Items.FindBySerial( scavengerBox )
#if scavengerBox == None:
#    scavengerBox = Mobiles.FindBySerial( targetBox ).Backpack
#else:
#    scavengerBox = scavengerBoxItem

scavengerBox = 0x4017E0F1 #dustbag
exceptionBox = Player.Backpack
resourceBox = 0x400FB8A6
scrollBox = 0x400262A8

Items.UseItem( sourceBox )
Misc.Pause( config.dragDelayMilliseconds )

Items.UseItem( resourceBox )
Misc.Pause( config.dragDelayMilliseconds )

Items.UseItem( scavengerBox )
Misc.Pause( config.dragDelayMilliseconds )

Items.UseItem( scrollBox )
Misc.Pause( config.dragDelayMilliseconds )

for item in sourceBox.Contains:
    if item.ItemID in reglist or item.ItemID in gemlist:
        MoveItem( Items, Misc, item, gemregBox )
    elif item.ItemID in spellscrolllist:
        MoveItem( Items, Misc, item, scrollBox )
    elif item.ItemID in resourcelist:
        #MoveItem( Items, Misc, item, resourceBox )
        MoveItem( Items, Misc, item, gemregBox )
    elif item.ItemID in exceptionlist:
        MoveItem( Items, Misc, item, exceptionBox )
    else:
        if item.Layer == 'Invalid':
            MoveItem( Items, Misc, item, exceptionBox )
        else:
            MoveItem( Items, Misc, item, scavengerBox )