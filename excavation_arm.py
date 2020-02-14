from math import *
from scipy.integrate import solve_ivp
import numpy as np
import matplotlib.pyplot as plt
from excavation_force import ExcForce


class ExcArm(object):
    def __init__(self):
        self.m = 200  # Mass of excavation arm
        self.l = 6  # Length of excavation arm
        self.e = 0.5  # Distance between axis and CoM
        self.g = 9.81  # Gravity

        self.Tm_max = 10  # Maximum Torque of the main motor

        self.excavation_begin = False
        self.excavation_range = pi / 4

    @property
    def inertia(self):
        return (1 / 12 + self.e ** 2) * self.m * self.l ** 2

    def eval_rhs(self, t, x, w_t, w_m):
        theta = x[0]
        omega = x[1]

        Tx, Ty = w_t(t, x)
        Tm = w_m(t, x)

        dot_theta = omega
        dot_omega = (-(self.m * self.g * self.e + Ty) * sin(theta) - Tx * cos(theta) + Tm) / (
                (1 / 12 + self.e ** 2) * self.m * self.l)

        return dot_theta, dot_omega

    def eval_input_excavation_force(self, t, x):
        theta = x[0]
        omega = x[1]

        # if -self.excavation_range < abs(theta % pi) < self.excavation_range and abs(theta) > 2 * pi:
        #     model = ExcForce('config/param_moon.json', '#1')
        #     tt, tx, ty = model.SwickPerumpralModel()
        #     return tx, ty
        # else:
        #     return 0, 0
        return 0, 0

    def eval_input_motor(self, t, x):
        theta = x[0]
        omega = x[1]
        return self.Tm_max if omega >= 0 else -self.Tm_max

    def integrate(self):
        return solve_ivp(self.eval_rhs, [0, 300], [0, 0], method='DOP853',
                         args=[self.eval_input_excavation_force, self.eval_input_motor], dense_output=True)

    def eval_output(self, t, xdot, x):
        return self.eval_input_excavation_force(t, x)

    def calc_output(self, ts, xs):
        res = np.zeros((2, 3000))
        for i in range(ts.size):
            t = ts[i]
            x = xs[:, i]
            xdot = self.eval_rhs(t, x, self.eval_input_excavation_force, self.eval_input_motor)
            res[:, i] = self.eval_output(t, xdot, x)
        return res


if __name__ == '__main__':
    arm = ExcArm()
    sol = arm.integrate()
    t = np.linspace(0, 300, 3000)
    z = sol.sol(t)
    res = arm.calc_output(t, z)
    plt.plot(t, z.T)
    # plt.plot(t, res.T)

    plt.xlabel('t')
    plt.legend(['theta', 'omega'], shadow=True)
    plt.title('Excavation System')
    plt.show()
