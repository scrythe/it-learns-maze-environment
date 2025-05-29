class Raycaster:
    def __init__(self, cell_width: int, rays_amount: int, fov: float): ...
    def cast_multiple_rays(
        self, player_position: tuple[float, float], player_angle: float
    ):
        tuple[list[float], list[list[float]]]

def generate_maze_graph(size: int, seed: int) -> list[list[int]]: ...
