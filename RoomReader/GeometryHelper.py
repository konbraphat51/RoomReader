from RoomReader.Config import Config
from RoomReader.Vector import Vector


def get_index(axis, position, config):
    if axis == "x":
        return int((position - config.room_x_min) / config.interval)
    elif axis == "y":
        return int((position - config.room_y_min) / config.interval)
    else:
        return int((position - config.room_z_min) / config.interval)


def in_room(position: Vector, config: Config) -> bool:
    if config.room_x_min <= position[0] <= config.room_x_max:
        if config.room_y_min <= position[1] <= config.room_y_max:
            if config.room_z_min <= position[2] <= config.room_z_max:
                return True
    return False
