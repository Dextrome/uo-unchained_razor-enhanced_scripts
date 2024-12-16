vendor = Target.PromptTarget("Target Vendor NPC")

for i in range(3):
    Misc.WaitForContext(vendor, 10000)
    Misc.ContextReply(vendor, 1)
    Misc.Pause(500)
    Gumps.WaitForGump(2611865322, 10000)
    Misc.Pause(500)
    Gumps.SendAction(2611865322, 1)
    Misc.Pause(500)
    
    
    
    
    
    
    
    
