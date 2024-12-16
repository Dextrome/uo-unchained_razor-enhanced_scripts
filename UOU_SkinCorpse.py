beetleSerial = 0x000139FA

filCorpse = Items.Filter()
filCorpse.Enabled = True
filCorpse.Movable = False
filCorpse.OnGround = True
filCorpse.RangeMax = 2
filCorpse.CheckIgnoreObject = True
lisCorpses = Items.ApplyFilter(filCorpse)

dagger = Items.FindByID(0x0F52,-1,Player.Backpack.Serial)
if not dagger:
    Player.HeadMessage(50,"No dagger found")
    sys.exit()
scissors = Items.FindByID(0x0F9F,-1,Player.Backpack.Serial)
if not scissors:
    Player.HeadMessage(50,"No scissors found")
    sys.exit()

bodyCorpse = None
if len(lisCorpses) >= 1: 
    for i in lisCorpses:
        if i.ItemID == 0x2006:
            Items.UseItem(i)
            Misc.Pause(700)
            Items.UseItem(dagger)
            Target.WaitForTarget(700,0)
            Target.TargetExecute(i)
            Misc.Pause(500)
            for k in i.Contains:
                if k.ItemID == 0x1079:
                    Items.UseItem(scissors)
                    Target.WaitForTarget(700,0)
                    Target.TargetExecute(k)
                    Misc.Pause(700)
            leather = Items.FindByID(0x1081,-1, i.Serial)
            if leather: 
                #Player.HeadMessage(50, "Leather Found")
                Misc.Pause(100)
                Items.Move(leather.Serial,Player.Backpack.Serial,-1)
                Misc.Pause(700)
                if Player.Mount: 
                    Mobiles.UseMobile(Player.Serial)
                    Misc.Pause(300)
                    beetle = Mobiles.FindBySerial(beetleSerial)
                    leather = Items.FindByID(0x1081,-1, Player.Backpack.Serial)
                    if beetle:      
                        Items.Move(leather.Serial, beetle.Backpack,-1)
                        Misc.Pause(700)
                        Mobiles.UseMobile(beetle)
        Misc.IgnoreObject(i)
                    
            #Player.HeadMessage(5,"Found corpse")
    
 