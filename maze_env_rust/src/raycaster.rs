use pyo3::prelude::*;
type Position<T> = [T; 2];

const WALL: i32 = 0;

#[pyclass]
pub struct Raycaster {
    cell_width: i32,
    rays_amount: usize,
    angle_step: f32,
    ray_angle_substraction: f32,
    maze_structure: Vec<Vec<i32>>,
}

#[pymethods]
impl Raycaster {
    #[new]
    fn new(cell_width: i32, rays_amount: usize, fov: f32) -> Self {
        let angle_step = fov / (rays_amount - 1) as f32;
        let ray_angle_substraction = fov / 2 as f32;
        Raycaster {
            cell_width,
            rays_amount,
            angle_step,
            ray_angle_substraction,
            maze_structure: vec![vec![0]],
        }
    }

    fn reset(&mut self, maze_structure: Vec<Vec<i32>>) {
        self.maze_structure = maze_structure;
    }

    fn cast_multiple_rays(&self, player_position: Position<f32>, player_angle: f32) -> Vec<f32> {
        let mut rays = vec![0.0; self.rays_amount];
        let mut ray_angle = player_angle - self.ray_angle_substraction;
        let mut player_pos_normalised = player_position;
        player_pos_normalised[0] /= self.cell_width as f32;
        player_pos_normalised[1] /= self.cell_width as f32;
        let player_maze_pos = player_pos_normalised.map(|x| x as i32);

        for ray in &mut rays {
            *ray = self.cast_single_ray(
                player_pos_normalised,
                player_maze_pos,
                player_angle,
                ray_angle,
            );
            ray_angle += self.angle_step
        }

        rays
    }

    fn cast_single_ray(
        &self,
        player_pos_normalised: Position<f32>,
        mut ray_maze_pos: Position<i32>,
        player_angle: f32,
        mut ray_angle: f32,
    ) -> f32 {
        if ray_angle == 0.0 {
            ray_angle = 0.000001
        }

        let ray_dir_x = ray_angle.cos();
        let ray_dir_y = ray_angle.sin();

        let ray_step_x;
        let ray_step_y;

        let mut ray_length_x;
        let mut ray_length_y;

        let ray_length_step_x = f32::powi(ray_dir_y / ray_dir_x, 2);
        let ray_length_step_x = f32::sqrt(1.0 + ray_length_step_x);

        let ray_length_step_y = f32::powi(ray_dir_x / ray_dir_y, 2);
        let ray_length_step_y = f32::sqrt(1.0 + ray_length_step_y);

        // looking left
        if ray_dir_x < 0.0 {
            ray_step_x = -1;
            ray_length_x = (player_pos_normalised[0] - ray_maze_pos[0] as f32) * ray_length_step_x
        }
        // looking right
        else {
            ray_step_x = 1;
            ray_length_x =
                (ray_maze_pos[0] as f32 + 1.0 - player_pos_normalised[0]) * ray_length_step_x
        }

        // looking up
        if ray_dir_y < 0.0 {
            ray_step_y = -1;
            ray_length_y = (player_pos_normalised[1] - ray_maze_pos[1] as f32) * ray_length_step_y
        }
        // looking down
        else {
            ray_step_y = 1;
            ray_length_y =
                (ray_maze_pos[1] as f32 + 1.0 - player_pos_normalised[1]) * ray_length_step_y;
        }

        let mut collision = false;
        let mut ray_length = 0.0;

        while !collision {
            if ray_length_x > ray_length_y {
                ray_maze_pos[1] += ray_step_y;
                ray_length = ray_length_y;
                ray_length_y += ray_length_step_y;
            } else {
                ray_maze_pos[0] += ray_step_x;
                ray_length = ray_length_x;
                ray_length_x += ray_length_step_x;
            }
            if self.maze_structure[ray_maze_pos[1] as usize][ray_maze_pos[0] as usize] == WALL {
                collision = true
            }
        }
        ray_length *= self.cell_width as f32;
        let no_fish_angle = f32::abs(player_angle - ray_angle);
        let no_fish_length = no_fish_angle.cos() * ray_length;
        no_fish_length
    }
}
