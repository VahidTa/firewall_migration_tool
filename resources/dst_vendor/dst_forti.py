import os


class Forti_DST:
    def service(*args):
        application_name = args[1]
        destination_port = args[2]
        source_port = args[3]
        application_protocol = args[4]
        application_desc = args[5]
        app_session_ttl = args[6]

        the_path = "exported/forti/services.txt"
        with open(the_path, "a") as f:
            if os.path.getsize(the_path) == 0:
                f.write("config firewall service custom\n\n")

            f.write(f"edit {application_name}\n")
            if destination_port and not source_port:
                f.write(f"set {application_protocol}-portrange {destination_port}\n")
            elif source_port and not destination_port:
                f.write(f"set {application_protocol}-portrange {source_port}\n")
            elif source_port and destination_port:
                f.write(f"set {application_protocol}-portrange {destination_port}:{source_port}\n")
            if app_session_ttl:
                f.write(f"set session-ttl {app_session_ttl}\n")
            if application_desc:
                f.write(f'set comment "{application_desc}"\n')

            f.write("next\n\n")

    def service_set(*args):
        app_set_name = args[1]
        app_name = args[2]
        app_set_desc = args[3]

        the_path = "exported/forti/service_group.txt"
        with open(the_path, "a") as f:
            if os.path.getsize(the_path) == 0:
                f.write("config firewall service group\n\n")
            f.write(f"edit {app_set_name}\n")
            f.write(f"set member {app_name}\n")
            if app_set_desc:
                f.write(f'set comment "{app_set_desc}"\n')
            f.write("next\n\n")

    def address(*args):
        address_name = args[1]
        address_ip = args[2]
        address_desc = args[3]

        the_path = "exported/forti/addresses.txt"
        with open(the_path, "a") as f:
            if os.path.getsize(the_path) == 0:
                f.write("config firewall address\n\n")
            f.write(f"edit {address_name}\n")
            if address_desc:
                f.write(f'set comment "{address_desc}"\n')
            if "-" in address_ip:
                f.write("set type iprange\n")
                start_ip = address_ip.split("-")[0].replace(" ", "")
                end_ip = address_ip.split("-")[1].replace(" ", "")
                f.write(f"set start-ip {start_ip}\n")
                f.write(f"set end-ip {end_ip}\n")
            else:
                f.write(f"set subnet {address_ip}\n")
            f.write("next\n\n")

    def address_set(*args):
        address_set_name = args[1]
        address_name = args[2]
        address_set_desc = args[3]

        the_path = "exported/forti/address_group.txt"
        with open(the_path, "a") as f:
            if os.path.getsize(the_path) == 0:
                f.write("config firewall addrgrp\n\n")
            f.write(f"edit {address_set_name}\n")
            f.write(f"set member {address_name}\n")
            if address_set_desc:
                f.write(f'set comment "{address_set_desc}"\n')
            f.write("next\n\n")

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
        policy_id = args[10]

        the_path = "exported/forti/policies.txt"
        with open(the_path, "a") as output:
            if os.path.getsize(the_path) == 0:
                output.write("config firewall policy\n\n")
            output.write(f"edit {policy_id}\n")
            output.write(f"set name {policy_name}\n")
            output.write(f"set srcintf {source_zone}\n")
            output.write(f"set dstintf {destination_zone}\n")
            output.write(f"set srcaddr {policy_src_address}\n")
            output.write(f"set dstaddr {policy_dst_address}\n")
            output.write(f"set action {policy_action}\n")
            output.write(f"set service {policy_app}\n")
            if policy_log:
                output.write("set logtraffic all\n")
            if "junos" in policy_app:
                output.write('set comments "Error, please check service for correction!"\n')
            output.write(f"set status {policy_state}\n")
            output.write("set schedule always\n")
            output.write("next\n\n")
