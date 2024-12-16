# True will move the boat with the 'foward' and 'backword' commands
# False will move the boat with the 'left' and 'right' commands
moveForwardBackward = False

from Scripts import config
from Scripts.glossary.colors import colors
from Scripts.glossary.items.containers import FindHatch
from Scripts.glossary.items.tools import tools
from Scripts.utilities.items import FindItem
from System.Collections.Generic import List
from System import Byte, Int32

fishIDs = [ 0x09CF, 0x09CE, 0x09CC, 0x09CD, 0x4307, 0x4306, 0x44C6, 0x4303, 0x44C4, 0x09CC, 0x44C3, 0x44C5, 0x4304, 0x4305 ]

def Fish( fishingPole, x, y ):
#    Player.UseSkill("Detect Hidden")
#    Misc.Pause(250)
#    Target.Self()
#    Misc.Pause(1000)
    
    if Player.Hits < 50:
        #Cure
        if Player.Poisoned:
            pot = Items.FindByID(0x0F07,0,Player.Backpack.Serial,True)
            if pot:
                Items.UseItem(pot)
                Misc.Pause(650)
            
            if Player.Poisoned and Player.GetSkillValue('Magery') >= 60:
                Spells.CastMagery('Cure')
                Target.WaitForTarget(1500)
                Target.Self()
        
        #Heal (Bandages are handled by bandage_self script)
        if Player.GetSkillValue('Healing') >= 50:
            if not Misc.ScriptStatus('bandage_self.py'):
                Misc.ScriptRun('bandage_self.py')

        if Player.Hits <= 70:
            pot = Items.FindByID(0x0F0C,0,Player.Backpack.Serial,True)
            if pot:
                Items.UseItem(pot)
                Misc.Pause(650)
        
        if Player.GetSkillValue('Magery') >= 80:
            if Player.Poisoned:
                Spells.CastMagery('Cure')
                Target.WaitForTarget(1500)
                Target.Self()
            else:
                if Player.Hits < 75:
                    if Player.Hits < 30:
                        Spells.CastMagery('Heal')
                        Target.WaitForTarget(1500)
                        Target.Self()
                        Misc.Pause(150)
                        Spells.CastMagery('Heal')
                        Target.WaitForTarget(1500)
                        Target.Self()
                    else:
                        Spells.CastMagery('Greater Heal')
                        Target.WaitForTarget(1500)
                        Target.Self()
                elif Player.Hits < 90:
                    Spells.CastMagery('Heal')
                    Target.WaitForTarget(1500)
                    Target.Self()
    
    '''
    Casts the fishing pole and returns True while the fish are biting
    '''
    

    global fishIDs

    Journal.Clear()
    #FISHING POLE:
    if Player.Name == "Dextrome":
        Items.UseItem(0x4052163B)
    if Player.Name == "Gaga":
        Items.UseItem(0x4008F659)

    Target.WaitForTarget( 2000, True )

    statics = Statics.GetStaticsTileInfo( x, y, 0 )
    
    if len( statics ) > 0:
        water = statics[ 0 ]
        Target.TargetExecute( x, y, water.StaticZ, water.StaticID )
    else:
        Target.TargetExecute( x, y, -5, 0x0000 )


    Misc.Pause( config.dragDelayMilliseconds )

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

    if Player.Weight >= Player.MaxWeight - 150:
        Player.ChatSay( 0, 'all guard me' )
        Misc.Pause( 100 )
        shoes = Items.FindByID( 0x170F, -1, Player.Backpack.Serial, True )
        if shoes:
            Items.DropItemGroundSelf(shoes)
            Misc.Pause( 1000 )
        boots = Items.FindByID( 0x170B, -1, Player.Backpack.Serial, True )
        if boots:
            Items.DropItemGroundSelf(boots)
            Misc.Pause( 1000 )
        thighboots = Items.FindByID( 0x1711, -1, Player.Backpack.Serial, True )
        if thighboots:
            Items.DropItemGroundSelf(thighboots)
            Misc.Pause( 1000 )
        sandals = Items.FindByID( 0x170D, -1, Player.Backpack.Serial, True )
        if sandals:
            Items.DropItemGroundSelf(sandals)
            Misc.Pause( 1000 )
        
        for fishID in fishIDs:
            Misc.Pause( 200 )
            fish = Items.FindByID( fishID, -1, Player.Backpack.Serial )
            if fish != None:
                #Player.HeadMessage( 0, 'Found %i' % (fishID) )
                Items.UseItemByID( 0x0F52 )
                Target.WaitForTarget( 2000, True )
                Target.TargetExecute( fish )
                Misc.Pause( 1000 )

        if Player.Weight > Player.MaxWeight - 140:
            # Throw the fish and shoes into the boats hatch
#            directionsToHatch = [ 'West', 'West', 'West', 'North', 'North', 'West', 'West', 'West' ]
#            for direction in directionsToHatch:
#                Player.Walk( direction )
#                Misc.Pause( 1000 )
#                
            if Player.Name == "Dextrome":
                hatch = Items.FindBySerial(0x401B416D)
            if Player.Name == "Gaga":
                #hatch = Items.FindBySerial(0x4009204D)
                hatch = Items.FindBySerial(0x401B416D)
            
            if hatch == None:
                hatch = Items.FindByID(0x3E93,-1,-1,4)
                
            if hatch:
                mib = Items.FindByID( 0x099F, -1, Player.Backpack.Serial )
                if mib:
                    Items.Move( mib, hatch, 0 )
                    Misc.Pause( config.dragDelayMilliseconds )
                    
                seaserpentscale = Items.FindByID( 0x26B4, -1, Player.Backpack.Serial )
                if seaserpentscale:
                    Items.Move( seaserpentscale, hatch, 0 )
                    Misc.Pause( config.dragDelayMilliseconds )
                    
                rawFishSteaks = Items.FindByID( 0x097A, -1, Player.Backpack.Serial )
                if rawFishSteaks:
                    Items.Move( rawFishSteaks, hatch, 0 )
                    Misc.Pause( config.dragDelayMilliseconds )
                    
                rawFishSteaks = Items.FindByID( 0x097A, -1, Player.Backpack.Serial )
                if rawFishSteaks:
                    Items.Move( rawFishSteaks, hatch, 0 )
                    Misc.Pause( config.dragDelayMilliseconds )
                    
                rawFishSteaks = Items.FindByID( 0x097A, -1, Player.Backpack.Serial )
                if rawFishSteaks:
                    Items.Move( rawFishSteaks, hatch, 0 )
                    Misc.Pause( config.dragDelayMilliseconds )
                    
                specialfish = Items.FindByID( 0x0DD6, -1, Player.Backpack.Serial )
                if specialfish:
                    Items.Move( specialfish, hatch, 0 )
                    Misc.Pause( config.dragDelayMilliseconds )
            
            shoes = Items.FindByID( 0x170F, -1, Player.Backpack.Serial, True )
            if shoes: 
                Items.DropItemGroundSelf(shoes)
                Misc.Pause( 720 )
            boots = Items.FindByID( 0x170B, -1, Player.Backpack.Serial, True )
            if boots:
                Items.DropItemGroundSelf(boots)
                Misc.Pause( 720 )
            thighboots = Items.FindByID( 0x1711, -1, Player.Backpack.Serial, True )
            if thighboots:
                Items.DropItemGroundSelf(thighboots)
                Misc.Pause( 720 )
#
#            sandals = Items.FindByID( 0x170D, -1, Player.Backpack.Serial )
#            if sandals:
#                Items.DropItemGroundSelf(sandals)
#                Misc.Pause( 720 )
#                
#            sandals = Items.FindByID( 0x170D, -1, -1 )
#            if sandals:
#                Items.MoveOnGround(sandals,1,Player.Position.X-1,Player.Position.Y-1,Player.Position.Z)
#                Misc.Pause( 720 )
            
            boots = Items.FindByID( 0x170B, 1, -1 )
            if boots:
                Items.MoveOnGround(boots,1,Player.Position.X-1,Player.Position.Y+1,Player.Position.Z)
                Misc.Pause( 720 )
                
            thighboots = Items.FindByID( 0x1711, 1, 0 )
            if thighboots:
                Items.MoveOnGround(thighboots,1,Player.Position.X-1,Player.Position.Y,Player.Position.Z)
                Misc.Pause( 720 )
                
            shoes = Items.FindByID( 0x170F, -1, 0 )
            if shoes: 
                Items.MoveOnGround(shoes,1,Player.Position.X+1,Player.Position.Y,Player.Position.Z)
                Misc.Pause( 720 )
#            
#            directionsToMast = [ 'East', 'East', 'East', 'South', 'South', 'East', 'East', 'East' ]
#            for direction in directionsToMast:
#                Player.Walk( direction )
#                Misc.Pause( 1000 )

    return True


def TrainFishing():
    '''
    Trains Fishing to its skill cap
    '''

    global moveForwardBackward

    fishingPoleTool = tools[ 'fishing pole' ]
    fishingPole = FindItem( fishingPoleTool.itemID, Player.Backpack )

    Misc.SendMessage( 'Beginning Fishing training', colors[ 'cyan' ] )

    moveBoatInThisDirection = None
    if moveForwardBackward:
        moveBoatInThisDirection = 'north'
    else:
        moveBoatInThisDirection = 'right'
    # while skill can increase and player is not dead
    while not Player.IsGhost:
        # Start fishing to the East
#        if not Player.Direction == 'Up':
#            Player.Walk( 'Up' )
        x = Player.Position.X - 3
        y = Player.Position.Y - 3
        while Fish( fishingPole, x, y ):
            enemy = Target.GetTargetFromList( 'enemy' )

#        Player.Walk( 'Right' )
        x = Player.Position.X + 3
        y = Player.Position.Y - 3
        while Fish( fishingPole, x, y ):
            enemy = Target.GetTargetFromList( 'enemy' )

#        Player.Walk( 'Down' )
        x = Player.Position.X + 3
        y = Player.Position.Y + 3
        while Fish( fishingPole, x, y ):
            enemy = Target.GetTargetFromList( 'enemy' )

#        Player.Walk( 'Left' )
        x = Player.Position.X - 3
        y = Player.Position.Y + 3
        while Fish( fishingPole, x, y ):
            enemy = Target.GetTargetFromList( 'enemy' )

# Start Fishing Training
Misc.IgnoreObject(0x40112EF3)
Misc.IgnoreObject(0x4034C9C3)
Misc.IgnoreObject(0x402A78DB)
TrainFishing()