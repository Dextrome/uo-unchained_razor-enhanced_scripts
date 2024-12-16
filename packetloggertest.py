packetDamage = """
{
  'packetID': 0x0B,
  'name': 'Damage 0x0B',
  'showHexDump': true,
  'fields':[
    { 'name':'packetID', 'length':1, 'type':'packetID'},
    { 'name':'Serial', 'length':4, 'type':'serial'},
    { 'name':'Damage', 'length': 2, 'type':'int'},
  ]
}
"""


packetItemInfo = """
{
  'packetID': 0xF3,
  'name': 'Object Information 0xF3',
  'showHexDump': true,
  'fields':[
    { 'name':'packetID', 'length':1, 'type':'packetID'},
    { 'name':'0x1 on OSI', 'length':1, 'type':'hex' },
    { 'name':'DataType', 'length':1, 'type':'hex' },
    { 'name':'Serial',  'type':'serial'},
    { 'name':'GraphicID', 'length':2, 'type':'hex' },
    { 'name':'Facing', 'length': 1, 'type':'hex' },
    { 'name':'Amount1', 'length': 2, 'type':'hex'},
    { 'name':'Amount2', 'length': 2, 'type':'hex'},
    { 'name':'X', 'length': 2, 'type':'uint'},
    { 'name':'Y', 'length': 2, 'type':'uint'},
    { 'name':'Z', 'length': 1, 'type':'uint'},
    { 'name':'Layer', 'length': 1, 'type':'hex'},
    { 'name':'Color', 'length': 2, 'type':'uint'},
    { 'name':'Flag', 'length': 1, 'type':'hex'} 
  ]
}
"""


log_folder = Misc.ScriptDirectory() + "\\log\\"
log_damage = log_folder + "damage.packets.log"

debug = True

if debug:
    PacketLogger.Reset()
    PacketLogger.RemoveTemplate()
    PacketLogger.AddTemplate(packetDamage)
    PacketLogger.DiscardAll(True)
    PacketLogger.DiscardShowHeader(False)
    PacketLogger.AddWhitelist(0x0B) 
    PacketLogger.Start(log_damage)
    
    while not Player.IsGhost:
        Misc.Pause(500)
    
    PacketLogger.Stop()