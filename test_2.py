from Inters_body import Inter
import numpy as np

d = 3
px = 60
py = 80
pz = 50

bodies_test = {}
body_1 = np.array([[-10, 10], [-20, 20], [-10, 10]])


def creation_workspace(name, Shape_body):
    body = [[0, 0, 0]]
    for i in range(Shape_body[0, 0], Shape_body[0, 1]):
        for j in range(Shape_body[1, 0], Shape_body[1, 1]):
            for k in range(Shape_body[2, 0], Shape_body[2, 1]):
                body = np.append(body, [[i, j, k]], axis=0)

    bodies_test[name] = body


def walls():


def restricted_area():


def change_position(name, number_wall, pos_1, pos_2, pos_3):
    number_wall = int(number_wall % 7)
    pos_3 = int(pos_3 % 3) * 90
    if number_wall == 0:
        alpha = 90
        offset_y = py / 2 - d / 2 + name[2, 0]
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
        offset_y = py / 2 + d / 2 - name[2, 0]
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
        offset_x = px / 2 - d / 2 + name[2, 0]
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
        offset_x = px / 2 + d / 2 - name[2, 0]
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
        offset_y = -(py / 2 - d / 2 + name[2, 0])
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
        offset_y = -(py / 2 + d / 2 - name[2, 0])
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
        offset_x = -(px / 2 - d / 2 + name[2, 0])
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
        offset_x = -(px / 2 + d / 2 - name[2, 0])
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

    test.filling(name, [alpha, beta, gamma, offset_x, offset_y, offset_z])


test = Inter(bodies_test)