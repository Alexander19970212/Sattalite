from OCC.Core.gp import gp_Pnt, gp_Pln
from OCC.Core.ChFi2d import ChFi2d_AnaFilletAlgo
from OCC.Core.BRepBuilderAPI import BRepBuilderAPI_MakeEdge
from OCC.Core.BRepPrimAPI import BRepPrimAPI_MakeBox
from OCC.Core.GProp import GProp_GProps
from OCC.Core.BRepGProp import brepgprop_VolumeProperties

from OCC.Extend.ShapeFactory import make_wire

from OCC.Display.SimpleGui import init_display
display, start_display, add_menu, add_function_to_menu = init_display()


def cube_inertia_properties():
    """ Compute the inertia properties of a shape
    """
    # Create and display cube
    print("Creating a cubic box shape (50*50*50)")
    cube_shape = BRepPrimAPI_MakeBox(50., 50., 50.).Shape()
    ais_boxshp = display.DisplayShape(cube_shape, update=True)
    # Compute inertia properties
    props = GProp_GProps()
    brepgprop_VolumeProperties(cube_shape, props)
    # Get inertia properties
    mass = props.Mass()
    cog = props.CentreOfMass()
    matrix_of_inertia = props.MatrixOfInertia()
    # Display inertia properties
    print("Cube mass = %s" % mass)
    cog_x, cog_y, cog_z = cog.Coord()
    print("Center of mass: x = %f;y = %f;z = %f;" % (cog_x, cog_y, cog_z))

if __name__ == '__main__':
    cube_inertia_properties()

    start_display()