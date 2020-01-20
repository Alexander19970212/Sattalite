import random

wall_1 = [-px/2-d/2, -px/2+d/2, -py/2+d/2, py/2-d/2, -pz/2, pz/2]
wall_1 = [px/2-d/2, px/2+d/2, -py/2+d/2, py/2-d/2, -pz/2, pz/2]
wall_1 = [-px/2-d/2, px/2+d/2, py/2-d/2, py/2+d/2, -pz/2, pz/2]
wall_1 = [-px/2-d/2, px/2+d/2, -py/2-d/2, -py/2+d/2, -pz/2, pz/2]

'''
получить список точек,
после создания экземпляра и заполнения списка тел класса (без стенок), добавить в список стенки 
пересчитать как новые тела с нулевыми смещениями
сразу добавлять список запрещенных зон по той же схеме
'''
#объявить новую величину - продолжительность запрещенной зоны
d_ban = 50
ban_1 = [-px/2-d/2-d_ban, -px-d/2, py/2+d/2, py/2+d/2+d_ban, -pz/2, pz/2]
ban_2 = [-px/2-d/2-d_ban, -px-d/2, -py/2-d/2-d_ban, -py/2-d/2, -pz/2, pz/2]
ban_3 = [px/2+d/2, px+d/2+d_ban, py/2+d/2, py/2+d/2+d_ban, -pz/2, pz/2]
ban_4 = [px/2+d/2, px+d/2, -py/2-d/2-d_ban, -py/2-d/2, -pz/2, pz/2]
'''
пересчитвть как новые тела с нулевыми смещениями
'''
# create dec of bodeis
list_bodies = {}
list_bodies['modul_1'] = [-10, 20, -30, 10, -10, 10, 100]
list_bodies['modul_2'] = [-10, 10, -20, 20, -10, 10, 150]
list_bodies['modul_3'] = [-20, 20, -5, 10, -20, 20, 200]
list_bodies['modul_4'] = [-5, 5, -20, 20, -20, 20, 100]
list_bodies['modul_5'] = [-6, 20, -10, 10, -15, 15, 300]
list_bodies['modul_6'] = [-9, 9, -10, 20, -20, 20, 50]

cen_mass = {}
#вызов фуекции перемещения со случайными числами
for name in list_bodies:
    pos_1 = random.uniform(max(px, py)/2, -max(px, py)/2)
    pos_2 = random.uniform(pz / 2, -pz / 2)
    pos_3 = random.uniform(-180, 180)

    function_1(name, pos_1, pos_2, pos_3)

# в функции_1 сделать заполнение цетров масс:
cen_mass[name] = [offset_x, offset_y, offset_z]
# в функции_1 запись входящих значений, чтобы историю
history_args[name] = [pos_1, pos_2, pos_3]

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
    inters = <function_class>
    dist = centre_mass()
    return (inters + 100*dist)


current_body = 'no_body'
#function for optimization
def function_for_optimization(pos_1, pos_2, pos_3):
    function_1(current_body, pos_1, pos_2, pos_3)
    return goal_function()

#optimization
from scipy.optimize import minimize
for i in range(3):
    for name in list_bodies:
        current_body = name
        x0 = history_args[current_body]
        res = minimize(function_for_optimization(), x0, method='nelder-mead',
            options={'xtol': 1e-8, 'disp': True})
        print(res.x)

print(goal_function())
#вызов функции визуализации


import numpy as np
from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits.mplot3d.art3d import Poly3DCollection, Line3DCollection
import matplotlib.pyplot as plt


fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

# list of sides' polygons of figure
verts = [[Z[0],Z[1],Z[2],Z[3]],
 [Z[4],Z[5],Z[6],Z[7]],
 [Z[0],Z[1],Z[5],Z[4]],
 [Z[2],Z[3],Z[7],Z[6]],
 [Z[1],Z[2],Z[6],Z[5]],
 [Z[4],Z[7],Z[3],Z[0]]]

# plot sides
ax.add_collection3d(Poly3DCollection(verts,
 facecolors='cyan', linewidths=1, edgecolors='r', alpha=.25))

ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')

plt.show()



