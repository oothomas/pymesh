# -*- coding: utf-8 -*-

from __future__ import absolute_import, print_function
import numpy
from .base import BaseMesh


class Obj(BaseMesh):

    obj_dtype = numpy.dtype([
        ('normals', numpy.float32, (3, )),
        ('vectors', numpy.float32, (3, 3)),
        ('attr', numpy.uint16, (1, )),
    ])

    def __init__(self, path=None):
        """Create an instance of Obj (Wavefront)
        :param str path:
        """
        super(Obj, self).__init__()

        if path is None:
            # Create EMPTY data
            self.name = "empty"
            self.data = numpy.zeros(0, dtype=Obj.obj_dtype)

        else:
            # Create data from file
            with open(path, "r") as fh:
                data = Obj.__load(fh)
            self.name = path
            self.data = data

        super(Obj, self).set_initial_values()
        return

    @staticmethod
    def __load(fh):
        return numpy.fromiter(Obj.__read(fh), dtype=Obj.obj_dtype)

    @staticmethod
    def __read(fh):
        vertices_list = []
        triangles_list = []

        try:
            while True:
                line = fh.readline()
                if line == "":
                    break

                elif line.lstrip().startswith("vn"):
                    continue

                elif line.lstrip().startswith("v"):
                    vertices = line.replace("\n", "").split(" ")[1:]
                    vertices_list.append(list(map(float, vertices)))

                elif line.lstrip().startswith("f"):
                    t_index_list = []
                    for t in line.replace("\n", "").split(" ")[1:]:
                        t_index = t.split("/")[0]
                        t_index_list.append(int(t_index) - 1)
                    triangles_list.append(t_index_list)

                else:
                    continue

            for t in triangles_list:
                yield ([0, 0, 0], (vertices_list[t[0]], vertices_list[t[1]], vertices_list[t[2]]), 0)

        except:
            raise RuntimeError("Failed to load OBJ file.")
