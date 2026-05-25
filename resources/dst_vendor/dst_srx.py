import os

from resources.dst_vendor.data_objects import AddressData, AddressSetData, PolicyData, ServiceData, ServiceSetData
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
    def service(self, data: ServiceData):
        application_name = data.application_name
        destination_port: list | int | str = data.destination_port
        source_port = data.source_port
        application_protocol = data.application_protocol
        application_desc = data.application_desc
        protocol_number = data.protocol_number
        icmp_code = data.icmp_code
        icmp_type = data.icmp_type

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

    def service_set(self, data: ServiceSetData):
        app_set_name: str = data.app_set_name
        app_list = data.app_list or []
        app_set_desc = data.app_set_desc

        if " " in app_set_name:
            app_set_name = f'"{app_set_name}"'

        with open("exported/srx/service_group.txt", "a") as f:
            for app in app_list:
                if "_FWMIG" in app:
                    f.write(f"set applications application-set {app_set_name} application-set {app}\n\n")
                else:
                    if " " in app:
                        app = f'"{app}"'
                    f.write(f"set applications application-set {app_set_name} application {app}\n\n")
            if app_set_desc:
                f.write(f'set applications application-set {app_set_name} description "{app_set_desc}"\n\n')

    def address(self, data: AddressData):
        address_name = data.address_name
        address_ip = data.address_ip
        address_desc = data.address_desc
        address_type = data.address_type or "subnet"

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

    def address_set(self, data: AddressSetData):
        address_set_name = data.address_set_name
        address_name_list = data.address_name_list
        address_set_desc = data.address_set_desc

        if " " in address_set_name:
            address_set_name = f'"{address_set_name}"'

        with open("exported/srx/address_group.txt", "a") as f:
            for name in address_name_list:
                f.write(f"set address-set {address_set_name} address {name}\n\n")
            if address_set_desc:
                f.write(f'set address-set {address_set_name} description "{address_set_desc}"\n\n')

    def policy(self, data: PolicyData):
        policy_name = data.policy_name
        source_zone = data.source_zone
        destination_zone = data.destination_zone
        policy_src_address = data.policy_src_address
        policy_dst_address = data.policy_dst_address
        policy_app = data.policy_app
        policy_log = data.policy_log
        policy_state = data.policy_state
        policy_action = data.policy_action

        the_path = "exported/srx/policies.txt"
        with open(the_path, "a") as output:
            if os.path.getsize(the_path) == 0:
                output.write("edit security policies\n\n")
            if source_zone == "global" and destination_zone == "global":
                output.write(f"set global policy {policy_name} match source-address [ {policy_src_address} ]\n")
                output.write(f"set global policy {policy_name} match destination-address [ {policy_dst_address} ]\n")
                output.write(f"set global policy {policy_name} match application [ {policy_app} ]\n")
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
