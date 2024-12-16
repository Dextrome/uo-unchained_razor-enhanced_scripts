while True:
    thing = Items.FindByID(0x0F39,-1,Player.Backpack.Serial,-1,False) #shovel
    #thing = Items.FindByID(0x097F,-1,Player.Backpack.Serial,-1,False) #skillet
    if thing:
        Target.TargetExecute(thing)
        Misc.Pause(1000)
        Gumps.WaitForGump(0x6abce12, 10000)
        Gumps.SendAction(0x6abce12, 122)
        Target.TargetExecute(thing)
        Misc.Pause(500)

    ingots = Items.FindByID(0x1BF2,-1,Player.Backpack.Serial,-1,False)
    if ingots:
        ingotsAmount = ingots.Amount
        if ingotsAmount < 4:
            Gumps.WaitForGump(0x6abce12, 2000)
            Gumps.SendAction(0x6abce12, 1)
            Misc.Pause(1000)
        else:
            Gumps.WaitForGump(0x38920abd, 2000)
            Gumps.SendAction(0x38920abd, 21)
            Misc.Pause(1000)
    else:
            Gumps.WaitForGump(0x6abce12, 2000)
            Gumps.SendAction(0x6abce12, 1)
            Misc.Pause(1000)
