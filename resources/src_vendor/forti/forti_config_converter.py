import logging
import os

import yaml

from resources.dst_vendor.dst_asa import AsaDst
from resources.dst_vendor.dst_chpoint import ChPointDst
from resources.dst_vendor.dst_palo import PaloDst
from resources.dst_vendor.dst_srx import SrxDst
from resources.ip_address_converter.netmask_convereter import prefixer
from resources.src_vendor.forti.forti_policy_convert import forti_policy

palo = PaloDst()
srx = SrxDst()
asa = AsaDst()
chpoint = ChPointDst()
logger = logging.getLogger("fwmig.forti.config")


def has_src_port(ports: int | list | str):
    if isinstance(ports, (int, list)):
        return False
    return len(ports.split(":")) > 1


class FortiCfg:
    """Converts SRX -> Fortigate, ASA, Forti, Palo Alto (except zone and interfaces)"""

    def __init__(self, cfg_file: str, vendor: str) -> None:
        self.cfg_file = cfg_file
        self.vendor = vendor

    def _job(self, section):
        with open(f"configs/{self.cfg_file}") as imp_file:
            yaml_dict = yaml.load(imp_file, yaml.SafeLoader)
        return yaml_dict[section]

    @property
    def service(self):
        """Exports custom application created on Fortigate"""

        dict_formatted: list[dict[str, dict]] = self._job("firewall_service_custom")
        for c_service in dict_formatted:
            application_name = list(c_service.keys())[0]
            application_protocol = c_service[application_name].get("protocol")
            application_desc = c_service[application_name].get("comment")
            source_port = None
            destination_port = None
            protocol_number = None
            icmp_code = None
            icmp_type = None
            if application_protocol == "IP":
                protocol_number = c_service[application_name].get("protocol-number", 0)
            elif application_protocol == "ICMP":
                icmp_code = c_service[application_name].get("icmpcode")
                icmp_type = c_service[application_name].get("icmptype")
            else:
                if c_service[application_name].get("tcp-portrange") is not None:
                    application_protocol = "tcp"
                    destination_port = c_service[application_name]["tcp-portrange"]
                    if has_src_port(destination_port):
                        destination_port, source_port = destination_port.split(":")
                if c_service[application_name].get("udp-portrange") is not None:
                    application_protocol = "udp"
                    destination_port = c_service[application_name].get("udp-portrange")
                    if has_src_port(destination_port):
                        destination_port, source_port = destination_port.split(":")
            session_ttl = None

            if self.vendor == "srx":
                srx.service(
                    application_name,
                    destination_port,
                    source_port,
                    application_protocol,
                    application_desc,
                    protocol_number,
                    icmp_code,
                    icmp_type,
                )
            elif self.vendor == "asa":
                asa.service(
                    application_name,
                    destination_port,
                    source_port,
                    application_protocol,
                    application_desc,
                    protocol_number,
                    icmp_code,
                    icmp_type,
                )

            elif self.vendor == "palo":
                if session_ttl == "never":
                    session_ttl = False
                palo.service(
                    application_name, destination_port, source_port, application_protocol, application_desc, session_ttl
                )
            elif self.vendor == "chpoint":
                if not source_port:
                    source_port = ""
                if (not session_ttl) or (session_ttl == "never"):
                    session_ttl = ""
                # Because the platform does not support name start with Digits!
                if application_name[:1].isdigit():
                    application_name = "custom_" + application_name

                chpoint.service(
                    application_name, destination_port, source_port, application_protocol, application_desc, session_ttl
                )

    @property
    def service_set(self):
        """Exports custome application-set created on Fortigate"""

        dict_formatted: list[dict[str, dict]] = self._job("firewall_service_group")

        for cg_service in dict_formatted:
            app_set_name = list(cg_service.keys())[0]
            app_list = cg_service[app_set_name].get("member", [])
            app_set_desc = cg_service[app_set_name].get("comment")
            if self.vendor != "asa":
                app_name = " ".join(app_list)

            if self.vendor == "srx":
                srx.service_set(app_set_name, app_list, app_set_desc)
            elif self.vendor == "asa":
                asa.service_set(app_set_name, app_list, app_set_desc)
            elif self.vendor == "palo":
                palo.service_set(app_set_name, app_name)
            elif self.vendor == "chpoint":
                chpoint.address_set(app_set_name, app_list, app_set_desc)

    @property
    def address(self):
        """Converts address books"""

        address_books: list[dict[str, dict]] = self._job("firewall_address")
        address_set_books: list[dict[str, dict]] = self._job("firewall_addrgrp")

        for address in address_books:
            address_name = list(address.keys())[0]
            address_description = address[address_name].get("comment")
            address_type = None

            if subnet := address[address_name].get("subnet", []):
                address_ip = "/".join(subnet)
                address_ip = prefixer(address_ip)
                address_type = "subnet"
            elif address[address_name].get("type", "") == "iprange":
                address_ip = f"{address[address_name]['start-ip']}-{address[address_name]['end-ip']}"
                address_type = "range"
            elif address[address_name].get("type", "") == "fqdn":
                address_ip = address[address_name]["fqdn"]
                address_type = "fqdn"
            else:
                logger.warning(f"skipping dynamic address ... {address_name}")
                continue
            if self.vendor == "srx":
                srx.address(address_name, address_ip, address_description, address_type)

            elif self.vendor == "asa":
                asa.address(address_name, address_ip, address_description, address_type)

            elif self.vendor == "palo":
                palo.address(address_name, address_ip, address_description, address_type)

            elif self.vendor == "chpoint":
                chpoint.address(address_name, address_ip, address_description, address_type)

        if address_set_books:
            for address in address_set_books:
                address_set_name = list(address.keys())[0]
                address_set_desc = address[address_set_name].get("comment")
                address_name_list = address[address_set_name].get("member", [])

                if self.vendor == "srx":
                    srx.address_set(address_set_name, address_name_list, address_set_desc)
                elif self.vendor == "asa":
                    asa.address_set(address_set_name, address_name_list, address_set_desc)
                elif self.vendor == "palo":
                    palo.address_set(address_set_name, address_name, address_set_desc)
                elif self.vendor == "chpoint":
                    chpoint.address_set(address_set_name, address_name_list, address_set_desc)

    @property
    def policy(self):
        forti_policy(self.cfg_file, self.vendor)

    @property
    def delete(self):
        os.remove(f"configs/{self.cfg_file}")

    @property
    def cleaner(self):
        if not os.path.exists(f"exported/{self.vendor}"):
            os.makedirs(f"exported/{self.vendor}")
        else:
            for f in os.listdir(f"exported/{self.vendor}/"):
                if f != "policies.txt":
                    os.remove(os.path.join(f"exported/{self.vendor}/", f))
