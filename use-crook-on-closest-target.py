if Target.HasTarget(): 
    Target.Cancel()
    Target.ClearQueue()
        
crook =  Items.FindByID(0x0E81, -1, Player.Backpack.Serial,True,False) 
        
if crook and Player.GetSkillValue('Herding') >= 65:
    Items.UseItem(crook)
    Target.WaitForTarget(500, False)
    Misc.Pause(200)
    Target.PerformTargetFromList('closest mob')
    Misc.Pause(150)
    if Target.HasTarget():
        Target.Cancel()