from Scripts.utilities.items import MoveItem
from Scripts import config

def Store():
    Items.UseItem(0x4002D26E)
    Gumps.WaitForGump(2834126535, 10000)
    Misc.Pause(250)
    Gumps.SendAction(2834126535, 1464)
    Misc.Pause(250)
    Gumps.WaitForGump(2834126535, 10000)
    Misc.Pause(150)
    Gumps.SendAction(2834126535, 0)
    Misc.Pause(250)
    Target.WaitForTarget(10000, False)
    Misc.Pause(250)
    Target.Self()
    Misc.Pause(150)
    Gumps.SendAction(2834126535, 0)
    Misc.Pause(950)

petalContainer=Items.FindBySerial(0x4051E335)

for item in petalContainer.Contains:
    Misc.Pause(50)
    if Player.Weight > 300:
        Store()
    else:
        if item.ItemID == 0x234D or item.ItemID == 0xBC86:
            Items.UseItem(item)
            
            
Store()


