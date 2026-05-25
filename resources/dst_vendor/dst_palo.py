import os

from resources.dst_vendor.data_objects import AddressData, AddressSetData, PolicyData, ServiceData, ServiceSetData
from resources.dst_vendor.vendor_abc import VendorAbc


class PaloDst(VendorAbc):
    def service(self, data: ServiceData):
        application_name = data.application_name
        destination_port = data.destination_port
        source_port = data.source_port
        application_protocol = data.application_protocol
        application_desc = data.application_desc
        app_session_ttl = data.app_session_ttl

        with open("exported/palo/services.txt", "a") as f:
            if destination_port:
                f.write(f"set service {application_name} protocol {application_protocol} port {destination_port}\n\n")
            elif source_port:
                f.write(f"set service {application_name} protocol {application_protocol} source-port {source_port}\n\n")
            if application_desc:
                f.write(f'set service {application_name} description "{application_desc}"\n\n')
            if app_session_ttl:
                f.write(
                    f"set service {application_name} protocol {application_protocol} override yes timeout {app_session_ttl}\n\n"
                )

    def service_set(self, data: ServiceSetData):
        app_set_name = data.app_set_name
        app_name = data.app_name or ""

        with open("exported/palo/service_group.txt", "a") as f:
            f.write(f"set service-group {app_set_name} members [ {app_name} ]\n\n")

    def address(self, data: AddressData):
        address_name = data.address_name
        address_ip = data.address_ip
        address_desc = data.address_desc
        address_type = data.address_type or "subnet"

        with open("exported/palo/addresses.txt", "a") as f:
            if address_type == "range":
                address_ip = address_ip.replace(" ", "")
                f.write(f"set address {address_name} ip-range {address_ip}\n\n")
            elif address_type == "subnet":
                f.write(f"set address {address_name} ip-netmask {address_ip}\n\n")
            elif address_type == "fqdn":
                f.write(f"set address {address_name} fqdn {address_ip}\n\n")
            if address_desc:
                f.write(f'set address {address_name} description "{address_desc}"\n\n')

    def address_set(self, data: AddressSetData):
        address_set_name = data.address_set_name
        address_name = data.address_name
        address_set_desc = data.address_set_desc

        if " " in address_set_name:
            address_set_name = f'"{address_set_name}"'

        with open("exported/palo/address_group.txt", "a") as f:
            f.write(f"set address-group {address_set_name} static [ {address_name} ]\n\n")
            if address_set_desc:
                f.write(f'set address-group {address_set_name} description "{address_set_desc}"\n\n')

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

        the_path = "exported/palo/policies.txt"
        with open(the_path, "a") as output:
            if os.path.getsize(the_path) == 0:
                output.write("edit rulebase security\n\n")
            output.write(f"set rules {policy_name} from {source_zone}\n")
            output.write(f"set rules {policy_name} to {destination_zone}\n")
            output.write(f"set rules {policy_name} source [ {policy_src_address} ]\n")
            output.write(f"set rules {policy_name} destination [ {policy_dst_address} ]\n")
            output.write(f"set rules {policy_name} service [ {policy_app} ]\n")
            output.write(f"set rules {policy_name} application any\n")
            if source_zone == destination_zone:
                output.write(f"set rules {policy_name} rule-type intrazone\n")
            else:
                output.write(f"set rules {policy_name} rule-type interzone\n")
            if policy_log:
                output.write(f"set rules {policy_name} log-start yes\n")
            if policy_state == "disabled":
                output.write(f"set rules {policy_name} disabled yes\n")
            output.write(f"set rules {policy_name} action {policy_action}\n\n")
