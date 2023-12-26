def get_index(axis, position, config):
    if axis=="x":
        return int((position - config.room_x_min) / config.interval)
    elif axis=="y":
        return int((position - config.room_y_min) / config.interval)
    else:
        return int((position - config.room_z_min) / config.interval)
