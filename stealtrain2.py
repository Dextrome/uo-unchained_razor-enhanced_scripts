#horse = Target.PromptTarget()
box = Target.PromptTarget()
while True:    
    #bottles = Items.FindByID(0x0F0E,-1,Player.Backpack.Serial)
    item2steal = Items.FindBySerial(0x4016823A)
    if item2steal:
        Items.Move(item2steal,box,0)
        Misc.Pause(1000)
    Player.UseSkill("Stealing")
    Misc.Pause(100)
    Target.WaitForTarget(10000)
    item2steal = Items.FindBySerial(0x4016823A)
    if item2steal:
        Target.TargetExecute(item2steal)
        Misc.Pause(10600)