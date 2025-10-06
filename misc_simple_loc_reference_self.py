inputstr = """
 ITA_CAS_equipment_1: "Breda Ba.65"
 ITA_CAS_equipment_1_short: "Ba.65"
 ITA_cv_CAS_equipment_1: "Breda Ba.65bis"
 ITA_cv_CAS_equipment_1_short: "Ba.65bis"
 ITA_CAS_equipment_2: "Breda Ba.12"                     # Uses Fiat FC.12 icon
 ITA_CAS_equipment_2_short: "Ba.12"
 ITA_cv_CAS_equipment_2: "Breda Ba.50N"                 # Uses G.50N icon
 ITA_cv_CAS_equipment_2_short: "Ba.50N"
 ITA_CAS_equipment_3: "Savoia-Marchetti SM.93"
 ITA_CAS_equipment_3_short: "SM.93"
 ITA_cv_CAS_equipment_3: "Breda Ba.201bis"
 ITA_cv_CAS_equipment_3_short: "Ba.201bis"

 ITA_fighter_equipment_0: "Macchi CR.32"
 ITA_fighter_equipment_0_short: "CR.32"
 ITA_cv_fighter_equipment_0: "Macchi ICR.32"
 ITA_cv_fighter_equipment_0_short: "ICR.32"
 ITA_fighter_equipment_1: "Macchi C.200 Saetta"
 ITA_fighter_equipment_1_short: "C.200 Saetta"
 ITA_cv_fighter_equipment_1: "Macchi IC.200"
 ITA_cv_fighter_equipment_1_short: "IC.200"
 ITA_fighter_equipment_2: "Macchi C.202 Folgore"
 ITA_fighter_equipment_2_short: "C.202 Folgore"
 ITA_cv_fighter_equipment_2: "Macchi IC.202"          # Uses Re.2001 icon
 ITA_cv_fighter_equipment_2_short: "IC.202"
 ITA_fighter_equipment_3: "Macchi C.205 Veltro"
 ITA_fighter_equipment_3_short: "C.205 Veltro"
 ITA_cv_fighter_equipment_3: "Macchi IC.205"          # Uses Re.2005 icon
 ITA_cv_fighter_equipment_3_short: "IC.205"

 ITA_jet_fighter_equipment_1: "Reggiane Re.2007"
 ITA_jet_fighter_equipment_1_short: "Re.2007"
 ITA_jet_fighter_equipment_2: "Reggiane Re.2008"
 ITA_jet_fighter_equipment_2_short: "Re.2008"
 ITA_small_plane_airframe_5_short:"Re.2008"

 ITA_nav_bomber_equipment_1: "Savoia-Marchetti SM.79 Sparviero"
 ITA_nav_bomber_equipment_1_short: "SM.79 Sparviero"
 ITA_cv_nav_bomber_equipment_1: "Savoia-Marchetti SM.79-II Sparviero"
 ITA_cv_nav_bomber_equipment_1_short: "SM.79-II Sparviero"
 ITA_nav_bomber_equipment_2: "Savoia-Marchetti SM.84"
 ITA_nav_bomber_equipment_2_short: "SM.84"
 ITA_cv_nav_bomber_equipment_2: "Savoia-Marchetti SM.84-II"
 ITA_cv_nav_bomber_equipment_2_short: "SM.84-II"
 ITA_nav_bomber_equipment_3: "Savoia-Marchetti SM.89"
 ITA_nav_bomber_equipment_3_short: "SM.89"
 ITA_cv_nav_bomber_equipment_3: "Savoia-Marchetti SM.89-II"
 ITA_cv_nav_bomber_equipment_3_short: "SM.89-II"

 ITA_heavy_fighter_equipment_1: "IMAM Ro.57"
 ITA_heavy_fighter_equipment_1_short: "Ro.57"
 ITA_heavy_fighter_equipment_2: "IMAM Ro.58"
 ITA_heavy_fighter_equipment_2_short: "Ro.58"
 ITA_heavy_fighter_equipment_3: "Savoia-Marchetti SM.92"
 ITA_heavy_fighter_equipment_3_short: "SM.92"

 ITA_tac_bomber_equipment_0: "Caproni Ca.101"
 ITA_tac_bomber_equipment_0_short: "Ca.101"
 ITA_tac_bomber_equipment_1: "Savoia-Marchetti SM.81 Pipistrello"
 ITA_tac_bomber_equipment_1_short: "SM.81 Pipistrello"
 ITA_tac_bomber_equipment_2: "Cant Z.1007bis Alcione"
 ITA_tac_bomber_equipment_2_short: "Z.1007bis Alcione"
 ITA_tac_bomber_equipment_3: "Cant Z.1018 Leone"
 ITA_tac_bomber_equipment_3_short: "Z.1018 Leone"

 ITA_strat_bomber_equipment_1: "Savoia-Marchetti SM.50"
 ITA_strat_bomber_equipment_1_short: "Savoia-Marchetti SM.50"
 ITA_strat_bomber_equipment_2: "Savoia-Marchetti SM.108"
 ITA_strat_bomber_equipment_2_short: "SM.108"
 ITA_strat_bomber_equipment_3: "Savoia-Marchetti SM.133"
 ITA_strat_bomber_equipment_3_short: "SM.133"

 ITA_scout_plane_equipment_1: "Caproni Ca.309 Ghibli"
 ITA_scout_plane_equipment_1_short: "Ca.309 Ghibli"
 ITA_scout_plane_equipment_2: "Caproni Ca.311"
 ITA_scout_plane_equipment_2_short: "Ca.311"

 ITA_transport_plane_equipment_1: "Caproni Ca.133"
 ITA_transport_plane_equipment_1_short: "Ca.133"
 ITA_transport_plane_equipment_2: "Savoia-Marchetti SM.82"
 ITA_transport_plane_equipment_2_short: "SM.82"
 ITA_transport_plane_equipment_3: "Savoia-Marchetti SM.95 GA"
 ITA_transport_plane_equipment_3_short: "SM.95 GA"
"""

x = []
for i in inputstr.split('\n'):
    if '"' in i:
        try:
            key, to_replace = i.strip().split(':')
            replaced_line = i.replace(to_replace, ' "$'+key+'$"')
            x.append(replaced_line)
        except Exception:
            print(i)
            raise

for i in x:
    print(i)