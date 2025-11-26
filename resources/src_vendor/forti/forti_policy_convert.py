import contextlib
import logging
import os

import yaml

from resources.dst_vendor.dst_asa import AsaDst
from resources.dst_vendor.dst_chpoint import ChPointDst
from resources.dst_vendor.dst_palo import PaloDst
from resources.dst_vendor.dst_srx import SrxDst

palo_translation = {
    "accept": "allow",
    "enable": "no",
    "disable": "yes",
    "HTTP": "service-http",
    "HTTPS": "service-https",
}

srx_translation = {
    "accept": "permit",
    "enable": "enabled",
    "disable": "disabled",
    "HTTP": "junos-http",
    "HTTPS": "junos-https",
}

chpoint_translation = {
    "allow": "accept",
    "deny": "drop",
    "yes": "false",
    "no": "true",
    "service-http": "http",
    "service-https": "https",
}

asa_translation = {
    "yes": "inactive",
    "service-http": ["tcp", "http"],
    "service-https": ["tcp", "https"],
    "accept": "permit",
}

logger = logging.getLogger("fwmig.forti.policy")


def forti_policy(file: str, vendor: str):
    if not os.path.exists(f"exported/{vendor}"):
        os.makedirs(f"exported/{vendor}")
    else:
        with contextlib.suppress(BaseException):
            os.remove(os.path.join(f"exported/{vendor}/", "policies.txt"))

    try:
        with open(f"configs/{file}") as f:
            my_text = yaml.load(f.read(), yaml.SafeLoader)
    except Exception as err:
        logger.error("Check file format. Maybe file is not yaml")
        raise ValueError(err)

    os.remove(f"configs/{file}")

    try:
        dict_formatted: list[dict[str, dict]] = my_text["firewall_policy"]
    except Exception:
        logger.error("firewall_policy are not exists on the config. Conversion failed!")

    position = 1

    try:
        len(dict_formatted)
    except Exception:
        raise ValueError("This tool can't work for one rule!")

    for policy in dict_formatted:
        policy_id = list(policy.keys())[0]
        policy_src_list = []
        policy_dst_list = []
        policy_app_list = []

        policy_name = policy[policy_id].get("name", policy_id)
        source_zone = policy[policy_id]["srcintf"]
        destination_zone = policy[policy_id]["dstintf"]
        source_address_list = policy[policy_id]["srcaddr"]
        destination_address_list = policy[policy_id]["dstaddr"]
        service_address_list = policy[policy_id]["service"]
        # policy_desc = policy[policy_id]['comments']

        policy_state = policy[policy_id].get("status", "enable")
        policy_action = policy[policy_id]["action"]
        policy_log = policy[policy_id]["logtraffic"]
        policy_id = int(policy_id)

        if isinstance(source_address_list, (list)):
            for sub_index in range(len(source_address_list)):
                policy_src_address = source_address_list[sub_index]
                policy_src_list.append(policy_src_address)
        else:
            policy_src_address = source_address_list

        if isinstance(destination_address_list, (list)):
            for sub_index in range(len(destination_address_list)):
                policy_dst_address = destination_address_list[sub_index]
                policy_dst_list.append(policy_dst_address)
        else:
            policy_dst_address = destination_address_list

        if isinstance(service_address_list, (list)):
            for sub_index in range(len(service_address_list)):
                policy_app = service_address_list[sub_index]
                policy_app_list.append(policy_app)
        else:
            policy_app = service_address_list

        policy_log = bool(policy_log)
        if policy_src_list:
            policy_src_address = " ".join(policy_src_list)
        if policy_dst_list:
            policy_dst_address = " ".join(policy_dst_list)
        if policy_app_list:
            try:
                policy_app = " ".join(policy_app_list)
            except Exception:
                policy_app = policy_app_list

        if vendor == "palo":
            policy_state = palo_translation.get(policy_state, policy_state)
            policy_action = palo_translation.get(policy_action, policy_action)
            if "any" in policy_src_address:
                policy_src_address = "all"
            if "any" in policy_dst_address:
                policy_dst_address = "all"
            if policy_app == "any":
                policy_app = "ALL"
            if len(policy_name) > 34:
                policy_name = policy_name[:34]

            palo = PaloDst()
            palo.policy(
                policy_name,
                source_zone,
                destination_zone,
                policy_src_address,
                policy_dst_address,
                policy_app,
                policy_log,
                policy_state,
                policy_action,
                policy_id,
            )

        elif vendor == "asa":
            policy_action = asa_translation.get(policy_action, policy_action)
            asa = AsaDst()
            asa.policy(
                policy_name,
                source_zone,
                destination_zone,
                policy_src_address,
                policy_dst_address,
                policy_app,
                policy_log,
                policy_state,
                policy_action,
                policy_id,
            )
        elif vendor == "srx":
            policy_action = srx_translation.get(policy_action, policy_action)
            policy_log = srx_translation.get(policy_log, policy_log)
            policy_state = policy_state == "enable"
            srx = SrxDst()
            srx.policy(
                policy_name,
                source_zone,
                destination_zone,
                policy_src_address,
                policy_dst_address,
                policy_app,
                policy_log,
                policy_state,
                policy_action,
            )

        elif vendor == "chpoint":
            policy_action = chpoint_translation.get(policy_action, policy_action)
            policy_state = chpoint_translation.get(policy_state, policy_state)

            if policy_dst_list:
                dst_list = []
                for i in range(len(policy_dst_list)):
                    dst_list.append(f'destination.{i + 1} "{policy_dst_list[i]}"')
                policy_dst_address = " ".join(dst_list)
            else:
                policy_dst_address = f'destination "{"Any" if str(policy_dst_address).strip().lower() == "any" else policy_dst_address}"'  # checkpoint need to have "Any" as string not "any" (Case is important)

            if policy_src_list:
                src_list = []
                for i in range(len(policy_src_list)):
                    src_list.append(f'source.{i + 1} "{policy_src_list[i]}"')
                policy_src_address = " ".join(src_list)
            else:
                policy_src_address = f'source "{"Any" if str(policy_src_address).strip().lower() == "any" else policy_src_address}"'  # checkpoint need to have "Any" as string not "any" (Case is important)
            if policy_app_list:
                app_list = []
                for i in range(len(policy_app_list)):
                    if policy_app_list[i][:1].isdigit():
                        policy_app = "custom_" + policy_app_list[i]
                    else:
                        policy_app = policy_app_list[i]
                    app_list.append(f'service.{i + 1} "{policy_app}"')
                policy_app = " ".join(app_list)
            else:
                if policy_app[:1].isdigit():
                    policy_app = "custom_" + policy_app
                elif str(policy_app).strip().lower() == "any":
                    policy_app = "Any"  # checkpoint need to have "Any" as string not "any" (Case is important)
                elif str(policy_app).strip().lower() == "application-default":
                    policy_app = "Any"  # application-default concept does not exist in checkpoint (see https://knowledgebase.paloaltonetworks.com/KCSArticleDetail?id=kA10g000000ClVwCAK)
                policy_app = f"service {policy_app}"

            chpoint = ChPointDst()
            chpoint.policy(
                policy_name,
                source_zone,
                destination_zone,
                policy_src_address,
                policy_dst_address,
                policy_app,
                policy_log,
                policy_state,
                policy_action,
                policy_id,
                position,
            )

        position += 1
