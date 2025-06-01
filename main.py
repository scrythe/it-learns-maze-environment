import neat
import gymnasium as gym
import it_learns_mazes
import numpy as np
import pygame
import pickle


def eval_genomes(genomes: list, config):
    def best_genome_max(genome):
        if genome[1].fitness == None:
            return -100
        return genome[1].fitness

    best_genome_id = max(genomes, key=best_genome_max)[0]
    env.reset(seed=env.unwrapped.current_episode)
    for genome_id, genome in genomes:
        rendering = False
        if genome_id == best_genome_id and env.unwrapped.current_episode % 50 == 0:
            rendering = True
        genome.fitness = 0.0
        ai = neat.nn.FeedForwardNetwork.create(genome, config)
        obs, _ = env.reset()
        terminated = False
        truncated = False
        while not terminated and not truncated:
            if rendering:
                env.render()
            actions = ai.activate(obs)
            action: int = int(np.argmax(actions))

            # keys = pygame.key.get_pressed()
            # action = 3
            # if keys[pygame.K_a]:
            #     action = 0
            # elif keys[pygame.K_d]:
            #     action = 1
            # elif keys[pygame.K_w]:
            #     action = 2

            obs, reward, terminated, truncated, _ = env.step(action)
            genome.fitness += float(reward)
    env.unwrapped.current_episode += 1


if __name__ == "__main__":
    # def train_ai():
    env = gym.make("it-learns-mazes-v0")
    config = neat.Config(
        neat.DefaultGenome,
        neat.DefaultReproduction,
        neat.DefaultSpeciesSet,
        neat.DefaultStagnation,
        "config.txt",
    )
    p = neat.Population(config)
    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)
    neat.ParallelEvaluator
    n_gen = 500
    best = p.run(eval_genomes, n_gen)
    with open("best.pickle", "wb") as file:
        pickle.dump(best, file)
