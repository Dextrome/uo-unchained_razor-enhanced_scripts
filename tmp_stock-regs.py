shelf = 0x401F6BEB
vendor1 = 0x000039B5
vendor2 = 0x00002322

while True:
    Misc.WaitForContext(vendor1, 10000)
    Misc.ContextReply(vendor1, 2)
    Misc.Pause(500)
    
    Misc.WaitForContext(shelf, 10000)
    Misc.ContextReply(shelf, 3)
    Target.WaitForTarget(10000, False)
    Misc.Pause(500)
    Target.Self()
    Misc.Pause(5000)
    
    Misc.WaitForContext(vendor2, 10000)
    Misc.ContextReply(vendor2, 2)
    Misc.Pause(500)
    
    Misc.WaitForContext(shelf, 10000)
    Misc.ContextReply(shelf, 3)
    Target.WaitForTarget(10000, False)
    Misc.Pause(500)
    Target.Self()
    Misc.Pause(60000)
    