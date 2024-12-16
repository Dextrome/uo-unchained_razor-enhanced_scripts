while True:
    Misc.Pause(1000)
    Misc.WaitForContext(0x00005BB2, 10000)
    Misc.ContextReply(0x00005BB2, 1)
    Misc.Pause(5000)
    bolts = Items.FindByID(0x0F95,-1,Player.Backpack.Serial,-1,False)
    
    if bolts:
        Items.UseItem(0x403654E2)
        Misc.Pause(500)
        Target.WaitForTarget(10000, False)
        Target.TargetExecute(bolts)
        Misc.Pause(5000)
        Items.UseItem(0x402DD22C)
        Misc.Pause(10000)
        Gumps.SendAction(111922706, 123)
        Misc.Pause(10000)