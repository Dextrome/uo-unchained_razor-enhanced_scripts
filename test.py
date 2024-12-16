from Scripts.utilities.items import FindItem

while not Player.IsGhost:
    Misc.Pause( 25 )
    
    if Player.Paralized:
        trappouch = FindItem( 0x09B0, Player.Backpack )
        Items.UseItem(trappouch)
        Misc.Pause( 150 )