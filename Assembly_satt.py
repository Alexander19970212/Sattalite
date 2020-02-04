from OCC.Core.gp import gp_Pnt, gp_Pln
from OCC.Core.ChFi2d import ChFi2d_AnaFilletAlgo
from OCC.Core.BRepBuilderAPI import BRepBuilderAPI_MakeEdge
from OCC.Core.BRepPrimAPI import BRepPrimAPI_MakeBox
from OCC.Core.GProp import GProp_GProps
from OCC.Extend.DataExchange import read_step_file
from OCC.Core.BRepGProp import brepgprop_VolumeProperties
from OCC.Core.BRepOffsetAPI import BRepOffsetAPI_MakeOffsetShape
import os
from OCC.Core.BRepBndLib import brepbndlib_Add
from OCC.Core.Bnd import Bnd_Box
from OCC.Core.gp import gp_Pnt, gp_Trsf, gp_Vec, gp_Quaternion, gp_Mat
from OCC.Core.TopLoc import TopLoc_Location
from OCC.Core.BRepAlgoAPI import BRepAlgoAPI_Fuse, BRepAlgoAPI_Common, BRepAlgoAPI_Section, BRepAlgoAPI_Cut

from OCC.Extend.ShapeFactory import make_wire

from OCC.Display.SimpleGui import init_display
from OCC.Extend.DataExchange import read_step_file_with_names_colors
from OCC.Core.Quantity import Quantity_Color, Quantity_TOC_RGB

# filename = 'part_of_sattelate/pribore/DAV_WS16.STEP'
# #filename = '../assets/models/Personal_Computer.stp'
# #filename = '../assets/models/KR600_R2830-4.stp'
# #filename = '../assets/models/mod-mpu9150.step'
# shapes_labels_colors = read_step_file_with_names_colors(filename)
#
display, start_display, add_menu, add_function_to_menu = init_display()
#
# for shpt_lbl_color in shapes_labels_colors:
#     label, c = shapes_labels_colors[shpt_lbl_color]
#     display.DisplayColoredShape(shpt_lbl_color, color=Quantity_Color(c.Red(),
#     	                                                             c.Green(),
#     	                                                             c.Blue(),
#     	                                                             Quantity_TOC_RGB))

shp = read_step_file(os.path.join('part_of_sattelate', 'pribore', 'DAV_WS16.STEP'))
#BRepOffsetAPI_MakeOffsetShape(shp, 10, 0.1)

#kode to rotation
trsf = gp_Trsf()
# vX = gp_Vec(12, 0, 0)
# vY = gp_Vec(0, 12, 0)
Mat = gp_Mat(0.5, (0.75**0.5), 0,
             -(0.75**2), 0.5, 0,
             0, 0, 1)

trsf.SetRotation(gp_Quaternion(Mat))
shp.Move(TopLoc_Location(trsf))
def measure(shape):
    bbox = Bnd_Box()
    #bbox.SetGap(tol)
    #bbox.SetShape(shape)

    brepbndlib_Add(shape, bbox)

    xmin, ymin, zmin, xmax, ymax, zmax = bbox.Get()
    my_box = BRepPrimAPI_MakeBox(gp_Pnt(xmin, ymin, zmin), gp_Pnt(xmax, ymax, zmax)).Shape()

    #display.SetBackgroundImage('nevers-pont-de-loire.jpg', stretch=True)
    display.DisplayShape(my_box, color='GREEN', transparency=0.9)
    print(zmin, zmax, 'zzzzzzzzzzzzz')

def glue_solids(event=None):
    display.EraseAll()
    display.Context.RemoveAll(True)
    # Without common edges
    S1 = read_step_file(os.path.join('part_of_sattelate', 'pribore', 'DAV_WS16.STEP'))
    display.DisplayShape(S1, color='BLUE', transparency=0.9)
    measure(S1)

    # the face to glue
    S2 = read_step_file(os.path.join('part_of_sattelate', 'pribore', 'Camara_WS16.STEP'))

    trsf = gp_Trsf()

    trsf.SetTranslation(gp_Vec(750, 0, 0))
    S2.Move(TopLoc_Location(trsf))

    fuse_shp = BRepAlgoAPI_Fuse(S1, S2).Shape()

    props = GProp_GProps()
    brepgprop_VolumeProperties(fuse_shp, props)
    # Get inertia properties
    mass = props.Mass()
    cog = props.CentreOfMass()
    matrix_of_inertia = props.MatrixOfInertia()
    # Display inertia properties
    print("Cube mass = %s" % mass)
    cog_x, cog_y, cog_z = cog.Coord()
    print("Center of mass: x = %f;y = %f;z = %f;" % (cog_x, cog_y, cog_z))


    display.DisplayShape(fuse_shp)
    #pstring = 'x: % \n y: % \n z: %' % (cog_x, cog_y, cog_z)
    pnt = gp_Pnt(cog_x, cog_y, cog_z)
    # display points
    display.DisplayShape(pnt, update=True)
    pnt = gp_Pnt(0, 0, 0)
    # display points
    display.DisplayShape(pnt, update=True)
    #display.DisplayMessage(pnt, pstring)
    display.FitAll()
    #S2 += S1

    #display.DisplayShape(S2, color='RED', transparency=0.9)


#kode to move
#trsf = gp_Trsf()
'''
trsf.SetTranslation(gp_Vec(750, 0, 0))
shp.Move(TopLoc_Location(trsf))

display.EraseAll()
display.DisplayShape(shp, update=True)
'''

'''
props = GProp_GProps()
brepgprop_VolumeProperties(shp, props)
# Get inertia properties
mass = props.Mass()
cog = props.CentreOfMass()
matrix_of_inertia = props.MatrixOfInertia()
# Display inertia properties
print("Cube mass = %s" % mass)
cog_x, cog_y, cog_z = cog.Coord()
print("Center of mass: x = %f;y = %f;z = %f;" % (cog_x, cog_y, cog_z))
'''
glue_solids()
start_display()