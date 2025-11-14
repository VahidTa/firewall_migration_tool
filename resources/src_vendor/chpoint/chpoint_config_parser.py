import os

import pandas as pd

from resources.dst_vendor.dst_asa import AsaDst
from resources.dst_vendor.dst_forti import FortiDst
from resources.dst_vendor.dst_palo import PaloDst
from resources.dst_vendor.dst_srx import SrxDst
from resources.ip_address_converter.netmask_convereter import prefixer
from resources.src_vendor.chpoint.chpoint_policy_parser import chpoint_policy

forti = FortiDst()
asa = AsaDst()
palo = PaloDst()
srx = SrxDst()


class ChPointCfg:
    def __init__(self, cfg_file: str, vendor: str) -> None:
        self.cfg_file = cfg_file
        self.vendor = vendor

    @property
    def _job(self):
        names = ["Name", "IPv4 address", "Mask", "IPv6 address", "Mask 6", "Port", "Comments"]
        with open(f"configs/{self.cfg_file}") as imp_file:
            imported = pd.read_csv(
                imp_file, usecols=names, skiprows=1, names=names, keep_default_na=False, skipinitialspace=True
            )
        parsed = imported[names]
        return parsed

    @property
    def address(self):
        raw_objects = self._job
        for _, row in raw_objects.iterrows():
            address_name = row["Name"]
            address_description = row["Comments"] if row["Comments"] else ""

            if row["IPv4 address"] and "-" not in row["IPv4 address"]:
                ip_address = row["IPv4 address"]

                mask = row["Mask"]
                address_ip = prefixer(f"{ip_address}/{mask}") if mask else prefixer(f"{ip_address}")
            # elif row["IPv6 address"]:
            #     ip_address = row["IPv6 address"]
            #     mask = row["Mask 6"]
            elif "-" in row["IPv4 address"]:
                address_ip = row["IPv4 address"]
            else:
                continue

            if self.vendor == "forti":
                forti.address(address_name, address_ip, address_description)
            elif self.vendor == "asa":
                asa.address(address_name, address_ip, address_description)
            elif self.vendor == "palo":
                palo.address(address_name, address_ip, address_description)
            elif self.vendor == "srx":
                srx.address(address_name, address_ip, address_description)

    @property
    def policy(self):
        chpoint_policy(self.cfg_file, self.vendor)

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
