if Misc.ScriptStatus('Dextrome_Unchained_MiningV2.py') == False:
    Misc.SendMessage('Mining Script Not Running')
else:
    if Misc.ScriptIsSuspended('Dextrome_Unchained_MiningV2.py'):
        Misc.ScriptResume('Dextrome_Unchained_MiningV2.py')
        Misc.SendMessage('Mining Script Resumed')
    else:
        Misc.ScriptSuspend('Dextrome_Unchained_MiningV2.py')
        Misc.SendMessage('Mining Script Paused')