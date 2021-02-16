import os
from typing import List
from resources.src_vendor.chpoint.chpoint_config_parser import CHP_CFG
from resources.src_vendor.chpoint.chpoint_policy_parser import chpoint_policy


def chpoint_main(action: str, cfg: str, vendor: str, acts: List[str]) -> bool:
    try:
        if action == 'policy':
            chpoint_policy(cfg, vendor)
        
        elif action == 'config':
            output = CHP_CFG(cfg, vendor)
            output.cleaner
            if 'address' in acts:
                output.address

            if 'service' in acts:
                return 'no'
                # output.service

            if 'service_set' in acts:
                return 'no'
                # output.service_set
            
            # if 'zone' in acts:
            #     output.zone

            output.delete
        return True
    except:
        os.remove(f'configs/{cfg}')
        return False
