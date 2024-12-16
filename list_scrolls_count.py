from Scripts.utilities.items import MoveItem
from Scripts import config
from System.Collections.Generic import List
from System import Byte, Int32
from Scripts.glossary.items.spellScrolls import spellScrolls
spellScrollIDs = [ spellScrolls[ scroll ].itemID for scroll in spellScrolls ]

spellscrolllist = [0x1F2E,0x1F2F,0x1F30,0x1F31,0x1F32,0x1F33,0x1F2D,0x1F34,0x1F35,0x1F36,0x1F37,0x1F38,0x1F39,0x1F3A,0x1F3B,0x1F3C,0x1F3D,0x1F3E,0x1F3F,0x1F40,0x1F41,0x1F42,0x1F43,0x1F44,0x1F45,0x1F46,0x1F47,0x1F48,0x1F49,0x1F4A,0x1F4B,0x1F4C,0x1F4D,0x1F4E,0x1F4F,0x1F50,0x1F51,0x1F52,0x1F53,0x1F54,0x1F55,0x1F56,0x1F57,0x1F58,0x1F59,0x1F5A,0x1F5B,0x1F5C,0x1F5D,0x1F5E,0x1F5F,0x1F60,0x1F61,0x1F62,0x1F63,0x1F64,0x1F65,0x1F66,0x1F67,0x1F68,0x1F69,0x1F6A,0x1F6B,0x1F6C]






targetBoxSerial = Target.PromptTarget( 'Select container' )
targetBoxItem = Items.FindBySerial( targetBoxSerial )
targetBox = targetBoxItem


for scrollID in spellscrolllist:
    scroll = Items.FindByID(scrollID,-1,targetBoxSerial,-1,False)
    if scroll:
        Misc.NoOperation()
        #Misc.SendMessage('%s: %i' % (scroll.Name , scroll.Amount ))
    else:
        #Misc.SendMessage('%s: %i' % (scrollID , 0 ))
        for scroll in spellScrolls:
            if spellScrolls[ scroll ].itemID == scrollID:
                Misc.SendMessage('%s: %i' % (scroll , 0 ))
    Misc.Pause(5)

#
#for item in targetBox.Contains:
#    Misc.SendMessage('%s: %i' % (item.Name , item.Amount ))
#    Misc.Pause(5)