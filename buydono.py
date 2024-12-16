while (True):
    Mobiles.UseMobile(0x00004321)
    Gumps.WaitForGump(0x2f815e5c, 10000)
    Gumps.SendAction(0x2f815e5c, 6)
    Misc.Pause(500)
    Misc.ResponsePrompt("63000")
    Misc.Pause(1000)
    Player.ChatSay(86, "[shop")
    Gumps.WaitForGump(0xb34705d2, 10000)
    Gumps.SendAdvancedAction(0xb34705d2, 101, [], [100], ["1"])
    Misc.Pause(1500)
    Misc.IgnoreObject(0x40089AE2) #stack of dono
    coin = Items.FindByID(0x0EF0,-1,Player.Bank.Serial,False,True)
    Items.Move(coin, 0x40089AE2, 1)
    Misc.Pause(650)


    