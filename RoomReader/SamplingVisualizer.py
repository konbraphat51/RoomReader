"""
Visualize how sampler took samples
"""

from __future__ import annotations
import matplotlib.pyplot as plt
from UnityQuaternion import Quaternion
from RoomReader.ImageData import ImageData
from RoomReader.Config import Config
from RoomReader.GeometryHelper import get_index
from RoomReader.Vector import Vector


def visualize_sampling(images: list[ImageData], config: Config):
    vectors = _convert_to_vectors(images, config)

    locations = []
    for image in images:
        locations.append(image.position)

    fig, ax = plt.subplots()
    ax.quiver(
        [location[0] for location in locations],
        [location[1] for location in locations],
        [vector[0] for vector in vectors],
        [vector[1] for vector in vectors],
        scale=10,
    )

    # axis label
    ax.set_xlabel("x")
    ax.set_ylabel("y")

    # save
    plt.savefig(config.result_directory / "sampling.png")


def _convert_to_vectors(images: list[ImageData], config):
    vectors = []
    for image in images:
        vectors.append(_convert_to_vector(image, config))

    return vectors


def _convert_to_vector(image: ImageData, config):
    vec = Quaternion.Inverse(image.quaternion) * config.camera_vector
    return Vector(vec[0], vec[1], vec[2]).normalized() * 1
