import neat
import gymnasium as gym
import it_learns_mazes
import numpy as np


def eval_genomes(genomes: list, config):
    for _, genome in genomes:
        genome.fitness = 0.0
        ai = neat.nn.FeedForwardNetwork.create(genome, config)
        obs, _ = env.reset()
        terminated = False
        truncated = False
        while not terminated and not truncated:
            actions = ai.activate(obs)
            action = np.argmax(actions)
            obs, reward, terminated, truncated, _ = env.step(action)
            genome.fitness += reward


# if __name__:"__main__":

# def train_ai():
env = gym.make("it-learns-mazes-v0", render_mode="human")
config = neat.Config(
    neat.DefaultGenome,
    neat.DefaultReproduction,
    neat.DefaultSpeciesSet,
    neat.DefaultStagnation,
    "config.txt",
)
p = neat.Population(config)
neat.ParallelEvaluator
n_gen = 50
winner = p.run(eval_genomes, n_gen)
