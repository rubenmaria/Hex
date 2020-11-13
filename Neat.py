import os
import neat
from AI import Ai
import math as m

class Neat:

    def __init__(self, canvas, board):
        self.game_state_nn_red = [0 for i in range(121)]
        self.game_state_nn_blue = [0 for i in range(121)]
        self.occupied_tiles = set()
        self.minimax = Ai(board, canvas, self.occupied_tiles)
        self.graph_blue = self.minimax.graph_blue
        self.graph_red = self.minimax.graph_red

    def update_state_after_graph_changed(self, graph, state, color):
        state_index = 0
        for row in range(1, 12):
            for col in range(1, 12):
                graph_color = graph[row][col].color
                if color == graph_color:
                    state[state_index] = 1
                elif "white" == graph_color:
                    state[state_index] = 0
                else:
                    state[state_index] = -1
                state_index += 1

    def update_graph_after_state_changed(self, state, graph, color):
        state_index = 0
        for row in range(1, 12):
            for col in range(1, 12):
                if state[state_index] == 1:
                    graph[row][col].color = color
                    self.occupied_tiles.add((row - 1, col - 1))
                elif state[state_index] == 0:
                    graph[row][col].color = "white"
                else:
                    self.occupied_tiles.add((row - 1, col - 1))
                    if color == "red":
                        graph[row][col].color = "blue"
                    else:
                        graph[row][col].color = "red"
                state_index += 1

    def eval_genomes(self, genomes, config):
        for genome_id, genome in genomes:
            net = neat.nn.FeedForwardNetwork.create(genome, config)
            start_row = 5
            start_col = 6
            self.graph_red[start_row + 1][start_col + 1].set_color("friendly", "red")
            self.graph_blue[start_row + 1][start_col + 1].set_color("enemy", "red")
            self.occupied_tiles.add((start_row, start_col))
            self.update_state_after_graph_changed(self.graph_red, self.game_state_nn_red, "red")
            self.update_state_after_graph_changed(self.graph_blue, self.game_state_nn_blue, "blue")
            move_count = 0
            fitness_sum = 0
            while not self.minimax.is_game_over():
                output = net.activate(self.game_state_nn_blue)
                self.process_nn_output(output, "blue")
                tile = self.minimax.minimax(list(), "red", 1, 1, -m.inf, +m.inf, True, list())
                self.process_player_move(tile, "red")
                fitness_sum += self.minimax.get_current_val("blue")
                move_count += 1
            genome.fitness = fitness_sum / move_count
            print(genome_id)
            print(genome.fitness)
            self.clear_all_boards()

    def clear_all_boards(self):
        self.minimax.setup_dijkstra_red()
        self.minimax.setup_dijkstra_blue()
        self.occupied_tiles.clear()
        self.game_state_nn_red = [0 for i in range(121)]
        self.game_state_nn_blue = [0 for i in range(121)]

    def process_player_move(self, tile, color):
        if color == "red":
            self.graph_red[tile[0] + 1][tile[1] + 1].set_color("friendly", "red")
            self.graph_blue[tile[0] + 1][tile[1] + 1].set_color("enemy", "red")
        else:
            self.graph_red[tile[0] + 1][tile[1] + 1].set_color("enemy", "blue")
            self.graph_blue[tile[0] + 1][tile[1] + 1].set_color("friendly", "blue")

        self.update_state_after_graph_changed(self.graph_red, self.game_state_nn_red, "red")
        self.update_state_after_graph_changed(self.graph_blue, self.game_state_nn_blue, "blue")

    def process_nn_output(self, output, color):
        max_o = -m.inf
        i = 0
        best_index = int()
        for o in output:
            if o > max_o:
                best_index = i
                max_o = o
            i += 1
        self.update_after_nn_move(best_index, color)

    def update_after_nn_move(self, index, color):
        if color == "blue":
            self.game_state_nn_red[index] = -1
            self.game_state_nn_blue[index] = 1
        else:
            self.game_state_nn_red[index] = 1
            self.game_state_nn_blue[index] = -1

        self.update_graph_after_state_changed(self.game_state_nn_blue, self.graph_blue, "blue")
        self.update_graph_after_state_changed(self.game_state_nn_red, self.graph_red, "red")


    def train(self):
        # Load configuration.
        local_dir = os.path.dirname(__file__)
        config_file = os.path.join(local_dir, 'config.cfg')
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
        winner = p.run(self.eval_genomes, 300)

        # Display the winning genome.
        print('\nBest genome:\n{!s}'.format(winner))

        # Show output of the most fit genome against training data.
        print('\nOutput:')
        winner_net = neat.nn.FeedForwardNetwork.create(winner, config)
        """for xi, xo in zip(xor_inputs, xor_outputs):
            output = winner_net.activate(xi)
            print("input {!r}, expected output {!r}, got {!r}".format(xi, xo, output))"""

        """node_names = {-1:'A', -2: 'B', 0:'A XOR B'}
        visualize.draw_net(config, winner, True, node_names=node_names)
        visualize.plot_stats(stats, ylog=False, view=True)
        visualize.plot_species(stats, view=True)"""

        p = neat.Checkpointer.restore_checkpoint('neat-checkpoint-4')
        p.run(self.eval_genomes, 10)
