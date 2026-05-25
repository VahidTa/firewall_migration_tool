from resources.dst_vendor.data_objects import AddressData, AddressSetData, PolicyData, ServiceData, ServiceSetData
from resources.dst_vendor.vendor_abc import VendorAbc
from resources.ip_address_converter.netmask_convereter import nethost, netmasker

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


class AsaDst(VendorAbc):
    def service(self, data: ServiceData):
        application_name = data.application_name
        destination_port = data.destination_port
        source_port = data.source_port
        application_protocol = data.application_protocol
        application_desc = data.application_desc
        protocol_number = data.protocol_number
        icmp_code = data.icmp_code
        icmp_type = data.icmp_type

        if " " in application_name:
            application_name = f'"{application_name}"'

        with open("exported/asa/service_objects.txt", "a") as f:
            f.write(f"object service {application_name}\n")
            if destination_port:
                destination_port = str(destination_port)
                if "-" in destination_port:
                    destination_port = destination_port.replace("-", " ")
                    f.write(f"service {application_protocol} destination range {destination_port}\n")
                else:
                    f.write(f"service {application_protocol} destination eq {destination_port}\n")
            elif source_port:
                source_port = str(source_port)
                if "-" in source_port:
                    source_port = source_port.replace("-", " ")
                    f.write(f"service {application_protocol} source range {source_port}\n")
                else:
                    f.write(f"service {application_protocol} source eq {source_port}\n")
            if application_protocol == "IP" and protocol_number == 0:
                f.write("service IP\n")
            elif protocol_number:
                f.write(f"service {protocol_mapper.get(protocol_number, protocol_number)}\n")
            elif application_protocol == "ICMP":
                cmd = "service icmp"
                if icmp_type:
                    cmd += f" {icmp_type}"
                if icmp_code:
                    cmd += f" {icmp_code}"
                cmd += "\n"
                f.write(cmd)
            if application_desc:
                f.write(f"description {application_desc} \n")
            f.write("exit\n\n")

    def service_set(self, data: ServiceSetData):
        app_set_name = data.app_set_name
        app_list = data.app_list or []
        app_set_desc = data.app_set_desc

        if " " in app_set_name:
            app_set_name = f'"{app_set_name}"'

        with open("exported/asa/service_object_group.txt", "a") as f:
            f.write(f"object-group service {app_set_name}\n")
            for object in app_list:
                if isinstance(object, (list)):
                    if object[0] == "icmp":
                        f.write(f"service-object {object[0]} {object[1]}\n")
                    else:
                        f.write(f"service-object {object[0]} destination eq {object[1]}\n")
                else:
                    f.write(f"service-object object {object} \n")
            if app_set_desc:
                f.write(f"description {app_set_desc} \n")
            f.write("exit\n\n")

    def address(self, data: AddressData):
        address_name = data.address_name
        address_ip = data.address_ip
        address_desc = data.address_desc
        address_type = data.address_type or ""

        with open("exported/asa/object_network.txt", "a") as f:
            if address_type == "fqdn":
                address_netmask = f"fqdn {address_ip}"
            elif "-" in address_ip:
                start_ip = address_ip.split("-")[0].replace(" ", "")
                end_ip = address_ip.split("-")[1].replace(" ", "")
                address_netmask = f"range {start_ip} {end_ip}"
            elif "/32" in address_ip:
                address_netmask = "host " + nethost(address_ip)
            else:
                address_netmask = "subnet " + netmasker(address_ip)
            if "/" in address_name:
                address_name = address_name.replace("/", "-")
            f.write(f"object network {address_name}\n")
            if address_desc:
                f.write(f"description {address_desc}\n")
            f.write(f"{address_netmask}\n")
            f.write("exit\n\n")

    def address_set(self, data: AddressSetData):
        address_set_name = data.address_set_name
        address_name_list = data.address_name_list
        address_set_desc = data.address_set_desc

        with open("exported/asa/object_group_network.txt", "a") as f:
            f.write(f"object-group network {address_set_name}\n")
            if address_set_desc:
                f.write(f"description {address_set_desc}\n")
            for address_name in address_name_list:
                f.write(f"network-object object {address_name}\n")
            f.write("exit\n\n")

    def policy(self, data: PolicyData):
        policy_src_address = data.policy_src_address
        policy_dst_address = data.policy_dst_address
        policy_app = data.policy_app
        policy_log = data.policy_log
        policy_state = data.policy_state
        policy_action = data.policy_action
        policy_id = data.policy_id

        the_path = "exported/asa/policies.txt"
        if policy_state != "inactive":
            policy_state = ""
        policy_log = "log" if policy_log else ""
        if " " in policy_src_address:
            src_group_name = f"DM_INLINE_NETWORK_111{policy_id}"
            with open(the_path, "a") as output:
                output.write(f"object-group network {src_group_name}\n")
                for src in policy_src_address.split(" "):
                    output.write(f" network-object object {src}\n")
                output.write(" exit\n\n")
            policy_src_address = f"object-group {src_group_name}"
        else:
            policy_src_address = f"object {policy_src_address}"
        if " " in policy_dst_address:
            dst_group_name = f"DM_INLINE_NETWORK_222{policy_id}"
            with open(the_path, "a") as output:
                output.write(f"object-group network {dst_group_name}\n")
                for dst in policy_dst_address.split(" "):
                    output.write(f" network-object object {dst}\n")
                output.write(" exit\n\n")
            policy_dst_address = f"object-group {dst_group_name}"
        else:
            policy_dst_address = f"object {policy_dst_address}"

        if " " in policy_app:
            app_group_name = f"DM_INLINE_SERVICE_333{policy_id}"
            with open(the_path, "a") as output:
                output.write(f"object-group service {app_group_name}\n")
                for dst in policy_app.split(" "):
                    if isinstance(dst, (list)):
                        if dst[1] == "na":
                            output.write(f" service-object {dst[0]}\n")
                        else:
                            dst = f"{dst[0]} destination eq {dst[1]}"
                            output.write(f" service-object {dst}\n")
                    else:
                        output.write(f" service-object object {dst}\n")
            policy_app = f"object-group {app_group_name}"
        elif isinstance(policy_app, (list)):
            app_group_name = f"DM_INLINE_SERVICE_333{policy_id}"
            with open(the_path, "a") as output:
                output.write(f"object-group service {app_group_name}\n")
                for dst in policy_app:
                    if isinstance(dst, (list)):
                        if dst[1] == "na":
                            output.write(f" service-object {dst[0]}\n")
                        else:
                            dst = f"{dst[0]} destination eq {dst[1]}"
                            output.write(f" service-object {dst}\n")
                    else:
                        output.write(f" service-object object {dst}\n")
            policy_app = f"object-group {app_group_name}"

        if not isinstance(policy_app, list) and "DM_INLINE_SERVICE_" not in policy_app:
            policy_app = f"object {policy_app}"
        # if ('DM_INLINE_SERVICE_' in policy_app) == False:
        #     policy_app = f'object {policy_app}'

        if isinstance(policy_app, (list)):
            with open("exported/asa/policies.txt", "a") as output:
                output.write(
                    f"access-list global_access line {policy_id} extended {policy_action} {policy_app[0]} {policy_src_address} {policy_dst_address} eq {policy_app[1]} {policy_log} {policy_state}\n\n"
                )
        else:
            with open("exported/asa/policies.txt", "a") as output:
                output.write(
                    f"access-list global_access line {policy_id} extended {policy_action} {policy_app} {policy_src_address} {policy_dst_address} {policy_log} {policy_state}\n\n"
                )
