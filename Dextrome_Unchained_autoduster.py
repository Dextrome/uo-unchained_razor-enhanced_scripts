###########DEXTROME UNCHAINED ---- AUTO DUSTER#############
###########################################################
# Drags magic items from nearby corpses to dustbag        #
# Set your dustbag serial in the parameters section       #
# Set also_loot_gold to True if you want to autoloot gold #
###########################################################
from System.Collections.Generic import List
from System import Byte, Int32

#PARAMETERS
dustbag = 0x4017E0F1
if Player.Name == 'Boy':
    dustbag = 0x40014939
if Player.Name == 'Pistik':
    dustbag = 0x40146456
    
#Settings
autodust = True
also_loot_gold = False
skinning = False
scavenging = False

#Ids
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
daggerId = 0x0F52
scissorsId = 0x0F9F

ignore_list = [citrine,amber,amethyst,ruby,emerald,diamond,sapphire,tourmaline,starsapph]

#LOOT
filCorpse = Items.Filter()
filCorpse.Enabled = True
filCorpse.Movable = False
filCorpse.OnGround = True
filCorpse.RangeMin = 0
filCorpse.RangeMax = 2
filCorpse.Graphics = List[Int32]([0x2006]) 
filCorpse.IsCorpse = True
filCorpse.CheckIgnoreObject = False
lisCorpses = Items.ApplyFilter(filCorpse)


if len(lisCorpses) >= 1: 
    for corpse in lisCorpses:
        Items.UseItem(corpse)
        Misc.Pause(650)
        
        #skinning / scavenging
        if skinning == False and scavenging == True:
            Player.UseSkill("Begging")
            Target.WaitForTarget(2500,False)
            Target.TargetExecute(corpse)
        elif skinning == True:
            if 'the remains of' in corpse.Name and 'ancient' not in corpse.Name and 'frozen lich' not in corpse.Name and 'Meta-Pet' not in corpse.Name and scavenging == True: #humanoid corpse
                Player.UseSkill("Begging")
                Target.WaitForTarget(2500,False)
                Target.TargetExecute(corpse)
            else:
                dagger = Items.FindByID(daggerId,-1,Player.Backpack.Serial,-1,False)
                if dagger:
                    Items.UseItem(dagger)
                    Target.WaitForTarget(2500,False)
                    Target.TargetExecute(corpse)
                    Misc.Pause(650)

        for i in corpse.Contains: #handle items on corpse
            if skinning == True:
                if i.ItemID == 0x1079: #hides
                    scissors = Items.FindByID(scissorsId,-1,Player.Backpack.Serial,-1,False)
                    if scissors:
                        Items.UseItem(scissors)
                        Target.WaitForTarget(2500,False)
                        Target.TargetExecute(i)
                        Misc.Pause(650)
                        leather = Items.FindByID(0x1081,-1,corpse.Serial,2,False)
                        Items.Move(leather,Player.Backpack,-1 ) # -1 -> all, for stackable items
                        Misc.Pause(650)
                
            if autodust == True:
                if i.ItemID not in ignore_list:
                    Journal.Clear()
                    Items.SingleClick(i.Serial)
                    Misc.Pause(175)
                    if Journal.Search("Unidentified"): 
                        Items.Move(i,dustbag,1)
                    elif i.ItemID == gold_ID and also_loot_gold:
                        Items.Move(i,Player.Backpack,-1 ) # -1 -> all, for stackable items
                        Misc.Pause(650)
            elif also_loot_gold:
                if i.ItemID == gold_ID and also_loot_gold:
                    Items.Move(i,Player.Backpack,-1 ) # -1 -> all, for stackable items
                    Misc.Pause(650)
