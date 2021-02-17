from ncclient import manager
from ncclient import transport

class NcMGR:

    def _conn_mgr(self, host: str, username: str, password: str, port: str, device_params: str):
        return manager.connect(
            host=f'{host}',
            username = f'{username}',
            password = f'{password}',
            port = f'{port}',
            hostkey_verify = False,
            device_params = {'name': f'{device_params}'}
        )
    

    # def junos_nc_conn(self, host: str, port: str, device_params: str, ):
    def junos_nc_conn(self, action: str, host: str, username: str, password: str, port: str, device_params: str):
        if action == 'policy':
            action = 'security policies | display xml'
        elif action == 'config':
            action = 'configuration | display xml'
        try:
            with self._conn_mgr(host, username, password, port, device_params) as m:
                result = m.command(f'show {action}')
        except transport.AuthenticationError:
            return False
        except:
            return 'other'
        with open('configs/nc_fw_result.log', 'w') as f:
            f.write(str(result))
        return 'nc_fw_result.log'