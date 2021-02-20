import json
import xmltodict
import os

from resources.src_vendor.srx.srx_policy_convert import forti_translation,\
                                            palo_translation,\
                                            chpoint_translation,\
                                            asa_translation

from resources.dst_vendor.dst_palo import Palo_DST
from resources.dst_vendor.dst_forti import Forti_DST
from resources.dst_vendor.dst_asa import ASA_DST
from resources.dst_vendor.dst_chpoint import CHPoint_DST
from resources.src_vendor.srx.srx_policy_convert import srx_policy

palo = Palo_DST()
forti = Forti_DST()
asa = ASA_DST()
chpoint = CHPoint_DST()

class SRX_Cfg:
    """Converts SRX -> Fortigate, ASA, Forti, Palo Alto (except zone and interfaces) """
    def __init__(self, cfg_file: str, vendor: str) -> None:
        self.cfg_file = cfg_file
        self.vendor = vendor
    
    @property
    def _job(self):
        with open(f'configs/{self.cfg_file}', 'r') as imp_file:
            xml_dict = xmltodict.parse(imp_file.read())
        json_formatted = json.dumps(xml_dict)
        dict_formatted = json.loads(json_formatted)
        return dict_formatted['rpc-reply']['configuration']
    
    @property
    def service(self):
        """Exports custom application created on SRX"""

        dict_formatted = self._job

        applications_list = dict_formatted['applications']
        apps= applications_list['application']

        for index in range(len(apps)):
            application_name = apps[index].get('name', 'None')
            application_desc = apps[index].get('description')
            application_protocol = apps[index].get('protocol', 'None')
            destination_port = apps[index].get('destination-port')
            source_port = apps[index].get('source-port')
            
            if self.vendor == 'forti':
                forti.service(application_name, destination_port, source_port, application_protocol, application_desc)
            elif self.vendor == 'asa':
                asa.service(application_name, destination_port, source_port, application_protocol, application_desc)
                
            elif self.vendor == 'palo':
                palo.service(application_name, destination_port, source_port, application_protocol, application_desc)

            elif self.vendor == 'chpoint':
                if not source_port:
                    source_port = ''
                # Because the platform does not support name start with Digits!
                if application_name[:1].isdigit():
                    application_name = 'custom_' + application_name
                
                chpoint.service(application_name, destination_port, source_port, application_protocol, application_desc)

                        
    
    @property
    def service_set(self):
        """Exports custome application-set created on SRX"""

        dict_formatted = self._job

        applications_list = dict_formatted['applications']
        apps_set = applications_list['application-set']

        for index in range(len(apps_set)):
            app_list = []
            app_set_name = apps_set[index].get('name', 'None')
            app_set_desc = apps_set[index].get('description')
            app_set_main = apps_set[index]['application']
            for sub_index in range(len(app_set_main)):
                app_name = app_set_main[sub_index].get('name', 'None')
                
                if self.vendor == 'forti' and 'junos' in app_name:
                    app_name = forti_translation.get(app_name, app_name)
                elif self.vendor == 'palo' and 'junos' in app_name:
                    app_name = palo_translation.get(app_name, app_name)
                elif self.vendor == 'chpoint' and 'junos' in app_name:
                    app_name = chpoint_translation.get(app_name, app_name)
                elif self.vendor == 'asa' and 'junos' in app_name:
                    app_name = asa_translation.get(app_name, app_name)

                app_list.append(app_name)
            if not self.vendor == 'asa':
                app_name = ' '.join(app_list)
            
            if self.vendor == 'forti':
                forti.service_set(app_set_name, app_name, app_set_desc)
            elif self.vendor == 'asa':
                asa.service_set(app_set_name, app_list, app_set_desc)
            elif self.vendor == 'palo':
                palo.service_set(app_set_name, app_name)
            elif self.vendor == 'chpoint':
                chpoint.address_set(app_set_name, app_list, app_set_desc)

    
    @property
    def address(self):
        """Converts address books"""

        security_cfg = self._job
        try:
            address_books = security_cfg['security']['address-book']['address']
            address_set_books = security_cfg['security']['address-book']['address-set']
            check = True
        except:
            address_books = security_cfg['security']['zones']['security-zone']
            address_set_books = security_cfg['security']['zones']['security-zone']
            check = False

        for index in range(len(address_books)):
            address_list = []
            if check:
                address_name = address_books[index].get('name', 'None')
                address_description = address_books[index].get('description')
                address_ip = address_books[index].get('ip-prefix', 'None')
            else:
                try:
                    address_b = address_books[index]['address-book']['address']
                except:
                    continue
                for sub_index in range(len(address_b)):
                    if isinstance(address_b, (list)):
                        address_name = address_b[sub_index].get('name', 'None')
                        address_description = address_b[sub_index].get('description')
                        address_ip = address_b[sub_index].get('ip-prefix', 'None')
                        address_list.append([address_name, address_description, address_ip])
                    else:
                        address_name = address_b.get('name', 'None')
                        address_description = address_b.get('description')
                        address_ip = address_b.get('ip-prefix', 'None')
                
            
            if self.vendor == 'forti':
                if address_list:
                    for i in range(len(address_list)):
                        address_name = address_list[i][0]
                        address_description = address_list[i][1]
                        address_ip = address_list[i][2]
                        forti.address(address_name, address_ip, address_description)
                else:
                    forti.address(address_name, address_ip, address_description)
            
            elif self.vendor == 'asa':
                if address_list:
                    for i in range(len(address_list)):
                        address_name = address_list[i][0]
                        address_description = address_list[i][1]
                        address_ip = address_list[i][2]
                        asa.address(address_name, address_ip, address_description)
                else:
                    asa.address(address_name, address_ip, address_description)

            elif self.vendor == 'palo':
                if address_list:
                    for i in range(len(address_list)):
                        address_name = address_list[i][0]
                        address_description = address_list[i][1]
                        address_ip = address_list[i][2]
                        palo.address(address_name, address_ip, address_description)
                else:
                    palo.address(address_name, address_ip, address_description)

            elif self.vendor == 'chpoint':
                if address_list:
                    for i in range(len(address_list)):
                        address_name = address_list[i][0]
                        address_description = address_list[i][1]
                        address_ip = address_list[i][2]
                        chpoint.address(address_name, address_ip, address_description)
                else:
                    chpoint.address(address_name, address_ip, address_description)


        
        if address_set_books:
            for index in range(len(address_set_books)):
                address_name_list = []
                if not check:
                    try:
                        address_b = address_set_books[index]['address-book']['address-set']
                    except:
                        continue
                    address_set_name = address_b.get('name', 'None')
                    address_set_desc = address_b.get('description')
                    address_set_main = address_b.get('address', 'None')
                else:
                    address_set_name = address_set_books[index].get('name', 'None')
                    address_set_desc = address_set_books[index].get('description')
                    address_set_main = address_set_books[index].get('address', 'None')
                for sub_index in range(len(address_set_main)):
                    address_name = address_set_main[sub_index].get('name', 'None')
                    address_name_list.append(address_name)
                address_name = ' '.join(address_name_list)

                if self.vendor == 'forti':
                    forti.address_set(address_set_name, address_name, address_set_desc)
                elif self.vendor == 'asa':
                    asa.address_set(address_set_name, address_name_list, address_set_desc)
                elif self.vendor == 'palo':
                    palo.address_set(address_set_name, address_name, address_set_desc)
                elif self.vendor == 'chpoint':
                    chpoint.address_set(address_set_name, address_name_list, address_set_desc)
    
    @property
    def policy(self):
        srx_policy(self.cfg_file, self.vendor)
    
    @property
    def zone(self):
        """Not Implemented"""
        return
        security_cfg = self._job()
        zones = security_cfg['security']['zones']['security-zone']
        interfaces = security_cfg['interfaces']['interface']

        for main_index in range(len(zones)):
            service_list = []
            zone_int_list = []

            zone_name = zones[main_index].get('name', 'None')
            zone_service = zones[main_index]['host-inbound-traffic']['system-services']
            zone_ints = zones[main_index]['interfaces']
            if isinstance(zone_service, (list)):
                for sub_index in range(len(zone_service)):
                    service = zone_service[sub_index].get('name', 'None')
                    service_list.append(service)
            else:
                service = zone_service.get('name', 'None')
                service_list.append(service)
            service = ' '.join(service_list)

            if isinstance(zone_ints, (list)):
                for sub_index in range(len(zone_ints)):
                    zone_int = zone_ints[sub_index].get('name', 'None')
                    zone_int_list.append(zone_int)
            else:
                zone_int = zone_ints.get('name', 'None')
                zone_int_list.append(zone_int)
            zone_int = ' '.join(zone_int_list)
            if self.vendor == 'forti':
                with open('exported/forti/zones.txt', 'a') as f:
                    f.write(f'zone {zone_name} ')

        
        for main_index in range(len(interfaces)):
            name_list = []
            vlan_list = []
            ip_list = []
            int_name = interfaces[main_index].get('name')
            int_units = interfaces[main_index].get('unit')
            if not int_units:
                continue
            if isinstance(int_units, (list)):
                for sub_index in range(len(int_units)):
                    unit_name = int_units[sub_index].get('name')
                    name_list.append(unit_name)
                    vlan_id = int_units[sub_index].get('vlan-id')
                    vlan_list.append(vlan_id)
                    ip_addr = int_units[sub_index]['family']['inet']['address'].get('name', 'None')
                    ip_list.append(ip_addr)
            else:
                unit_name = int_units.get('name')
                name_list.append(unit_name)
                vlan_id = int_units.get('vlan-id')
                if vlan_id:
                    vlan_list.append(vlan_id)
                try:
                    ip_addr = int_units['family']['inet']['address'].get('name', 'None')
                    ip_list.append(ip_addr)
                except:
                    pass
            unit_name = ' '.join(name_list)
            if vlan_list:
                vlan_id = ' '.join(vlan_list)
            else:
                vlan_id = 0
            if ip_list:
                ip_addr = ' '.join(ip_list)
            else:
                ip_addr = "n/a"


            if self.vendor == 'forti':
                with open('exported/forti/zones.txt', 'a') as f:
                    for i in range(len(name_list)):
                        f.write(f'int {name_list[i]}\n')
    
    @property
    def delete(self):
        os.remove(f'configs/{self.cfg_file}')
    
    @property
    def cleaner(self):
        if not os.path.exists(f'exported/{self.vendor}'):
            os.makedirs(f'exported/{self.vendor}')
        else:
            for f in os.listdir(f'exported/{self.vendor}/'):
                if f != 'policies.txt':
                    os.remove(os.path.join(f'exported/{self.vendor}/', f))
    