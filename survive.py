from Scripts.utilities.items import FindItem

Misc.SendMessage( 'Survive Script Running', 65)

counter = 0

while not Player.IsGhost:
    Misc.Pause( 150 )
    counter += 1
    
    if counter == 20:
        counter = 0
        Misc.SendMessage( 'Survive Script Running', 65)
    
    #Un-paralyze
    if Player.Paralized:
        trappouch = FindItem( 0x09B0, Player.Backpack )
        Items.UseItem(trappouch)
        Misc.Pause( 150 )
        
        
    #Refresh
    if Player.Stam <= Player.StamMax - 5:
        pot = Items.FindByID(0x0F0B,0,Player.Backpack.Serial,True)
        if pot:
            Items.UseItem(pot)
            Misc.Pause(650)
    
    #Strength
    if Player.Str < 100:
        pot = Items.FindByID(0x0F09,0,Player.Backpack.Serial,True)
        if pot:
            Items.UseItem(pot)
            Misc.Pause(650)
            
    #Cure
    if Player.Poisoned:
        pot = Items.FindByID(0x0F07,0,Player.Backpack.Serial,True)
        if pot:
            Items.UseItem(pot)
            Misc.Pause(650)
        
        if Player.Poisoned and Player.GetSkillValue('Magery') >= 60:
            Spells.CastMagery('Cure')
            Target.WaitForTarget(1500)
            Target.Self()

    #Heal (Bandages are handled by bandage_self script)
    if Player.GetSkillValue('Healing') >= 50:
        if not Misc.ScriptStatus('bandage_self.py'):
            Misc.ScriptRun('bandage_self.py')

    if Player.Hits <= 70:
        pot = Items.FindByID(0x0F0C,0,Player.Backpack.Serial,True)
        if pot:
            Items.UseItem(pot)
            Misc.Pause(650)
    
    if Player.GetSkillValue('Magery') >= 80:
        if Player.Poisoned:
            Spells.CastMagery('Cure')
            Target.WaitForTarget(1500)
            Target.Self()
        else:
            if Player.Hits < 75:
                if Player.Hits < 30:
                    Spells.CastMagery('Heal')
                    Target.WaitForTarget(1500)
                    Target.Self()
                else:
                    Spells.CastMagery('Greater Heal')
                    Target.WaitForTarget(1500)
                    Target.Self()
            elif Player.Hits < 90:
                Spells.CastMagery('Heal')
                Target.WaitForTarget(1500)
                Target.Self()