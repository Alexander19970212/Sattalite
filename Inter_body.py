import numpy as  np
import scipy
from scipy.spatial.transform import Rotation as R
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection, Line3DCollection
from mpl_toolkits.mplot3d import Axes3D


class Inter:

    def __init__(self, bodies, names_modules, cernals):

        # self.workspace = np.zeros(workspace)
        self.bodies = bodies
        self.modules = names_modules
        self.bodies_new = {}
        self.cernals = cernals

    def append_body(self, name_body, body):
        self.bodies[name_body] = body

    def filling(self, name_body, coord_centres):
        '''

        :param name_body:
        :param coord_centres: 0 - угол поворота x (градусы)
        1 - угол поворота y (градусы)
        2 - угол поворота z (градусы)
        3 - смещенмие по x
        4 - смещенмие по y
        5 - смещенмие по z
        :return:
        '''
        body = self.bodies[name_body]
        # print(body)

        r = R.from_euler('xyz', [coord_centres[0], coord_centres[1], coord_centres[2]], degrees=True)
        Rot = r.as_dcm()
        # print(Rot)

        body_new = np.dot(body, Rot)
        body_new += [coord_centres[3], coord_centres[4], coord_centres[5]]
        self.bodies_new[name_body] = np.round(body_new)

        '''fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')
        ax.scatter(body_new[:, 0], body_new[:, 1], body_new[:, 2], c='r', marker='o')
        ax.scatter(body[:, 0], body[:, 1], body[:, 2], c='b', marker='^')

        ax.set_xlabel('X Label')
        ax.set_ylabel('Y Label')
        ax.set_zlabel('Z Label')
        plt.show()'''

    def chek_intersection(self):

        inter = 0
        for body_1 in self.bodies:
            for body_2 in self.bodies:
                if body_1 == body_2:
                    continue
                else:

                    # inter_bodies = np.intersect1d(self.bodies[body_1], self.bodies[body_2])
                    inter_bodies = np.array([x for x in set(tuple(x) for x in self.bodies_new[body_1]) & set(
                        tuple(x) for x in self.bodies_new[body_2])])
                    inter += inter_bodies.shape[0]

        return inter

    def visual_workspace(self):

        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')
        for name in self.bodies_new:
            if name in self.modules:
                ax.scatter(self.bodies_new[name][:, 0], self.bodies_new[name][:, 1], self.bodies_new[name][:, 2], c='r',
                           marker='o')
            else:
                ax.scatter(self.bodies_new[name][:, 0], self.bodies_new[name][:, 1], self.bodies_new[name][:, 2], c='b',
                           marker='o')
        # ax.scatter(body[:, 0], body[:, 1], body[:, 2], c='b', marker='^')

        ax.set_xlabel('X Label')
        ax.set_ylabel('Y Label')
        ax.set_zlabel('Z Label')
        plt.show()

    def visual_workspace_poly(self):

        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')
        print(self.cernals)
        for name in self.bodies_new:
            print(self.cernals[name])
            Z = self.bodies_new[name][self.cernals[name], :]
            verts = [[Z[0], Z[1], Z[3], Z[2]],
                     [Z[4], Z[5], Z[7], Z[6]],

                     [Z[0], Z[1], Z[5], Z[4]],
                     [Z[2], Z[3], Z[7], Z[6]],
                     [Z[1], Z[3], Z[7], Z[5]],
                     [Z[4], Z[6], Z[2], Z[0]]]

            # plot sides

            if name in self.modules:
            #if name == 'module_1':
                ax.scatter3D(Z[:, 0], Z[:, 1], Z[:, 2])
                ax.add_collection3d(Poly3DCollection(verts,
                                                     facecolors='red', linewidths=1, edgecolors='r', alpha=.25))
            else:
                ax.add_collection3d(Poly3DCollection(verts,
                                                     facecolors='green', linewidths=1, edgecolors='r', alpha=.25))

                pass
        # ax.scatter(body[:, 0], body[:, 1], body[:, 2], c='b', marker='^')

        ax.set_xlabel('X Label')
        ax.set_ylabel('Y Label')
        ax.set_zlabel('Z Label')
        plt.show()

    '''name = 'module_2'

    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.scatter(self.bodies_new[name][:, 0], self.bodies_new[name][:, 1], self.bodies_new[name][:, 2], c='r',
                       marker='o')

    ax.set_xlabel('X Label')
    ax.set_ylabel('Y Label')
    ax.set_zlabel('Z Label')
    plt.show()'''


if __name__ == '__main__':

    bodies_test = {}
    Shape_body = np.array([[-10, 10], [-20, 20], [-10, 10]])
    body = [[0, 0, 0]]
    for i in range(Shape_body[0, 0], Shape_body[0, 1]):
        for j in range(Shape_body[1, 0], Shape_body[1, 1]):
            for k in range(Shape_body[2, 0], Shape_body[2, 1]):
                body = np.append(body, [[i, j, k]], axis=0)

    bodies_test['prizm'] = body

    Shape_body = np.array([[-5, 2], [-10, 0], [-9, 10]])
    body = [[0, 0, 0]]
    for i in range(Shape_body[0, 0], Shape_body[0, 1]):
        for j in range(Shape_body[1, 0], Shape_body[1, 1]):
            for k in range(Shape_body[2, 0], Shape_body[2, 1]):
                body = np.append(body, [[i, j, k]], axis=0)

    bodies_test['prizm_2'] = body

    test = Inter(bodies_test)
    test.filling('prizm', [30, 50, 60, 15, 15, 15])
    test.filling('prizm_2', [0, 0, 0, 0, 0, 0])
    print(test.chek_intersection())
