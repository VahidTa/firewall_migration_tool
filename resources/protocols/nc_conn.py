import logging

from ncclient import manager, transport

logger = logging.getLogger("fwmig.nc")


class NcMGR:
    def _conn_mgr(self, host: str, username: str, password: str, port: str, device_params: str):
        return manager.connect(
            host=f"{host}",
            username=f"{username}",
            password=f"{password}",
            port=f"{port}",
            hostkey_verify=False,
            device_params={"name": f"{device_params}"},
        )

    def junos_nc_conn(self, action: str, host: str, username: str, password: str, port: str, device_params: str):
        if action == "policy":
            action = "security policies | display xml"
        elif action == "config":
            action = "configuration | display xml"
        try:
            with self._conn_mgr(host, username, password, port, device_params) as m:
                result = m.command(f"show {action}")
        except transport.AuthenticationError:
            logger.warning(f"Authentication error for {username} on {host}:{port}")
            return False
        except Exception as exc:
            logger.warning(f"Something went wrong with connection or receiving data. {exc}")
            return "other"
        with open("configs/nc_fw_result.log", "w") as f:
            logger.info("Writing result to the file ...")
            f.write(str(result))
        return "nc_fw_result.log"
