from Scripts.utilities.items import FindItem

done = False
trappouch = FindItem( 0x09B0, Player.Backpack )

while not done:
    Misc.Pause(150)
    Spells.CastMagery("Magic Trap")
    
    Misc.Pause(1000)
    Target.TargetExecute(trappouch)
    
    Items.SingleClick(trappouch.Serial)
    
    regularText = Journal.GetTextByType( 'Label' )
    regularText.Reverse()
    
    for line in regularText[ 0 : 20 ]:
        if line == 'a pouch [Charges 10/10]':
            Player.ChatSay("woop")
            done = True
            Misc.Pause(1000)
            break


