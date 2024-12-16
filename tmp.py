
petals_str = Items.FindByID(0x1021,0x000e, Player.Backpack.Serial)

if petals_str:
    Items.UseItem(petals_str.Serial)
else:
    Items.UseItem(0x4001298E)