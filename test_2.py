from Inter_body import Inter
import numpy as np
import random

d = 2
px = 60
py = 80
pz = 50
d_ban = 10

walls = {}
bans = {}
bodies_test = {}
cen_mass = {}
list_bodies = {}
history_args = {}
list_bodies_r ={}
verts = {}
m = 5


list_bodies['module_1'] = [-2, 4, -6, 2, -2, 2, 100]
list_bodies['module_2'] = [-2, 2, -4, 4, -2, 2, 150]
list_bodies['module_3'] = [-4, 4, -1, 2, -4, 4, 200]
list_bodies['module_4'] = [-1, 1, -4, 4, -4, 4, 100]
list_bodies['module_5'] = [-1, 4, -2, 2, -3, 3, 300]
list_bodies['module_6'] = [-2, 2, -2, 4, -4, 4, 50]

list_bodies_r['module_1'] = m*np.array([[-10, 20], [-30, 10], [-10, 10]])
list_bodies_r['module_2'] = m*np.array([[-10, 10], [-20, 20], [-10, 10]])
list_bodies_r['module_3'] = m*np.array([[-20, 20], [-5, 10], [-20, 20]])
list_bodies_r['module_4'] = m*np.array([[-5, 5], [-20, 20], [-20, 20]])
list_bodies_r['module_5'] = m*np.array([[-6, 20], [-10, 10], [-15, 15]])
list_bodies_r['module_6'] = m*np.array([[-9, 9], [-10, 20], [-20, 20]])

modules = list_bodies_r.keys()

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


def creation_workspace(name, Shape_body):
    body = [[0, 0, 0]]
    for i in range(int(Shape_body[0, 0]), int(Shape_body[0, 1])):
        for j in range(int(Shape_body[1, 0]), int(Shape_body[1, 1])):
            for k in range(int(Shape_body[2, 0]), int(Shape_body[2, 1])):
                body = np.append(body, [[i, j, k]], axis=0)
                #print(i, j, k)

    bodies_test[name] = body

#creation_workspace('test', [-10,  20, -30,  10, -10,  10].reshape((3, 2)))
print(bodies_test)

for name in list_bodies:
    #print(np.delete(list_bodies[name], [6]).reshape((3, 2)))
    creation_workspace(name, np.delete(list_bodies[name], [6]).reshape((3, 2)))

print(bodies_test['module_4'])


def walls_function():
    walls['wall_1'] = np.array([[-px / 2 - d / 2, -px / 2 + d / 2], [-py / 2 + d / 2, py / 2 - d / 2], [-pz / 2, pz / 2]])
    walls['wall_2'] = np.array([[px / 2 - d / 2, px / 2 + d / 2], [-py / 2 + d / 2, py / 2 - d / 2], [-pz / 2, pz / 2]])
    walls['wall_3'] = np.array([[-px / 2 - d / 2, px / 2 + d / 2], [py / 2 - d / 2, py / 2 + d / 2], [-pz / 2, pz / 2]])
    walls['wall_4'] = np.array([[-px / 2 - d / 2, px / 2 + d / 2], [-py / 2 - d / 2, -py / 2 + d / 2], [-pz / 2, pz / 2]])

    for name in walls:
        creation_workspace(name=name, Shape_body=walls[name])

    '''for name in walls:
        test.filling(name, [0, 0, 0, 0, 0, 0])'''

def body_random():
    for name in list_bodies:
        pos_1 = random.uniform(max(px, py) / 2, -max(px, py) / 2)
        pos_2 = random.uniform(pz / 2, -pz / 2)
        pos_3 = random.uniform(0, 4)
        Number_wall = random.uniform(0, 9)

        change_position(name, Number_wall, pos_1, pos_2, pos_3)



def restricted_area():

    bans['ban_1'] = np.array([[-px / 2 - d / 2 - d_ban, -px/2 - d / 2], [py / 2 + d / 2, py / 2 + d / 2 + d_ban], [-pz / 2, pz / 2]])
    bans['ban_2'] = np.array([[-px / 2 - d / 2 - d_ban, -px/2 - d / 2], [-py / 2 - d / 2 - d_ban, -py / 2 - d / 2], [-pz / 2, pz / 2]])
    bans['ban_3'] = np.array([[px / 2 + d / 2, px/2 + d / 2 + d_ban], [py / 2 + d / 2, py / 2 + d / 2 + d_ban], [-pz / 2, pz / 2]])
    bans['ban_4'] = np.array([[px / 2 + d / 2, px/2 + d / 2 + d_ban], [-py / 2 - d / 2 - d_ban, -py / 2 - d / 2], [-pz / 2, pz / 2]])

    for name in bans:
        creation_workspace(name=name, Shape_body=bans[name])

    '''for name in bans:
        test.filling(name, [0, 0, 0, 0, 0, 0])'''


def change_position(name, number_wall, pos_1, pos_2, pos_3):
    number_wall = int(number_wall % 7)
    pos_3 = int(pos_3 // 3) * 90
    if number_wall == 0:
        alpha = 90
        offset_y = py / 2 - d / 2 + list_bodies_r[name][2, 0]
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
        offset_y = py / 2 + d / 2 - list_bodies_r[name][2, 0]
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
        offset_x = px / 2 - d / 2 + list_bodies_r[name][2, 0]
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
        offset_x = px / 2 + d / 2 - list_bodies_r[name][2, 0]
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
        offset_y = -(py / 2 - d / 2 + list_bodies_r[name][2, 0])
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
        offset_y = -(py / 2 + d / 2 - list_bodies_r[name][2, 0])
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
        offset_x = -(px / 2 - d / 2 + list_bodies_r[name][2, 0])
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
        offset_x = -(px / 2 + d / 2 - list_bodies_r[name][2, 0])
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

    print(alpha, beta, gamma)
    cen_mass[name] = [offset_x, offset_y, offset_z]
    history_args[name] = [number_wall, pos_1, pos_2, pos_3]

    test.filling(name, [alpha, beta, gamma, offset_x, offset_y, offset_z])

def centre_mass():
    m_x = 0
    m_y = 0
    m_z = 0
    sum_m = 0
    for name in cen_mass:
        m_x += cen_mass[name][0]*list_bodies[name][6]
        m_y += cen_mass[name][1]*list_bodies[name][6]
        m_z += cen_mass[name][2]*list_bodies[name][6]
        sum_m += list_bodies[name][6]

    c_x = m_x/sum_m
    c_y = m_y/sum_m
    c_z = m_z/sum_m

    result = (c_x**2 + c_y**2 + c_z)**0.5
    return result

def goal_function():
    #call amount of inter
    inters = test.chek_intersection()
    dist = centre_mass()
    return (inters + 100*dist)


walls_function()
restricted_area()
test = Inter(bodies_test, modules)
for name in walls:
    test.filling(name, [0, 0, 0, 0, 0, 0])
for name in bans:
    test.filling(name, [0, 0, 0, 0, 0, 0])

body_random()
test.visual_workspace()
print(goal_function())