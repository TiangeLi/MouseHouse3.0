# coding=utf-8

"""Handles IO and Configurations across all modules and devices"""

from Misc.GlobalVars import HOME_DIR


class MainSettings(object):
    """Holds all relevant user configurable settings"""
    def __init__(self):
        # Last Used Settings
        self.last_save_dir = ''
        self.ttl_time = 0.0

    def load_examples(self):
        """Example settings for first time users"""
        self.last_save_dir = HOME_DIR + '\\Desktop\\MiniscopeSaves'
        self.ttl_time = 300.0  # in secs; 5 min Default
