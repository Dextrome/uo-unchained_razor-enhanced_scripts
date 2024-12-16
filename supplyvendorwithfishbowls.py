vaultserial = 0x40679A23
vendorserial = 0x40177A39
#open bank vault
vault = Items.FindBySerial(vaultserial)
Items.UseItem( vault )
Misc.Pause( 650 )
bowls = Items.FindByID(0x70B9,-1,Player.Bank.Serial, 2)
if bowls:
    Items.Move(bowls.Serial, vendorserial, 75)
    Misc.Pause( 650 )