import numpy as np

# Input the new_position, color and current situation
# Output the same color stones' situation in the opposite color stones
max_line = 15

# find the forward oppo
def find_left_oppo(current, line):
    if current >= len(line):
        current = len(line)-1
        print 'lalal'
    # If the current is the left border, return -1
    if current == 0:
        return -1
    oppo = 0 - line[current]

    for i in range(current - 1, -1, -1):
        if line[i] == oppo:
            return i
    return -1


def find_right_oppo(current, line):    # If the current is the right border, return len(line)
    if current >= len(line):
        return len(line)
    oppo = 0 - line[current]
    for i in range(current + 1, len(line), 1):
        if line[i] == oppo:
            return i
    return len(line)


# Consider the situation in one line
def same_color_situation_in_line(current, line, color):
    left_border = max(find_left_oppo(current, line), current - 5, -1)
    right_boarder = min(find_right_oppo(current, line), current + 5, len(line))

    output_list = list()
    for temp in range(left_border + 1, right_boarder):
        if temp == current:
            output_list.append(2)
        elif line[temp] == color:
            output_list.append(1)
        else:
            output_list.append(0)
    return output_list


# find left diagonal of the current and table
def left_diagonal(current, table):
    left_diagonal_list = list()
    min_board = -min(current[0], current[1])
    max_board = max_line - max(current[0], current[1])
    for i in range(min_board, max_board):
        left_diagonal_list.append(table[current[0] + i][current[1] + i])
    return left_diagonal_list, -min_board


def right_diagonal(current, table):
    right_diagonal_list = list()
    sum_coor = sum(current)
    for i in range(0, sum_coor+1):
        if i <= 14 and sum_coor - i <= 14:
            right_diagonal_list.append(table[i][sum_coor - i])
    return right_diagonal_list, current[0]-max(0,sum_coor-14)


# consider the situation in a table, it has four direction
def same_color_situation_in_table(current, color, table):
    table[current[0]][current[1]] = color
    list_1 = same_color_situation_in_line(current[1], table[current[0]], color)
    list_2 = same_color_situation_in_line(current[0], np.transpose(table)[current[1]], color)
    left, left_index = left_diagonal(current, table)
    right, right_index = right_diagonal(current, table)
    list_3 = same_color_situation_in_line(left_index, left, color)
    list_4 = same_color_situation_in_line(right_index, right, color)
    return list_1, list_2, list_3, list_4


