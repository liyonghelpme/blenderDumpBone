import bpy, math
from mathutils import Vector, Matrix
import mathutils

def dumpVertData():
    obj = bpy.data.objects['Cube']
    ob = obj
    vert = obj.data.vertices
    #arm = bpy.data.objects['Armature']
    
    vert_groups = obj.vertex_groups.values()
    group_tot = len(obj.vertex_groups)
     
    if not group_tot:
        weight_ls = [[] for i in range(len(vert))]
    else:
        weight_ls = [[0.0]*group_tot for i in range(len(vert))]
    
    for i, v in enumerate(vert):
        for g in v.groups:
            index = g.group
            if index < group_tot:
                weight_ls[i][index] = g.weight
    
    
    f = open('vert.dat', 'w')
    #f.write("%d\n" % len(vert))
    #12 *3 = 36 vertice
    f.write('%d\n' % (len(ob.data.polygons)*3))

    #for v in vert:
    #    f.write('%f %f %f\n'% (v.co.x, v.co.y, v.co.z))


    for face in ob.data.polygons:
        for v, loop in zip(face.vertices, face.loop_indices):
            f.write('%f %f %f\n' % (vert[v].co.x, vert[v].co.y, vert[v].co.z))
            '''
            if hasUv:
                uv = ob.data.uv_layers.active.data[loop].uv
                fi.write('%.2f, %.2f\n' % (uv[0], uv[1]))
            else:
                fi.write('%.2f, %.2f\n' % (0, 0))
            '''

    #weight vertex
    f.write("%d\n"% group_tot)
    for i, w in enumerate(weight_ls):
        for k in w:
            f.write("%f "%(k))
        f.write('\n')
    f.close()
    
    #groups---> group0  group 1
    #vert ---> groupId ---> weight
    
    '''
    count = 0
    s = ''
    for v in vert:
        for g in v.groups:
            s += "%d %d %f\n" % (v.index, g.group, g.weight)
            count = count+1
    f.write('%d\n'% count)
    f.write(s)
    f.close() 
    '''
    print("finish vertices")
    
#no animation data
def dumpAnimation():
    fi = open('ani.dat', 'w')
    fi.write("%d\n"%(2))
    for f in [1, 29]:
        fi.write("%d\n" % (f))
        bpy.context.scene.frame_set(f)
        dumpPoseBoneData(fi)
    fi.close()    
            
    
def dumpFaceData():
    fi = open('face.dat', 'w')
    ob = bpy.data.objects['Cube']
    faces = ob.data.polygons
    #mesh = bpy.data.meshes['Cube']
    #fi.write('%d\n' % (len(mesh.faces)))
    fi.write('%d\n' % (len(faces)))
    #for f in mesh.faces:
    count = 0
    for f in faces:
        s = ''
        #s += '%d\n' % (len(f.vertices))
        for i in f.vertices:
            #s += '%d ' % (i) 
            s += '%d ' % (count) 
            count += 1
        s += '\n'
        fi.write(s)
    fi.close()
    print("finish Face")
      
def dumpPoseBoneData(f):
    bo = bpy.context.object.pose.bones
    f.write('%d\n' % (len(bo)))
    for k in bo:
        q = k.matrix.to_quaternion()
        f.write('%f %f %f %f\n' % (q.x, q.y, q.z, q.w))
        f.write('%f\n' % (k.length))
        f.write('%f %f %f\n'%( k.head.x, k.head.y, k.head.z))
        if k.parent == None:
            f.write('-1\n')
        else:
            f.write('%d\n' % (bv.index(k.parent)))

def dumpBoneData(fi):
    bv = bpy.data.armatures.get('Armature').bones.values()
    oldFi = fi
    if fi == None:
        fi = open('bone.dat', 'w')
    f = fi
    f.write('%d\n'%(len(bv)))
    for k in bv:
        q = k.matrix.to_quaternion()
        f.write('%f %f %f %f\n' % (q.x, q.y, q.z, q.w))
        f.write('%f\n'% (k.length))
        f.write('%f %f %f\n'%( k.head.x, k.head.y, k.head.z))
        if k.parent == None:
            f.write('-1\n')
        else:
            f.write('%d\n' % (bv.index(k.parent)))
    if oldFi == None:
        f.close()        

def dumpTex():
    ob = bpy.data.objects['Cube']
    hasUv = ob.data.uv_layers.active
    count = len(ob.data.polygons)
    fi = open('tex.dat', 'w')
    fi.write('%d\n' % count)

    for face in ob.data.polygons:
        for vert, loop in zip(face.vertices, face.loop_indices):
            if hasUv:
                uv = ob.data.uv_layers.active.data[loop].uv
                fi.write('%.2f %.2f\n' % (uv[0], uv[1]))
            else:
                fi.write('%.2f %.2f\n' % (0, 0))
                #print(0, 0)
            
            #for item in (ob.data.uv_layers.active.data[loop].uv if  is not None else (0.0, 0.0)):
                #print(item)
    fi.close()
    print("finish Tex")

if __name__ == '__main__':
    dumpVertData()
    dumpFaceData()
    #dumpBoneData(None)    
    #dumpAnimation()
    dumpTex()
