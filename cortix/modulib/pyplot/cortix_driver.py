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
Cortix driver for the PyPlot module.
'''
# *********************************************************************************
import os
import sys
import io
import time
import datetime
import logging

from cortix.modulib.pyplot.pyplot import PyPlot
# *********************************************************************************

class CortixDriver():
    '''
     Cortix driver for guest module: PyPlot.
    '''

#*********************************************************************************
# Construction 
#*********************************************************************************

    def __init__( self,
            slot_id,
            input_full_path_file_name,
            manifesto_full_path_file_name,
            work_dir,
            ports=list(),
            cortix_start_time = 0.0,
            cortix_final_time = 0.0,  
            cortix_time_step  = 0.0,
            cortix_time_unit  = None
            ):

        # Sanity tests.
        assert isinstance(slot_id, int), '-> slot_id type %r is invalid.'% type(slot_id)
        assert isinstance(ports, list), '-> ports type %r is invalid.'% type(ports)
        assert len(ports) > 0
        assert isinstance(cortix_start_time, float), '-> time type %r is invalid.'% \
            type(cortix_start_time)
        assert isinstance(cortix_final_time, float), '-> time type %r is invalid.'% \
            type(cortix_final_time)
        assert isinstance(cortix_time_step, float), '-> time step type %r is invalid.'% \
            type(cortix_time_step)
        assert isinstance(cortix_time_unit, str), '-> time unit type %r is invalid.'% \
            type(cortix_time_unit)

        # Logging.
        self.__log = logging.getLogger('launcher-modulib.pyplot_' + str(slot_id) +\
                                      '.cortix_driver')
        self.__log.debug('initializing an object of CortixDriver()')

        self.__wall_clock_time_stamp = None  # initialize

        # Guest library module: PyPlot.
        self.pyplot = PyPlot( slot_id,
                              input_full_path_file_name,
                              manifesto_full_path_file_name,
                              work_dir,
                              ports,
                              cortix_start_time,
                              cortix_final_time,
                              cortix_time_step,
                              cortix_time_unit )

        return

#*********************************************************************************
# Public member functions 
#*********************************************************************************

    def call_ports(self, cortix_time=0.0):
        '''
        Call all ports at cortix_time.
        '''

        self.__log_debug(cortix_time, 'call_ports')

        self.pyplot.call_ports(cortix_time)

        self.__log_debug(cortix_time, 'call_ports')

        return

    def execute(self, cortix_time=0.0, time_step=0.0):
        '''
        Evolve system from cortix_time to cortix_time + time_step
        '''

        self.__log_debug(cortix_time, 'execute')

        self.pyplot.execute(cortix_time, time_step)

        self.__log_debug(cortix_time, 'execute')

        return

#*********************************************************************************
# Private helper functions (internal use: __)
#*********************************************************************************

    def __log_debug(self, cortix_time=0.0, caller='null-function-name'):

        if self.__wall_clock_time_stamp is None:
            s = ''
            self.__log.debug(s)
            s = '=========================================================='
            self.__log.debug(s)
            s = 'CORTIX::DRIVER->***->DRIVER->***->DRIVER->***->DRIVER->***'
            self.__log.debug(s)
            s = '=========================================================='
            self.__log.debug(s)

            s = caller + '(' + str(round(cortix_time, 2)) + '[min]):'
            self.__log.debug(s)

            self.__wall_clock_time_stamp = time.time()

        else:

            end_time = time.time()

            s = caller + '(' + str(round(cortix_time, 2)) + '[min]): '
            m = 'CPU elapsed time (s): ' + \
                str(round(end_time - self.__wall_clock_time_stamp, 2))
            self.__log.debug(s + m)

            self.__wall_clock_time_stamp = None
            if caller == 'execute':
                s = ''
                self.__log.debug(s)

        return

# ====================== end class CortixDriver: =================================
