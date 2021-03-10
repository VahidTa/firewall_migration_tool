import xmltodict
import json
import os

from resources.dst_vendor.dst_srx import SRX_DST
from resources.dst_vendor.dst_forti import Forti_DST
from resources.dst_vendor.dst_chpoint import CHPoint_DST
from resources.dst_vendor.dst_asa import ASA_DST

forti_translation = {
    'allow': 'accept',
    'no': 'enable',
    'yes': 'disable',
    'service-http': 'HTTP',
    'service-https': 'HTTPS',
}
srx_translation = {
    'allow': 'permit',
    'no': 'enabled',
    'yes': 'disabled',
    'service-http': 'junos-http',
    'service-https': 'junos-https',
}

chpoint_translation = {
    'allow': 'accept',
    'deny': 'drop',
    'yes': 'false',
    'no': 'true',
    'service-http': 'http',
    'service-https': 'https',
}

asa_translation = {
    'yes': 'inactive',
    'service-http': ['tcp', 'http'],
    'service-https': ['tcp', 'https'],
}

def palo_policy(file: str, vendor: str):
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
    dict_formatted = json.loads(json_formatted)['root']['response']
    for i in range(len(dict_formatted)):
        try:
            if 'rulebase' in dict_formatted[i]['result']:
                security_cfg = dict_formatted[i]['result']['rulebase']['security']['rules']['entry']
        except:
            continue
    position = 1
    for main_index in range(len(security_cfg)):
        policy_src_list = []
        policy_dst_list = []
        policy_app_list = []

        policy_name = security_cfg[main_index]['@name']
        source_zone = security_cfg[main_index]['from']['member']
        destination_zone = security_cfg[main_index]['to']['member']
        source_address_list = security_cfg[main_index]['source']['member']
        destination_address_list = security_cfg[main_index]['destination']['member']
        service_address_list = security_cfg[main_index]['service']['member']
        # application_address_list = security_cfg[main_index]['application']
        try:
            policy_state = security_cfg[main_index]['disabled']
        except:
            policy_state = 'no'
        policy_action = security_cfg[main_index]['action']
        try:
            policy_log = security_cfg[main_index]['log-start']
        except:
            policy_log = False
        policy_id = position

        if isinstance(source_address_list, (list)):
            for sub_index in range(len(source_address_list)):
                policy_source_address = source_address_list[sub_index]
                policy_src_list.append(policy_source_address)
        else:
            policy_source_address = source_address_list
        
        if isinstance(destination_address_list, (list)):
            for sub_index in range(len(destination_address_list)):
                policy_dst_address = destination_address_list[sub_index]
                policy_dst_list.append(policy_dst_address)
        else:
            policy_dst_address = destination_address_list
        
        if isinstance(service_address_list, (list)):
            for sub_index in range(len(service_address_list)):
                policy_app = destination_address_list[sub_index]
                policy_app_list.append(policy_app)
        else:
            policy_app = service_address_list

        if policy_log:
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
                policy_dst_address = 'all'
            if policy_app == 'any':
                policy_app = 'ALL'
            if len(policy_name) > 34:
                policy_name = policy_name[:34]
            
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
        elif vendor == 'srx':
            policy_action = srx_translation.get(policy_action, policy_action)
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
