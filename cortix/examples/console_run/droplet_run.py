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
Cortix: a program for system-level modules coupling, execution, and analysis.
'''
#*********************************************************************************
import os
from cortix import Cortix
#*********************************************************************************

def run():
    '''
    Run the Cortix Droplet example. If Cortix and its dependencies are installed,
    this program should be executed at the command prompt inside the directory
    this program resides, namely, cortix/cortix/example/console_run/ directory.
    '''

    pwd = os.path.dirname(__file__)
    full_path_config_file = os.path.join(pwd, '../input/cortix-config-droplet.xml')
    cortix = Cortix('cortix-droplet', full_path_config_file)
    cortix.run_simulations(task_name="droplet-fall")
#    cortix.run_simulations(task_name="solo-droplet-fall")
#    cortix.run_simulations(task_name="solo-pyplot") # this needs additional config
#---------------------- end def run():--------------------------------------------

#*********************************************************************************
if __name__ == "__main__":
    run()
