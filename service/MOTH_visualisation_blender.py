import bpy


from os import listdir
from os.path import isfile, join
import os
import numpy as np
def get_parameters(path):
        filenames = [f for f in listdir(path) if isfile(join(path, f))]
        fields=[]
        temps=[]
        for i,name in enumerate(filenames):
            h=float(name.split("H=")[1].split("_")[0])
            fields.append(h)
            t=float(name.split("T=")[1].split("_")[0])
            temps.append(t)
        fields=np.sort(np.unique(np.array(fields)))
        temps=np.sort(np.unique(np.array(temps)))
        lowest_T_name=compose_name(fields[0],temps[0])
        s,m,o=read_state(path+os.path.sep+lowest_T_name)
        global max_m
        max_m=np.max(m)
        number_of_layers=s.size
        return fields,temps,number_of_layers 
def compose_name(field_i,temp_i):
    name="H="+str(field_i)+"_T="+str(temp_i)+"_M(H)_profile.txt"
    return name
def read_state(path_to_file):
    data=np.loadtxt(path_to_file)
    space, magnitude, angle = data[:,0],data[:,1],data[:,2]
    return space,magnitude,angle

def select_specific(set_to_select):
    for o in bpy.data.objects:
            # Check for given object names
            if o.name in set_to_select:
                o.select_set(True)
    return 0

def create_arrows(number):
    arrow_length=5
    head_length=1
    names=[]
    for d in range(number):
        #create arrow body
        bpy.ops.mesh.primitive_cylinder_add(radius=0.075,
                                            depth=arrow_length,
                                            enter_editmode=False,
                                            align='WORLD',
                                            location=(0, 0, arrow_length/2),
                                            scale=(1, 1, 1))
        #get its name
        body_name=bpy.context.object.name
        #create arrow head
        bpy.ops.mesh.primitive_cone_add(radius1=0.15,
                                        radius2=0,
                                        depth=head_length,
                                        enter_editmode=False,
                                        align='WORLD',
                                        location=(0, 0, arrow_length+head_length/2),
                                        scale=(1, 1, 1))
        #get its name
        head_name=bpy.context.object.name
        #deselect everething
        bpy.ops.object.select_all(action='DESELECT')
        
        select_specific([body_name,head_name])
        #join head and body
        bpy.ops.object.join()
        bpy.ops.object.origin_set(type='ORIGIN_CURSOR', center='MEDIAN')
        bpy.context.object.location[0] = d/2
        names.append(bpy.context.object.name)
    arrow_names=names
    return arrow_names

def create_description(h_value,t_value):
    h_text="H="+str(h_value)
    t_text="T="+str(t_value)
    string=h_text+os.linesep+t_text
    font_curve = bpy.data.curves.new(type="FONT", name="Font Curve")
    font_curve.body = string
    d_name="Description"
    font_obj = bpy.data.objects.new(name=d_name, object_data=font_curve)
    bpy.context.scene.collection.objects.link(font_obj)
    select_specific([d_name])
    bpy.ops.transform.translate(value=(-5.3, -0.87, -0),
                                orient_axis_ortho='X',
                                orient_type='GLOBAL',
                                orient_matrix=((1, 0, 0),
                                                (0, 1, 0),
                                                (0, 0, 1)),
                                orient_matrix_type='GLOBAL',
                                constraint_axis=(True, True, False),
                                mirror=False,
                                use_proportional_edit=False,
                                proportional_edit_falloff='SMOOTH',
                                proportional_size=1,
                                use_proportional_connected=False,
                                use_proportional_projected=False,
                                release_confirm=True)

    bpy.context.object.location[0] = -5.3
    bpy.context.object.location[1] = -0.87
    


    text_name=None
    return text_name
def modify_description(text_name,h_text,t_text):
    #select descriprion text
    #edit description text
    #set key
    return 0
def modify_arrows(names,magnitudes,orientations):
    for c,arrow in enumerate(names):
        #select arrow
        #set magnitude
        #set orientation
        #set key
        a=1
    return 0

def go_through_files_H_T(path):
    fields,temps,number_of_layers=get_parameters(path)
    arrows      =   create_arrows(number_of_layers)
    description =   create_description("H=0","T=0")
    for i,t in enumerate(temps):
        for j,h in enumerate(fields):
            modify_description(description,h,t)
            file_name=compose_name(h,t)
            space, magnitude, angle = read_state(path+os.path.sep+file_name)
            modify_arrows(arrows, magnitude, angle)







path="C:\Dropbox\KTH data\WIP\high priority\Layered Model bare system\Multilayer-simulation\CS_L=0.15nm_J=1proc"
#go_through_files_H_T(path)
create_description(0.125258,300.0)