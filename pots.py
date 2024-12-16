from System import Byte, Int32


while not Player.IsGhost:
    Misc.Pause(600)
    Gumps.WaitForGump(2834126535, 10000)
    Misc.Pause(250)
    Gumps.SendAction(2834126535, 18)
    Misc.Pause(750)
    bluepots = Items.FindByID(0x0F08, -1, -1)
    Misc.Pause(750)
    Items.Move(bluepots.Serial, 0x40020BE9, 100)
    Misc.Pause(500)
    Gumps.SendAction(2834126535, 1450)
    Misc.Pause(500)
    emptypots = Items.FindByID(0x0F0E, -1, Player.Backpack.Serial)
    Misc.Pause(250)
    Target.TargetExecute(emptypots)
    Misc.Pause(500)
    Target.TargetExecute(0x40020BE9)
    Misc.Pause(1500)
    Target.Cancel( )





