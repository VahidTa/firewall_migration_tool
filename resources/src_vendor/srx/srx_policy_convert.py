import xmltodict
import json
import os

from resources.dst_vendor.dst_palo import Palo_DST
from resources.dst_vendor.dst_forti import Forti_DST
from resources.dst_vendor.dst_chpoint import CHPoint_DST
from resources.dst_vendor.dst_asa import ASA_DST

forti_translation = {
    'permit': 'accept',
    'enabled': 'enable',
    'disabled': 'disable',
    'junos-ftp': 'FTP',
    'junos-tftp': 'TFTP',
    'junos-rtsp': 'RTSP',
    'junos-ssh': 'SSH',
    'junos-telnet': 'TELNET',
    'junos-ping': 'PING',
    'junos-ntp': 'NTP',
    'junos-nntp': 'NNTP',
    'junos-http': 'HTTP',
    'junos-https': 'HTTPS',
    'junos-smtp': 'SMTP',
    'junos-syslog': 'SYSLOG',
    'junos-icmp-ping': 'PING',
    'junos-icmp-all': 'ALL_ICMP',
    'junos-dns-udp': 'DNS',
    'junos-dns-tcp': 'DNS',
    'junos-ms-sql': 'MS-SQL',
    'junos-sql-monitor': 'MS-SQL',
    'junos-vnc': 'VNC',
    'junos-smb-session': 'SMB',
    'junos-smb': 'SAMBA',
    'junos-radius': 'RADIUS',
    'junos-pptp': 'PPTP',
    'junos-ldap': 'LDAP',
    'junos-internet-locator-service': 'LDAP',
    'junos-ms-rpc-any': 'DCE-RPC',
    'junos-h323': 'H323',
    'junos-ospf': 'OSPF',
    'junos-tcp-any': 'ALL_TCP',
    'junos-udp-any': 'ALL_UDP',
}
palo_translation = {
    'permit': 'allow',
    'junos-http': 'service-http',
    'junos-https': 'service-https',
}

chpoint_translation = {
    'permit': 'accept',
    'deny': 'drop',
    'disabled': 'false',
    'enabled': 'true',
    'junos-ftp': 'ftp',
    'junos-tftp': 'tftp',
    'junos-rtsp': 'rtsp',
    'junos-ssh': 'ssh',
    'junos-telnet': 'telnet',
    'junos-ping': 'echo-request',
    'junos-ntp': 'ntp-udp',
    'junos-nntp': 'nntp',
    'junos-http': 'http',
    'junos-https': 'https',
    'junos-smtp': 'smtp',
    'junos-syslog': 'syslog',
    'junos-icmp-ping': 'echo-request',
    'junos-dns-udp': 'domain-udp',
    'junos-dns-tcp': 'domain-tcp',
    'junos-ms-sql': 'MS-SQL-Server',
    'junos-sql-monitor': 'MS-SQL-Monitor_UDP',
    'junos-smb-session': 'smb',
    'junos-smb': 'nbsession',
    'junos-radius': 'NEW-RADIUS',
    'junos-radacct': 'NEW-RADIUS-ACCOUNTING',
    'junos-tacacs': 'TACACSplus',
    'junos-pptp': 'pptp-tcp',
    'junos-ldap': 'ldap',
    'junos-internet-locator-service': 'ldap',
    'junos-ms-rpc-any': 'ALL_DCE_RPC',
    'junos-who': 'who',
    'junos-cifs': 'CIFS',
    'junos-ospf': 'ospf',
    'junos-tcp-any': 'unknown_protocol_tcp',
    'junos-udp-any': 'unknown_protocol_udp',
}

asa_translation = {
    'disabled': 'inactive',
    'junos-ftp': ['tcp', 'ftp'],
    'junos-tftp': ['udp', 'tftp'],
    'junos-rtsp': ['tcp', 'rtsp'],
    'junos-ssh': ['tcp', 'ssh'],
    'junos-telnet': ['tcp', 'telnet'],
    'junos-ping': ['icmp', 'na'],
    'junos-ntp': ['udp', 'ntp'],
    'junos-nntp': ['tcp','nntp'],
    'junos-http': ['tcp', 'http'],
    'junos-https': ['tcp', 'https'],
    'junos-smtp': ['tcp', 'smtp'],
    'junos-syslog': ['udp', 'syslog'],
    'junos-icmp-ping': ['icmp', 'echo'],
    'junos-dns-udp': ['udp', 'domain'],
    'junos-dns-tcp': ['tcp', 'domain'],
    'junos-smb': ['tcp', 'netbios-ssn'],
    'junos-radius': ['udp', 'radius'],
    'junos-radacct': ['udp', 'radius-acct'],
    'junos-tacacs': ['tcp', 'tacacs'],
    'junos-pptp': ['tcp', 'pptp'],
    'junos-ldap': ['tcp', 'ldap'],
    'junos-internet-locator-service': ['tcp', 'ldap'],
    'junos-who': ['udp', 'who'],
    'junos-cifs': ['tcp-udp', 'cifs'],
    'junos-ospf': ['ospf', 'na'],
    'junos-tcp-any': ['tcp', 'na'],
    'junos-udp-any': ['udp', 'na'],
}

def srx_policy(file: str, vendor: str):
    """Uses <show security policies | display xml> to provide rule order!"""
    if not os.path.exists(f'exported/{vendor}'):
            os.makedirs(f'exported/{vendor}')
    else:
        try:
            os.remove(os.path.join(f'exported/{vendor}/', 'policies.txt'))
        except:
            pass

    with open(f'configs/{file}', 'r') as f:
        my_text = xmltodict.parse(f.read())

    os.remove(f'configs/{file}')

    json_formatted = json.dumps(my_text)
    dict_formatted = json.loads(json_formatted)
    try:
        security_cfg = dict_formatted['rpc-reply']['multi-routing-engine-results']['multi-routing-engine-item']['security-policies']['security-context']
    except:
        security_cfg = dict_formatted['rpc-reply']['security-policies']['security-context']
    
    position = 1
    for main_index in range(len(security_cfg)):
        source_zone = security_cfg[main_index]['context-information'].get('source-zone-name', 'None')
        destination_zone = security_cfg[main_index]['context-information'].get('destination-zone-name', 'None')
        policy = security_cfg[main_index]['policies']

        
        for sub_index in range(len(policy)):
            policy_src_list = []
            policy_dst_list = []
            policy_app_list = []

            if isinstance(policy, (list)):
                policy_name = policy[sub_index]['policy-information'].get('policy-name', 'None')
                policy_state = policy[sub_index]['policy-information'].get('policy-state', 'None')
                policy_id = policy[sub_index]['policy-information'].get('policy-identifier', 'None')
                policy_seq = policy[sub_index]['policy-information'].get('policy-sequence-number', 'None')
                policy_source_address = policy[sub_index]['policy-information']['source-addresses']['source-address']
                policy_destination_address = policy[sub_index]['policy-information']['destination-addresses']['destination-address']
                policy_application = policy[sub_index]['policy-information']['applications']['application']
                if isinstance(policy_source_address, (list)):
                    for inc_index in range(len(policy_source_address)):
                        policy_src_address = policy_source_address[inc_index].get('address-name', 'None')
                        policy_src_list.append(policy_src_address)
                else:
                    policy_src_address = policy_source_address.get('address-name', 'None')
                if isinstance(policy_destination_address, (list)):
                    for inc_index in range(len(policy_destination_address)):
                        policy_dst_address = policy_destination_address[inc_index].get('address-name', 'None')
                        policy_dst_list.append(policy_dst_address)
                else:
                    policy_dst_address = policy_destination_address.get('address-name', 'None')
                if isinstance(policy_application, (list)):
                    for inc_index in range(len(policy_application)):
                        policy_app = policy_application[inc_index].get('application-name', 'None')
                        if vendor == 'forti' and 'junos' in policy_app:
                            policy_app = forti_translation.get(policy_app, policy_app)
                        elif vendor == 'palo' and 'junos' in policy_app:
                            policy_app = palo_translation.get(policy_app, policy_app)
                        elif vendor == 'chpoint' and 'junos' in policy_app:
                            policy_app = chpoint_translation.get(policy_app, policy_app)
                        elif vendor == 'asa' and 'junos' in policy_app:
                            policy_app = asa_translation.get(policy_app, policy_app)
                        
                        policy_app_list.append(policy_app)
                else:
                    policy_app = policy_application.get('application-name', 'None')
                    if vendor == 'forti' and 'junos' in policy_app:
                            policy_app = forti_translation.get(policy_app, policy_app)
                    elif vendor == 'palo' and 'junos' in policy_app:
                        policy_app == palo_translation.get(policy_app, policy_app)
                    elif vendor == 'chpoint' and 'junos' in policy_app:
                            policy_app = chpoint_translation.get(policy_app, policy_app)
                    elif vendor == 'asa' and 'junos' in policy_app:
                            policy_app = asa_translation.get(policy_app, policy_app)
                    
                policy_action = policy[sub_index]['policy-information']['policy-action'].get('action-type', 'None')

                if 'log' in list(policy[sub_index]['policy-information']['policy-action'].keys()):
                    policy_log = True
                else:
                    policy_log = False
            else:
                policy_name = policy['policy-information'].get('policy-name', 'None')
                policy_state = policy['policy-information'].get('policy-state', 'None')
                policy_id = policy['policy-information'].get('policy-identifier', 'None')
                # policy_seq = policy['policy-information'].get('policy-sequence-number', 'None')
                policy_source_address = policy['policy-information']['source-addresses']['source-address']
                policy_destination_address = policy['policy-information']['destination-addresses']['destination-address']
                policy_application = policy['policy-information']['applications']['application']

                if isinstance(policy_source_address, (list)): 
                    for inc_index in range(len(policy_source_address)):
                        policy_src_address = policy_source_address[inc_index].get('address-name', 'None')
                        policy_src_list.append(policy_src_address)
                else:
                    policy_src_address = policy_source_address.get('address-name', 'None')
                if isinstance(policy_destination_address, (list)):
                    for inc_index in range(len(policy_destination_address)):
                        policy_dst_address = policy_destination_address[inc_index].get('address-name', 'None')
                        policy_dst_list.append(policy_dst_address)
                else:
                    policy_dst_address = policy_destination_address.get('address-name', 'None')
                if isinstance(policy_application, (list)):
                    for inc_index in range(len(policy_application)):
                        policy_app = policy_application[inc_index].get('application-name', 'None')
                        if vendor == 'forti' and 'junos' in policy_app:
                            policy_app = forti_translation.get(policy_app, policy_app)
                        elif vendor == 'palo' and 'junos' in policy_app:
                            policy_app = palo_translation.get(policy_app, policy_app)
                        elif vendor == 'chpoint' and 'junos' in policy_app:
                            policy_app = chpoint_translation.get(policy_app, policy_app)
                        elif vendor == 'asa' and 'junos' in policy_app:
                            policy_app = asa_translation.get(policy_app, policy_app)
                        
                        if vendor == 'chpoint':
                            if policy_app[:1].isdigit():
                                policy_app = 'custom_' + policy_app
                        policy_app_list.append(policy_app)
                else:
                    policy_app = policy_application.get('application-name', 'None')
                    if vendor == 'forti' and 'junos' in policy_app:
                        policy_app = forti_translation.get(policy_app, policy_app)
                    elif vendor == 'palo' and 'junos' in policy_app:
                        policy_app = palo_translation.get(policy_app, policy_app)
                    elif vendor == 'chpoint' and 'junos' in policy_app:
                        policy_app = chpoint_translation.get(policy_app, policy_app)
                    elif vendor == 'asa' and 'junos' in policy_app:
                        policy_app = asa_translation.get(policy_app, policy_app)
                    
                    if vendor == 'chpoint':
                            if policy_app[:1].isdigit():
                                policy_app = 'custom_' + policy_app


                policy_action = policy['policy-information']['policy-action'].get('action-type', 'None')

                if 'log' in list(policy['policy-information']['policy-action'].keys()):
                    policy_log = True
                else:
                    policy_log = False
            if policy_src_list:
                policy_src_address = ' '.join(policy_src_list)
            if policy_dst_list:
                policy_dst_address = ' '.join(policy_dst_list)
            if policy_app_list:
                try:
                    policy_app = ' '.join(policy_app_list)
                except:
                    policy_app = policy_app_list
            
            if vendor == 'forti':
                policy_state = forti_translation.get(policy_state, policy_state)
                policy_action = forti_translation.get(policy_action, policy_action)
                if 'any' in policy_src_address:
                    policy_src_address = 'all'
                if 'any' in policy_dst_address:
                    policy_dst_address == 'all'
                if policy_app == 'any':
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
                    
            elif vendor == 'chpoint':
                policy_action = chpoint_translation.get(policy_action, policy_action)
                policy_state = chpoint_translation.get(policy_state, policy_state)

                if policy_dst_list:
                    dst_list = []
                    for i in range(len(policy_dst_list)):
                        dst_list.append(f'destination.{i+1} "{policy_dst_list[i]}"')
                    policy_dst_address = ' '.join(dst_list)
                else:
                    policy_dst_address = f'destination "{policy_dst_address}"'
                
                if policy_src_list:
                    src_list = []
                    for i in range(len(policy_src_list)):
                        src_list.append(f'source.{i+1} "{policy_src_list[i]}"')
                    policy_src_address = ' '.join(src_list)
                else:
                    policy_src_address = f'source "{policy_src_address}"'
                if policy_app_list:
                    app_list = []
                    for i in range(len(policy_app_list)):
                        if policy_app_list[i][:1].isdigit():
                            policy_app = 'custom_' + policy_app_list[i]
                        else:
                            policy_app = policy_app_list[i]
                        app_list.append(f'service.{i+1} "{policy_app}"')
                    policy_app = ' '.join(app_list)
                else:
                    if policy_app[:1].isdigit():
                        policy_app = 'custom_' + policy_app

                    policy_app = f'service "{policy_app}"'
                
                chpoint = CHPoint_DST()
                chpoint.policy(
                    policy_name,
                    source_zone,
                    destination_zone,
                    policy_src_address,
                    policy_dst_address,
                    policy_app,
                    policy_log,
                    policy_state,
                    policy_action,
                    policy_id,
                    position
                )
                

                position += 1
