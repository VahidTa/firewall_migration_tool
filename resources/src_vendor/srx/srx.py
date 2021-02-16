import os
from typing import List
from resources.src_vendor.srx.srx_config_converter import SRX_Cfg
from resources.src_vendor.srx.srx_policy_convert import srx_policy


def srx_main(action: str, cfg: str, vendor: str, acts: List[str]) -> bool:
    try:
        if action == 'policy':
            srx_policy(cfg, vendor)
        
        elif action == 'config':
            output = SRX_Cfg(cfg, vendor)
            output.cleaner
            if 'address' in acts:
                output.address

            if 'service' in acts:
                output.service

            if 'service_set' in acts:
                output.service_set
            
            # if 'zone' in acts:
            #     output.zone

            output.delete
        return True
    except:
        os.remove(f'configs/{cfg}')
        return False
