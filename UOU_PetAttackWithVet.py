from Scripts.utilities.items import FindItem
from System.Collections.Generic import List
from System import Byte

global HealTarget, curePets, guardingMode
HealTarget = None
guardingMode = False

#===== Settings=====#
curePets = False
attackFullHP = True
ignoreSummonModels = False
#####################

Player.HeadMessage(60,"--ATTACK BOT ON--")

Journal.Clear()
Bandaids = FindItem( 0x0E21, Player.Backpack )
if Bandaids:
    Player.HeadMessage(60,"-Bandaids Found-")
#if not Bandaids:
#    Mobiles.Message(Mobiles.FindBySerial(Player.Serial), 52, 'No bandaids')
#    sys.exit()
    
def Fight():
    global guardingMode
    
    lisSummons = [0x0010, 0x0009]
    
    filter = Mobiles.Filter()
    filter.Enabled = True
    filter.Friend = False
    filter.Notorieties = List[Byte](bytes([3,4,5,6])) #1:cyan 2:green 3:gray 4:criminal 5:orange 6:red 7:yellow
    filter.CheckLineOfSight = True
    filter.RangeMax = 14      
    Mobs = Mobiles.ApplyFilter(filter)
    
    #weakestMob = Mobiles.Select(Mobs, 'Weakest')
    closestMob = Mobiles.Select(Mobs, 'Nearest')
    
    filMobs = Mobiles.Filter()
    filMobs.Enabled = True
    filMobs.Friend = True
    filMobs.IsHuman = False
    filMobs.RangeMax = 15
    Pets = Mobiles.ApplyFilter(filMobs)
    
    #if not Pets:
        #Player.HeadMessage(59,"-Fight: no pets found-")

    #Player.HeadMessage(62,"-Fight: iterating mobs-")

    #Pets = [Mobiles.FindBySerial(0x0000B252),Mobiles.FindBySerial(0x000016C8)]
    
    if Player.Followers < 2:
        if closestMob:
            Player.Attack(closestMob)
            Misc.Pause(500)
    else:
        for m in Mobs:
            if (m.Hits == m.HitsMax and not attackFullHP) or (m.MobileID in lisSummons and ignoreSummonModels):
                Misc.NoOperation()
            elif Player.Followers >= 2:
                if not Pets:
                    Player.Attack(m)
                    Misc.Pause(500)
                else:
                    for pet in Pets:
                        if pet.CanRename:
                            if not pet.WarMode and pet.Hits >= 23:
                                if Target.HasTarget(): 
                                    Target.Cancel()
                                Target.ClearQueue()
                                Misc.UseContextMenu(pet.Serial,"Command: Kill",1000)
                                if Target.WaitForTarget(500):
                                    Target.TargetExecute(m)
                                    Player.Attack(m)
                            if not guardingMode:
                                Misc.UseContextMenu(pet.Serial,"Command: Guard",1000)
                                guardingMode = True
        if len(Mobs) == 0 and guardingMode:
            for pet in Pets:
                Misc.UseContextMenu(pet.Serial,"Command: Follow",1000)
                if Target.WaitForTarget(500):
                    Target.Self()
                guardingMode = False
        
    
def UseBandaid(Heal):
    global HealTarget
    
    if not Target.HasTarget():
        Target.ClearQueue()
        lastTarget = Target.GetLast()
        Bandaids = Items.FindByID(0x0E21, -1, Player.Backpack.Serial)
        if Bandaids:
            Items.UseItemByID(0x0E21, -1)
            Target.WaitForTarget(1000)
            if Target.HasTarget():
                Target.TargetExecute(Heal.Serial)
                Misc.Pause(150)
            else:
                Misc.SendMessage('No bandaid target')
        else:
            Mobiles.Message(Mobiles.FindBySerial(Player.Serial), 52, 'No bandaids')
            Misc.Pause(500)
        
        lastMob = Mobiles.FindBySerial(lastTarget)
        if lastMob:
            Target.SetLast(lastMob)
        HealTarget = Heal
        
def Cure(Heal):
    if Player.GetRealSkillValue('Magery') >= 40.0:
        if Target.HasTarget():
            Target.Cancel()
        Spells.Cast('Cure')
        Target.WaitForTarget(1200)
        Target.TargetExecute(Heal)
        
def HealSelf():
    global guardingMode
    
    if Player.Poisoned and Player.GetRealSkillValue("Magery") >= 40.0 and Player.Mana >= 12:
        Target.Cancel()
        Target.ClearQueue()
        Spells.Cast("Cure")
        if Target.WaitForTarget(1200):
            Target.Self()
    elif Player.Hits < (Player.HitsMax - 20):
        if not Timer.Check("ChatSpam"):
            Player.ChatSay('all guard me')
            guardingMode = True
            Timer.Create("ChatSpam", 5000)
        if Player.GetRealSkillValue("Magery") >= 40.0 and Player.Mana >= 12:
            Target.Cancel()
            Target.ClearQueue()
            Spells.Cast("Greater Heal")
            if Target.WaitForTarget(1500):
                Target.Self()
                Misc.Pause(750)
                Spells.Cast("Reactive Armor")
            
    
def HealCheck():
    filMobs = Mobiles.Filter()
    filMobs.Enabled = True
    filMobs.Friend = True
    filMobs.IsHuman = True
    filMobs.RangeMax = 2       
    Mobs = Mobiles.ApplyFilter(filMobs)
    Heal = False
    
    for m in Mobs:
        if (m.Hits < m.HitsMax-10 or m.Poisoned) and not m.IsGhost and Player.GetRealSkillValue("Healing") >= 40.0:
            Heal = m
            UseBandaid(Heal)
    if not Heal and Player.GetRealSkillValue("Healing") >= 40.0:
        if Player.Hits < Player.HitsMax or Player.Poisoned and not Player.IsGhost:
            Heal = Mobiles.FindBySerial(Player.Serial)
            UseBandaid(Heal)
    if not Heal and Player.GetRealSkillValue("Veterinary") >= 40.0 and Player.Followers > 0:
        lowestPet = False
        deadPet = False
        filMobs = Mobiles.Filter()
        filMobs.Enabled = True
        filMobs.Friend = True
        filMobs.IsHuman = False
        filMobs.RangeMax = 15       
        Pets = Mobiles.ApplyFilter(filMobs)          
        
        for mob in Pets:
            if (mob.Hits < mob.HitsMax or mob.Poisoned) and not mob.Hits == 0:
                if not lowestPet:
                    lowestPet = mob
                elif mob.Hits < lowestPet.Hits:
                    lowestPet = mob
            if mob.CanRename and (mob.Hits < mob.HitsMax or mob.Poisoned) and mob.Hits == 0:
                deadPet = mob
        if lowestPet:
            if Player.DistanceTo(lowestPet) > 3 and lowestPet.Hits <= 10 and not Timer.Check("ChatSpam") and lowestPet.CanRename:
                if Target.HasTarget():
                    Target.Cancel()
                Misc.UseContextMenu(lowestPet.Serial,"Command: Follow",1000)
                if Target.WaitForTarget(500):
                    Target.Self()
                Timer.Create("ChatSpam", 5000)
            if Player.DistanceTo(lowestPet) <= 3:
                UseBandaid(lowestPet)
                if curePets and lowestPet.Poisoned: Cure(lowestPet)
            elif not Timer.Check("NotifSpam"):
                Mobiles.Message(lowestPet, 52, "Out of range")
                Timer.Create("NotifSpam", 4000)
                if curePets and lowestPet.Poisoned: Cure(lowestPet)
                
                filMobs = Mobiles.Filter()
                filMobs.Enabled = True
                filMobs.Friend = True
                filMobs.IsHuman = False
                filMobs.RangeMax = 2       
                Pets = Mobiles.ApplyFilter(filMobs) 
                
                strongestPet = Mobiles.Select(Pets,"Strongest")
                
                filMobs = Mobiles.Filter()
                filMobs.Enabled = True
                filMobs.Friend = False
                filMobs.IsHuman = False
                filMobs.RangeMax = 3
                
                Mobs = Mobiles.ApplyFilter(filMobs)
                
                for p in Pets: #Check all pet positions relative to all mobs nearby
                    for m in Mobs:
                        if not p.WarMode and p.CanRename:
                            if Target.HasTarget(): 
                                Target.Cancel()
                            Target.ClearQueue()
                            Misc.UseContextMenu(p.Serial,"Command: Kill",1000)
                            if Target.WaitForTarget(500):
                                Target.TargetExecute(m)
                            break
                    
                if strongestPet:
                    UseBandaid(strongestPet)
                
        elif deadPet:
            UseBandaid(deadPet)

def CheckJournal():
    hardBreak = 0
    timeout = 6000
    while Journal.SearchByType("You begin applying","System") and not Player.IsGhost:
        if Journal.SearchByType("You finish applying", "System"):
            break
        if Journal.SearchByType("You are too far away","System"):
            break
        if Journal.SearchByType("You fail to", "System"):
            break
        if Journal.SearchByType("You are able to", "System"):
            break
        if Journal.SearchByType("You have cured", "System"):
            break
        if Journal.SearchByType("You did not stay", "System"):
            break
        if Journal.SearchByType("You heal what little", "System"):
            break
        if Journal.SearchByType("You bind the wound", "System"):
            break
        if Journal.SearchByType("You apply the bandages, but", "System"):
            break
        if hardBreak >= timeout:
            Player.HeadMessage(35,"Hard time limit reached check journal for message")
            break
        hardBreak += 10
        if hardBreak % 1000 == 0:
            Mobiles.Message(HealTarget, 52, "%d" %(hardBreak/1000))
        if Player.DistanceTo(HealTarget) > 3 and HealTarget.Hits <= 10 and not Timer.Check("ChatSpam") and HealTarget.CanRename:
            Misc.UseContextMenu(HealTarget.Serial,"Command: Follow",1000)
            if Target.WaitForTarget(500):
                Target.Self()
        if curePets and HealTarget.Poisoned: 
            Cure(HealTarget)
        Fight()
        HealSelf()
        Misc.Pause(10)
    Journal.Clear()
        
        
def EquipWep():
    if Player.GetRealSkillValue("Archery") >= 40.0:
        weptype = "bow"
        lisArcheryWeps = [0x13B2, 0x26C3, 0x26C2]
        leftwep = Player.GetItemOnLayer("LeftHand")
        rightwep = Player.GetItemOnLayer("RightHand")
        
        try:
            if rightwep.ItemID == 0x0EFA and weptype == "spellbook":
                return
            elif rightwep.ItemID == 0x0EFA:
                Player.UnEquipItemByLayer("RightHand",True)
                Misc.Pause(750)
        except:
            Misc.Pause(5)
        try:
            if leftwep.ItemID in lisArcheryWeps and weptype == "bow":
                return
            elif leftwep.ItemID in lisArcheryWeps:
                Player.UnEquipItemByLayer("LeftHand",True)
                Misc.Pause(750)
        except:
            Misc.Pause(5)
   
        if weptype == "spellbook":
            book = Items.FindByID(0x0EFA,-1,Player.Backpack.Serial)
            if book: 
                Player.EquipItem(book)
                Misc.Pause(1000)
                return
        elif weptype == "bow":
            for i in lisArcheryWeps:
                wep = Items.FindByID(i, -1, Player.Backpack.Serial)
                if wep: 
                    Player.EquipItem(wep)
                    Misc.Pause(750)
                    return
            
while not Player.IsGhost:
    #Player.HeadMessage(61,"~Looping~")
    HealCheck()
    CheckJournal()
    Fight()
    HealSelf()
    EquipWep()
    Misc.Pause(500)