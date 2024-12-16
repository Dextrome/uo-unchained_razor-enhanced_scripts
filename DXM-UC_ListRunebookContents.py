runebookDelay = 600
runebookID = 0x0EFA

if Player.GetRealSkillValue('Magery') > 35:
    mageRecall = True
else:
    mageRecall = False
    Misc.SendMessage('Recalling by Charges')
    
    
    
    
def makeRunebookList( ):
    sortedRuneList = []
    for i in Player.Backpack.Contains:
        if i.ItemID == runebookID:
            # opens runebook
            Items.UseItem( i )
            Misc.Pause(120) 
            Gumps.WaitForGump( 1431013363, 500 )
            if Journal.Search('You must wait'):
                Misc.SendMessage('trying runebook again')
                Items.UseItem( i )
                Gumps.WaitForGump( 1431013363, 500 )
                Journal.Clear()
            
            bookSerial = i.Serial
            runeNames = []
            lineList = Gumps.LastGumpGetLineList()

            # Remove the default 3 lines from the top of the list
            lineList = lineList[ 3 : ]

            # Remove the items before the names of the runes
            endIndexOfDropAndDefault = 0
            for i in range( 0, len( lineList ) ):
                if lineList[ i ] == 'Set default' or lineList[ i ] == 'Drop rune':
                    endIndexOfDropAndDefault += 1
                else:
                    break

            # Add two for the charge count and max charge numbers
            endIndexOfDropAndDefault += 2
            runeNames = lineList[ endIndexOfDropAndDefault : ( endIndexOfDropAndDefault + 16 ) ]
            runeNames = [ name for name in runeNames if name != 'Empty' ]
            mageRecall = 5
            chargeRecall = 2
            gate = 6
            for x in runeNames:
                sortedRuneList.append( (bookSerial, x.lower(), mageRecall , chargeRecall , gate) )
                mageRecall = mageRecall + 6
                chargeRecall = chargeRecall + 6
                gate = gate + 6
            Gumps.CloseGump(1431013363)
            Misc.Pause(runebookDelay)
    Misc.SendMessage('Runebooks Updated', 66)
    return sortedRuneList
    
    
runeNames = makeRunebookList()

for runename in runeNames:
    Misc.SendMessage(runename)
