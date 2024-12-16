from System.Collections.Generic import List
from System import Byte
import clr
clr.AddReference('System.Speech')
from System.Speech.Synthesis import SpeechSynthesizer
global mystic
mystic = False

def ReadJournal():
    global mystic
    
    if Journal.Search('tidal wave'):
        Journal.Clear()
        say("Tidal")
        
    if Journal.Search('regurgitates'):
        Journal.Clear()
        say("Regurgitate")
        
    if Journal.Search('chasing flames'):
        Journal.Clear()
        say("flames")
    if Journal.Search('burn!') or Journal.Search('BURN!'):
        Journal.Clear()
        say("burn")
    
    if Journal.Search('mystic energy') or (mystic and not Timer.Check('blastcd')):
        Journal.Clear()
        say("mystic run")
        mystic = True
        Timer.Create('blastcd',17000)
        
    Journal.Clear()
    Misc.Pause(30)
    if Journal.Search('summons flames'):
        Misc.Beep()
        Player.ChatSay(33, 'all follow me')
        Misc.Pause(100)
        Player.ChatSay(33, 'all follow me')
        Journal.Clear()
    if Journal.Search('summons dark flames'):
        Misc.Beep()
        Player.ChatSay(33, 'all follow me')
        Misc.Pause(100)
        Player.ChatSay(33, 'all follow me')
        Journal.Clear()
    if Journal.Search('shatters'):
        Misc.Beep()
        Player.ChatSay(33, 'all follow me')
        Misc.Pause(100)
        Player.ChatSay(33, 'all follow me')
        Journal.Clear()
    if Journal.Search('confused'):
        Player.ChatSay(33, 'all guard me')
        Misc.Pause(100)
        Player.ChatSay(33, 'all guard me')
        Journal.Clear()
        
def say(text):
    spk = SpeechSynthesizer()
    spk.Speak(text)  
    
while True:
    ReadJournal()
    Misc.Pause(10)