PathFinding.PathFindTo(1465,1617,20)
Misc.Pause(250)
PathFinding.PathFindTo(1467,1594,20)
Misc.Pause(500)

for i in range(3):
    Misc.WaitForContext(0x00000DA5, 10000)
    Misc.ContextReply(0x00000DA5, 1)
    Misc.Pause(500)
    Gumps.WaitForGump(2611865322, 10000)
    Misc.Pause(500)
    Gumps.SendAction(2611865322, 1)
    Misc.Pause(500)
    
PathFinding.PathFindTo(1465,1617,20)
Misc.Pause(250)
PathFinding.PathFindTo(1464,1670,0)
Misc.Pause(500)
    
for i in range(3):
    Misc.WaitForContext(0x00000D8A, 10000)
    Misc.ContextReply(0x00000D8A, 1)
    Misc.Pause(500)
    Gumps.WaitForGump(2611865322, 10000)
    Misc.Pause(500)
    Gumps.SendAction(2611865322, 1)
    Misc.Pause(500)    
    
PathFinding.PathFindTo(1465,1646,20)
Misc.Pause(250) 
PathFinding.PathFindTo(1459,1617,20)
Misc.Pause(250) 
PathFinding.PathFindTo(1451,1616,41)

if Player.Name != "DXM":
    bod = Items.FindByID(0x14EF,-1,Player.Backpack.Serial,-1,False)
    while bod:
        Items.DropItemGroundSelf(bod.Serial,1)
        Misc.Pause(750)
        bod = Items.FindByID(0x14EF,-1,Player.Backpack.Serial,-1,False)