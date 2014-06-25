#!/usr/bin/env python
"""
Valmor F. de Almeida dealmeidav@ornl.gov; vfda

Cortix Nitron dissolver module wrapper 

Tue Jun 24 01:03:45 EDT 2014
"""
#*********************************************************************************
import os, sys, io, time
import datetime
from xml.etree.ElementTree import ElementTree
from xml.etree.ElementTree import Element
#from holdingdrum import SetupHoldingDrum
#*********************************************************************************

def main(argv):

 assert len(argv) == 5, 'incomplete command line input.'

# First command line argument is the module input file name with full path.
# This input file is used by both the wrapper and the inner-code for 
# communication.
 inputFullPathFileName = argv[1]

 fin = open(inputFullPathFileName,'r')
 for line in fin:
  homeDir = line.strip()

 print('dissolver.py: input dir: ',homeDir)

 tree = ElementTree()

# Second command line argument is the Cortix parameter file
 cortexParamFullPathFileName = argv[2]
 tree.parse(cortexParamFullPathFileName)
 cortexParamXMLRootNode = tree.getroot()
 node = cortexParamXMLRootNode.find('evolveTime')
 evolveTimeUnit = node.get('unit')
 evolveTime     = float(node.text.strip())

# Third command line argument is the Cortix communication file
 cortexCommFullPathFileName = argv[3]
 tree.parse(cortexCommFullPathFileName)
 cortexCommXMLRootNode = tree.getroot()

# Get useports
 nodes = cortexCommXMLRootNode.findall('usePort')
 usePorts = list()
 if nodes is not None: 
   for node in nodes:
     usePortName = node.get('name')
     usePortFile = node.get('file')
     usePorts.append( (usePortName, usePortFile) )
 print('usePorts: ',usePorts)

# Get provideports
 nodes = cortexCommXMLRootNode.findall('providePort')
 providePorts = list()
 if nodes is not None: 
   for node in nodes:
     providePortName = node.get('name')
     providePortFile = node.get('file')
     providePorts.append( (providePortName, providePortFile) )
 print('providePorts: ',providePorts)

# Fourth command line argument is the module runtime-status.xml file
 runtimeStatusFullPathFileName = argv[4]

#---------------------------------------------------------------------------------
# Run Nitron 
 runCommand = homeDir + 'main.m' + ' ' + inputFullPathFileName + ' &'
 print( 'dissolver.py: run time ' + runCommand  )
# os.system( 'time ' + runCommand  )

 fout = open( runtimeStatusFullPathFileName,'w' )
 s = '<?xml version="1.0" encoding="UTF-8"?>\n'; fout.write(s)
 s = '<!-- Written by Dissolver.py -->\n'; fout.write(s)
 s = '<runtime>\n'; fout.write(s)
 s = '<status>running</status>\n'; fout.write(s)
 s = '</runtime>\n'; fout.write(s)
 fout.close()

# for (portName,portFile) in usePorts:
#   if portName == 'solids':
#    holdingDrumContents = SetupHoldingDrum(portFile)

 if    evolveTimeUnit == 'min':  evolveTime *= 1.0
 elif  evolveTimeUnit == 'hour': evolveTime *= 60.0
 elif  evolveTimeUnit == 'day':  evolveTime *= 24.0 * 60.0
 else: assert True, 'bad time unit.'

 time.sleep(10)

# for t in range(evolveTime):
#   (mass, GetSolidLoad(t)


# Communicate with Nitron to check running status

#---------------------------------------------------------------------------------
# Shutdown 

 tree.parse(runtimeStatusFullPathFileName)
 runtimeStatusXMLRootNode = tree.getroot()
 root = runtimeStatusXMLRootNode
 node = root.find('status')
 node.text = 'finished'
 a = Element('comment')
 a.text = 'Written by Dissolver.py'
 root.append(a)
 tree.write(runtimeStatusFullPathFileName,xml_declaration=True,encoding="UTF-8",method="xml")

#*********************************************************************************
# Usage: -> python dissolver.py or ./dissolver.py
if __name__ == "__main__":
   main(sys.argv)
