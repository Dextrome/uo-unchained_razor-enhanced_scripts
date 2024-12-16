


def notDecoded():
    regularText = Journal.GetTextByType( 'Focus' )
    regularText.Reverse()
    
    for line in regularText[ 0 : len( regularText ) ]:
        if ( line == 'You succesfully decode a treasure map!' ) or ( line == 'The treasure map is marked by the red pin. Grab a shovel and go dig it up!' ):
            return False
    return True
    
    
    
tmap = Target.PromptTarget( 'Select tmap to decode' )
tmap = Items.FindBySerial( tmap )


while not (Journal.SearchByType('You succesfully decode a treasure map!','Regular') or
        Journal.SearchByType('You succesfully decode a treasure map!','System') or
        Journal.SearchByType('You succesfully decode a treasure map!','Label') or
        Journal.SearchByType('You succesfully decode a treasure map!','Encoded') or
        Journal.SearchByType('You succesfully decode a treasure map!','Special') or
        Journal.SearchByType('You succesfully decode a treasure map!','Objects') or
        Journal.SearchByType('The treasure map is marked by the red pin. Grab a shovel and go dig it up!','Regular') or
        Journal.SearchByType('The treasure map is marked by the red pin. Grab a shovel and go dig it up!','System') or
        Journal.SearchByType('The treasure map is marked by the red pin. Grab a shovel and go dig it up!','Label') or
        Journal.SearchByType('The treasure map is marked by the red pin. Grab a shovel and go dig it up!','Encoded') or
        Journal.SearchByType('The treasure map is marked by the red pin. Grab a shovel and go dig it up!','Special') or
        Journal.SearchByType('The treasure map is marked by the red pin. Grab a shovel and go dig it up!','Objects')):
    Misc.WaitForContext(tmap, 10000)
    Misc.ContextReply(tmap, 0)
    Misc.Pause(250)

