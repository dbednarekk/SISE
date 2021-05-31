import argparse
import random
import time

solved = [['1', '2', '3', '4'], ['5', '6', '7', '8'], ['9', '10', '11', '12'], ['13', '14', '15', '0']]
puzzle_board = []
point = {}
order = []
depth = 20


def initial_arguments():
    parser = argparse.ArgumentParser('Solving fifteen puzzle algorithm'
                                     'Arguments: strategy, order, init file, output file, additional info file')
    parser.add_argument(metavar='STRATEGY', choices=['bfs', 'dfs', 'astr'],
                        help='strategy for solving puzzle, choose between bfs, dfs, astr', dest='algorithm')
    parser.add_argument(metavar='ORDER', help='additional order for given strategy', dest='order')
    parser.add_argument(metavar='INIT_FILE', help='file with initial data', dest='source_file')
    parser.add_argument(metavar='OUTPUT_FILE', default='output.txt',
                        help='output file with results', dest='solution_file')
    parser.add_argument(metavar='INFO_FILE', default='info.txt',
                        help='output file with additional information`s', dest='statistic_file')
    return parser.parse_args()


def change_position_of_blank_field(last_move):
    if last_move == 'U':
        point['row'] += 1
    if last_move == 'D':
        point['row'] -= 1
    if last_move == 'L':
        point['column'] += 1
    if last_move == 'R':
        point['column'] -= 1


def find_and_set_empty_field(test_board):
    for j in range(len(test_board)):
        for i in range(len(test_board[j])):
            if test_board[j][i] == '0':
                point['row'] = j
                point['column'] = i


class Node:
    def __init__(self, current_board, parent, last_move, path):
        self.board = current_board
        self.children = {}
        self.errors = {}
        if parent != 'Root':
            self.parent = parent
        self.last = last_move
        self.way = path.copy()
        self.way.append(last_move)
        self.to_visit = order.copy()

    def create_child(self, board_after_move, move):
        child = Node(board_after_move, self, move, self.way)
        self.children[move] = child

    def make_move(self, move):
        y = point['row']
        x = point['column']
        if move == 'L':
            tmp_array = []
            for row in self.board:
                tmp_array.append(row.copy())
            tmp_array[y][x - 1], tmp_array[y][x] = tmp_array[y][x], tmp_array[y][x - 1]
            point['column'] -= 1
            self.create_child(tmp_array, move)
        elif move == 'R':
            tmp_array = []
            for row in self.board:
                tmp_array.append(row.copy())
            tmp_array[y][x], tmp_array[y][x + 1] = tmp_array[y][x + 1], tmp_array[y][x]
            point['column'] += 1
            self.create_child(tmp_array, move)
        elif move == 'U':
            tmp_array = []
            for row in self.board:
                tmp_array.append(row.copy())
            tmp_array[y - 1][x], tmp_array[y][x] = tmp_array[y][x], tmp_array[y - 1][x]
            point['row'] -= 1
            self.create_child(tmp_array, move)
        elif move == 'D':
            tmp_array = []
            for row in self.board:
                tmp_array.append(row.copy())
            tmp_array[y][x], tmp_array[y + 1][x] = tmp_array[y + 1][x], tmp_array[y][x]
            point['row'] += 1
            self.create_child(tmp_array, move)


def handle_out_of_bound(current_node, flag=False):
    is_removed_l = False
    is_removed_r = False
    is_removed_u = False
    is_removed_d = False
    if point['column'] == len(solved[0]) - 1 and point['row'] == len(solved) - 1:
        current_node.to_visit.remove('R')
        current_node.to_visit.remove('D')
        is_removed_r = True
        is_removed_d = True
    elif point['column'] == len(solved[0]) - 1 and point['row'] == 0:
        current_node.to_visit.remove('R')
        current_node.to_visit.remove('U')
        is_removed_r = True
        is_removed_u = True
    elif point['column'] == 0 and point['row'] == 0:
        current_node.to_visit.remove('L')
        current_node.to_visit.remove('U')
        is_removed_l = True
        is_removed_u = True
    elif point['column'] == 0 and point['row'] == len(solved) - 1:
        current_node.to_visit.remove('L')
        current_node.to_visit.remove('D')
        is_removed_l = True
        is_removed_d = True
    elif point['column'] == 0:
        current_node.to_visit.remove('L')
        is_removed_l = True
    elif point['column'] == len(solved[0]) - 1:
        current_node.to_visit.remove('R')
        is_removed_r = True
    elif point['row'] == 0:
        current_node.to_visit.remove('U')
        is_removed_u = True
    elif point['row'] == len(solved) - 1:
        current_node.to_visit.remove('D')
        is_removed_d = True
    if not flag:
        if current_node.last == 'R' and not is_removed_l:
            current_node.to_visit.remove('L')
        elif current_node.last == 'L' and not is_removed_r:
            current_node.to_visit.remove('R')
        elif current_node.last == 'U' and not is_removed_d:
            current_node.to_visit.remove('D')
        elif current_node.last == 'D' and not is_removed_u:
            current_node.to_visit.remove('U')


def write_output(way, amount_of_processed_nodes, amount_of_visited_nodes, depth_level, start_time, solution_file,
                 statistic_file):
    if way != -1:
        way.remove(way[0])
        solution_length = len(way)
        solution = way
    else:
        solution_length = -1
        solution = []
    file = open(solution_file, 'w+')
    file.write(str(solution_length))
    if way != -1:
        file.write('\n')
        file.write(str(solution))
    file.close()
    file = open(statistic_file, 'w+')
    file.write(str(solution_length))
    file.write('\n')
    file.write(str(amount_of_visited_nodes))
    file.write('\n')
    file.write(str(amount_of_processed_nodes))
    file.write('\n')
    file.write(str(depth_level))
    file.write('\n')
    file.write(str(round((time.time() - start_time) * 1000, 3)))
    file.close()


if __name__ == '__main__':

    arguments = initial_arguments()

    for elem in arguments.order:
        order.append(elem)

    with open(arguments.source_file) as board:
        first_line_flag = True
        for line in board:
            if first_line_flag:
                first_line_flag = False
                continue
            else:
                puzzle_board.append(line.split())
    # Setting coordinates of empty field
    find_and_set_empty_field(puzzle_board)
    start_time = time.time()
    if arguments.algorithm == 'dfs':
        amount_of_processed_nodes = 1
        amount_of_visited_nodes = 1
        current_node = Node(puzzle_board, 'Root', None, [])
        root_flag = True
        parent_flag = False
        max_depth = False
        depth_level = 0
        handle_out_of_bound(current_node, root_flag)
        while True:
            if current_node.board == solved:
                if max_depth:
                    depth_level = depth
                else:
                    depth_level = len(current_node.way) - 1
                    write_output(current_node.way, amount_of_processed_nodes, amount_of_visited_nodes, depth_level,
                                 start_time, arguments.solution_file, arguments.statistic_file)
                    break
            elif len(current_node.way) == depth:
                current_node = current_node.parent
                find_and_set_empty_field(current_node.board)
                parent_flag = True
                max_depth = True
            elif len(current_node.to_visit) != 0:
                if not root_flag and not parent_flag:
                    handle_out_of_bound(current_node)
                if len(current_node.to_visit) != 0:
                    move = current_node.to_visit[0]
                    current_node.make_move(move)
                    current_node.to_visit.remove(move)
                    current_node = current_node.children[move]
                    find_and_set_empty_field(current_node.board)
                    root_flag = False
                    parent_flag = False
                    amount_of_visited_nodes += 1
                    amount_of_processed_nodes += 1
                else:
                    if current_node.last is None or time.time() - start_time > depth:
                        write_output(-1, amount_of_processed_nodes, amount_of_visited_nodes, depth_level, start_time,
                                     arguments.solution_file, arguments.statistic_file)
                        break
                    else:
                        current_node = current_node.parent
                        find_and_set_empty_field(current_node.board)
                        parent_flag = True
            else:
                if current_node.last is None or time.time() - start_time > depth:
                    write_output(-1, amount_of_processed_nodes, amount_of_visited_nodes, depth_level, start_time,
                                 arguments.solution_file, arguments.statistic_file)
                    break
                else:
                    current_node = current_node.parent
                    find_and_set_empty_field(current_node.board)
                    parent_flag = True
    elif arguments.algorithm == 'bfs':
        amount_of_processed_nodes = 1
        amount_of_visited_nodes = 1
        current_node = Node(puzzle_board, 'Root', None, [])
        handle_out_of_bound(current_node, True)
        queue = []
        counter = 0
        while True:
            counter += 1
            if time.time() - start_time > depth:
                write_output(-1, amount_of_processed_nodes, amount_of_visited_nodes, len(current_node.way) - 1,
                             start_time, arguments.solution_file, arguments.statistic_file)
                break
            if current_node.board == solved:
                write_output(current_node.way, amount_of_processed_nodes, amount_of_visited_nodes,
                             len(current_node.way) - 1,
                             start_time, arguments.solution_file, arguments.statistic_file)
                break
            else:
                if not current_node.last is None:
                    handle_out_of_bound(current_node, False)
                for move in current_node.to_visit:
                    amount_of_processed_nodes += 1
                    current_node.make_move(move)
                    current_node = current_node.children[move]
                    queue.append(current_node)
                    last_move = current_node.way[-1]
                    change_position_of_blank_field(last_move)
                    current_node = current_node.parent
                try:
                    if current_node.last is not None:
                        queue.remove(current_node)
                except ValueError:
                    pass
                current_node = queue[0]
                amount_of_visited_nodes += 1
                find_and_set_empty_field(current_node.board)
    else:
        order = ['L', 'R', 'D', 'U']
        amount_of_visited_nodes = 1
        amount_of_processed_nodes = 1


        def get_index_of_value(board, value):
            for index_row, row in enumerate(board):
                for index_col, elem in enumerate(row):
                    if elem == value:
                        return index_row, index_col


        if order == 'manh':
            def calculate_error(current_board, solved_board):
                manh_error = 0
                for index_row, row in enumerate(current_board):
                    for index_col, elem in enumerate(row):
                        target_row, target_col = get_index_of_value(solved_board, elem)
                        manh_error += abs(index_row - target_row) + abs(index_col - target_col)
                return manh_error
        else:
            def calculate_error(current_board, solved_board):
                hamm_error = 0
                for index_row, row in enumerate(current_board):
                    for index_col, elem in enumerate(row):
                        target_row, target_col = get_index_of_value(solved_board, elem)
                        if abs(index_row - target_row) + abs(index_col - target_col) != 0:
                            hamm_error += 1
                return hamm_error
        current_node = Node(puzzle_board, 'Root', None, [])
        handle_out_of_bound(current_node, True)
        while True:
            try:
                if time.time() - start_time > depth:
                    write_output(-1, amount_of_processed_nodes, amount_of_visited_nodes,
                                 len(current_node.way) - 1,
                                 start_time, arguments.solution_file, arguments.statistic_file)
                    break
                if current_node.board == solved:
                    write_output(current_node.way, amount_of_processed_nodes, amount_of_visited_nodes,
                                 len(current_node.way) - 1,
                                 start_time, arguments.solution_file, arguments.statistic_file)
                    break
                else:
                    for move in current_node.to_visit:
                        amount_of_processed_nodes += 1
                        current_node.make_move(move)
                        current_node = current_node.children[move]
                        error = calculate_error(current_node.board, solved)
                        current_node = current_node.parent
                        find_and_set_empty_field(current_node.board)
                        current_node.errors[move] = error
                    min_value = min(current_node.errors.values())
                    tmp = []
                    for key in current_node.errors:
                        if current_node.errors[key] == min_value:
                            tmp.append(key)
                    nr = random.randint(0, len(tmp) - 1)
                    next_move = tmp[nr]
                    current_node.make_move(next_move)
                    current_node = current_node.children[next_move]
                    amount_of_visited_nodes += 1
                    try:
                        handle_out_of_bound(current_node, False)
                    except ValueError:
                        pass
            except MemoryError:
                write_output(-1, amount_of_processed_nodes, amount_of_visited_nodes,
                             len(current_node.way) - 1,
                             start_time, arguments.solution_file, arguments.statistic_file)
                break
