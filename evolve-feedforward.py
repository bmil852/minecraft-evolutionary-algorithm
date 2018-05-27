from __future__ import print_function
import os
import neat
import visualize
import katniss
import random

def eval_genomes(genomes, config):
    z1 = 5
    z2 = 25
    y1 = 56
    y2 = 65
    x = 0
    rand_y = random.randint(y1+2, y2-2)
    rand_z = random.randint(z1+2, z2-2)
    environment = [z1, z2, y1, y2, x, rand_y, rand_z]
    nn_inputs = [normalize(rand_y-(y1+1),y2-y1), normalize(rand_z-(z1+1),z2-z1)]
    print(nn_inputs)
    genomeList = []
    outputList = []
    
    for genome_id, genome in genomes:
        genome.fitness = 1
        net = neat.nn.FeedForwardNetwork.create(genome, config)
        genomeList.append(genome)
        output = net.activate(nn_inputs)
        outputList.append(output)

    errorList = katniss.evaluateFitness(environment, outputList)

    i = 0
    for g in genomeList:
        g.fitness -= errorList[i]
        i += 1
        print("New fitness for individual is: " + str(g.fitness))

def normalize(value, valueRange):
    valueRange -= 4
    valueRange /= 2.0
    return (value - valueRange * 1.0)/valueRange

def run(config_file):
    # Load configuration.
    config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
                         neat.DefaultSpeciesSet, neat.DefaultStagnation,
                         config_file)

    # Create the population, which is the top-level object for a NEAT run.
    p = neat.Population(config)

    # Add a stdout reporter to show progress in the terminal.
    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)
    p.add_reporter(neat.Checkpointer(5))

    # Run for up to 300 generations.
    winner = p.run(eval_genomes, 300)

    # Display the winning genome.
    print('\nBest genome:\n{!s}'.format(winner))

    #node_names = {-1:'A', -2: 'B', 0:'A XOR B'}
    #visualize.draw_net(config, winner, True, node_names=node_names)
    visualize.plot_stats(stats, ylog=False, view=True)
    visualize.plot_species(stats, view=True)

if __name__ == '__main__':
    # Determine path to configuration file. This path manipulation is
    # here so that the script will run successfully regardless of the
    # current working directory.
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, 'config-feedforward')
    run(config_path)
