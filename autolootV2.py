from System.Collections.Generic import List
from System import Byte, Int32

#PARAMETERS

skinning = False
only_loot_and_dust_magic_items = True   
loot_scrolls = False #only works if only_loot_and_dust_magic_items == False

#SETTINGS 
corpse_ID = 0x2006
gold_ID = 0x0EED
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
arcanedust = 0x5745
arcanescroll = 0x0EF3
scrolloftrans = 0x0E34
tmap = 0x14EC
artifact1 = 0x1576
plant1 = 0x63DF
plant2 = 0x1E0F
plant3 = 0x11C8
plant4 = 0xAC91
deed = 0x14F0
dye1 = 0x0E2A
dye2 = 0x0E2B
dye3 = 0x0EFF
scales = 0x26B4
MIB = 0x099F
artifact1 = 0x1576
artifact2 = 0x2228
artifact3 = 0x1F14
artifact4 = 0x2D28
artifact5 = 0x14ED
artifact6 = 0x1227
artifact7 = 0x4076
artifact8 = 0x223D
artifact9 = 0x1F18
artifact10 = 0x2B01
artifact11 = 0x15BB
artifact12 = 0x14F4
artifact13 = 0x1B0C

loot_list  = [artifact1,artifact2,artifact3,artifact4,artifact5,artifact6,artifact7,artifact8,artifact9,artifact10,artifact11,artifact12,artifact13,MIB,scales,gold_ID,biggem1,biggem2,biggem3,biggem4,biggem5,biggem6,biggem7,arcanedust,arcanescroll,scrolloftrans,tmap,artifact1,plant1,plant2,plant3,plant4,deed,dye1,dye2,dye3]
ignore_list = [citrine,amber,amethyst,ruby,emerald,diamond,sapphire,tourmaline,starsapph]

circle7scroll_list = [0x1F5D,0x1F5E,0x1F5F,0x1F60,0x1F61,0x1F62,0x1F63,0x1F64]
circle8scroll_list = [0x1F65,0x1F66,0x1F67,0x1F68,0x1F69,0x1F6A,0x1F6B,0x1F6C]

#LOOT
filCorpse = Items.Filter()
filCorpse.Enabled = True
filCorpse.Movable = False
filCorpse.OnGround = True
filCorpse.RangeMax = 2
filCorpse.CheckIgnoreObject = False
lisCorpses = Items.ApplyFilter(filCorpse)

dagger = Items.FindByID(0x0F52,-1,Player.Backpack.Serial)
#if not dagger:
#    Player.HeadMessage(50,"No dagger found")
    #sys.exit()
scissors = Items.FindByID(0x0F9F,-1,Player.Backpack.Serial)
#if not scissors:
#    Player.HeadMessage(50,"No scissors found")
    #sys.exit()
    
saw = Items.FindByID(0x1034,0x0000,Player.Backpack.Serial)

bodyCorpse = None
if len(lisCorpses) >= 1: 
    for corpse in lisCorpses:
        for i in corpse.Contains:
            if i.ItemID not in ignore_list:
                Journal.Clear()
                Items.SingleClick(i.Serial)
                Misc.Pause(200)
                if Journal.Search("Unidentified"): 
                    Items.Move(i, Player.Backpack.Serial, 1)
                    Misc.Pause(650)
                    if Target.HasTarget(): 
                        Target.TargetExecute(i)
                        Target.WaitForTarget(700,0)
                    else:
                        Player.HeadMessage(1000,"Using Saw")
                        Items.UseItem(saw)
                        Gumps.WaitForGump(949095101, 1500)
                        Gumps.SendAction(949095101, 63)
                        Target.WaitForTarget(1000,0)
                        Target.TargetExecute(i)
                        Target.WaitForTarget(700,0)
                elif only_loot_and_dust_magic_items == False and (i.ItemID in loot_list or (loot_scrolls and (i.ItemID in circle7scroll_list or i.ItemID in circle8scroll_list))):
                    Items.Move(i,Player.Backpack,-1 ) # -1 -> all, for stackable items
                    Misc.Pause(650)
                
Target.Cancel()