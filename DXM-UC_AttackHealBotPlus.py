from Scripts.utilities.items import FindItem
from System.Collections.Generic import List
from System import Byte
import clr
clr.AddReference('System.Speech')
from System.Speech.Synthesis import SpeechSynthesizer

global HealTarget, curePets, guardingMode
HealTarget = None
guardingMode = False
spk = SpeechSynthesizer()

#===== Settings=====#
captchaGumpId = 1565867016
curePets = False
attackFullHP = True
ignoreSummonModels = False
mode = "Tamer"
if Player.Name == "pp" or Player.Name == "Jimmy Bolas":
    mode = "Dexxer"
#####################

Player.HeadMessage(60,"--ATTACK BOT ON--")

Journal.Clear()
Bandaids = FindItem( 0x0E21, Player.Backpack )
if Bandaids:
    Player.HeadMessage(60,"-Bandaids Found-")
#if not Bandaids:
#    Mobiles.Message(Mobiles.FindBySerial(Player.Serial), 52, 'No bandaids')
#    sys.exit()


def sayTTS(text):
    spk.Speak(text)
    
def GetGM():
    enemyfil = Mobiles.Filter()
    enemyfil.Enabled = True
    enemyfil.RangeMin = 0
    enemyfil.RangeMax = 8
    enemyfil.ZLevelMin = Player.Position.Z -8
    enemyfil.ZLevelMax = Player.Position.Z +8
    enemyfil.CheckLineOfSight = True
    enemyfil.Friend = False
    #enemyfil.IsHuman = True
    enemyfil.Notorieties = List[Byte](bytes([7]))
    enemyList = Mobiles.ApplyFilter(enemyfil)
    gm = Mobiles.Select(enemyList, 'Nearest')
    return gm
    
def AlertCheck():
    while GetGM():
        sayTTS("%s GM Alert" % (Player.Name))
        Misc.Pause(555)
    while Gumps.HasGump(captchaGumpId):
        sayTTS("%s Captcha Alert" % (Player.Name))
        Misc.Pause(666)
    
def Fight():
    global guardingMode
    
    lisSummons = [0x0010, 0x0009]
    
    filter = Mobiles.Filter()
    filter.Enabled = True
    filter.Friend = False
    filter.Notorieties = List[Byte](bytes([3,4,5,6])) #1:cyan 2:green 3:gray 4:criminal 5:orange 6:red 7:yellow
    filter.CheckLineOfSight = True
    filter.RangeMax = 15      
    Mobs = Mobiles.ApplyFilter(filter)
    
    
    
    if mode == "Dexxer":
        if Player.Name == "Boy":
            filter.RangeMax = 11
            Mobs = Mobiles.ApplyFilter(filter)

        weakestMob = Mobiles.Select(Mobs, 'Weakest')
        if weakestMob:
            Player.Attack(weakestMob)
            Misc.Pause(999)
    elif mode == "Tamer":
        filMobs = Mobiles.Filter()
        filMobs.Enabled = True
        filMobs.Friend = True
        filMobs.IsHuman = False
        filMobs.RangeMax = 15
        Pets = Mobiles.ApplyFilter(filMobs)
        
        if not Pets:
            filMobs.IsHuman = True
            Pets = Mobiles.ApplyFilter(filMobs)
            if not Pets:
                Player.HeadMessage(59,"-Fight: no pets found-")

        #Player.HeadMessage(62,"-Fight: iterating mobs-")

        #Pets = [Mobiles.FindBySerial(0x0000B252),Mobiles.FindBySerial(0x000016C8)]
       
        for m in Mobs:
            if (m.Hits == m.HitsMax and not attackFullHP) or (m.MobileID in lisSummons and ignoreSummonModels):
                Misc.NoOperation()
            elif Player.Followers >= 1:
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
        if len(Mobs) == 0:
            if guardingMode:
                for pet in Pets:
                    Misc.UseContextMenu(pet.Serial,"Command: Follow",1000)
                    if Target.WaitForTarget(500):
                        Target.Self()
                    guardingMode = False
                
            thorns = Items.FindByID(0x0F42,0x0042,Player.Backpack.Serial,False)
            if thorns:
                if thorns:
                    Items.UseItem(thorns)
                    PathFinding.PathFindTo(2065,907, 0)
                    Target.WaitForTarget(1500,False)
                    Target.TargetExecute(2065, 908 ,0)
                    Misc.Pause(10000)
def Barding():
    if not Timer.Check("DiscoTimer") and (Player.GetSkillValue('Discordance') >= 70 or Player.GetSkillValue('Peacemaking') >= 70):
        filter = Mobiles.Filter()
        filter.Enabled = True
        filter.Friend = False
        filter.Notorieties = List[Byte](bytes([3,4,5,6])) #1:cyan 2:green 3:gray 4:criminal 5:orange 6:red 7:yellow
        filter.CheckLineOfSight = True
        filter.RangeMax = 4      
        Mobs = Mobiles.ApplyFilter(filter)
        
        if len(Mobs) > 0:
            instrument =  Items.FindByID(0x0E9D, -1, -1) #tambourine
            
            if not instrument:
                instrument =  Items.FindByID(0x0E9E, -1, -1) #tambourine(tassel)
                
            if not instrument:
                instrument =  Items.FindByID(0x0E9C, -1, -1) #drum
                
            if instrument:
                if Target.HasTarget(): 
                    Target.Cancel()
                    Target.ClearQueue()
                    
                if Player.GetSkillValue('Peacemaking') >= 70:
                    Player.UseSkill("Peacemaking")
                else:
                    Player.UseSkill("Discordance")
                Target.WaitForTarget(500, False)
                Target.PerformTargetFromList('closest mob')
                Misc.Pause(150)
                if Target.HasTarget():
                    Target.Cancel()
                    
            Timer.Create("DiscoTimer", 5500)
                
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
    
    if Player.Paralized:
        trappouch = FindItem( 0x09B0, Player.Backpack )
        Items.UseItem(trappouch)
        Misc.Pause( 150 )
    
    if Player.Poisoned:
        if Player.Hits < 60:
            curepot = Items.FindByID(0x0F07,-1,Player.Backpack.Serial,-1,False)
            if curepot:
                Items.UseItem(curepot)
        if Player.Poisoned and Player.GetRealSkillValue("Magery") >= 40.0 and Player.Mana >= 12 and mode != "Dexxer":
            Target.Cancel()
            Target.ClearQueue()
            Spells.Cast("Cure")
            if Target.WaitForTarget(1200):
                Target.Self()
    elif Player.Hits < (Player.HitsMax - 20):
        if not Timer.Check("ChatSpam") and mode == "Tamer":
            Player.ChatSay('all guard me')
            guardingMode = True
            Timer.Create("ChatSpam", 5000)
        if Player.GetRealSkillValue("Magery") >= 40.0 and Player.Mana >= 12 and mode != "Dexxer":
            Target.Cancel()
            Target.ClearQueue()
            Spells.Cast("Greater Heal")
            if Target.WaitForTarget(1500):
                Target.Self()
                Misc.Pause(750)
                Spells.Cast("Magic Reflection")
                
                
        if Player.Hits < 30:
            healpot = Items.FindByID(0x0F0C,-1,Player.Backpack.Serial,-1,False)
            if healpot:
                Items.UseItem(healpot) #Heal Pot
            
    
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

def Buff():
    if Player.Name == "Boy":
        if Player.Dex == 95 or Player.Dex == 115:
            dexpetal = Items.FindByID(0x1021,0x07c6,Player.Backpack.Serial,-1,False)
            if dexpetal: 
                Items.UseItem(dexpetal) #Dex Petal
                Misc.Pause(650)
                poisonpetal = Items.FindByID(0x1021,0x002b,Player.Backpack.Serial,-1,False)
                if poisonpetal: 
                    Items.UseItem(poisonpetal) 
                    Misc.Pause(650)
                cursepetal = Items.FindByID(0x1021,0x082b,Player.Backpack.Serial,-1,False)
                if cursepetal: 
                    Items.UseItem(cursepetal)
                    Misc.Pause(650)
                
        if Player.Dex == 100:    
            dexpot = Items.FindByID(0x0F08,-1,Player.Backpack.Serial,-1,False)
            if dexpot:
                Items.UseItem(dexpot) #Dex Pot
                refreshpot = Items.FindByID(0x0F0B,-1,Player.Backpack.Serial,-1,False)
                if refreshpot:
                    Misc.Pause(100)
                    Items.UseItem(refreshpot)
                    
        if Player.Str == 117:
            strpot = Items.FindByID(0x0F09,-1,Player.Backpack.Serial,-1,False)
            if strpot:
                Misc.Pause(100)
                Items.UseItem(strpot)
                    
while not Player.IsGhost:
    #Player.HeadMessage(61,"~Looping~")
    HealCheck()
    #AlertCheck()
    CheckJournal()
    Barding()
    Fight()
    HealSelf()
    EquipWep()
    Buff()
    Misc.Pause(100)