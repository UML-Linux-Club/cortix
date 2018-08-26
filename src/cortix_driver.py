# -*- coding: utf-8 -*-
# This file is part of the Cortix toolkit evironment
# https://github.com/dpploy/...
#
# All rights reserved, see COPYRIGHT for full restrictions.
# https://github.com/dpploy/COPYRIGHT
#
# Licensed under the GNU General Public License v. 3, please see LICENSE file.
# https://www.gnu.org/licenses/gpl-3.0.txt
"""
Cortix driver for guest modules.
Module developers must implement the public methods in this driver.
Ideally, this implementation should be minimal.         
Developers should use this class to wrap their module (MyModule) implemented in a
file named my_module.py. This file will be placed inside the developer's module
directory which is pointed to in the Cortix config.xml file.
"""
#*********************************************************************************
import os
import sys
import io
import time
import datetime
import logging

# uncomment
#from .my_module import MyModule
#*********************************************************************************

class CortixDriver():
 """
  Cortix driver for guest modules.
 """

 def __init__( self,
               slot_id,
               input_full_path_file_name,
               exec_full_path_file_name,
               work_dir,
               ports=list(),
               cortix_start_time=0.0,
               cortix_final_time=0.0  
             ):

  # Sanity test
  assert isinstance(slot_id, int), '-> slot_id type %r is invalid.' % type(slot_id)
  assert isinstance(ports, list), '-> ports type %r is invalid.'  % type(ports)
  assert len(ports) > 0
  assert isinstance(cortix_start_time,float), '-> time type %r is invalid.' % type(cortix_start_time)
  assert isinstance(cortix_final_time, float), '-> time type %r is invalid.' % type(cortix_final_time)

  # Logging
  self.log = logging.getLogger( 'launcher-mymodule'+str(slot_id)+'.cortixdriver' )
  self.log.info( 'initializing an object of CortixDriver()' )

  # Guest library module: MyModule
  # uncomment
  # self.my_module = MyModule( slot_id, input_full_path_file_name, work_dir, ports, 
  #                            cortix_start_time, cortix_final_time )

  self.time_stamp = None # temporary

  return
#---------------------- end def __init__():---------------------------------------

 def call_ports( self, cortix_time=0.0 ):
  """
  Call all ports at cortix_time
  """

  self.__log_debug(facility_time, 'call_ports')

  # uncomment
  # self.my_module.call_ports( cortix_time ) 

  self.__log_debug(facility_time, 'call_ports')

  return
#---------------------- end def call_ports():-------------------------------------

 def execute( self, cortix_time=0.0, timeStep=0.0 ):
  """
  Evolve system from cortix_time to cortix_time + timeStep
  """

  self.__log_debug(facility_time, 'execute')

  # uncomment
  # self.my_module.execute( cortix_time, timeStep )

  self.__log_debug(facility_time, 'execute')

  return
#---------------------- end def execute():----------------------------------------

#*********************************************************************************
# Private helper functions (internal use: __)

 def __log_debug(self, facility_time=0.0, caller='null-function-name'):

  if self.time_stamp == None:
      s = ''
      self.__log.debug(s)
      s = '=========================================================='
      self.__log.debug(s)
      s = 'CORTIX::DRIVER->***->DRIVER->***->DRIVER->***->DRIVER->***'
      self.__log.debug(s)
      s = '=========================================================='
      self.__log.debug(s)

      s = caller+'('+str(round(facility_time,2))+'[min]):'
      self.__log.debug(s)

      self.time_stamp = time.time()

  else:

      end_time = time.time()

      s = caller+'('+str(round(facility_time,2))+'[min]): '
      m = 'CPU elapsed time (s): '+str(round(end_time-self.time_stamp,2))
      self.__log.debug(s+m)

      self.time_stamp = None
      if caller == 'execute':
          s = ''
          self.log.debug(s)

  return
#---------------------- end def __log_debug():------------------------------------

#====================== end class CortixDriver: ==================================
