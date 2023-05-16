from cyber_city.game import Ability, Role

# Defining the Defenders Abilities
ENC = Ability("Data Encryption", 300, 10)
AMAL = Ability("Anti-Malware", 600, 30)
FWAL = Ability("Firewall", 600, 30)
TRU = Ability("Trust Zones", 400, 15)
HON = Ability("Honey Pot", 500, 20)
MULAUTH = Ability("Multifactor Authentication", 300, 10)
AUDIT = Ability("Audit Devices & Assets", 500, 20)

# Defining the Attackers Abilities
MITM = Ability("Man in the Middle (Steal Data)", 300, 20)
MAL = Ability("Malware (Steal Data)", 600, 60)
DDOS = Ability("DDoS (Control)", 600, 60)
PHI = Ability("Phishing (Steal Data)", 400, 30)
TRO = Ability("Trojan (Control)", 500, 40)
PSWD = Ability("Password Attack (Steal Data)", 300, 20)
RAN = Ability("Ransomware (Control)", 500, 40)

# Pairing the matchups `defense for attacker`
MITM.matchup = ENC
MAL.matchup = AMAL
DDOS.matchup = FWAL
PHI.matchup = TRU
TRO.matchup = HON
PSWD.matchup = MULAUTH
RAN.matchup = AUDIT

# Roles
ATTACKER = Role("Attacker", 5000)
DEFENDER = Role("Defender", 5000)
