
from Scripts.glossary.items.armor import armor
from Scripts.glossary.items.shields import shields
from Scripts.glossary.items.weapons import weapons
from Scripts.utilities.items import MoveItem
from Scripts.glossary.colors import colors
from Scripts import config

sourceBox = Target.PromptTarget( 'Select container containing unidentified items' )
sourceBox = Items.FindBySerial( sourceBox )
if sourceBox == None or not sourceBox.IsContainer:
    Misc.SendMessage( 'Invalid selection for container to identify! Stopping script', colors[ 'red' ] )
    Stop

targetBox = Target.PromptTarget( 'Select container to move items into' )
targetBox = Items.FindBySerial( targetBox )
if targetBox == None or not targetBox.IsContainer:
    Misc.SendMessage( 'Invalid selection for targetBox! Stopping script', colors[ 'red' ] )
    Stop
    
Items.UseItem( sourceBox )
Misc.Pause( config.dragDelayMilliseconds )

Items.UseItem( targetBox )
Misc.Pause( config.dragDelayMilliseconds )
    
for item in sourceBox.Contains:
    if item
    MoveItem( Items, Misc, item, targetBox )