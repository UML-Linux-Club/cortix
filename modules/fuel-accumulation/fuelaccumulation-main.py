#!/usr/bin/env python
"""
Valmor F. de Almeida dealmeidav@ornl.gov; vfda

Cortix FuelAccumulation module executable

Sun Jun 29 21:34:18 EDT 2014
"""
#*********************************************************************************
import os, sys, io, time
import datetime
import xml.etree.ElementTree as ElementTree
from fuelaccumulation import FuelAccumulation
#*********************************************************************************

#---------------------------------------------------------------------------------
def main(argv):

 assert len(argv) == 5, 'incomplete command line input.'

#.................................................................................
# First command line argument is the module input file name with full path.
# This input file may be used by both the wrapper and the inner-code for 
# communication.
 inputFullPathFileName = argv[1]

 fin = open(inputFullPathFileName,'r')
 inputData = list()
 for line in fin:
  inputData.append(line.strip())
 fin.close()

#.................................................................................
# Second command line argument is the Cortix parameter file: cortix-param.xml
 cortexParamFullPathFileName = argv[2]
 tree = ElementTree.parse(cortexParamFullPathFileName)
 cortexParamXMLRootNode = tree.getroot()

 node = cortexParamXMLRootNode.find('evolveTime')

 evolveTimeUnit = node.get('unit')
 evolveTime     = float(node.text.strip())

 if    evolveTimeUnit == 'min':  evolveTime *= 1.0
 elif  evolveTimeUnit == 'hour': evolveTime *= 60.0
 elif  evolveTimeUnit == 'day':  evolveTime *= 24.0 * 60.0
 else: assert True, 'time unit invalid.'

 node = cortexParamXMLRootNode.find('timeStep')

 timeStepUnit = node.get('unit')
 timeStep       = float(node.text.strip())

 if    timeStepUnit == 'min':  timeStep *= 1.0
 elif  timeStepUnit == 'hour': timeStep *= 60.0
 elif  timeStepUnit == 'day':  timeStep *= 24.0 * 60.0
 else: assert True, 'time unit invalid.'

#.................................................................................
# Third command line argument is the Cortix communication file: cortix-comm.xml
 cortexCommFullPathFileName = argv[3]
 tree = ElementTree.parse(cortexCommFullPathFileName)
 cortexCommXMLRootNode = tree.getroot()

# Setup ports
 nodes = cortexCommXMLRootNode.findall('port')
 ports = list()
 if nodes is not None: 
   for node in nodes:
     portName = node.get('name')
     portType = node.get('type')
     portFile = node.get('file')
     ports.append( (portName, portType, portFile) )
 print('fuelaccumulation-main.py::ports: ',ports)

 tree = None

#.................................................................................
# Fourth command line argument is the module runtime-status.xml file
 runtimeStatusFullPathFileName = argv[4]

#---------------------------------------------------------------------------------
# Run FuelAccumulation

#................................................................................
# Left here as an example; vfda
# Setup input (this was used when debugging; need proper cortix-config.xml

# found = False
# for port in ports:
#  if port[0] is 'solids':
#   print( 'cp -f ' + inputData[0] + ' ' + port[2] )
#   os.system( 'cp -f ' + inputData[0] + ' ' + port[2] )
#   found = True

# assert found, 'Input setup failed.'

# found = False
# for port in ports:
#  if port[0] is 'withdrawal-request':
#   print( 'cp -f ' + inputData[1] + ' ' + port[2] )
#   os.system( 'cp -f ' + inputData[1] + ' ' + port[2] )
#   found = True

# assert found, 'Input setup failed.'

#................................................................................
# Create a fuel holding drum
 fuelDrum = FuelAccumulation( ports )

#................................................................................
# Evolve the fuel accumulation

 SetRuntimeStatus( runtimeStatusFullPathFileName, 'running' )

 facilityTime = 0.0

 while facilityTime <= evolveTime:

  fuelDrum.CallPorts( facilityTime )

  fuelDrum.Execute( facilityTime, timeStep )

  facilityTime += timeStep

#---------------------------------------------------------------------------------
# Shutdown 

 SetRuntimeStatus(runtimeStatusFullPathFileName, 'finished') 

#---------------------------------------------------------------------------------
def SetRuntimeStatus(runtimeStatusFullPathFileName, status):

 status = status.strip()
 assert status == 'running' or status == 'finished', 'status invalid.'

 fout = open( runtimeStatusFullPathFileName,'w' )
 s = '<?xml version="1.0" encoding="UTF-8"?>\n'; fout.write(s)
 s = '<!-- Written by fuelaccumulation-main.py -->\n'; fout.write(s)
 s = '<runtime>\n'; fout.write(s)
 s = '<status>'+status+'</status>\n'; fout.write(s)
 s = '</runtime>\n'; fout.write(s)
 fout.close()

#*********************************************************************************
# Usage: -> python fuel-accumulation.py or ./fuel-accumulation.py
if __name__ == "__main__":
   main(sys.argv)
