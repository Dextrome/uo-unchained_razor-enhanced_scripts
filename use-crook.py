if Target.HasTarget(): 
    Target.Cancel()
    Target.ClearQueue()
        
crook =  Items.FindByID(0x0E81, -1, Player.Backpack.Serial,True,False) 
        
if crook:
    Items.UseItem(crook)
    Target.WaitForTarget(500,False)