import os
import logging

from typing import List

from resources.src_vendor.chpoint.chpoint_config_parser import CHP_CFG
from resources.src_vendor.srx.srx_config_converter import SRX_Cfg

logger = logging.getLogger('fwmig.parser')

def main_parser(action: str, cfg: str, src_vendor: str, dst_vendor: str, acts: List[str]) -> bool:
    if src_vendor == 'srx':
        output = SRX_Cfg(cfg, dst_vendor)
    elif src_vendor == 'chpoint':
        output = CHP_CFG(cfg, dst_vendor)
    
    try:
        if action == 'policy':
            logger.info('Policy conversion started ...')
            output.policy

        elif action == 'config':
            output.cleaner
            if 'address' in acts:
                logger.info('Address and Address_set conversion started ...')
                output.address

            if 'service' in acts:
                if src_vendor == 'chpoint':
                    return 'no'
                logger.info('Service conversion started ...')
                output.service

            if 'service_set' in acts:
                if src_vendor == 'chpoint':
                    return 'no'
                logger.info('Service_set conversion started ...')
                output.service_set
            
            # if 'zone' in acts:
            #     output.zone

            output.delete
        logger.info('Conversion finished successfully!')
        return True
    except:
        logger.warning('Conversion Failed! Please re-check file content or Source vendor.')
        logger.info(50*'=')
        os.remove(f'configs/{cfg}')
        return False