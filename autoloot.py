from System.Collections.Generic import List
from System import Byte, Int32

# SETTINGS 
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
seaserpentscale = 0x26B4
MIB = 0x099F

loot_list  = [MIB,seaserpentscale,gold_ID,biggem1,biggem2,biggem3,biggem4,biggem5,biggem6,biggem7,arcanedust,arcanescroll,scrolloftrans,tmap,artifact1,plant1,plant2,plant3,plant4,deed,dye1,dye2,dye3]

use_skinning = False
use_dagger = True

if Player.Name == "Dextrome":
    use_skinning = True

#loot_names = ['bread','arrow','gold coin']

# SCRIPT



def findCorpses():
    corpses_filter = Items.Filter()
    corpses_filter.IsCorpse = True # optional
    corpses_filter.OnGround = True # Questionably optional
    corpses_filter.RangeMin = 0 # optional
    corpses_filter.RangeMax = 2 # optoinal
    corpses_filter.Graphics = List[Int32]([corpse_ID,]) # optional, use item IDs
    corpses_filter.CheckIgnoreObject = True # optioinal, if you use Misc.IgnoreObject(item) the fitler will ignore if true.

    corpse_list = Items.ApplyFilter(corpses_filter) # returns list of items, manipulate list after this as you wish

    return corpse_list

def lootCorpse(corpse):
    for item_to_loot in corpse.Contains:
        Misc.SendMessage("found a {} with ID {}".format(item_to_loot.Name, item_to_loot.ItemID),130)
        Misc.Pause(10)
        shouldLoot = False
        
        if use_skinning == True and item_to_loot.ItemID == 0x1079:
            scissors = Items.FindByID(0x0F9F,-1,Player.Backpack.Serial)
            if scissors:
                Items.UseItem(scissors)
                Target.WaitForTarget(700,0)
                Target.TargetExecute(item_to_loot)
                Misc.Pause(700)
                leather = Items.FindByID(0x1081,-1, corpse.Serial)
                if leather: 
                    #Player.HeadMessage(50, "Leather Found")
                    Misc.Pause(100)
                    Items.Move(leather.Serial,Player.Backpack.Serial,-1)
                    Misc.Pause(700)
        elif checkItemByID(item_to_loot, loot_list):
            shouldLoot = True
        #if checkItemByName(item_to_loot, loot_names):
        #    shouldLoot = True
        if shouldLoot:
            Items.Move(item_to_loot,Player.Backpack,-1 ) # -1 -> all, for stackable items
            Misc.Pause(750)
        
            
def checkItemByID(item_to_check, valid_ids):
    if item_to_check.ItemID in loot_list:
        return True
    return False
    
def checkItemByName(item_to_check, valid_names):
    for name in valid_names:
        if name.lower() in str(item_to_check.Name).lower():
            return True
    return False
    
    
def tooMuchWeight():
    if Player.Weight > Player.MaxWeight - 20:
        Player.HeadMessage(138, "Burp, Feeling full")
        Misc.Pause(5000)
        
    
def main(): # define the function
    crps_list = findCorpses()

    for current_corpse in crps_list:
        if not tooMuchWeight():
            Items.Message(current_corpse,170,"loot this")
            Items.UseItem(current_corpse)
            Misc.Pause(750)
            if use_dagger == True:
                dagger = Items.FindByID(0x0F52,-1,Player.Backpack.Serial)
                if dagger:
                    Items.UseItem(dagger)
                    Target.WaitForTarget(700,0)
                    Target.TargetExecute(current_corpse)
                    Misc.Pause(750)
            lootCorpse(current_corpse)
            
    beetleSerial = 0x000139FA

    filCorpse = Items.Filter()
    filCorpse.Enabled = True
    filCorpse.Movable = False
    filCorpse.OnGround = True
    filCorpse.RangeMax = 2
    filCorpse.CheckIgnoreObject = True
    lisCorpses = Items.ApplyFilter(filCorpse)

#    dagger = Items.FindByID(0x0F52,-1,Player.Backpack.Serial)
#    if not dagger:
#        Player.HeadMessage(50,"No dagger found")
#        sys.exit()
#    scissors = Items.FindByID(0x0F9F,-1,Player.Backpack.Serial)
#
#    if scissors:
#        bodyCorpse = None
#        if len(lisCorpses) >= 1: 
#            for i in lisCorpses:
#                if i.ItemID == 0x2006:
#                    Items.UseItem(i)
#                    Misc.Pause(700)
#                    Items.UseItem(dagger)
#                    Target.WaitForTarget(700,0)
#                    Target.TargetExecute(i)
#                    Misc.Pause(500)
#                    for k in i.Contains:
#                        if k.ItemID == 0x1079:
#                            Items.UseItem(scissors)
#                            Target.WaitForTarget(700,0)
#                            Target.TargetExecute(k)
#                            Misc.Pause(700)
#                    leather = Items.FindByID(0x1081,-1, i.Serial)
#                    if leather: 
#                        #Player.HeadMessage(50, "Leather Found")
#                        Misc.Pause(100)
#                        Items.Move(leather.Serial,Player.Backpack.Serial,-1)
#                        Misc.Pause(700)
    #                    if Player.Mount: 
    #                        Mobiles.UseMobile(Player.Serial)
    #                        Misc.Pause(300)
    #                        beetle = Mobiles.FindBySerial(beetleSerial)
    #                        leather = Items.FindByID(0x1081,-1, Player.Backpack.Serial)
    #                        if beetle:      
    #                            Items.Move(leather.Serial, beetle.Backpack,-1)
    #                            Misc.Pause(700)
    #                            Mobiles.UseMobile(beetle)
#                Misc.IgnoreObject(i)
        
           
                
# RUN       
main()