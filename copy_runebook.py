# Runebook copy by Wardoctor. Upated by MatsaMilla
# Last update: 12/9/21

# If copying a locked down book, DO THIS BEFORE STARTING
#   Mark a rune for a location close to runebook being copied
#
#   Put this rune into a book for safe keeping (runes are not blessed, runebooks are)
#   Set the rune as the default location for the book
#   Select the correct book when the target comes up for Select item to recall off of to return to runebook being copied


def PromptRunebook( promptString ):
    runebookSerial = Target.PromptTarget( promptString )
    runebook = Items.FindBySerial( runebookSerial )

    if runebook == None or runebook.ItemID != 0x0EFA:
        Player.HeadMessage( 33, 'That is not a runebook!' )
        return None
    else:
        return runebook


def GetNamesOfRunesInBook( runebook ):
    Items.UseItem( runebook )

    # Pause here since the next part goes pretty quick
    Misc.Pause( 650 )

    Gumps.WaitForGump( 89, 5000 )
    while Gumps.CurrentGump() != 89:
        Player.HeadMessage( 33, 'Too far from runebook to copy, please move closer.' )
        Misc.Pause( 1000 )
        Items.UseItem( runebook )
        Gumps.WaitForGump( 89, 5000 )

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

    return runeNames


def GetNumberOfRunesInBook( runebook ):
    return len( GetNamesOfRunesInBook( runebook ) )


def CopyRunebookName( runebookToCopy, runebookToPlaceIn, runebookMoveable ):
    Journal.Clear()
    if Gumps.CurrentGump() == 89:
        Gumps.WaitForGump( 89, 1000 )
        Gumps.SendAction( 89, 0 )

    Items.SingleClick( runebookToCopy.Serial )
    Misc.Pause( 200 )
    runebookName = None
    if runebookMoveable:
        for line in Journal.GetTextByType( 'Label' ):
            if '[' in line:
                bracketIndex = line.find( '[' )
                runebookName = line[ 0 : ( bracketIndex - 1 ) ]
    else:
        journalText = Journal.GetTextByType( 'Label' )
        journalText.Reverse()
        runebookName = journalText[ 0 ]

    if runebookName != None and runebookName != '':
        Items.UseItem( runebookToPlaceIn )
        Gumps.WaitForGump( 89, 10000 )
        Misc.Pause( 200 )
        Gumps.SendAction( 89, 1 )
        Misc.WaitForPrompt( 1000 )
        Misc.ResponsePrompt( runebookName )
        Gumps.WaitForGump( 89, 1000 )
        Gumps.SendAction( 89, 0 )


def CopyRunebook():
    global runebookToCopy
    global runebookToPlaceIn

    runebookToCopy = PromptRunebook( 'Select the runebook to copy from' )
    if runebookToCopy == None:
        return

    runebookToPlaceIn = PromptRunebook( 'Select the runebook to copy to' )
    if runebookToPlaceIn == None:
        return

    # Test if the runebook is locked down or not
    Journal.Clear()
    runebookMoveable = True
    recallRunebook = None
    if runebookToCopy.RootContainer != Player.Serial:
        Items.Move( runebookToCopy, Player.Backpack, 0 )
        Misc.Pause( 650 + 100 ) # plus 100 to be extra safe

        runebookToCopy = Items.FindBySerial( runebookToCopy.Serial )

        if runebookToCopy.RootContainer != Player.Backpack.Serial:
            runebookMoveable = False
            recallRunebook = Target.PromptTarget( 'Select item to recall off of to return to runebook being copied' )

    numberOfRunesInOldBook = GetNumberOfRunesInBook( runebookToCopy )
    numberOfRunesInNewBook = GetNumberOfRunesInBook( runebookToPlaceIn )
    runeNames = GetNamesOfRunesInBook( runebookToCopy )

    Misc.SendMessage( '# of runes to copy: %i' % numberOfRunesInOldBook )
    Misc.SendMessage( '# of runes already copied: %i' % numberOfRunesInNewBook )
    numberOfRunesToBeMarked = numberOfRunesInOldBook - numberOfRunesInNewBook

    # Make sure we have enough runes to be marked
    blankRuneBagSerial = Target.PromptTarget( 'Select bag with empty runes' )
    blankRuneBag = Items.FindBySerial( blankRuneBagSerial )
    if blankRuneBag == None or not blankRuneBag.IsContainer:
        Player.HeadMessage( 33, 'Invalid item selection!' )
        return

    numberOfBlankRunes = 0
    for item in blankRuneBag.Contains:
        if item.ItemID == 0x1F14:
            numberOfBlankRunes += 1

    if numberOfRunesToBeMarked > numberOfBlankRunes:
        Player.HeadMessage( 33, 'You don\'t have enough blank runes to copy this book! You need %i more runes' % ( numberOfRunesToBeMarked - numberOfBlankRunes ) )
        return

    # Copy the runebook
    for i in range( numberOfRunesInNewBook, numberOfRunesInOldBook ):
        Items.UseItem( runebookToCopy )
        Misc.Pause( 650 )
        Gumps.WaitForGump( 89, 5000 )

        if i == 0:
            Gumps.SendAction( 89, 5 )
        else:
            Gumps.SendAction( 89, ( 5 + ( i * 6 ) ) )

        Timer.Create( 'spellCooldown', 2500 )
        Misc.Pause( 100 )
        playerPosition = Player.Position

        runeToMark = Items.FindByID( 0x1F14, -1, blankRuneBag.Serial )

        while Timer.Check( 'spellCooldown' ):
            Misc.Pause( 50 )

        markScrolls = Items.FindByID( 0x1F59, 0x0000, Player.Backpack.Serial )
        if markScrolls != None:
            Items.UseItem( markScrolls )
            Timer.Create( 'markScrollDragDelay', 650 )
        else:
            Spells.CastMagery( 'Mark' )

        Target.WaitForTarget( 2000, True )
        Target.TargetExecute( runeToMark )

        if markScrolls != None and Timer.Check( 'markScrollDragDelay' ):
            while Timer.Check( 'markScrollDragDelay' ):
                Misc.Pause( 20 )
        elif markScrolls == None:
            Timer.Create( 'spellCooldown', 1800 )

        Items.UseItem( runeToMark )

        Misc.WaitForPrompt( 1000 )
        Misc.ResponsePrompt( runeNames[ i ] )
        Misc.Pause( 650 )

        Items.Move( runeToMark, runebookToPlaceIn, 0 )
        Misc.Pause( 650 )

        if runebookMoveable:
            if Player.Mana < 41:
                Player.UseSkill( 'Meditation' )
                while Player.Mana < ( Player.ManaMax - 3 ):
                    Misc.Pause( 50 )

            while Timer.Check( 'spellCooldown' ):
                Misc.Pause( 50 )
        else:
            while Timer.Check( 'spellCooldown' ):
                Misc.Pause( 50 )

            Spells.CastMagery( 'Recall' )
            Target.WaitForTarget( 15000, False )
            Target.TargetExecute( recallRunebook )

            Player.HeadMessage( 44, 'Move within recall range of the runebook being copied' )
            Timer.Create( 'messageCooldown', 2000 )
            while not Player.InRangeItem( runebookToCopy, 1 ):
                Misc.Pause( 100 )
                if not Timer.Check( 'messageCooldown' ):
                    Player.HeadMessage( 44, 'Move within recall range of the runebook being copied' )
                    Timer.Create( 'messageCooldown', 2000 )

            if Player.Mana < 42: # 42 = 11 for 2 Recalls and 20 for one Mark
                Player.HeadMessage( 44, 'Meditating' )
                Player.UseSkill( 'Meditation' )
                while Player.Mana < ( Player.ManaMax - 3 ):
                    if not Player.BuffsExist( 'Meditation' ):
                        Player.UseSkill( 'Meditation' )
                    Misc.Pause( 50 )

    Misc.Pause( 650 )
    CopyRunebookName( runebookToCopy, runebookToPlaceIn, runebookMoveable )

    Player.HeadMessage( 33, 'Done copying runebook!' )
    Misc.Beep()


runebookToCopy = None
runebookToPlaceIn = None
CopyRunebook()