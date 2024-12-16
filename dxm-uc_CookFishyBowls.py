tool = Target.PromptTarget("target skillet")
while (True):
    Items.UseItem(0x40035DF6)
    Gumps.WaitForGump(0x6abce12, 10000)
    Gumps.SendAction(0x6abce12, 26)
    Misc.Pause(150)
    Items.UseItem(tool)
    Gumps.WaitForGump(0x38920abd, 10000)
    Misc.Pause(150)
    Gumps.SendAction(0x38920abd, 29)
    Gumps.WaitForGump(0x38920abd, 10000)
    Gumps.SendAction(0x38920abd, 16)
    Misc.Pause(1250)

    cookedSteaks = Items.FindByID(0x097B,0x0000,Player.Backpack.Serial,-1,False)
    if cookedSteaks:
        if cookedSteaks.Amount >= 5:
            Items.UseItem(tool)
            Gumps.WaitForGump(0x38920abd, 10000)
            Misc.Pause(150)
            Gumps.SendAction(0x38920abd, 43)
            Gumps.WaitForGump(0x38920abd, 10000)
            Gumps.SendAction(0x38920abd, 30)
            Misc.Pause(1250)
        
    fishyBowls = Items.FindByID(0x70B9,0x0000,Player.Backpack.Serial,-1,False)
    if fishyBowls:
        if fishyBowls.Amount >= 100:
            Items.UseItem(0x40035DF6)
            Gumps.WaitForGump(0x6abce12, 10000)
            Gumps.SendAction(0x6abce12, 111)
            Misc.Pause(250)