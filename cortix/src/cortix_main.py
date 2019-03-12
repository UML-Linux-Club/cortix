#!/usr/bin/env python
# -*- coding: utf-8 -*-
# This file is part of the Cortix toolkit environment
# https://cortix.org
#
# All rights reserved, see COPYRIGHT for full restrictions.
# https://github.com/dpploy/cortix/blob/master/COPYRIGHT.txt
#
# Licensed under the University of Massachusetts Lowell LICENSE:
# https://github.com/dpploy/cortix/blob/master/LICENSE.txt
'''
The Cortix class definition.

Cortix: a program for system-level modules coupling, execution, and analysis.
'''
#*********************************************************************************
import os
import logging
from cortix.src.simulation import Simulation
from cortix.src.utils.configtree import ConfigTree
from cortix.src.utils.set_logger_level import set_logger_level
#*********************************************************************************

class Cortix():
    '''
    The main Cortix class definition. This class encapsulates the
    concepts of simulations, tasks, and modules, for a given application providing
    the user with an interface to the simulations.
    '''

    def __init__(self, name, config_file='cortix-config.xml'):

        assert isinstance(name,str), 'must give Cortix object a name'

        assert isinstance(config_file, str), '-> configFile not a str.'
        self.__config_file = config_file

        # Create a configuration XML tree
        config_tree = ConfigTree(config_file_name=self.__config_file)

        # Read the cortix config element (tag) name <name></name>
        node = config_tree.get_sub_node('name')  # get node (or XML element)
        self.__name = node.text.strip()   # name is now, say, 'droplet-fall'

        # Consistency check
        assert self.__name == name,\
            'Runtime Cortix object name %r conflicts with cortix-config.xml %r' \
            % (self.__name, name)

        # Read the work directory name
        node = config_tree.get_sub_node('work_dir')
        work_dir = node.text.strip()
        if work_dir[-1] != '/':
            work_dir += '/'

        self.__work_dir = work_dir + self.__name + '-wrk/'

        # Create the work directory
        if os.path.isdir(self.__work_dir):
            os.system('rm -rf ' + self.__work_dir)

        os.system('mkdir -p ' + self.__work_dir)

        # Create the logging facility for each object
        self.__create_logging_facility( config_tree )

        # Setup simulations (one or more as specified in the config file)
        self.__simulations = list()

        self.__setup_simulations( config_tree )

        self.__log.info('Created Cortix object %s', self.__name)
#----------------------- end def __init__():--------------------------------------

    def __del__(self):

        self.__log.info("Destroyed Cortix object: %s", self.__name)
#----------------------- end def __del__():---------------------------------------

    def run_simulations(self, task_name=None):
        '''
        This method runs every simulation
        defined by the Cortix object.
        At the moment this is done one simulation at a time.
        '''

        for sim in self.__simulations:

            sim.execute(task_name)
#----------------------- end def run_simulations():-------------------------------

#*********************************************************************************
# Private helper functions (internal use: __)

    def __create_logging_facility(self, config_tree):
        '''
        A helper function to setup the logging facility used in  self.__init__()
        '''

        node = config_tree.get_sub_node('logger')
        logger_name = self.__name
        self.__log = logging.getLogger(logger_name)
        self.__log.setLevel(logging.NOTSET)
        logger_level = node.get('level').strip()
        self.__log = set_logger_level(self.__log, logger_name, logger_level)

        file_handler = logging.FileHandler(self.__work_dir + 'cortix.log')
        file_handler.setLevel(logging.NOTSET)
        file_handler_level = None

        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.NOTSET)
        console_handler_level = None

        for child in node:
            if child.tag == 'file_handler':
                file_handler_level = child.get('level').strip()
                file_handler = set_logger_level(file_handler, logger_name,
                                                file_handler_level)
            if child.tag == 'console_handler':
                console_handler_level = child.get('level').strip()
                console_handler = set_logger_level(console_handler, logger_name,
                                                   console_handler_level)

        # Formatter added to handlers
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        file_handler.setFormatter(formatter)
        console_handler.setFormatter(formatter)

        # add handlers to logger
        self.__log.addHandler(file_handler)
        self.__log.addHandler(console_handler)
        self.__log.info('Created Cortix logger: %s', self.__name)
        self.__log.debug('Logger level: %s', logger_level)
        self.__log.debug('Logger file handler level: %s', file_handler_level)
        self.__log.debug(
            'Logger console handler level: %s',
            console_handler_level)
        self.__log.info('Created Cortix work directory: %s', self.__work_dir)

        return
#----------------------- end def __create_logging_facility():---------------------

    def __setup_simulations(self, config_tree):
        '''
        This method is a helper function for the Cortix constructor
        whose purpose is to set up the simulations defined by the
        Cortix configuration.
        '''

        for sim in config_tree.get_all_sub_nodes('simulation'):
            self.__log.debug(
                '__setup_simulations(): simulation name: %s',
                sim.get('name'))
            sim_config_tree = ConfigTree(sim)

            simulation = Simulation( self.__work_dir, sim_config_tree )

            self.__simulations.append(simulation)

        return
#----------------------- end def __setup_simulations():---------------------------

#======================= end class Cortix: =======================================
