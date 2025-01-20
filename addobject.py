import bpy
import bmesh
import numpy as np

def clear_scene():
    """Clear existing objects in the scene"""
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete()

def create_coordinate_axes(size=5):
    """Create coordinate axes for reference"""
    # Create vertices and edges for X, Y, Z axes
    verts = [(0, 0, 0), (size, 0, 0), (0, size, 0), (0, 0, size)]
    edges = [(0, 1), (0, 2), (0, 3)]
    
    # Create mesh and object
    mesh = bpy.data.meshes.new('Axes')
    axes = bpy.data.objects.new('Axes', mesh)
    
    # Link object to scene
    bpy.context.scene.collection.objects.link(axes)
    
    # Create mesh from vertices and edges
    mesh.from_pydata(verts, edges, [])
    mesh.update()
    
    # Color the axes
    mat_x = create_material('X_axis', (1, 0, 0, 1))  # Red for X
    mat_y = create_material('Y_axis', (0, 1, 0, 1))  # Green for Y
    mat_z = create_material('Z_axis', (0, 0, 1, 1))  # Blue for Z
    
    return axes

def create_material(name, color):
    """Create a new material with given color"""
    mat = bpy.data.materials.new(name=name)
    mat.use_nodes = True
    nodes = mat.node_tree.nodes
    
    # Clear default nodes
    nodes.clear()
    
    # Create emission node
    node_emission = nodes.new(type='ShaderNodeEmission')
    node_emission.inputs[0].default_value = color
    
    # Create output node
    node_output = nodes.new(type='ShaderNodeOutputMaterial')
    
    # Link nodes
    links = mat.node_tree.links
    links.new(node_emission.outputs[0], node_output.inputs[0])
    
    return mat

def create_hyperplane(normal_vector=[1, 1, 1], point=[0, 0, 0], size=5):
    """Create a hyperplane with given normal vector and point"""
    # Normalize the normal vector
    normal = np.array(normal_vector)
    normal = normal / np.linalg.norm(normal)
    point = np.array(point)
    
    # Create two vectors perpendicular to the normal vector
    v1 = np.array([-normal[1], normal[0], 0])
    if np.all(v1 == 0):
        v1 = np.array([0, -normal[2], normal[1]])
    v1 = v1 / np.linalg.norm(v1)
    v2 = np.cross(normal, v1)
    
    # Create vertices for the plane
    verts = []
    verts.append(point + size * (-v1 - v2))
    verts.append(point + size * (v1 - v2))
    verts.append(point + size * (v1 + v2))
    verts.append(point + size * (-v1 + v2))
    
    # Create faces
    faces = [[0, 1, 2, 3]]
    
    # Create mesh and object
    mesh = bpy.data.meshes.new('Hyperplane')
    plane = bpy.data.objects.new('Hyperplane', mesh)
    
    # Link object to scene
    bpy.context.scene.collection.objects.link(plane)
    
    # Create mesh from vertices and faces
    mesh.from_pydata(verts, [], faces)
    mesh.update()
    
    # Add material
    mat = create_material('Plane_material', (0.8, 0.8, 0.8, 0.5))
    mat.blend_method = 'BLEND'  # Make material transparent
    plane.data.materials.append(mat)
    
    return plane

def main():
    # Clear existing scene
    clear_scene()
    
    # Create coordinate axes
    create_coordinate_axes()
    
    # Create hyperplane (you can modify these parameters)
    normal_vector = [1, 1, 1]  # Normal vector to the plane
    point = [0, 0, 0]         # Point on the plane
    create_hyperplane(normal_vector, point)
    
    # Set up camera and lighting
    bpy.ops.object.camera_add(location=(10, -10, 10))
    bpy.ops.object.light_add(type='SUN', location=(5, 5, 5))
    
    # Set viewport shading to rendered
    for area in bpy.context.screen.areas:
        if area.type == 'VIEW_3D':
            for space in area.spaces:
                if space.type == 'VIEW_3D':
                    space.shading.type = 'RENDERED'

if __name__ == "__main__":
    main()