import numpy
from .tri_mesh import TriMesh


def new_empty_verts() -> numpy.ndarray:
    return numpy.zeros(0, dtype=numpy.float32)