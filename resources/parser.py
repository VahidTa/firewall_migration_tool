import contextlib
import logging
import os

logger = logging.getLogger("fwmig.parser")


def main_parser(action: str, cfg: str, src_vendor: str, dst_vendor: str, acts: list[str]) -> bool:
    if src_vendor == "srx":
        from resources.src_vendor.srx.srx_config_converter import SRX_Cfg

        output = SRX_Cfg(cfg, dst_vendor)
    elif src_vendor == "chpoint":
        from resources.src_vendor.chpoint.chpoint_config_parser import CHP_CFG

        output = CHP_CFG(cfg, dst_vendor)
    elif src_vendor == "palo":
        from resources.src_vendor.palo.palo_config_coverter import PALO_Cfg

        output = PALO_Cfg(cfg, dst_vendor)
    # elif src_vendor == 'asa':
    #     from resources.src_vendor.asa.asa_config_converter import ASA_CFG
    #     output = ASA_CFG(cfg, dst_vendor)

    try:
        if action == "policy":
            logger.info("Policy conversion started ...")
            output.policy

        elif action == "config":
            output.cleaner
            if "address" in acts:
                logger.info("Address and Address_set conversion started ...")
                output.address

            if "service" in acts:
                if src_vendor == "chpoint":
                    return "no"
                logger.info("Service conversion started ...")
                output.service

            if "service_set" in acts:
                if src_vendor == "chpoint":
                    return "no"
                logger.info("Service_set conversion started ...")
                output.service_set

            # if 'zone' in acts:
            #     output.zone

            output.delete
        logger.info("Conversion finished successfully!")
        return True
    except Exception as err:
        logger.warning(f"Conversion Failed! Please re-check file content or Source vendor. {err}")
        logger.info(50 * "=")
        with contextlib.suppress(BaseException):
            os.remove(f"configs/{cfg}")
        return False
