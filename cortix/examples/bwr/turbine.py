#!/usr/bin/env python
# -*- coding: utf-8 -*-
# This file is part of the Cortix toolkit environment.
# https://cortix.org
"""
Cortix Example Module
"""

import logging
from copy import deepcopy

import scipy.constants as unit
import numpy as math

import iapws.iapws97 as steam_table

from cortix import Module
from cortix.support.phase_new import PhaseNew as Phase
from cortix import Quantity

class Turbine(Module):
    """Boiling water single-point reactor.

    Notes
    -----
    These are the `port` names available in this module to connect to respective
    modules: `turbine`, and `pump`.
    See instance attribute `port_names_expected`.

    """

    def __init__(self, params):
        """Constructor.

        Parameters
        ----------
        params: dict
            All parameters for the module in the form of a dictionary.

        """

        super().__init__()

        self.params = deepcopy(params)
        self.params['entropy'] = 4.5 # Kj/Kg-K

        self.port_names_expected = ['inflow', 'outflow-1', 'outflow-2']

        self.initial_time = 0.0 * unit.day
        self.end_time = 4 * unit.hour

        self.time_step = 10.0
        self.show_time = (False, 10.0)

        self.log = logging.getLogger('cortix')

        # Inflow phase history
        quantities = list()

        temp = Quantity(name='temp', formal_name='T_in', unit='k', value=params['coolant-temp'],
                        info='Turbine Steam Inflow Temperature', latex_name=r'$T_i$')

        quantities.append(temp)

        self.inflow_phase = Phase(self.initial_time, time_unit='s',
                                  quantities=quantities)

        # Outflow phase history
        quantities = list()

        temp = Quantity(name='temp', formal_name='T_o', unit='k', value=params['turbine-outflow-temp'],
                        info='Turbine Steam Outflow Temperature', latex_name=r'$T_o$')

        quantities.append(temp)

        press = Quantity(name='pressure', formal_name='P_t', unit='Pa',
                         value=params['runoff-pressure'],
                         info='Turbine Steam Outflow Pressure', latex_name=r'$P_t$')

        quantities.append(press)

        x = Quantity(name='quality', formal_name='chi_t', unit='%', value=params['turbine-chi'],
                     info='Turbine Steam Outflow Quality', latex_name=r'$\chi_t$')

        quantities.append(x)

        work = Quantity(name='power', formal_name='P_t', unit='W', value=params['turbine-work'],
                        info='Turbine Power', latex_name=r'$W_t$')

        quantities.append(work)

        self.outflow_phase = Phase(self.initial_time, time_unit='s',
                                   quantities=quantities)

        self.temp = 0.0
        self.chi = 0.0

    def run(self, *args):

        time = self.initial_time

        while time < self.end_time + self.time_step:

            if self.show_time[0] and abs(time%self.show_time[1]-0.0) <= 1.e-1:
                msg = 'time = '+str(round(time/unit.minute, 1))
                self.log.info(msg)

            # Communicate information
            #------------------------
            self.__call_ports(time)

            # Evolve one time step
            #---------------------

            time = self.__step(time)

    def __call_ports(self, time):

        # Interactions in the steam-outflow-1 port
        #-----------------------------------------
        # one way "to" outflow-1

        # to
        if self.get_port('outflow-1').connected_port:

            message_time = self.recv('outflow-1')

            outflow_state = dict()

            steam_temp = self.outflow_phase.get_value('temp', time)
            steam_quality = self.outflow_phase.get_value('quality', time)
            steam_press = self.outflow_phase.get_value('pressure', time)

            outflow_state['temp'] = steam_temp
            outflow_state['quality'] = steam_quality
            outflow_state['press'] = steam_press

            self.send((message_time, outflow_state), 'outflow-1')

        # Interactions in the steam-outflow-2 port
        #-----------------------------------------
        # one way "to" outflow-2

        # to
        if self.get_port('outflow-2').connected_port:

            message_time = self.recv('outflow-2')

            outflow_state = dict()

            steam_temp = self.outflow_phase.get_value('temp', time)
            steam_quality = self.outflow_phase.get_value('quality', time)
            steam_press = self.outflow_phase.get_value('pressure', time)

            outflow_state['temp'] = steam_temp
            outflow_state['quality'] = steam_quality
            outflow_state['press'] = steam_press

            self.send((message_time, outflow_state), 'outflow-2')

        # Interactions in the steam-inflow port
        #----------------------------------------
        # one way "from" inflow

        # from
        if self.get_port('inflow').connected_port:

            self.send(time, 'inflow')

            (check_time, inflow_state) = self.recv('inflow')
            assert abs(check_time-time) <= 1e-6

            self.temp = inflow_state['temp']
            self.chi = inflow_state['quality']

    def __step(self, time=0.0):
        r"""
        Advance the state of the turbine.

        Parameters
        ----------
        time: float
            Time in SI unit.

        Returns
        -------
        None
        """
        output = self.__turbine(time, self.temp, self.chi, self.params)

        tmp = self.outflow_phase.get_row(time)

        time += self.time_step

        self.outflow_phase.add_row(time, tmp)

        t_runoff = output[0]

        x_runoff = output[2]
        #if x_runoff < 0 and x_runoff != -1:
            #x_runoff = 0

        w_turbine = output[1]

        self.outflow_phase.set_value('power', w_turbine, time)
        self.outflow_phase.set_value('quality', x_runoff, time)
        self.outflow_phase.set_value('temp', t_runoff, time)

        return time

    def __turbine(self, time, temp_in, steam_quality, params):
        # Expand the entering steam from whatever temperature and pressure it enters
        # at to 0.035 kpa, with 80% efficiency.
        # Pressure of steam when it enters the turbine equals the current reactor
        # operating pressure
        #if self.params['high_pressure_turbine']:
            #print(time, ' and temp is', temp_in)
        if self.params['high_pressure_turbine']:
            # vfda: access of a protected member?
            # austin: I could not find a public method in the IAPWS class that does what the
            # private methods do. Therefore, I have to use the protected members.
            p_in = steam_table._PSat_T(temp_in)
        else:
            p_in = self.params['turbine_inlet_pressure']

        p_out = self.params['turbine_outlet_pressure']

        if temp_in <= 273.15: # if temp is below this the turbine will not work
            t_runoff = temp_in
            w_real = 0
            steam_quality = 0
            return (t_runoff, w_real, steam_quality)
        if temp_in < 373.15 and self.params['high_pressure_turbine']:
            #vfda: access of a protected member?
            t_runoff = temp_in
            w_real = 0
            steam_quality = -3
            return (t_runoff, w_real, steam_quality)
        if temp_in < steam_table._TSat_P(0.5) and self.params['high_pressure_turbine'] == False:
            t_runoff = temp_in
            w_real = 0
            return(t_runoff, w_real, steam_quality)

        #properties of the inlet steam

        # vfda: access of a protected member?
        inlet_parameters = steam_table._Region4(p_in, steam_quality)
        inlet_entropy = inlet_parameters['s']
        inlet_enthalpy = inlet_parameters['h']

        if self.params['high_pressure_turbine']:
            inlet_parameters = steam_table.IAPWS97(P=p_in, x=0)
            #inlet_entropy = self.params['entropy']
            #inlet_enthalpy = inlet_parameters.h
            
            #testing the entropy modell
            base_temp = 373.15 # K
            base_pressure = 0.101 # mPa
            base_params = steam_table.IAPWS97(P=base_pressure, x=0) # bubl pt 373.15 K
            base_entropy = base_params.s # Kj/Kg-K
            base_cp = base_params.Liquid.cp # Kj/Kg-K
            inlet_cp = inlet_parameters.Liquid.cp # Kj/Kg-K
            average_cp = (base_cp + inlet_cp)/2

            delta_s =  average_cp * math.log(temp_in/base_temp) - (unit.R/1000) * math.log(p_in/base_pressure)

            inlet_entropy = (delta_s + base_entropy) * 1.25 # fudge factor
            bubl_entropy = inlet_parameters.Liquid.s
            bubl_enthalpy = inlet_parameters.Liquid.h

            inlet_parameters = steam_table.IAPWS97(P=p_in, x=1)
            dew_entropy = inlet_parameters.Vapor.s
            dew_enthalpy = inlet_parameters.Vapor.h
            quality = (inlet_entropy - bubl_entropy)/(dew_entropy - bubl_entropy)
            inlet_enthalpy = quality * dew_enthalpy + (1 - quality) * bubl_enthalpy

        #bubble and dewpoint properties at turbine outlet
        # vfda: access of a protected member?
        bubl = steam_table._Region4(p_out, 0)
        # vfda: access of a protected member?
        dew = steam_table._Region4(p_out, 1)
        bubl_entropy = bubl['s']
        dew_entropy = dew['s']
        bubl_enthalpy = bubl['h']
        dew_enthalpy = dew['h']

        #print(bubl_entropy, inlet_entropy, dew_entropy, self.params['high_pressure_turbine'])

        #if the ideal runoff is two-phase mixture:
        #if inlet_entropy < dew_entropy and inlet_entropy > bubl_entropy:
        if  bubl_entropy < inlet_entropy < dew_entropy:
            x_ideal = (inlet_entropy - bubl_entropy)/(dew_entropy - bubl_entropy)
            # vfda: access of a protected member?
            h_ideal = steam_table._Region4(p_out, x_ideal)['h']

        #if the ideal runoff is a superheated steam
        #elif inlet_entropy > dew_entropy:
            # vfda: access of a protected member?
            #t_ideal = steam_table._Backward2_T_Ps(p_out, inlet_entropy)
            # vfda: access of a protected member?
            #h_ideal = steam_table._Region2(t_ideal, p_out)['h']

        #calculate the real runoff enthalpy
        w_ideal = inlet_enthalpy - h_ideal #on a per mass basis
        #assert(w_ideal > 0)
        w_real = w_ideal * params['turbine efficiency']
        h_real = inlet_enthalpy - w_ideal
        assert h_real > 0
        if w_real < 0:
            w_real = 0

        # if the real runoff is a superheated steam
        if h_real > dew_enthalpy:
            # vfda: access of a protected member?
            t_runoff = steam_table._Backward2_T_Ph(p_out, h_real)
            x_runoff = -1 # superheated steam

        #if the real runoff is a subcooled liquid
        elif h_real < bubl_enthalpy:
            # vfda: access of a protected member?
            t_runoff = steam_table._Backward1_T_Ph(p_out, h_real)
            x_runoff = 2 # subcooled liquid

        #if the real runoff is a two-phase mixture
        else:
            # saturated vapor
            x_runoff = (h_real - bubl_enthalpy)/(dew_enthalpy - bubl_enthalpy)
            # vfda: access of a protected member?
            t_runoff = steam_table._TSat_P(p_out)

        w_real = w_real * params['steam flowrate'] * unit.kilo
        #print(self.params['high_pressure_turbine'], ' and time is ', time, ' and x is ', x_runoff)
        #w_real = heat_removed

        #if t_runoff < steam_table._TSat_P(0.5) and params['high_pressure_turbine'] == False:
            #t_runoff = temp_in
            #x_runoff = -5
            #w_real = 0
        return (t_runoff, w_real, x_runoff)
