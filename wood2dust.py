toolserial = Target.PromptTarget("target tool")

while True:
    Items.UseItem(0x402DD22C)
    Misc.Pause(650)
    Gumps.WaitForGump(111922706, 10000)
    #Gumps.SendAction(111922706, 11) #normal boardz
    #Gumps.SendAction(111922706, 12) #oak boardz
    #Gumps.SendAction(111922706, 14) #yew boardz
    Gumps.SendAction(111922706, 1) #iron ingots
    Misc.Pause(100)
    Items.UseItem(toolserial) #tool


    for i in range(1,100):
        Gumps.WaitForGump(949095101, 10000) #craft menu
        Gumps.SendAction(949095101, 21) #make last
        Gumps.WaitForGump(949095101, 10000) #craft menu
        
#        staff = Items.FindByID(0x0E89,-1,Player.Backpack.Serial,-1,False)
#        if staff:
#            Items.Move(staff, 0x401A433A, 1)
#            Misc.Pause(650)

#        bow = Items.FindByID(0x13B2,-1,Player.Backpack.Serial,-1,False)
#        if bow:
#            Items.Move(bow, 0x401A433A, 1)
#            Misc.Pause(650)
            
        dagger = Items.FindByID(0x0F52,-1,Player.Backpack.Serial,-1,False)
        if dagger:
            Items.Move(dagger, 0x401A433A, 1)
            Misc.Pause(650)

    Misc.WaitForContext(0x401A433A, 10000)
    Misc.ContextReply(0x401A433A, 0)
    Misc.Pause(650)
    Misc.WaitForContext(0x401B271D, 10000)
    Misc.ContextReply(0x401B271D, 1)
    Target.WaitForTarget(10000, False)
    dust = Items.FindByID(0x5745,-1,Player.Backpack.Serial,-1,False)
    if dust:
        Target.TargetExecute(dust)
        Target.WaitForTarget(10000, False)
        Target.Cancel( )
        Gumps.WaitForGump(2834126535, 10000)
        Gumps.SendAction(2834126535, 0)
    else:
        Target.Cancel( )
