tool = Items.FindByID(0x12B3,-1,Player.Backpack.Serial,-1,False)

while tool:
    stone = Items.FindByID(0x1779,0x0000,0x403C0EAC,2,False)
    Items.Move(stone, Player.Backpack, 9)
    Misc.Pause(1500)
    Items.UseItem(tool)
    Gumps.WaitForGump(949095101, 10000)
    Misc.Pause(500)
    Gumps.SendAction(949095101, 21)
    Misc.Pause(1500)
    thing = Items.FindByID(0x14F0,-1,Player.Backpack.Serial,-1,False)
    if thing:
        Items.Move(thing, 0x401266E9, 1)
    tool = Items.FindByID(0x12B3,-1,Player.Backpack.Serial,-1,False)