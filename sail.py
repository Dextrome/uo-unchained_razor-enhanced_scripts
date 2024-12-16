done = False
    
def Done():
    Player.ChatSay(0,'stop')
    done = True

while not done:
    Player.HeadMessage(0, '%i - %i' % (Player.Position.X, Player.Position.Y))
    if Player.Position.Y >= 3255:
        Done()
        
    Misc.Pause( 1000 )
    
    
