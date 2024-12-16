while True:
    if not Gumps.HasGump(0xdb32a94d): 
        Items.UseItem(0x4001F3C8)
        Gumps.WaitForGump(0xdb32a94d,1000)
        Misc.Pause(150)
    
    else:
        jackpotText = Gumps.GetGumpRawText(0xdb32a94d)[7]
        #Misc.SendMessage(jackpotText)
        if jackpotText:
            jackpotAmount = [int(s) for s in jackpotText.split() if s.isdigit()][0]

            if jackpotAmount > 123456:
                Gumps.WaitForGump(0xdb32a94d, 1000)
                Misc.Pause(55)
                Gumps.SendAction(0xdb32a94d, 1)
                Misc.Pause(105)
            else:
                break