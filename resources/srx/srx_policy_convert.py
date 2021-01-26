import xmltodict
import json


translation = {
    'permit': 'accept',
    'deny': 'deny',
    'enabled': 'enable',
    'disabled': 'disable'
}


def srx_policy(file):
    """Uses <show security | display xml> to provide rule order!"""

    with open(f'configs/{file}', 'r') as f:
        my_text = xmltodict.parse(f.read())

    json_formatted = json.dumps(my_text)
    dict_formatted = json.loads(json_formatted)

    security_cfg = dict_formatted['rpc-reply']['multi-routing-engine-results']['multi-routing-engine-item']['security-policies']['security-context']
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
                policy_state = translation.get(policy_state, 'None')
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
                        policy_app_list.append(policy_app)
                else:
                    policy_app = policy_application.get('application-name', 'None')
                policy_action = policy[sub_index]['policy-information']['policy-action'].get('action-type', 'None')
                policy_action = translation.get(policy_action, 'None')

                if 'log' in list(policy[sub_index]['policy-information']['policy-action'].keys()):
                    policy_log = True
                else:
                    policy_log = False
            else:
                policy_name = policy['policy-information'].get('policy-name', 'None')
                policy_state = policy['policy-information'].get('policy-state', 'None')
                policy_state = translation.get(policy_state, 'None')
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
                        policy_app_list.append(policy_app)
                else:
                    policy_app = policy_application.get('application-name', 'None')


                policy_action = policy['policy-information']['policy-action'].get('action-type', 'None')
                policy_action = translation.get(policy_action, 'None')

                if 'log' in list(policy['policy-information']['policy-action'].keys()):
                    policy_log = True
                else:
                    policy_log = False
            if policy_src_list:
                policy_src_address = ' '.join(policy_src_list)
            if policy_dst_list:
                policy_dst_address = ' '.join(policy_dst_list)
            if policy_app_list:
                policy_app = ' '.join(policy_app_list)

            with open('exported/policies.txt', 'a') as output:
                output.write(f'edit {policy_id}\n')
                output.write(f'set name {policy_name}\n')
                output.write(f'set srcintf {source_zone}\n')
                output.write(f'set dstintf {destination_zone}\n')
                output.write(f'set srcaddr {policy_src_address}\n')
                output.write(f'set dstaddr {policy_dst_address}\n')
                output.write(f'set action {policy_action}\n')
                output.write(f'set service {policy_app}\n')
                if policy_log:
                    output.write(f'set logtraffic all\n')
                output.write(f'set status {policy_state}\n')
                output.write(f'next\n\n')

