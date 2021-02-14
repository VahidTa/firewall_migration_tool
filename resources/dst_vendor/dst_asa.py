from resources.ip_address_converter.netmask_convereter import netmasker, nethost

class ASA_DST:

    def service(*args):
        application_name = args[1]
        destination_port = args[2]
        source_port = args[3]
        application_protocol = args[4]
        application_desc = args[5]

        with open('exported/asa/service_objects.txt', 'a') as f:
            f.write(f'object service {application_name}\n')
            if destination_port:
                if '-' in destination_port:
                    destination_port = destination_port.replace('-', ' ')
                    f.write(f'service {application_protocol} destination range {destination_port}\n')
                else:
                    f.write(f'service {application_protocol} destination eq {destination_port}\n')
            elif source_port:
                if '-' in source_port:
                    source_port = source_port.replace('-', ' ')
                    f.write(f'service {application_protocol} source range {source_port}\n')
                else:
                    f.write(f'service {application_protocol} source eq {source_port}\n')
            if application_desc:
                f.write(f'description {application_desc} \n')
            f.write('exit\n\n')       
    
    def service_set(*args):
        app_set_name = args[1]
        app_list = args[2]
        app_set_desc = args[3]

        with open('exported/asa/service_object_group.txt', 'a') as f:
            f.write(f'object-group service {app_set_name}\n')
            for object in app_list:
                if isinstance(object, (list)):
                    if object[0] == 'icmp':
                        f.write(f'service-object {object[0]} {object[1]}\n')
                    else:
                        f.write(f'service-object {object[0]} destination eq {object[1]}\n')
                else:
                    f.write(f'service-object object {object} \n')
            if app_set_desc:
                f.write(f'description "{app_set_desc}" \n')
            f.write('exit\n\n')
    
    def address(*args):
        address_name = args[1]
        address_ip = args[2]
        address_desc = args[3]

        with open('exported/asa/object_network.txt', 'a') as f:
            if '-' in address_ip:
                start_ip = address_ip.split('-')[0].replace(' ', '')
                end_ip = address_ip.split('-')[1].replace(' ', '')
                address_netmask = f'range {start_ip} {end_ip}'
            elif '/32' in address_ip:
                address_netmask = 'host ' + nethost(address_ip)
            else:
                address_netmask = 'subnet ' + netmasker(address_ip)
            if '/' in address_name:
                address_name = address_name.replace('/', '-')
            f.write(f'object network {address_name}\n')
            if address_desc:
                f.write(f'description {address_desc}\n')
            f.write(f'{address_netmask}\n')
            f.write('exit\n\n')
    
    
    def address_set(*args):
        address_set_name = args[1]
        address_name_list = args[2]
        address_set_desc = args[3]

        with open('exported/asa/object_group_network.txt', 'a') as f:
            f.write(f'object-group network {address_set_name}\n')
            if address_set_desc:
                f.write(f'description {address_set_desc}\n')
            for address_name in address_name_list:
                f.write(f'network-object object {address_name}\n')
            f.write('exit\n\n')
    
    def policy(*args):
        """Not Implemented"""
        return
        policy_name = args[1]
        source_zone = args[2]
        destination_zone = args[3]
        policy_src_address = args[4]
        policy_dst_address = args[5]
        policy_app = args[6]
        policy_log = args[7]
        policy_state = args[8]
        policy_action = args[9]
        policy_id = args[10]

