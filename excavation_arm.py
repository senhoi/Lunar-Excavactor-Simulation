from math import *
from scipy.integrate import solve_ivp
import numpy as np
import matplotlib.pyplot as plt

class ExcArm(object):
    def __init__(self):
        self.m = 200        # Mass of excavation arm
        self.l = 6          # Length of excavation arm
        self.e = 0.5        # Distance between axis and CoM
        self.g = 9.81       # Gravity

        self.Tm_max = 10    # Maximum Torque of the main motor

        self.excavation_begin = False
        self.excavation_range = pi/3

    @property
    def inertia(self):
        return (1/12+self.e**2)*self.m*self.l**2

    def eval_rhs(self, t, x, w_t, w_m):
        theta = x[0]
        omega = x[1]

        Tx, Ty = w_t(t, x)
        Tm = w_m(t, x)

        dot_theta = omega
        dot_omega = ((self.m*self.g*self.e+Ty)*cos(theta)-Tx*sin(theta)+Tm)/((1/12+self.e**2)*self.m*self.l)

        return dot_theta, dot_omega

    def eval_input_excavation_force(self, t, x):
        theta = x[0]
        omega = x[1]
        return 0, 0

    def eval_input_motor(self, t, x):
        theta = x[0]
        omega = x[1]
        return self.Tm_max if omega >= 0 else -self.Tm_max

    def integrate(self):
        return solve_ivp(self.eval_rhs, [0, 300], [pi/2, 0], args=[self.eval_input_excavation_force, self.eval_input_motor], dense_output=True)

if __name__ == '__main__':
    arm = ExcArm()
    sol = arm.integrate()
    t = np.linspace(0, 300, 3000)
    z = sol.sol(t)
    plt.plot(t, z.T[:,[1]])
    plt.xlabel('t')
    plt.legend(['theta', 'omega'], shadow=True)
    plt.title('Excavation System')
    plt.show()


