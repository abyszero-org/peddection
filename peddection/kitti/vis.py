# AUTOGENERATED! DO NOT EDIT! File to edit: ../../nbs/01_kitti_explore.ipynb.

# %% auto 0
__all__ = ['KITTI_ROOT', 'ds', 'loadVeloAsPcd', 'plotCloud']

# %% ../../nbs/01_kitti_explore.ipynb 3
from typing import Union, Iterable, List
from pathlib import Path
from os import PathLike, environ

from pathlib import Path
from PIL import Image
import numpy as np
import open3d as o3d

import matplotlib.pyplot as plt
from mpl_toolkits import mplot3d
import plotly.graph_objects as go


# %% ../../nbs/01_kitti_explore.ipynb 4
KITTI_ROOT:Path = environ.get("KITTI_ROOT", Path("/media/usbhd4tb/datasets/kitti"))

# Documentation: https://www.open3d.org/docs/release/python_api/open3d.ml.torch.datasets.KITTI.html
ds:o3d.ml.datasets.KITTI = o3d.ml.datasets.KITTI(KITTI_ROOT)

# %% ../../nbs/01_kitti_explore.ipynb 8
def loadVeloAsPcd(fname: Union[str, PathLike])->o3d.geometry.PointCloud:
    points                  = o3d.ml.datasets.KITTI.read_lidar(fname)
    cloud                   = o3d.t.geometry.PointCloud()
    cloud.point.positions   = o3d.core.Tensor(points[:, :3])
    cloud.point.intensities = o3d.core.Tensor(points[:, 3])
    cloud.remove_duplicated_points()
    cloud.remove_statistical_outliers(3, .999)
    cloud.estimate_normals()
    cloud.point.colors      = 0.5 + cloud.point.normals * 0.5
    cloud.estimate_color_gradients()
 #  cloud.estimate_normals(search_param = o3d.geometry.KDTreeSearchParamHybrid(radius = 0.1, max
    return cloud

# %% ../../nbs/01_kitti_explore.ipynb 10
def plotCloud(
        cloud: o3d.t.geometry.PointCloud, 
        boxes:Iterable[o3d._ml3d.datasets.kitti.Object3d] = [])->go.Figure:
    
    points = cloud.point.positions.numpy()
    colors = cloud.point.colors.numpy()

    # Add the point cloud
    data = [go.Scatter3d(
        x=points[:, 0], y=points[:, 1], z=points[:, 2],
        mode = 'markers',
        marker = {"size": 1, "color": colors}
    )]

    # Add bounding boxes
    for box in boxes:
        corners = box.generate_corners3d()
        x, y, z = corners[:, 0], corners[:, 1], corners[:, 2]
        mesh = go.Mesh3d(
            x=x, y=y, z=z,
            color='rgba(0, 255, 0, 0.5)',  # Semi-transparent green
            opacity=0.5
        )
        data.append(mesh)

    # Global figure settings
    layout = {
        "scene": {
            "xaxis": {"visible": False},
            "yaxis": {"visible": False},
            "zaxis": {"visible": False}
        }
    }

    fig = go.Figure(data=data, layout=layout)
    return fig
