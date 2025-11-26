import os

from resources.dst_vendor.vendor_abc import VendorAbc

protocol_mapper = {
    89: "ospf",
    51: "ah",
    47: "gre",
    50: "esp",
    2: "igmp",
    4: "ipip",
    103: "pim",
    46: "rsvp",
    132: "sctp",
}


class SrxDst(VendorAbc):
    def service(*args):
        application_name = args[1]
        destination_port: list | int | str = args[2]
        source_port = args[3]
        application_protocol = args[4]
        application_desc = args[5]
        protocol_number = args[6]
        icmp_code = args[7]
        icmp_type = args[8]

        if " " in application_name:
            application_name = f'"{application_name}"'

        with open("exported/srx/services.txt", "a") as f:
            if application_protocol == "IP" and protocol_number is not None:
                f.write(
                    f"set applications application {application_name} protocol {protocol_mapper.get(protocol_number, protocol_number)}\n\n"
                )
            elif application_protocol == "ICMP":
                cmd = f"set applications application {application_name} protocol icmp"
                if icmp_code:
                    cmd += f" icmp-code {icmp_code}"
                if icmp_type:
                    cmd += f" icmp-type {icmp_type}"
                cmd += "\n\n"
                f.write(cmd)
            else:
                if destination_port:
                    if isinstance(destination_port, list):
                        for i, port in enumerate(destination_port):
                            f.write(
                                f"set applications application {application_name} term T{i} protocol {application_protocol} destination-port {port}\n\n"
                            )
                    else:
                        f.write(
                            f"set applications application {application_name} protocol {application_protocol} destination-port {destination_port}\n\n"
                        )
                if source_port:
                    if isinstance(source_port, list):
                        for i, port in enumerate(source_port):
                            f.write(
                                f"set applications application {application_name} term T{i} protocol {application_protocol} source-port {port}\n\n"
                            )
                    else:
                        f.write(
                            f"set applications application {application_name} protocol {application_protocol} source-port {source_port}\n\n"
                        )
            if application_desc:
                f.write(f'set applications application {application_name} description "{application_desc}"\n\n')

    def service_set(*args):
        app_set_name: str = args[1]
        app_list = args[2]
        app_set_desc = args[3]

        if " " in app_set_name:
            app_set_name = f'"{app_set_name}"'

        with open("exported/srx/service_group.txt", "a") as f:
            for app in app_list:
                ### if vendor does not distinguish app_grpup and app, this can be added to the source vendor to let code convert it to application-set child
                if "_FWMIG" in app:
                    f.write(f"set applications application-set {app_set_name} application-set {app}\n\n")
                else:
                    if " " in app:
                        app = f'"{app}"'
                    f.write(f"set applications application-set {app_set_name} application {app}\n\n")
            if app_set_desc:
                f.write(f'set applications application-set {app_set_name} description "{app_set_desc}"\n\n')

    def address(*args):
        address_name = args[1]
        address_ip = args[2]
        address_desc = args[3]
        address_type = args[4] or "subnet"

        if " " in address_name:
            address_name = f'"{address_name}"'

        the_path = "exported/srx/addresses.txt"
        with open(the_path, "a") as f:
            if os.path.getsize(the_path) == 0:
                f.write("edit security address-book global\n\n")
            if address_type == "range":
                address_ip = address_ip.split("-")
                start_ip = address_ip[0].replace(" ", "")
                end_ip = address_ip[1].replace(" ", "")
                f.write(f"set address {address_name} range-address {start_ip} to {end_ip}\n\n")
            elif address_type == "subnet":
                f.write(f"set address {address_name} {address_ip}\n\n")
            elif address_type == "fqdn":
                f.write(f"set address {address_name} dns-name {address_ip}\n\n")
            if address_desc:
                f.write(f'set address {address_name} description "{address_desc}"\n\n')

    def address_set(*args):
        address_set_name = args[1]
        address_name_list = args[2]
        address_set_desc = args[3]

        if " " in address_set_name:
            address_set_name = f'"{address_set_name}"'

        with open("exported/srx/address_group.txt", "a") as f:
            for name in address_name_list:
                f.write(f"set address-set {address_set_name} address {name}\n\n")
            if address_set_desc:
                f.write(f'set address-set {address_set_name} description "{address_set_desc}"\n\n')

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

        the_path = "exported/srx/policies.txt"
        with open(the_path, "a") as output:
            if os.path.getsize(the_path) == 0:
                output.write("edit security policies\n\n")
            if source_zone == "global" and destination_zone == "global":
                output.write(f"set global policy {policy_name} match source-address [ {policy_src_address} ]\n")
                output.write(f"set global policy {policy_name} match destination-address [ {policy_src_address} ]\n")
                output.write(f"set global policy {policy_name} match application [ {policy_src_address} ]\n")
                if policy_log:
                    output.write(f"set global policy {policy_name} then log session-close session-init \n")
                output.write(f"set global policy {policy_name} then  {policy_action} \n\n")
                if not policy_state:
                    output.write(f"deactivate global policy {policy_name}\n\n")
            else:
                output.write(
                    f"set from-zone {source_zone} to-zone {destination_zone} policy {policy_name} match source-address [ {policy_src_address} ]\n"
                )
                output.write(
                    f"set from-zone {source_zone} to-zone {destination_zone} policy {policy_name} match destination-address [ {policy_dst_address} ]\n"
                )
                output.write(
                    f"set from-zone {source_zone} to-zone {destination_zone} policy {policy_name} match application [ {policy_app} ]\n"
                )
                if policy_log:
                    output.write(
                        f"set from-zone {source_zone} to-zone {destination_zone} policy {policy_name} then log session-close session-init \n"
                    )
                output.write(
                    f"set from-zone {source_zone} to-zone {destination_zone} policy {policy_name} then {policy_action}\n\n"
                )
                if not policy_state:
                    output.write(
                        f"deactivate from-zone {source_zone} to-zone {destination_zone} policy {policy_name}\n\n"
                    )
