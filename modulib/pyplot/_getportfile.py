# -*- coding: utf-8 -*-
# This file is part of the Cortix toolkit evironment
# https://github.com/dpploy/cortix
#
# All rights reserved, see COPYRIGHT for full restrictions.
# https://github.com/dpploy/cortix/blob/master/COPYRIGHT.txt
#
# Licensed under the GNU General Public License v. 3, please see LICENSE file.
# https://www.gnu.org/licenses/gpl-3.0.txt
"""
PyPlot module.
Valmor F. de Almeida dealmeidav@ornl.gov; vfda
Tue Jun 24 01:03:45 EDT 2014
"""
#*********************************************************************************
import os, sys, io, time, datetime
#*********************************************************************************

#---------------------------------------------------------------------------------
# This may return a None portfile
# vfda REVISE ME!!

def _GetPortFile( self, usePortName=None, usePortFile=None, providePortName=None ):

  portFile = None

  #..........
  # Use ports
  #..........
  if usePortName is not None:

    assert providePortName is None

    for port in self.ports:
      (portName,portType,thisPortFile) = port
      if portName == usePortName and portType == 'use' and thisPortFile == usePortFile: portFile = thisPortFile

    if portFile is None: return None

    maxNTrials = 50
    nTrials    = 0
    while os.path.isfile(portFile) is False and nTrials <= maxNTrials:
      nTrials += 1
      time.sleep(0.1)

    if nTrials >= 10:
      s = '_GetPortFile(): waited ' + str(nTrials) + ' trials for port: ' + portFile
      self.log.warn(s)

    assert os.path.isfile(portFile) is True, 'portFile %r not available; stop.' % portFile

  #..............
  # Provide ports
  #..............
  if providePortName is not None:

    assert usePortName is None

    for port in self.ports:
      (portName,portType,thisPortFile) = port
      if portName == providePortName and portType == 'provide': portFile = thisPortFile

  return portFile

#*********************************************************************************
