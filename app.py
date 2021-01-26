import argparse
import os
import sys

from resources.srx.srx_config_converter import SRXConfig
from resources.srx.srx_policy_convert import srx_policy

convert_parser = argparse.ArgumentParser(description='SRX source configuration', allow_abbrev=False)
convert_parser.add_argument('--file',
                       '-f',
                       metavar='',
                       help='The file fullname inside <./configs> (e.g. config.log)',
                       required=True
                       )
convert_parser.add_argument('--action',
                       '-a',
                       metavar='',
                       help='Select action <policy|config> based on <Config file>',
                       required=True)

args = convert_parser.parse_args()

if args.action == 'policy':
    try:
        srx_policy(args.file)
        print('Enjoy!')
        print('Please find output on <./exported> path')
    except FileNotFoundError:
        print('Invalid Input or maybe there is no file in <./Conifg> path, try again!')
    except:
        print('Make sure policy is xml formatted with proper <show> command. Please see instruction on Github')

elif args.action == 'config':
    try:
        actions = SRXConfig(args.file)
        actions.address_book
        actions.custom_service
        actions.custom_service_set
        print('Enjoy!')
        print('Please find output on <./exported> path')
    except FileNotFoundError:
        print('Invalid Input or maybe there is no file in <./Conifg> path, try again!')
    except:
        print('Make sure config is xml formatted. Please see instruction on Github')
else:
    raise ValueError('Please check "-a" action (policy|config)')

