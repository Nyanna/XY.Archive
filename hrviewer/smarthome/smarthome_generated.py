# Describe this function...
def allOff():
  # Gaestedose
  sh.control('zigbee2mqtt.0.0xa4c1387253897923.state', False)
  # Z-Pumpe
  sh.control('zigbee2mqtt.0.0xa4c1383c7d3c4cb5.state', False)
  # Phillips
  sh.control('zigbee2mqtt.0.0x001788010ea481b2.state', False)
  # Heizung
  sh.control('zigbee2mqtt.0.0xa4c138edbd20f773.state', False)
  # Wendy Schreibtisch
  sh.control('zigbee2mqtt.0.0x00124b0026b82cce.state', False)
  # Kimi Buero
  sh.control('zigbee2mqtt.0.0xa4c138425776c645.state', False)
  # Espresso
  sh.control('zigbee2mqtt.0.0xa4c1380d85a6455f.state', False)
  # Aura PC
  sh.control('zigbee2mqtt.0.0xa4c1380d5aeeffff.state', False)
  # Wohnzimmer Licht
  sh.control('zigbee2mqtt.0.0xa4c138089de1ffff.state', False)
  # Wasserkocher
  sh.control('zigbee2mqtt.0.0xa4c138083f13ffff.state', False)


# All Off
def _sched_ChHXfnMZJaCF6__DU__3():
  sh.debug('Kill Off Schedule', 'info')
  allOff()
sh.schedule('0 1 * * *', _sched_ChHXfnMZJaCF6__DU__3)

def _on__vqOTTS6_N_Z5gYm2___():
  sh.debug('Kill Off Switch', 'info')
  allOff()
sh.on('zigbee2mqtt.0.0x60a423fffe803811.1_single', 'true', _on__vqOTTS6_N_Z5gYm2___)

def _sched__OHZ_A__EATHj_lt9K9_():
  # Schlafzimemer Dose
  sh.control('zigbee2mqtt.0.0xa4c1380d4358ffff.state', False)
  # Aura PC
  sh.control('zigbee2mqtt.0.0xa4c1380d5aeeffff.state', True)
  # Wasserkocher
  sh.control('zigbee2mqtt.0.0xa4c138083f13ffff.state', True)
sh.schedule('0 7 * * *', _sched__OHZ_A__EATHj_lt9K9_)

def _sched_uK94_P_Ev_d_eTtZzXFv():
  # Schlafzimemer Dose
  sh.control('zigbee2mqtt.0.0xa4c1380d4358ffff.state', True)
  # Wasserkocher
  sh.control('zigbee2mqtt.0.0xa4c138083f13ffff.state', True)
sh.schedule('0 22 * * *', _sched_uK94_P_Ev_d_eTtZzXFv)

# Espresso Schedule
def _sched_Xan_3oJ_tjii_aZ7_hp_():
  sh.control('zigbee2mqtt.0.0xa4c1380d85a6455f.state', True)
sh.schedule('0 7 * * *', _sched_Xan_3oJ_tjii_aZ7_hp_)

# Espresso Office out
def _sched_ZhA_nA____R_Wat4Z7vu():
  sh.control('zigbee2mqtt.0.0xa4c1380d85a6455f.state', False)
sh.schedule('0 18 * * *', _sched_ZhA_nA____R_Wat4Z7vu)

# Heizungtimer Off
def _on_P_1Ws_7et__iuoB9a_tG():
  if sh.time('wd') != 7:
    sh.debug('Heizungstimer triggered', 'info')
    sh.clear_timeout('heizung')
    def _to__6_G_Jv7dQ_z_fdO_4_K():
      sh.debug('Turning Heizung off', 'info')
      sh.control('zigbee2mqtt.0.0xa4c138edbd20f773.state', False)
    sh.set_timeout('heizung', 3600, _to__6_G_Jv7dQ_z_fdO_4_K)
sh.on('zigbee2mqtt.0.0xa4c138edbd20f773.state', 'true', _on_P_1Ws_7et__iuoB9a_tG)

def _sched__3r_E72_g_VDmXzL6tW_():
  sh.debug('Daily hot water check', 'info')
  if sh.get_value('zigbee2mqtt.0.0xa4c1383c7d3c4cb5.temperature', 'val') < 39:
    sh.debug('Water to cold starting heater', 'info')
    sh.control('zigbee2mqtt.0.0xa4c138edbd20f773.state', True)
sh.schedule('0 17 * * *', _sched__3r_E72_g_VDmXzL6tW_)
