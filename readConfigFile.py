import configparser
import os
import sys

def get_config_path():
    """Determine the correct path to the config.ini file."""
    if hasattr(sys, '_MEIPASS'):
        # If running as a bundled executable
        return os.path.join(sys._MEIPASS, "config.ini")
    else:
        # If running in development
        return os.path.abspath("config.ini")


config = configparser.ConfigParser()

config.read("config.ini")


def GetQGivToken():
    return config['QGiv']['ApiToken']

def GetClientId():
    return config['Azure']['ClientId']

def GetClientSecret():
    return config['Azure']['ClientSecret']

def GetTenantId():
    return config['Azure']['ClientTenantId']
