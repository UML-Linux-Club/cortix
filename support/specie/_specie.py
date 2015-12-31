"""
Valmor de Almeida dealmeidav@ornl.gov; vfda

This Secie class is to be used with other classes in plant-level process modules.

Sat May  9 21:40:48 EDT 2015 created; vfda
"""
#*******************************************************************************
import os, sys

from ..periodictable import ELEMENTS
#*******************************************************************************

#*******************************************************************************
# constructor

def _Specie( self, 
             name    = 'null',
             formula = 'null',
             phase   = 'null',
             atoms   = list(),
             molarCC = 0.0,      # M 
             massCC  = 0.0,      # g/L
             flag    = None   ):

 assert type(name) == type(str()), 'oops not string.'
 self._name = name;    

 assert type(formula) == type(str()), 'oops not string.'
 self._formula = formula; 

 assert type(phase) == type(str()), 'oops not string.'
 self._phase = phase;   

 assert type(atoms) == type(list()), 'oops not list.'
 self._atoms = atoms;   

 self._flag = flag  # flag can be any type

 self._molarMass = 0.0
 self._molarHeatPwr = 0.0
 self._molarGammaPwr = 0.0
 self._molarRadioactivity = 0.0

 self._molarMassUnit = 'g/mole'

 self._molarHeatPwrUnit = 'W/mole'
 self._molarGammaPwrUnit = 'W/mole'
 self._molarRadioactivityUnit = 'Ci/mole'

 self._molarCCUnit = 'mole/L'
 self._massCCUnit  = 'g/L'

 self._nAtoms        = 0
 self._nNuclideTypes = 0
 nuclides = dict()
 if len(self._atoms) > 0:
   nAtoms = 0
   summ = 0.0
   for entry in self._atoms:
     assert type(entry) == type(str()), 'oops'
     # format example:  3.2*O-18, or 3*O or O or O-16
     tmp = entry.split('*')
     multiple  = 1.0
     # single nuclide    
     if len(tmp) == 1: 
        nuclide = tmp[0]
     # multiple nuclide
     elif len(tmp) == 2: 
        multiple = float(tmp[0])
        nuclide = tmp[1]
     else:
        assert False

     nuclides[ nuclide ] = multiple
     nAtoms += multiple

     try: 
       tmp = nuclide.split('-')
       if len(tmp) == 1:
          element = ELEMENTS[tmp[0]]
          molarMass = element.exactmass # from isotopic composition
       elif len(tmp) == 2:
          element = ELEMENTS[tmp[0]].isotopes[int(tmp[1].strip('m'))]
          molarMass = element.mass
#          print( element, molarMass )
       else:
          assert False
     except KeyError:
       summ += multiple * 0.0
     else:
       summ += multiple * molarMass    

   self._molarMass = summ
#   print( summ )
   self._nAtoms    = nAtoms
   self._nNuclideTypes = len(nuclides)

 if self._molarMass == 0.0:
   self._molarCC = 0.0
   self._massCC  = 0.0
   return

 assert type(molarCC) == type(float()), 'oops not a float.'
 assert molarCC >= 0.0, 'oops negative value.'
 self._molarCC = molarCC
 self._massCC  = molarCC * self._molarMass

 assert type(massCC) == type(float()), 'oops not a float.'
 assert massCC >= 0.0, 'oops negative value.'
 if self._massCC == 0.0: 
    self._massCC  = massCC 
    self._molarCC = massCC / self._molarMass

 return

#*******************************************************************************
