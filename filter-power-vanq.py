from Scripts.utilities.items import MoveItem
from Scripts import config



sourceBox = Target.PromptTarget( 'Select container to move items out of' )
sourceBoxItem = Items.FindBySerial( sourceBox )
if sourceBoxItem == None:
    sourceBox = Mobiles.FindBySerial( sourceBox ).Backpack
else:
    sourceBox = sourceBoxItem
    
targetBox = Target.PromptTarget( 'Select container to move items into' )
targetBoxItem = Items.FindBySerial( targetBox )
if targetBoxItem == None:
    targetBox = Mobiles.FindBySerial( targetBox ).Backpack
else:
    targetBox = targetBoxItem

Items.UseItem( sourceBox )
Misc.Pause( config.dragDelayMilliseconds )

Items.UseItem( targetBox )
Misc.Pause( config.dragDelayMilliseconds )


for i in sourceBox.Contains:
    Journal.Clear()
    Items.SingleClick(i.Serial)
    Misc.Pause(200)
    if Journal.Search("Vanquishing") or Journal.Search("Invulnerability") or Journal.Search("Supremely Accurate") or ((Journal.Search("Exceedingly Accurate") or Journal.Search("Eminently Accurate")) and Journal.Search("Power")):
        MoveItem( Items, Misc, i, targetBox )