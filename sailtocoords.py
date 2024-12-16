x = 1832
y = 3060
boatdirection = 'east'

saildirection = 'none'

def Fish( fishX, fishY ):
    Items.UseItem(0x401B4709)
    Target.WaitForTarget( 2000, True )
    Target.TargetExecute( x, y, -5, 0x0000 )
    Misc.Pause(250)
    Timer.Create( 'timeout', 20000 )
    while not ( Journal.SearchByType( 'You pull', 'System' ) or #Regular or System or Label?
            Journal.SearchByType( 'You fish a while, but fail to catch anything.', 'System' ) or
            Journal.SearchByType( 'The fish don\'t seem to be biting here', 'System' ) or
            Journal.SearchByType( 'Your fishing pole bends as you pull a big fish from the depths!', 'System' ) or
            Journal.SearchByType( 'Uh oh! That doesn''t look like a fish!', 'System' ) ):
        if not Timer.Check( 'timeout' ):
            return False
        Misc.Pause( 50 )

    if Journal.SearchByType( 'The fish don\'t seem to be biting here', 'System' ):
        return False
        
    return True

while Player.Position.X != x or Player.Position.Y != y:
    Misc.Pause(150)

    
    if Player.Position.X > x:
        if boatdirection == 'east':
            Player.ChatSay(0,'come about')
            boatdirection = 'west'
            Misc.Pause(250)
        if saildirection != 'forward':
            Player.ChatSay(0,'forward')
            saildirection = 'forward'
    elif Player.Position.X < x:
        if boatdirection == 'west':
            Player.ChatSay(0,'come about')
            boatdirection = 'east'
            Misc.Pause(250)
        if saildirection != 'forward':
            Player.ChatSay(0,'forward')
            saildirection = 'forward'
    elif Player.Position.Y > y:
        if boatdirection == 'east':
            if saildirection != 'left':
                Player.ChatSay(0,'left')
                saildirection = 'left'
        else:
            if saildirection != 'right':
                Player.ChatSay(0,'right')
                saildirection = 'right'
    elif Player.Position.Y < y:
        if boatdirection == 'east':
            if saildirection != 'right':
                Player.ChatSay(0,'right')
                saildirection = 'right'
        else:
            if saildirection != 'left':
                Player.ChatSay(0,'left')
                saildirection = 'left'
                
                
Player.ChatSay(0,'stop')                

while not Player.IsGhost:
    while Fish( x, y ):
        Misc.Pause(9500)