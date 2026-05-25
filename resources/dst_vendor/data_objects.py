from dataclasses import dataclass

__all__ = (
    "ServiceData",
    "ServiceSetData",
    "AddressData",
    "AddressSetData",
    "PolicyData",
)


@dataclass
class ServiceData:
    application_name: str
    destination_port: str | int | None
    source_port: str | int | None
    application_protocol: str
    application_desc: str
    app_session_ttl: str | None = None
    icmp_code: str | None = None
    icmp_type: str | None = None
    protocol_number: str | None = None


@dataclass
class ServiceSetData:
    app_set_name: str
    app_set_desc: str
    app_list: list[str] | None = None
    app_name: str | None = None


@dataclass
class AddressData:
    address_name: str
    address_ip: str
    address_desc: str
    address_type: str | None = None


@dataclass
class AddressSetData:
    address_set_name: str
    address_name_list: list
    address_set_desc: str
    address_name: str | None = None


@dataclass
class PolicyData:
    policy_name: str
    source_zone: str
    destination_zone: str
    policy_src_address: str
    policy_dst_address: str
    policy_app: str
    policy_log: str
    policy_state: str
    policy_action: str
    policy_id: str | None = None
    position: str | None = None
