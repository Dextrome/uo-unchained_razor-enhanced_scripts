import sys

def GetPlayers():
    enemyfil = Mobiles.Filter()
    enemyfil.Enabled = True
    enemyfil.RangeMin = 0
    enemyfil.RangeMax = 1
    enemyfil.ZLevelMin = Player.Position.Z -8
    enemyfil.ZLevelMax = Player.Position.Z +8
    enemyfil.CheckLineOfSight = True
    enemyfil.Friend = False
    enemyfil.IsHuman = True
    #enemyfil.Notorieties = List[Byte](bytes([7]))
    enemyList = Mobiles.ApplyFilter(enemyfil)
    return enemyList
    #p = Mobiles.Select(enemyList, 'Nearest')
#    return p

tmpcount = 0

#while Player.IsGhost == False:
while tmpcount < 5:
    Misc.Pause(5)
    StealTargets = GetPlayers()
    
    for StealTarget in StealTargets:
        Misc.SendMessage(StealTarget.Name)
        Items.UseItem(StealTarget.Backpack)
        Misc.Pause(250)
        
        if StealTarget.Backpack:
            for item in StealTarget.Backpack.Contains:
                skipItem = False
                
                if item.ItemID == 0x0E21:
                    skipItem = True
                    Misc.SendMessage("Skipping Bandages")
                elif item.ItemID == 0x1BFB:
                    skipItem = True
                    Misc.SendMessage("Skipping Bolts")
                elif item.ItemID == 0x0F3F:
                    skipItem = True
                    Misc.SendMessage("Skipping Arrows")    
                elif item.ItemID == 0x0A28:
                    skipItem = True
                    Misc.SendMessage("Skipping Candle")    
                elif item.ItemID == 0x71AF:
                    skipItem = True
                    Misc.SendMessage("Skipping Compendium")   
                elif item.ItemID == 0x2254:
                    skipItem = True
                    Misc.SendMessage("Skipping Book of Knowledge")   
                else:
                    for prop in item.Properties:
                        #Misc.SendMessage(prop.ToString())
                        if prop.ToString() == "Blessed":
                            skipItem = True
                            Misc.SendMessage("Skipping Blessed Item")
                        elif prop.ToString() == "<b>Insured</b>":
                            skipItem = True
                            Misc.SendMessage("Skipping Insured Item")    
                    
                        
                if item.IsContainer == False and skipItem == False:  
                    Player.UseSkill("Stealing")
                    Target.WaitForTarget(2000, False)
                    Misc.SendMessage(item.ToString())
                    Target.TargetExecute(item)
                    #Misc.Pause(10000)
                    #sys.exit(99)
                    tmpcount = tmpcount + 1
            
        
