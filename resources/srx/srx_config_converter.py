import json
import xmltodict


class SRXConfig:
    """Converts SRX -> Fortigate (except zone and interfaces) """
    def __init__(self, cfg_file: str) -> None:
        self.cfg_file = cfg_file
    

    def _job(self):
        with open(f'configs/{self.cfg_file}', 'r') as imp_file:
            xml_dict = xmltodict.parse(imp_file.read())

        json_formatted = json.dumps(xml_dict)
        dict_formatted = json.loads(json_formatted)
        return dict_formatted['rpc-reply']['configuration']
    
    @property
    def custom_service(self):
        """Exports custom application created on SRX"""
        dict_formatted = self._job()

        applications_list = dict_formatted['applications']
        apps= applications_list['application']

        for index in range(len(apps)):
            application_name = apps[index].get('name', 'None')
            application_protocol = apps[index].get('protocol', 'None')
            application_port = apps[index].get('destination-port', 'None')
            with open('exported/custom_services.txt', 'a') as f:
                f.write(f'edit {application_name}\n')
                f.write('set category General\n')
                f.write(f'set {application_protocol}-portrange {application_port}\n')
                f.write('next\n\n')
    
    @property
    def custom_service_set(self):
        """Exports custome application-set created on SRX"""
        dict_formatted = self._job()

        applications_list = dict_formatted['applications']
        apps_set = applications_list['application-set']

        for index in range(len(apps_set)):
            app_list = []
            app_set_name = apps_set[index].get('name', 'None')
            app_set_main = apps_set[index]['application']
            for sub_index in range(len(app_set_main)):
                app_name = app_set_main[sub_index].get('name', 'None')
                app_list.append(app_name)

            app_name = ' '.join(app_list)

            with open('exported/custom_service_group.txt', 'a') as f:
                f.write(f'edit {app_set_name}\n')
                f.write(f'set member {app_name}')
                f.write('next\n\n')
    
    @property
    def address_book(self):
        """Converts address books"""
        security_cfg = self._job()
        address_books = security_cfg['security']['address-book']['address']

        for index in range(len(address_books)):
            address_name = address_books[index].get('name', 'None')
            address_ip = address_books[index].get('ip-prefix', 'None')
            with open('exported/address_objects.txt', 'a') as f:
                f.write(f'edit {address_name}\n')
                f.write(f'set subnet {address_ip}\n')
                f.write('next\n\n')
    
    @property
    def intf(self):
        """Not Implemented"""
        return None
        
    
    @property
    def zone(self):
        """Not Implemented"""
        return None
        security_cfg = self._job()
        zones = security_cfg['security']['zones']['security-zone']

        for main_index in range(len(zones)):
            service_list = []
            zone_name = zones[main_index].get('name', 'None')
            zone_service = zones[main_index]['host-inbound-traffic']['system-services']
            if isinstance(zone_service, (list)):
                for sub_index in range(len(zone_service)):
                    service = zone_service[sub_index].get('name', 'None')
                    service_list.append(service)
            else:
                service = zone_service.get('name', 'None')
                service_list.append(service)
            service = ' '.join(service_list)
            
            with open('exported/zones.txt', 'a') as f:
                f.write(f'edit {zone_name}\n')
                # f.write(f'set interface {interface_name}\n')
                f.write('next\n\n')
