def PickupAnyItem():
    Misc.SendMessage("targRandom")
    targFilter = Items.Filter()
    targFilter.Enabled = True
    targFilter.RangeMax = 1
    targRandom = Items.ApplyFilter(targFilter)
    currentTarg = Items.Select(targRandom, 'Random')
    if currentTarg:
        currentItem = Items.FindBySerial(currentTarg.Serial)
        #Target.TargetExecute(currentTarget.Serial)
        if currentItem:
            Items.Move(currentItem, Player.Backpack,0)

while Player.IsGhost == False:
    PickupAnyItem()
    Misc.Pause(650)