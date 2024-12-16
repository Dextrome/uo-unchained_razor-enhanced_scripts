while True:
    for item in Player.Backpack.Contains:    
        Items.UseItem(0x400B6F99)
        Misc.Pause(1650)
        Gumps.SendAction(0x38920abd, 14)
        Misc.Pause(1650)
        Target.TargetExecute(item)
        
    Player.GuildButton()
    Misc.Pause(2500)
    Gumps.SendAction(516474935, 15)
    Misc.Pause(2500)
        
    for item in Player.Backpack.Contains:
        if item.ItemID == 0x1BF2:
            Misc.SendMessage('Moving %s to Guild Treasury' % (item.Name))
            Gumps.SendAction(1478311224, 100) #add to guild buff treasury
            Target.WaitForTarget(2500, False)
            Misc.Pause(50)
            Target.TargetExecute(item)
            Misc.Pause(100)
            
    Misc.Pause(31000)   
    Misc.WaitForContext(0x00004D68, 10000)
    Misc.Pause(150)
    Misc.ContextReply(0x00004D68, 1)
    Misc.Pause(150)