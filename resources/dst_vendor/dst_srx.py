import os

class SRX_DST:

    def service(*args):
        application_name = args[1]
        destination_port = args[2]
        source_port = args[3]
        application_protocol = args[4]
        application_desc = args[5]
        app_session_ttl = args[6]
        
        with open('exported/srx/services.txt', 'a') as f:
            if destination_port:
                f.write(f'set service {application_name} protocol {application_protocol} port {destination_port}\n\n')
            elif source_port:
                f.write(f'set service {application_name} protocol {application_protocol} source-port {source_port}\n\n')
            if application_desc:
                f.write(f'set service {application_name} description "{application_desc}"\n\n')
    
    def service_set(*args):
        app_set_name = args[1]
        app_name = args[2]

        with open('exported/srx/service_group.txt', 'a') as f:
            f.write(f'set service-group {app_set_name} members [ {app_name} ]\n\n')
    
    def address(*args):
        address_name = args[1]
        address_ip = args[2]
        address_desc = args[3]

        the_path = 'exported/srx/addresses.txt'
        with open(the_path, 'a') as f:
            if os.path.getsize(the_path) == 0:
                f.write(f'edit security address-book global\n\n')
            if '-' in address_ip:
                start_ip = address_ip.split('-')[0].replace(' ', '')
                end_ip = address_ip.split('-')[1].replace(' ', '')
                f.write(f'set address {address_name} range-address {start_ip} to {end_ip}\n\n')
            else:
                f.write(f'set address {address_name} ip-netmask {address_ip}\n\n')
            if address_desc:
                f.write(f'set address {address_name} description "{address_desc}"\n\n')
    
    def address_set(*args):
        address_set_name = args[1]
        address_name = args[2]
        address_set_desc = args[3]

        with open('exported/srx/address_group.txt', 'a') as f:
            f.write(f'set address-group {address_set_name} static [ {address_name} ]\n\n')
            if address_set_desc:
                f.write(f'set address-group {address_set_name} description "{address_set_desc}"\n\n')
    
    def policy(*args):
        policy_name = args[1]
        source_zone = args[2]
        destination_zone = args[3]
        policy_src_address = args[4]
        policy_dst_address = args[5]
        policy_app = args[6]
        policy_log = args[7]
        policy_state = args[8]
        policy_action = args[9]

        the_path = 'exported/srx/policies.txt'
        with open(the_path, 'a') as output:
            if os.path.getsize(the_path) == 0:
                output.write('edit security policies\n\n')
            if source_zone == 'global' and destination_zone == 'global':
                output.write(f'set global policy {policy_name} match source-address [ {policy_src_address} ]\n')
                output.write(f'set global policy {policy_name} match destination-address [ {policy_src_address} ]\n')
                output.write(f'set global policy {policy_name} match application [ {policy_src_address} ]\n')
                if policy_log:
                    output.write(f'set global policy {policy_name} then log session-close session-init \n')
                output.write(f'set global policy {policy_name} then  {policy_action} \n\n')
            else:
                output.write(f'set from-zone {source_zone} to-zone {destination_zone} policy {policy_name} match source-address [ {policy_src_address} ]\n')
                output.write(f'set from-zone {source_zone} to-zone {destination_zone} policy {policy_name} match destination-address [ {policy_dst_address} ]\n')
                output.write(f'set from-zone {source_zone} to-zone {destination_zone} policy {policy_name} match application [ {policy_app} ]\n')
                if policy_log:
                    output.write(f'set from-zone {source_zone} to-zone {destination_zone} policy {policy_name} then log session-close session-init \n')
                output.write(f'set from-zone {source_zone} to-zone {destination_zone} policy {policy_name} then {policy_action}\n\n')

        