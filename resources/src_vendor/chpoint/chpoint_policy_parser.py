import os
import pandas as pd

from resources.dst_vendor.dst_palo import Palo_DST
from resources.dst_vendor.dst_forti import Forti_DST
from resources.dst_vendor.dst_srx import SRX_DST
from resources.dst_vendor.dst_asa import ASA_DST

forti_translation = {
    'Accept': 'accept',
    'enabled': 'enable',
    'disabled': 'disable',
    'ftp': 'FTP',
    'tftp': 'TFTP',
    'rtsp': 'RTSP',
    'ssh': 'SSH',
    'telnet': 'TELNET',
    'echo-request': 'PING',
    'ntp-udp': 'NTP',
    'nntp': 'NNTP',
    'http': 'HTTP',
    'https': 'HTTPS',
    'smtp': 'SMTP',
    'syslog': 'SYSLOG',
    'domain-udp': 'DNS',
    'domain-tcp': 'DNS',
    'MS-SQL-Server': 'MS-SQL',
    'smb': 'SMB',
    'nbsession': 'SAMBA',
    'NEW-RADIUS': 'RADIUS',
    'pptp-tcp': 'PPTP',
    'ldap': 'LDAP',
    'ALL_DCE_RPC': 'DCE-RPC',
    'H323': 'H323',
    'ospf': 'OSPF',
    'unknown-protocol-tcp': 'ALL_TCP',
    'unknown-protocol-udp': 'ALL_UDP',
}
palo_translation = {
    'Allow': 'allow',
    'http': 'service-http',
    'https': 'service-https',
}

srx_translation = {
    'Accept': 'permit',
    'Drop': 'deny',
    'false': 'disabled',
    'true': 'enabled',
    'ftp': 'junos-ftp',
    'tftp': 'junos-tftp',
    'rtsp': 'junos-rtsp',
    'ssh': 'junos-ssh',
    'telnet': 'junos-telnet',
    'echo-request': 'junos-ping',
    'echo-request': 'junos-icmp-ping',
    'ntp-udp': 'junos-ntp',
    'nntp': 'junos-nntp',
    'http': 'junos-http',
    'https': 'junos-https',
    'smtp': 'junos-smtp',
    'syslog': 'junos-syslog',
    'domain-udp': 'junos-dns-udp',
    'domain-tcp': 'junos-dns-tcp',
    'MS-SQL-Server': 'junos-ms-sql',
    'MS-SQL-Monitor_UDP': 'junos-sql-monitor',
    'smb': 'junos-smb-session',
    'nbsession': 'junos-smb',
    'NEW-RADIUS': 'junos-radius',
    'NEW-RADIUS-ACCOUNTING': 'junos-radacct',
    'TACACSplus': 'junos-tacacs',
    'pptp-tcp': 'junos-pptp',
    'ldap': 'junos-ldap',
    'ALL_DCE_RPC': 'junos-ms-rpc-any',
    'who': 'junos-who',
    'CIFS': 'junos-cifs',
    'ospf': 'junos-ospf',
    'unknown_protocol_tcp': 'junos-tcp-any',
    'unknown_protocol_udp': 'junos-udp-any',
}

asa_translation = {
    'Accept': 'permit',
    'disabled': 'inactive',
    'ftp': ['tcp', 'ftp'],
    'tftp': ['udp', 'tftp'],
    'rtsp': ['tcp', 'rtsp'],
    'ssh': ['tcp', 'ssh'],
    'telnet': ['tcp', 'telnet'],
    'echo-request': ['icmp', 'na'],
    'ntp': ['udp', 'ntp'],
    'nntp': ['tcp','nntp'],
    'http': ['tcp', 'http'],
    'https': ['tcp', 'https'],
    'smtp': ['tcp', 'smtp'],
    'syslog': ['udp', 'syslog'],
    'echo-request': ['icmp', 'echo'],
    'domain-udp': ['udp', 'domain'],
    'domain-tcp': ['tcp', 'domain'],
    'smb': ['tcp', 'netbios-ssn'],
    'NEW-RADIUS': ['udp', 'radius'],
    'NEW-RADIUS-ACCOUNTING': ['udp', 'radius-acct'],
    'TACACSplus': ['tcp', 'tacacs'],
    'pptp-tcp': ['tcp', 'pptp'],
    'ldap': ['tcp', 'ldap'],
    'who': ['udp', 'who'],
    'CIFS': ['tcp-udp', 'cifs'],
    'ospf': ['ospf', 'na'],
    'unknown_protocol_tcp': ['tcp', 'na'],
    'unknown_protocol_udp': ['udp', 'na'],
}

def chpoint_policy(file: str, vendor: str):
    """Uses <show security policies | display xml> to provide rule order!"""
    if not os.path.exists(f'exported/{vendor}'):
            os.makedirs(f'exported/{vendor}')
    else:
        try:
            os.remove(os.path.join(f'exported/{vendor}/', 'policies.txt'))
        except:
            pass
    
    names = ["No.", "Name", "Source", "Destination", "Services & Applications", "Action", "Track"]
    cols = [0, 2, 3, 4, 6, 8, 9]
    with open(f'configs/{file}', 'r') as f:
        imported = pd.read_csv(f, usecols=cols, names=names, skiprows=1, keep_default_na=False, skipinitialspace=True)
    os.remove(f'configs/{file}')

    for _, row in imported.iterrows():
        policy_id = row["No."]
        policy_name = row["Name"]
        policy_src_address = row["Source"]
        policy_dst_address = row["Destination"]
        policy_action = row["Action"]
        policy_log = row["Track"]
        policy_app = row["Services & Applications"]
        source_zone = 'global'
        destination_zone = 'global'
        policy_state = ''

        try:
            app_list = policy_app.split(';')
            new_list = []
            for app in app_list:
                if vendor == 'forti':
                    policy_app = forti_translation.get(app, app)
                elif vendor == 'palo':
                    policy_app = palo_translation.get(app, app)
                elif vendor == 'srx':
                    policy_app = srx_translation.get(app, app)
                elif vendor == 'asa':
                    policy_app = asa_translation.get(app, app)
                new_list.append(policy_app)
            policy_app = ' '.join(new_list)
        except:
            pass
        try:
            src_list = policy_src_address.split(';')
            policy_src_address = ' '.join(src_list)
        except:
            pass

        try:
            dst_list = policy_dst_address.split(';')
            policy_dst_address = ' '.join(dst_list)
        except:
            pass
    
        if vendor == 'forti':
            policy_action = forti_translation.get(policy_action, policy_action)
            if 'Any' in policy_src_address:
                policy_src_address = 'all'
            if 'Any' in policy_dst_address:
                policy_dst_address == 'all'
            if policy_app == 'Any':
                policy_app = 'ALL'
            
            forti = Forti_DST()
            forti.policy(
                policy_name,
                source_zone,
                destination_zone,
                policy_src_address,
                policy_dst_address,
                policy_app,
                policy_log,
                policy_state,
                policy_action,
                policy_id
                )
            
        elif vendor == 'asa':
            policy_action = asa_translation.get(policy_action, policy_action)
            if 'Any' in policy_src_address:
                policy_src_address = 'any'
            if 'Any' in policy_dst_address:
                policy_dst_address == 'any'
            if policy_app == 'Any':
                policy_app = 'any'
            asa = ASA_DST()
            asa.policy(
                policy_name,
                source_zone,
                destination_zone,
                policy_src_address,
                policy_dst_address,
                policy_app,
                policy_log,
                policy_state,
                policy_action,
                policy_id
                )
        elif vendor == 'palo':
            policy_action = palo_translation.get(policy_action, policy_action)
            palo = Palo_DST()
            palo.policy(
                policy_name,
                source_zone,
                destination_zone,
                policy_src_address,
                policy_dst_address,
                policy_app,
                policy_log,
                policy_state,
                policy_action
                )
        elif vendor == 'srx':
            policy_action = srx_translation.get(policy_action, policy_action)
            if 'Any' in policy_src_address:
                policy_src_address = 'any'
            if 'Any' in policy_dst_address:
                policy_dst_address == 'any'
            if policy_app == 'Any':
                policy_app = 'any'
            srx = SRX_DST()
            srx.policy(
                policy_name,
                source_zone,
                destination_zone,
                policy_src_address,
                policy_dst_address,
                policy_app,
                policy_log,
                policy_state,
                policy_action
                )
