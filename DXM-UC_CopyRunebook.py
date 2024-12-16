runebook_to_copy_from_serial = Target.PromptTarget("runebook to copy from") 
runebook_to_copy_to_serial = Target.PromptTarget("runebook to copy to") 

recall_to_runebook_to_from = False  
rune_to_runelibrary_serial = 0x401444A4
steps_to_runebook = 7
direction_to_runebook = 'North'

def makeRunebookList( ):
    #sortedRuneList = []
    for i in Player.Backpack.Contains:
        if i.Serial == runebook_to_copy_from_serial:
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
            endIndexOfDropAndDefault += 4
            runeNames = lineList[ endIndexOfDropAndDefault : ( endIndexOfDropAndDefault + 16 ) ]
            runeNames = [ name for name in runeNames if name != 'Empty' ]
#            mageRecall = 5
#            chargeRecall = 2
#            gate = 6
#            for x in runeNames:
#                sortedRuneList.append( (bookSerial, x.lower(), mageRecall , chargeRecall , gate) )
#                mageRecall = mageRecall + 6
#                chargeRecall = chargeRecall + 6
#                gate = gate + 6
#            Gumps.CloseGump(1431013363)
            Misc.Pause(600)
#    Misc.SendMessage('Runebooks Updated', 66)
#    return sortedRuneList
    return runeNames 
    
runeNames = makeRunebookList()

for runename in runeNames:
    Misc.SendMessage(runename)

#Misc.Pause(25000)


#tmaploccounter = 82

for i in range(0,16):
    Misc.SendMessage('i = %i' % (i))
    Player.UseSkill("Meditation")
    Misc.WaitForContext(Player.Serial, 2500)
    Misc.ContextReply(Player.Serial, 5)
    Misc.Pause(5000)
    
    #recall to runelibrary
    if recall_to_runebook_to_from:
        Spells.Cast("Recall")
        Target.WaitForTarget(5000)
        Target.TargetExecute(rune_to_runelibrary_serial) 
        Misc.Pause(500)
        
        if steps_to_runebook > 0: #move to runebook
            for step in range (1,steps_to_runebook):
                Player.Run(direction_to_runebook)
            
    Misc.Pause(250)
    
    #recall to next spot to mark
    Items.UseItem(runebook_to_copy_from_serial)
    Gumps.WaitForGump(89, 10000)
    Misc.Pause(1000)
    Misc.SendMessage('Sending Gump Action %i' % (50+i))
    Misc.SendMessage('rune name = %s' % (runeNames[i]))
    Gumps.SendAction( 89, 50 + i ) 
    Misc.Pause(5000)
    Player.ChatSay("all guard me")
    
    #look for recall rune in backpack annd mark it
    blankrune = Items.FindByID(0x1F14, -1, Player.Backpack.Serial) 
    
    if blankrune:
        Spells.Cast("Mark")
        Target.WaitForTarget(5000)
        Target.TargetExecute(blankrune.Serial)
        Misc.Pause(500)
        Items.UseItem(blankrune.Serial)
        Misc.Pause(500)
        #Misc.ResponsePrompt('%i' % (tmaploccounter + i))
        Misc.ResponsePrompt('%s' % (runeNames[i]))
        Misc.Pause(500)
        Items.Move(blankrune.Serial, runebook_to_copy_to_serial, 1)
        
    Misc.Pause(500)