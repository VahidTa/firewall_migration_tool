import os

class Palo_DST:

    def service(*args):
        application_name = args[1]
        destination_port = args[2]
        source_port = args[3]
        application_protocol = args[4]
        application_desc = args[5]
        app_session_ttl = args[6]
        
        with open('exported/palo/services.txt', 'a') as f:
            if destination_port:
                f.write(f'set service {application_name} protocol {application_protocol} port {destination_port}\n\n')
            elif source_port:
                f.write(f'set service {application_name} protocol {application_protocol} source-port {source_port}\n\n')
            if application_desc:
                f.write(f'set service {application_name} description "{application_desc}"\n\n')
            if app_session_ttl:
                f.write(f'set service {application_name} protocol {application_protocol} override yes timeout {app_session_ttl}\n\n')
                

    
    def service_set(*args):
        app_set_name = args[1]
        app_name = args[2]

        with open('exported/palo/service_group.txt', 'a') as f:
            f.write(f'set service-group {app_set_name} members [ {app_name} ]\n\n')
    
    def address(*args):
        address_name = args[1]
        address_ip = args[2]
        address_desc = args[3]

        with open('exported/palo/addresses.txt', 'a') as f:
            if '-' in address_ip:
                address_ip = address_ip.replace(' ', '')
                f.write(f'set address {address_name} ip-range {address_ip}\n\n')
            else:
                f.write(f'set address {address_name} ip-netmask {address_ip}\n\n')
            if address_desc:
                f.write(f'set address {address_name} description "{address_desc}"\n\n')
    
    def address_set(*args):
        address_set_name = args[1]
        address_name = args[2]
        address_set_desc = args[3]

        with open('exported/palo/address_group.txt', 'a') as f:
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

        the_path = 'exported/palo/policies.txt'
        with open(the_path, 'a') as output:
            if os.path.getsize(the_path) == 0:
                output.write('edit rulebase security\n\n')
            output.write(f'set rules {policy_name} from {source_zone}\n')
            output.write(f'set rules {policy_name} to {destination_zone}\n')
            output.write(f'set rules {policy_name} source [ {policy_src_address} ]\n')
            output.write(f'set rules {policy_name} destination [ {policy_dst_address} ]\n')
            output.write(f'set rules {policy_name} service [ {policy_app} ]\n')
            output.write(f'set rules {policy_name} application any\n')
            if source_zone == destination_zone:
                output.write(f'set rules {policy_name} rule-type intrazone\n')
            else:
                output.write(f'set rules {policy_name} rule-type interzone\n')
            if policy_log:
                output.write(f'set rules {policy_name} log-start yes\n')
            if policy_state == 'disabled':
                output.write(f'set rules {policy_name} disabled yes\n')
            output.write(f'set rules {policy_name} action {policy_action}\n\n')
        