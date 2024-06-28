"""Pre-processing utilities."""

import pyvista as pv
import trimesh
import vtk

vtk.vtkLogger.SetStderrVerbosity(vtk.vtkLogger.VERBOSITY_OFF)

# dimensions in meters
NORMALIZED_X_MAX = 10.0
NORMALIZED_Y_MAX = 2.0
NORMALIZED_Z_MAX = 1.0


def _get_scaling_factor(mesh: pv.PolyData) -> float:
    """
    Calculate the scaling factor required to normalize the mesh dimensions.

    Returns the most restrictive scaling factor to ensure the entire mesh fits
    within the specified bounds.

    Args:
        mesh (pv.PolyData): The input mesh to be normalized.

    Returns:
        float: The scaling factor to apply to the mesh.
    """
    x_dimension = mesh.bounds[1] - mesh.bounds[0]
    y_dimension = mesh.bounds[3] - mesh.bounds[2]
    z_dimension = mesh.bounds[5] - mesh.bounds[4]

    # Calculate the scaling factors for each axis
    scaling_factor_x = NORMALIZED_X_MAX / x_dimension
    scaling_factor_y = NORMALIZED_Y_MAX / y_dimension
    scaling_factor_z = NORMALIZED_Z_MAX / z_dimension

    # Use the most restrictive scaling factor
    return min(scaling_factor_x, scaling_factor_y, scaling_factor_z)


def normalize_mesh(mesh: pv.PolyData) -> pv.PolyData:
    """
    Normalize the dimensions of the input mesh.

    The mesh is scaled to fit within the specified bounds of the wind tunnel.

    Args:
        mesh (pv.PolyData): The input mesh to be normalized.

    Returns:
        pv.PolyData: The normalized mesh.
        float: The scaling factor applied to the mesh.
    """
    scaling_factor = _get_scaling_factor(mesh)
    mesh = mesh.scale(scaling_factor)

    return mesh, scaling_factor


def move_mesh_to_origin(mesh: pv.PolyData):
    """
    Translate the mesh to the origin of the wind tunnel.
    """
    # Get the z-coordinate of the lowest point of the mesh
    z_displace = mesh.bounds[4]
    # Get the y-coordinate of the center of the mesh
    y_displace = (mesh.bounds[2] + mesh.bounds[3]) / 2
    # Get the x-coordinate of the center of the mesh
    x_displace = (mesh.bounds[0] + mesh.bounds[1]) / 2

    displace_vector = [-x_displace, -y_displace, -z_displace]
    mesh = mesh.translate(displace_vector)
    return mesh, displace_vector


def compute_projected_area(mesh: pv.PolyData, face_normal):
    """Compute the projected area of an object.

    Args:
        mesh: pyvista.PolyData mesh representing the object.
    """

    # Compute roughly the projected area of the object. Slice the object mesh at
    # its center, which provides an outline curve of the object. Then fill it
    # with a simple mesh and compute the area of the filled mesh.
    mesh_slice = mesh.slice(origin=mesh.center, normal=face_normal)
    filled_slice = mesh_slice.delaunay_2d()
    area = filled_slice.area

    return area


def compute_object_length(mesh: pv.PolyData):
    # Length of the object in x-direction
    length = mesh.bounds[1] - mesh.bounds[0]

    return length


def save_mesh_obj(mesh, dest_object_path):
    trimesh_mesh = trimesh.Trimesh(vertices=mesh.points,
                                   faces=mesh.faces.reshape((-1, 4))[:, 1:])
    trimesh.exchange.export.export_mesh(trimesh_mesh, dest_object_path)
