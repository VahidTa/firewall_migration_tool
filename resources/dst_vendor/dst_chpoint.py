import os

from resources.dst_vendor.data_objects import AddressData, AddressSetData, PolicyData, ServiceData, ServiceSetData
from resources.dst_vendor.vendor_abc import VendorAbc
from resources.ip_address_converter.netmask_convereter import nethost, sub_mask


class ChPointDst(VendorAbc):
    def service(self, data: ServiceData):
        application_name = data.application_name
        destination_port = data.destination_port
        source_port = data.source_port
        application_protocol = data.application_protocol
        application_desc = data.application_desc
        app_session_ttl = data.app_session_ttl

        the_path = f"exported/chpoint/service-{application_protocol}.csv"
        with open(the_path, "a") as f:
            if os.path.getsize(the_path) == 0:
                f.write("name,port,source-port,session-timeout,set-if-exists,ignore-warnings,ignore-errors,comments\n")
            if application_desc and destination_port:
                f.write(
                    f'{application_name},{destination_port},{source_port},{app_session_ttl},true,true,true,"{application_desc}"\n'
                )
            elif destination_port:
                f.write(f"{application_name},{destination_port},{source_port},{app_session_ttl},true,true,true,\n")

    def service_set(self, data: ServiceSetData):
        app_set_name = data.app_set_name
        app_list = data.app_list or []
        app_set_desc = data.app_set_desc

        the_path = "exported/chpoint/service_groups.csv"
        with open(the_path, "a") as f:
            if os.path.getsize(the_path) == 0:
                f.write("name,ignore-warnings,ignore-errors,comments\n")
            if app_set_desc:
                f.write(f'{app_set_name},true,true,"{app_set_desc}"\n')
            else:
                f.write(f"{app_set_name},true,true,\n")
        the_path = "exported/chpoint/service_groups_members.csv"
        with open(the_path, "a") as f:
            if os.path.getsize(the_path) == 0:
                f.write("name,members.add,ignore-warnings,ignore-errors\n")
            for object in app_list:
                if object[:1].isdigit():
                    object = "custom_" + object
                f.write(f"{app_set_name},{object},true,true\n")

    def address(self, data: AddressData):
        address_name = data.address_name
        address_ip = data.address_ip
        address_desc = data.address_desc
        address_type = data.address_type or ""

        if address_type in ("fqdn", "range"):
            return

        if "/32" in address_ip:
            address_netmask = nethost(address_ip)
            the_path = "exported/chpoint/network_objects_host.csv"
            with open(the_path, "a") as f:
                if os.path.getsize(the_path) == 0:
                    f.write("name,ip-address,set-if-exists,ignore-warnings,ignore-errors,comments\n")
                if address_desc:
                    f.write(f'{address_name},{address_netmask},true,true,true,"{address_desc}"\n')
                else:
                    f.write(f"{address_name},{address_netmask},true,true,true,\n")
        else:
            add_subnet = nethost(address_ip)
            add_mask = sub_mask(address_ip)
            the_path = "exported/chpoint/network_objects_network.csv"
            with open(the_path, "a") as f:
                if os.path.getsize(the_path) == 0:
                    f.write("name,subnet,subnet-mask,set-if-exists,ignore-warnings,ignore-errors,comments\n")
                if address_desc:
                    f.write(f'{address_name},{add_subnet},{add_mask},true,true,true,"{address_desc}"\n')
                else:
                    f.write(f"{address_name},{add_subnet},{add_mask},true,true,true,\n")

    def address_set(self, data: AddressSetData):
        address_set_name = data.address_set_name
        address_name_list = data.address_name_list
        address_set_desc = data.address_set_desc

        the_path = "exported/chpoint/network_groups.csv"
        with open(the_path, "a") as f:
            if os.path.getsize(the_path) == 0:
                f.write("name,ignore-warnings,ignore-errors,comments\n")
            if address_set_desc:
                f.write(f'{address_set_name},true,true,"{address_set_desc}"\n')
            else:
                f.write(f"{address_set_name},true,true,\n")

        the_path = "exported/chpoint/network_group_members.csv"
        with open(the_path, "a") as f:
            if os.path.getsize(the_path) == 0:
                f.write("name,members.add,ignore-warnings,ignore-errors\n")
            for address_name in address_name_list:
                f.write(f"{address_set_name},{address_name},true,true\n")

    def policy(self, data: PolicyData):
        policy_name = data.policy_name
        policy_src_address = data.policy_src_address
        policy_dst_address = data.policy_dst_address
        policy_app = data.policy_app
        policy_log = data.policy_log
        policy_state = data.policy_state
        policy_action = data.policy_action
        policy_id = data.policy_id
        position = data.position

        the_path = "exported/chpoint/policies.txt"
        with open(the_path, "a") as output:
            if os.path.getsize(the_path) == 0:
                output.write('mgmt_cli login -u "your username" -p "your password" > "sid.txt"\n\n')

            if policy_log:
                output.write(
                    f'mgmt_cli add access-rule layer "Network" position "{position}" name "{policy_name}" action "{policy_action}" {policy_src_address} {policy_dst_address} {policy_app} enabled {policy_state} comments "original rule order {policy_id}" track Log -s "sid.txt"\n\n'
                )

            else:
                output.write(
                    f'mgmt_cli add access-rule layer "Network" position "{position}" name "{policy_name}" action "{policy_action}" {policy_src_address} {policy_dst_address} {policy_app} enabled {policy_state} comments "original rule order{policy_id}" -s "sid.txt"\n\n'
                )

            if position != 0 and position % 53 == 0:
                output.write('mgmt_cli publish -s "sid.txt"\n\n')
