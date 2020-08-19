import os
import configparser
import colorama
from pathlib import Path

config = configparser.ConfigParser()
try:
    try: 
        config.read('./tuckr.conf')
    except:
        config.read(Path.expanduser('~/.config/tuckr.conf'))
except KeyError:
    print(f"{colorama.Fore.RED}Error: No config file was found{colorama.Fore.RESET}")


def clone_dotfiles():
    '''
    Clones the dotfile for the repo provided by dotfiles_repo.
    Git needs to be installed for it to work.
    '''
    try:
        if ('dotfiles_repo' in config['GENERAL']):
            if ('dotfiles_dest' in config['GENERAL']):
                os.system(f"git clone {config['GENERAL']['dotfiles_repo']} {config['GENERAL']['dotfiles_dest']}")
            else:
                os.system(f"git clone {config['GENERAL']['dotfiles_repo']} $HOME/dotfiles")
        else:
            os.system(config['GENERAL']['clone_dotfiles_cmd'])
    except KeyError:
        print(colorama.Fore.RED + 'Error: No dotfile repo was specified. Make sure you set it up in your tuckr.ini file.' + colorama.Fore.RESET)

def install_packages():
    '''
    Installs packages using the pkg_install_cmd
    intended for use with native packages.
    '''
    if ('pkg_install_cmd' in config['PACKAGES']):
        with open(config['PACKAGES']['pkg_list'], 'r') as pkgs:
            pkgs = pkgs.read().replace('\n', ' ')
            os.system(f"{config['PACKAGES']['pkg_install_cmd']} {pkgs}")

def run_scripts():
    '''
    Runs scripts specified in the config file in insertion order
    '''
    for script in config['SCRIPTS']:
        print(f"\n{colorama.Fore.GREEN}running {script}{colorama.Fore.RESET}")
        os.system(f"sh -c {config['SCRIPTS'][script]}")

def install_from_list():
    '''
    Takes a list and a key with the name of the package manager
    Checks a dictionary and if present it will run the appropriate command
    '''
    install_cmd = {
        'pip': 'install --user',
        'npm': 'install -g',
        'yarn': 'global add'
    }
    for list_ in config['PACKAGES']:
        if('_list' in list_):
            cmd = list_.split('_')[0]
            try: 
                with open(config['PACKAGES'][list_], 'r') as list_file:
                    list_file = list_file.read().replace('\n', ' ')
                    os.system(f"{cmd} {install_cmd[cmd]} {list_file}")
            except KeyError:
                pass
