import argparse


def initial_arguments():
    parser = argparse.ArgumentParser('Solving fifteen puzzle algorithm'
                                     'Arguments: strategy, order, init file, output file, additional info file')
    parser.add_argument(metavar='STRATEGY',  choices=['bfs', 'dfs', 'astr'],
                        help='strategy for solving puzzle, choose between bfs, dfs, astr', dest='strategy')
    parser.add_argument(metavar='ORDER', help='additional order for given strategy', dest='order')
    parser.add_argument(metavar='INIT_FILE', help='file with initial data', dest='init_data')
    parser.add_argument(metavar='OUTPUT_FILE', default='output.txt',
                        help='output file with results', dest='out_file')
    parser.add_argument(metavar='INFO_FILE', default='info.txt',
                        help='output file with additional information`s', dest='info_file')
    return parser.parse_args()


def open_initial_data_file(file):
    with open(file) as f:
        puzzle_size = f.readline().split()
        puzzle_board = []
        for line in f:
            puzzle_board.append(line.split())
    return puzzle_size, puzzle_board
