# 1.
import math

import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl
import matplotlib.pyplot as plt

class FuzzyController(object):
    def __init__(self):
        self.max_angle = 25.0 / 180 * math.pi
        inp_discr = 1.0 / 180 * math.pi
        inp_mean = 20.0 / 180 * math.pi
        inp_sigma = 20.0 / 180 * math.pi

        inp_values = np.linspace(-self.max_angle, 
            self.max_angle, int(2 * self.max_angle / inp_discr) + 1)
        input = ctrl.Antecedent(inp_values, 'input')
        input['low'] = fuzz.gaussmf(input.universe, -inp_mean, inp_sigma)
        input['high'] = fuzz.gaussmf(input.universe, inp_mean, inp_sigma)

        self.max_output = 1
        output_discr = 1
        outp_mean = 1
        outp_hbreadth = 0.8

        outp_values = np.linspace(-self.max_output, self.max_output, int(2 * self.max_output / output_discr) + 1)
        output = ctrl.Consequent(outp_values, 'output')
#         output['too_low'] = fuzz.trimf(output.universe, [-outp_mean - outp_hbreadth, -outp_mean, -outp_mean + outp_hbreadth])
#         output['too_high'] = fuzz.trimf(output.universe, [outp_mean - outp_hbreadth, outp_mean, outp_mean + outp_hbreadth])
        output['low'] = fuzz.trimf(output.universe, [-outp_mean - outp_hbreadth, -outp_mean, -outp_mean + outp_hbreadth])
        output['high'] = fuzz.trimf(output.universe, [outp_mean - outp_hbreadth, outp_mean, outp_mean + outp_hbreadth])

        rule1 = ctrl.Rule(input['low'], output['high'])
        rule2 = ctrl.Rule(input['high'], output['low'])

        control_system =  ctrl.ControlSystem([rule1, rule2])
        self.simulation = ctrl.ControlSystemSimulation(control_system)

    def calc(self, inp_value):
        self.simulation.input['input'] = inp_value
        self.simulation.compute()
        return self.simulation.output['output']
    
    def plot(self, num_points = 100):
        inp = np.linspace(-1.5*self.max_angle, 1.5*self.max_angle, num_points)
        outp = np.zeros(num_points)
        for i in range(num_points):
            outp[i] = self.calc(inp[i])
        plt.plot(inp, outp)
        plt.show()
        
