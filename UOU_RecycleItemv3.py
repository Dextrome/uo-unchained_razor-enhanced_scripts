Journal.Clear()
global saw, dragDelay
saw = Items.FindByID(0x1034,0x0000,Player.Backpack.Serial)
dragDelay = 700

def recycle(magic):
    global saw
    
    theContainer = Items.FindBySerial(magic.Container)
    for i in theContainer.Contains:
        Journal.Clear()
        Items.SingleClick(i.Serial)
        Misc.Pause(200)
        if Journal.Search("Unidentified"): 
            Items.Move(i, Player.Backpack.Serial, 1)
            Misc.Pause(dragDelay)
            if Target.HasTarget(): 
                Target.TargetExecute(i)
                Target.WaitForTarget(700,0)
            elif Gumps.HasGump():
                Gumps.SendAction(949095101, 63)
                Target.WaitForTarget(1000,0)
                Target.TargetExecute(i)
                Target.WaitForTarget(700,0)
            else:
                Player.HeadMessage(1000,"Using Saw")
                Items.UseItem(saw)
                Gumps.WaitForGump(949095101, 1500)
                Gumps.SendAction(949095101, 63)
                Target.WaitForTarget(1000,0)
                Target.TargetExecute(i)
                Target.WaitForTarget(700,0)
                

if saw: 
    magic = Items.FindBySerial(Target.PromptTarget("Select item to destroy", 1000))

    recycle(magic)
    
    if Gumps.HasGump(): 
        Gumps.CloseGump(Gumps.CurrentGump())
    Target.WaitForTarget(500,0)
    if Target.HasTarget():
        Target.Cancel()
    
else:
    Player.HeadMessage(5,"No saws in backpack")
    
