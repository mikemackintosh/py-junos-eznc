import re

def switch_style( junos, facts ):
  persona = facts['personality']

  if persona in ['MX', 'SRX_HIGHEND']:
    style = 'BRIDGE_DOMAIN'
  elif persona in ['SWITCH', 'SRX_BRANCH']:
    model = facts['hardwaremodel']
    if re.match('junosv-firefly',model,re.IGNORECASE):
      style = 'NONE'
    elif re.match('^(EX9)|(EX43)', model):
      style = 'VLAN_L2NG'
    else:
      style = 'VLAN'
  else:
    style = 'NONE'

  facts['switch_style'] = style