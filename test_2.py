from Inter_body import Inter
import numpy as np
import random
from scipy.optimize import minimize
import matplotlib.pyplot as plt


class Optimization:

    def __init__(self):
        self.d = 2
        self.px = 60
        self.py = 80
        self.pz = 50
        self.d_ban = 10

        self.goal = np.array([])
        self.walls = {}
        self.bans = {}
        self.bodies_test = {}
        self.cen_mass = {}
        self.list_bodies = {}
        self.history_args = {}
        self.list_bodies_r = {}
        self.verts = {}
        m = 3
        self.num_iter = 0

        self.list_bodies['module_1'] = m * np.array([-2, 4, -6, 2, -2, 2, 100])
        self.list_bodies['module_2'] = m * np.array([-2, 2, -4, 4, -2, 2, 150])
        self.list_bodies['module_3'] = m * np.array([-4, 4, -1, 2, -4, 4, 200])
        self.list_bodies['module_4'] = m * np.array([-1, 1, -4, 4, -4, 4, 100])
        self.list_bodies['module_5'] = m * np.array([-1, 4, -2, 2, -3, 3, 300])
        self.list_bodies['module_6'] = m * np.array([-2, 2, -2, 4, -4, 4, 50])

        for name in self.list_bodies:
            # print(np.delete(list_bodies[name], [6]).reshape((3, 2)))
            self.creation_workspace(name, np.delete(self.list_bodies[name], [6]).reshape((3, 2)))

    '''for name in list_bodies_r:
        verts[name] = np.array([[[list_bodies_r[name][0, 0], list_bodies_r[name][1, 0], list_bodies_r[name][2, 0]],
                        [list_bodies_r[name][0, 0], list_bodies_r[name][1, 1], list_bodies_r[name][2, 0]],
                        [list_bodies_r[name][0, 1], list_bodies_r[name][1, 1], list_bodies_r[name][2, 0]],
                        [list_bodies_r[name][0, 1], list_bodies_r[name][1, 0], list_bodies_r[name][2, 0]]],
                       [[list_bodies_r[name][0, 0], list_bodies_r[name][1, 0], list_bodies_r[name][2, 1]],
                        [list_bodies_r[name][0, 0], list_bodies_r[name][1, 1], list_bodies_r[name][2, 1]],
                        [list_bodies_r[name][0, 1], list_bodies_r[name][1, 1], list_bodies_r[name][2, 1]],
                        [list_bodies_r[name][0, 1], list_bodies_r[name][1, 0], list_bodies_r[name][2, 1]]],
                       [[list_bodies_r[name][0, 0], list_bodies_r[name][1, 0], list_bodies_r[name][2, 0]],
                        [list_bodies_r[name][0, 0], list_bodies_r[name][1, 0], list_bodies_r[name][2, 1]],
                        [list_bodies_r[name][0, 1], list_bodies_r[name][1, 0], list_bodies_r[name][2, 1]],
                        [list_bodies_r[name][0, 1], list_bodies_r[name][1, 0], list_bodies_r[name][2, 0]]],
                       [[list_bodies_r[name][0, 0], list_bodies_r[name][1, 1], list_bodies_r[name][2, 0]],
                        [list_bodies_r[name][0, 0], list_bodies_r[name][1, 1], list_bodies_r[name][2, 1]],
                        [list_bodies_r[name][0, 1], list_bodies_r[name][1, 1], list_bodies_r[name][2, 1]],
                        [list_bodies_r[name][0, 1], list_bodies_r[name][1, 1], list_bodies_r[name][2, 0]]],
                       [[list_bodies_r[name][0, 0], list_bodies_r[name][1, 0], list_bodies_r[name][2, 0]],
                        [list_bodies_r[name][0, 0], list_bodies_r[name][1, 1], list_bodies_r[name][2, 0]],
                        [list_bodies_r[name][0, 0], list_bodies_r[name][1, 1], list_bodies_r[name][2, 1]],
                        [list_bodies_r[name][0, 0], list_bodies_r[name][1, 0], list_bodies_r[name][2, 1]]],
                       [[list_bodies_r[name][0, 1], list_bodies_r[name][1, 0], list_bodies_r[name][2, 0]],
                        [list_bodies_r[name][0, 1], list_bodies_r[name][1, 1], list_bodies_r[name][2, 0]],
                        [list_bodies_r[name][0, 1], list_bodies_r[name][1, 1], list_bodies_r[name][2, 1]],
                        [list_bodies_r[name][0, 1], list_bodies_r[name][1, 0], list_bodies_r[name][2, 1]]]])'''

    def creation_workspace(self, name, Shape_body):
        body = [[0, 0, 0]]
        for i in range(int(Shape_body[0, 0]), int(Shape_body[0, 1])):
            for j in range(int(Shape_body[1, 0]), int(Shape_body[1, 1])):
                for k in range(int(Shape_body[2, 0]), int(Shape_body[2, 1])):
                    body = np.append(body, [[i, j, k]], axis=0)
                    # print(i, j, k)

        self.bodies_test[name] = body

    def walls_function(self):
        self.walls['wall_1'] = np.array([[-self.px / 2 - self.d / 2, -self.px / 2 + self.d / 2],
                                         [-self.py / 2 + self.d / 2, self.py / 2 - self.d / 2],
                                         [-self.pz / 2, self.pz / 2]])
        self.walls['wall_2'] = np.array([[self.px / 2 - self.d / 2, self.px / 2 + self.d / 2],
                                         [-self.py / 2 + self.d / 2, self.py / 2 - self.d / 2],
                                         [-self.pz / 2, self.pz / 2]])
        self.walls['wall_3'] = np.array([[-self.px / 2 - self.d / 2, self.px / 2 + self.d / 2],
                                         [self.py / 2 - self.d / 2, self.py / 2 + self.d / 2],
                                         [-self.pz / 2, self.pz / 2]])
        self.walls['wall_4'] = np.array([[-self.px / 2 - self.d / 2, self.px / 2 + self.d / 2],
                                         [-self.py / 2 - self.d / 2, -self.py / 2 + self.d / 2],
                                         [-self.pz / 2, self.pz / 2]])

        for name in self.walls:
            self.creation_workspace(name=name, Shape_body=self.walls[name])

        '''for name in walls:
            test.filling(name, [0, 0, 0, 0, 0, 0])'''

    def body_random(self):
        for name in self.list_bodies:
            pos_1 = random.uniform(max(self.px, self.py) / 2, -max(self.px, self.py) / 2)
            pos_2 = random.uniform(self.pz / 2, -self.pz / 2)
            pos_3 = random.uniform(0, 4)
            Number_wall = random.uniform(0, 9)

            self.change_position(name, Number_wall, pos_1, pos_2, pos_3)

    def restricted_area(self):

        self.bans['ban_1'] = np.array(
            [[-self.px / 2 - self.d / 2 - self.d_ban, -self.px / 2 - self.d / 2], [py / 2 + d / 2, py / 2 + d / 2 + d_ban], [-pz / 2, pz / 2]])
        bans['ban_2'] = np.array(
            [[-px / 2 - d / 2 - d_ban, -px / 2 - d / 2], [-py / 2 - d / 2 - d_ban, -py / 2 - d / 2], [-pz / 2, pz / 2]])
        bans['ban_3'] = np.array(
            [[px / 2 + d / 2, px / 2 + d / 2 + d_ban], [py / 2 + d / 2, py / 2 + d / 2 + d_ban], [-pz / 2, pz / 2]])
        bans['ban_4'] = np.array(
            [[px / 2 + d / 2, px / 2 + d / 2 + d_ban], [-py / 2 - d / 2 - d_ban, -py / 2 - d / 2], [-pz / 2, pz / 2]])

        for name in bans:
            creation_workspace(name=name, Shape_body=bans[name])

        '''for name in bans:
            test.filling(name, [0, 0, 0, 0, 0, 0])'''

    def change_position(name, number_wall, pos_1, pos_2, pos_3):
        history_args[name] = np.array([number_wall, pos_1, pos_2, pos_3])
        number_wall = int(number_wall % 7)

        pos_3 = int(pos_3 // 3) * 90
        if number_wall == 0:
            alpha = 90
            offset_y = py / 2 - d / 2 + list_bodies[name][4]
            beta = pos_3
            if pos_1 >= px / 2: offset_x = px / 2
            if pos_1 <= -px / 2:
                offset_x = -px / 2
            else:
                offset_x = pos_1

            if pos_2 >= pz / 2: offset_z = pz / 2
            if pos_2 <= -pz / 2:
                offset_z = -pz / 2
            else:
                offset_z = pos_2
            gamma = 0

        if number_wall == 1:
            alpha = -90
            offset_y = py / 2 + d / 2 - list_bodies[name][4]
            beta = pos_3
            if pos_1 >= px / 2: offset_x = px / 2
            if pos_1 <= -px / 2:
                offset_x = -px / 2
            else:
                offset_x = pos_1

            if pos_2 >= pz / 2: offset_z = pz / 2
            if pos_2 <= -pz / 2:
                offset_z = -pz / 2
            else:
                offset_z = pos_2
            gamma = 0

        if number_wall == 2:
            beta = -90
            offset_x = px / 2 - d / 2 + list_bodies[name][4]
            alpha = pos_3
            if pos_1 >= py / 2: offset_y = py / 2
            if pos_1 <= -py / 2:
                offset_y = -py / 2
            else:
                offset_y = pos_1

            if pos_2 >= pz / 2: offset_z = pz / 2
            if pos_2 <= -pz / 2:
                offset_z = -pz / 2
            else:
                offset_z = pos_2
            gamma = 0

        if number_wall == 3:
            beta = 90
            offset_x = px / 2 + d / 2 - list_bodies[name][4]
            alpha = pos_3
            if pos_1 >= py / 2: offset_y = py / 2
            if pos_1 <= -py / 2:
                offset_y = -py / 2
            else:
                offset_y = pos_1

            if pos_2 >= pz / 2: offset_z = pz / 2
            if pos_2 <= -pz / 2:
                offset_z = -pz / 2
            else:
                offset_z = pos_2
            gamma = 0

        if number_wall == 4:
            alpha = -90
            offset_y = -(py / 2 - d / 2 + list_bodies[name][4])
            beta = pos_3
            if pos_1 >= px / 2: offset_x = px / 2
            if pos_1 <= -px / 2:
                offset_x = -px / 2
            else:
                offset_x = pos_1

            if pos_2 >= pz / 2: offset_z = pz / 2
            if pos_2 <= -pz / 2:
                offset_z = -pz / 2
            else:
                offset_z = pos_2
            gamma = 0

        if number_wall == 5:
            alpha = 90
            offset_y = -(py / 2 + d / 2 - list_bodies[name][4])
            beta = pos_3
            if pos_1 >= px / 2: offset_x = px / 2
            if pos_1 <= -px / 2:
                offset_x = -px / 2
            else:
                offset_x = pos_1

            if pos_2 >= pz / 2: offset_z = pz / 2
            if pos_2 <= -pz / 2:
                offset_z = -pz / 2
            else:
                offset_z = pos_2
            gamma = 0

        if number_wall == 6:
            beta = 90
            offset_x = -(px / 2 - d / 2 + list_bodies[name][4])
            alpha = pos_3
            if pos_1 >= py / 2: offset_y = py / 2
            if pos_1 <= -py / 2:
                offset_y = -py / 2
            else:
                offset_y = pos_1

            if pos_2 >= pz / 2: offset_z = pz / 2
            if pos_2 <= -pz / 2:
                offset_z = -pz / 2
            else:
                offset_z = pos_2
            gamma = 0

        if number_wall == 7:
            beta = -90
            offset_x = -(px / 2 + d / 2 - list_bodies[name][4])
            alpha = pos_3
            if pos_1 >= py / 2: offset_y = py / 2
            if pos_1 <= -py / 2:
                offset_y = -py / 2
            else:
                offset_y = pos_1

            if pos_2 >= pz / 2: offset_z = pz / 2
            if pos_2 <= -pz / 2:
                offset_z = -pz / 2
            else:
                offset_z = pos_2
            gamma = 0

        # print(number_wall)
        cen_mass[name] = [offset_x, offset_y, offset_z]
        history_args[name] = [number_wall, pos_1, pos_2, pos_3]

        test.filling(name, [alpha, beta, gamma, offset_x, offset_y, offset_z])

    def centre_mass():
        m_x = 0
        m_y = 0
        m_z = 0
        sum_m = 0
        for name in cen_mass:
            m_x += cen_mass[name][0] * list_bodies[name][6]
            m_y += cen_mass[name][1] * list_bodies[name][6]
            m_z += cen_mass[name][2] * list_bodies[name][6]
            sum_m += list_bodies[name][6]

        c_x = m_x / sum_m
        c_y = m_y / sum_m
        c_z = m_z / sum_m

        result = (c_x ** 2 + c_y ** 2 + c_z) ** 0.5
        # num_iter += 1
        print(current_body, result)
        return result

    def goal_function():
        # call amount of inter
        inters = test.chek_intersection()
        dist = centre_mass()
        return (inters + 100 * dist)

    def function_for_opt(args):

        change_position(current_body, args[0], args[1], args[2], args[3])
        np.append(goal, goal_function())
        return (goal_function())

    current_body = ''

    def my_optimization():
        for i in range(3):
            for name in list_bodies:
                current_body = name
                x0 = history_args[current_body]
                res = minimize(function_for_opt, x0, method='powell',
                               options={'maxfev': 30})
                print(res.x)

    # def my_optimization():
    #     x0 = history_args[current_body].copy()
    #     x0 = np.array([0.7, 0.8, 1.9, 1.2])
    #     #print(x0.insert(0, 'module_1'))
    #     res = minimize(function_for_opt, x0, method='powell',
    #                            options={'xtol': 1e-6, 'disp': True})
    #     print(res.x)


walls_function()
restricted_area()
test = Inter(bodies_test, modules)
for name in walls:
    test.filling(name, [0, 0, 0, 0, 0, 0])
for name in bans:
    test.filling(name, [0, 0, 0, 0, 0, 0])

body_random()
# test.visual_workspace()
# print(goal_function())

# print(history_args)
my_optimization()

test.visual_workspace()
plt.plot(goal)
plt.ylabel('Goal')
plt.show()
print(goal_function())
