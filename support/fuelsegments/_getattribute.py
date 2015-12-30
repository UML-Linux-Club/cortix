#!/usr/bin/env python
"""
Valmor F. de Almeida dealmeidav@ornl.gov; vfda

Fuel segment support class

Thu Jun 25 18:16:06 EDT 2015
"""
#*********************************************************************************
import os, sys, io, time, datetime
import math, random
from ..periodictable import ELEMENTS
from ..periodictable import SERIES
#*********************************************************************************

# Get stored fuel segment property either overall or on a nuclide basis 

#---------------------------------------------------------------------------------
def _GetAttribute(self, attributeName, symbol=None, series=None ):

  assert attributeName in self.attributeNames, ' attribute name: %r; options: %r; fail.' % (attributeName,self.attributeNames)

  if symbol is not None: assert series is None, 'fail.'
  if series is not None: assert symbol is None, 'fail.'

#.................................................................................
# # of segments

  if attributeName == 'nSegments':  return 1

#.................................................................................
# segmentId   

  if attributeName == 'segmentId': return self.geometry['segment id'] 

#.................................................................................
# fuel volume

  if attributeName == 'fuelVolume':   return  __GetFuelSegmentVolume( self )
#.................................................................................
# segment volume

  if attributeName == 'segmentVolume': 
 
    claddingLength = self.geometry['cladding length [cm]'] 
    claddingDiam   = self.geometry['OD [cm]']
    volume = claddingLength * math.pi * (claddingDiam/2.0)**2
    return volume

#.................................................................................
# mass or mass concentration

  if attributeName == 'massCC' or attributeName == 'mass': 
     colName = 'Mass CC [g/cc]'

#.................................................................................
# radioactivity               

  if attributeName == 'radioactivityDens' or attributeName == 'radioactivity': 
     colName = 'Radioactivity Dens. [Ci/cc]'

#.................................................................................
# thermal                     

  if attributeName == 'thermalDens' or attributeName == 'thermal' or  \
     attributeName == 'heatDens'    or attributeName == 'heat': 
     colName = 'Thermal Dens. [W/cc]'

#.................................................................................
# gamma                       

  if attributeName == 'gammaDens' or attributeName == 'gamma': 
     colName = 'Gamma Dens. [W/cc]'

#.................................................................................
##################################################################################
#.................................................................................

  if attributeName[-4:] == 'Dens' or attributeName[-2:] == 'CC': 
     attributeDens = True
  else:
     attributeDens = False 

#.................................................................................
# all nuclide content of the fuel added

  if symbol is None and series is None:

     density = 0.0
     density = self.propertyDensities[ colName ].sum()
     if attributeDens is False:  
        volume = __GetFuelSegmentVolume( self )
        prop = density * volume
        return prop
     else:
        return density

#.................................................................................
# get chemical element series

  if series is not None:
 
     density = 0.0

     for isotope in isotopes:
       density += self.propertyDensities.loc[isotope,colName]

     if attributeDens is False:  
        volume = __GetFuelSegmentVolume( self )
        prop = density * volume
        return prop
     else:
        return density
   
#.................................................................................
# get specific nuclide (either the isotopes of the nuclide or the specific isotope) property

  if symbol is not None:

    density = 0.0

  # isotope
    if len(symbol.split('-')) == 2:
      density = self.propertyDensities.loc[symbol,colName]

  # chemical element 
    else:
      nuclidesNames = self.propertyDensities.index
#    print(self.propertyDensities)
      isotopes = [x for x in nuclidesNames if x.split('-')[0].strip()==symbol]
#    print(isotopes)
      for isotope in isotopes:
        density += self.propertyDensities.loc[isotope,colName]

    if attributeDens is False:  
       volume = __GetFuelSegmentVolume( self )
       prop = density * volume
       return prop
    else:
       return density

#---------------------------------------------------------------------------------
def __GetFuelSegmentVolume(self):
 
  fuelLength = self.geometry['fuel length [cm]'] 
  fuelDiam   = self.geometry['fuel diameter [cm]']

  volume = fuelLength * math.pi * (fuelDiam/2.0)**2

  return volume

#*********************************************************************************
