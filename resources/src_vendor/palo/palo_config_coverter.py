import json
import xmltodict
import os
import logging


from resources.dst_vendor.dst_srx import SRX_DST
from resources.dst_vendor.dst_forti import Forti_DST
from resources.dst_vendor.dst_asa import ASA_DST
from resources.dst_vendor.dst_chpoint import CHPoint_DST
from resources.src_vendor.palo.palo_policy_convert import palo_policy

srx = SRX_DST()
forti = Forti_DST()
asa = ASA_DST()
chpoint = CHPoint_DST()
logger = logging.getLogger('fwmig.palo.config')


class PALO_Cfg:
    """Converts PA -> Fortigate, ASA, Forti, Palo Alto (except zone and interfaces) """
    def __init__(self, cfg_file: str, vendor: str) -> None:
        self.cfg_file = cfg_file
        self.vendor = vendor
    
    @property
    def _job(self):
        with open(f'configs/{self.cfg_file}', 'r') as imp_file:
            xml_dict = xmltodict.parse(imp_file.read())
        json_formatted = json.dumps(xml_dict)
        dict_formatted = json.loads(json_formatted)
        try:
            return dict_formatted['root']['response']
        except:
            return False
    
    @property
    def service(self):
        """Exports custom application created on PaloAlto"""

        dict_formatted = self._job
        if not dict_formatted:
            return False
        for i in range(len(dict_formatted)):
            try:
                if 'service' in dict_formatted[i]['result']:
                    applications_list = dict_formatted[i]['result']['service']['entry']
            except:
                continue

        for index in range(len(applications_list)):
            application_name = applications_list[index].get('@name', 'None')
            application_desc = applications_list[index].get('description')
            application_protocol = applications_list[index]['protocol'].keys()
            application_protocol = list(application_protocol)[0]
            destination_port = applications_list[index]['protocol'][application_protocol]['port']
            source_port = 'None'

            
            if self.vendor == 'forti':
                forti.service(application_name, destination_port, source_port, application_protocol, application_desc)
            elif self.vendor == 'asa':
                asa.service(application_name, destination_port, source_port, application_protocol, application_desc)
                
            elif self.vendor == 'srx':
                srx.service(application_name, destination_port, source_port, application_protocol, application_desc)

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
        if not dict_formatted:
            return False
        
        for i in range(len(dict_formatted)):
            try:
                if 'service-group' in dict_formatted[i]['result']:
                    applications_list = dict_formatted[i]['result']['service-group']['entry']
            except:
                continue

        for index in range(len(applications_list)):
            app_list = []
            app_set_name = applications_list[index].get('@name', 'None')
            app_set_desc = applications_list[index].get('description')
            app_set_main = applications_list[index]['members']['member']
            for sub_index in range(len(app_set_main)):
                app_name = app_set_main[sub_index]


                app_list.append(app_name)
            if not self.vendor == 'asa':
                app_name = ' '.join(app_list)
            
            if self.vendor == 'forti':
                forti.service_set(app_set_name, app_name, app_set_desc)
            elif self.vendor == 'asa':
                asa.service_set(app_set_name, app_list, app_set_desc)
            elif self.vendor == 'srx':
                srx.service_set(app_set_name, app_name)
            elif self.vendor == 'chpoint':
                chpoint.address_set(app_set_name, app_list, app_set_desc)

    
    @property
    def address(self):
        """Converts address books"""
        dict_formatted = self._job
        if not dict_formatted:
            return False
        
        for i in range(len(dict_formatted)):
            try:
                if 'address' in dict_formatted[i]['result']:
                    address_list = dict_formatted[i]['result']['address']['entry']
                elif 'address-group' in dict_formatted[i]['result']:
                    address_set_books = dict_formatted[i]['result']['address-group']['entry']
            except:
                continue

        for index in range(len(address_list)):
            address_name = address_list[index].get('@name', 'None')
            address_description = address_list[index].get('description')
            address_ip = address_list[index].get('ip-netmask', 'None')
            if address_ip == 'None' or address_name == 'None':
                continue


            if self.vendor == 'forti':
                forti.address(address_name, address_ip, address_description)
            
            elif self.vendor == 'asa':
                asa.address(address_name, address_ip, address_description)

            elif self.vendor == 'srx':
                srx.address(address_name, address_ip, address_description)

            elif self.vendor == 'chpoint':
                chpoint.address(address_name, address_ip, address_description)


        
        if address_set_books:
            for index in range(len(address_set_books)):
                address_name_list = []
                address_set_name = address_set_books[index].get('@name', 'None')
                address_set_desc = address_set_books[index].get('description')
                
                address_set_main = address_set_books[index]['static']['member']
                for sub_index in range(len(address_set_main)):
                    address_name = address_set_main[sub_index]
                    address_name_list.append(address_name)
                address_name = ' '.join(address_name_list)

                if self.vendor == 'forti':
                    forti.address_set(address_set_name, address_name, address_set_desc)
                elif self.vendor == 'asa':
                    asa.address_set(address_set_name, address_name_list, address_set_desc)
                elif self.vendor == 'srx':
                    srx.address_set(address_set_name, address_name, address_set_desc)
                elif self.vendor == 'chpoint':
                    chpoint.address_set(address_set_name, address_name_list, address_set_desc)
    
    @property
    def policy(self):
        palo_policy(self.cfg_file, self.vendor)
    
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
    
    