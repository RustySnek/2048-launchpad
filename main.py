import launchpad_py as lppy
from random import random, randint, sample, choice
import time


lp = lppy.Launchpad()
lp.ListAll()
lp.Open()
lp.Reset()

area = [[0 for i in range(4)] for i in range(4)]
two_chance = 0.9
four_chance = 0.1


def randomize_spawn():
    return 2 if random() > four_chance else 4


def gen_starting_area():
    rows = sample([0, 1, 2, 3], 2)
    cols = [randint(0, 3), randint(0, 3)]
    for i in range(2):
        area[cols[i]][rows[i]] = randomize_spawn()


def spawn_number(empty_cells: list[tuple[int, int]]):
    col, row = choice(empty_cells)
    if area[col][row] != 0:
        raise IndexError("???")
    area[col][row] = randomize_spawn()


def can_move(row, direction):
    if direction == "right":
        row = row[::-1]
    for i in range(1, len(row)):  # Start from the second column
        if row[i] != 0:
            if row[i - 1] == 0 or row[i - 1] == row[i]:
                return True  # There's a valid move to the left
    return False  # No valid move to the left
def move(direction: str):
    match direction:
        case "left":
            moved = False
            empty_rows = []
            for idx, col in enumerate(area):
                if can_move(col, direction):
                    moved = True
                else:
                    for i_idx, i in enumerate(col):
                        if i == 0:
                            empty_rows.append((idx, i_idx))
                        continue

                col = [cell for cell in col if cell != 0]
                i = 0
                while i < len(col) - 1:
                    if col[i] == col[i + 1]:
                        col[i] += col[i + 1]
                        col.pop(i + 1)
                    i += 1
                while len(col) < 4:
                    col.append(0)
                    empty_rows.append((idx, len(col) - 1))
                area[idx] = col
            if moved == True:
                spawn_number(empty_rows)
        case "right":
            empty_rows = []
            moved = False
            for idx, col in enumerate(area):
                if can_move(col, direction):
                    moved = True
                else:
                    for i_idx, i in enumerate(col):
                        if i == 0:
                            empty_rows.append((idx, i_idx))
                    continue

                col = col[::-1]

                col = [cell for cell in col if cell != 0]
                i = 0
                while i < len(col) - 1:
                    if col[i] == col[i + 1]:
                        col[i] += col[i + 1]
                        col.pop(i + 1)
                    i += 1
                count = 0
                while len(col) < 4:
                    col.append(0)
                    empty_rows.append((idx, count))
                    count += 1
                col = col[::-1]
                area[idx] = col
            if moved:
                spawn_number(empty_rows)
        case "up":
            transposed_area = [list(row) for row in zip(*area)]
            empty_rows = []
            moved = False
                
            for idx, col in enumerate(transposed_area):
                if can_move(col, "left"):
                    moved = True
                else:
                    for i_idx, i in enumerate(col):
                        if i == 0:
                            empty_rows.append((i_idx, idx))
                        continue


                col = [cell for cell in col if cell != 0]
                i = 0
                while i < len(col) - 1:
                    if col[i] == col[i + 1]:
                        col[i] += col[i + 1]
                        col.pop(i + 1)
                    i += 1
                while len(col) < 4:
                    col.append(0)
                    empty_rows.append((len(col) - 1, idx))
                transposed_area[idx] = col

            area[:] = [list(row) for row in zip(*transposed_area)]
            if moved == True:
                spawn_number(empty_rows)

        case "down":
            transposed_area = [list(row) for row in zip(*area)]
            empty_rows = []
            moved = False
            for idx, col in enumerate(transposed_area):
                if can_move(col, "right"):
                    moved = True
                else:
                    for i_idx, i in enumerate(col):
                        if i == 0:
                            empty_rows.append((i_idx, idx))
                        continue


                col = col[::-1]
                col = [cell for cell in col if cell != 0]
                i = 0
                while i < len(col) - 1:
                    if col[i] == col[i + 1]:
                        col[i] += col[i + 1]
                        col.pop(i + 1)
                    i += 1
                while len(col) < 4:
                    col.append(0)
                    empty_rows.append((3 - len(col) + 1, idx))
                col = col[::-1]
                transposed_area[idx] = col
            
            area[:] = [list(row) for row in zip(*transposed_area)]
            if moved == True:
                spawn_number(empty_rows)

        case _:
            return


colors = {
        2: [(1, 0, True), None],
        4: [(3, 0, True), None],
        8: [(3, 0, True), (0,1)],
        16: [(0, 1,False), None],
        32: [(0, 1,True), None],
        64: [(0, 1,True), (1,1)],
        128: [(1, 1,False), None],
        256: [(1, 1,True), None],
        512: [(1, 1,True), (1,0)],
        1024: [(3, 3,True), (3,0)],
        2048: [(3, 3,True), (0,3)],


        }

def light_keys(number_coords, number):
    y,x = number_coords
    _colors, state_color = colors[number]
    color1, color2, state = _colors
    lp.LedCtrlXY(x,y+2,color1, color2)
    lp.LedCtrlXY(x+1,y+1,color1,color2)
    if state == True:
        if state_color != None:
            color1, color2 = state_color
        lp.LedCtrlXY(x,y+1,color1,color2)

        lp.LedCtrlXY(x+1,y+2,color1, color2)

def gesture_to_direction(btns):
    prev_x, prev_y = None, None
    movement_direction = ""
    for btn in btns:
        x, y, state = btn
        if prev_x is not None and prev_y is not None:
            x_move = prev_x - x
            y_move = prev_y - y
            
            if x_move > 0 and abs(x_move) > abs(y_move):
                movement_direction = "Left"
            elif x_move < 0 and abs(x_move) > abs(y_move):
                movement_direction = "Right"
            elif y_move > 0 and abs(y_move) > abs(x_move):
                movement_direction = "Up"
            elif y_move < 0 and abs(y_move) > abs(x_move):
                movement_direction = "Down"
            else:
                movement_direction = "No Significant Movement"
        prev_x, prev_y = x, y
    return movement_direction.lower()

def draw_numbers():
    for y, col in enumerate(area):
        print(col)
        for x ,row in enumerate(col):
            if row != 0:
                light_keys(((y)*2,(x)*2), row)

def rewind(prev_area):
    global area
    area = prev_area

def calc_score():
    score = 0
    for col in area:
        for row in col:
            score += row
    return score


previous_area = list(area)


menu_options = {
        (0,0): lambda: lp.LedCtrlString(str(calc_score()), 3, 0),
        (8,8): lambda: rewind(previous_area)
        }

def light_menu_keys():
    for opt in menu_options:
        x, y = opt
        lp.LedCtrlXY(x, y, 0, 3)

gen_starting_area()
draw_numbers()
light_menu_keys()
gesture_buttons = []
start_time = time.time()
while True:
    end_button = None
    initial_button = lp.ButtonStateXY()
    if initial_button != [] and initial_button[2] != False:
        x, y, state = initial_button
        if x == 8 or y == 0:
            lp.Reset()
            if (x,y) in menu_options:
                menu_options[(x,y)]()
            lp.Reset()
            draw_numbers()
            light_menu_keys()
        else: 
            start_time = time.time()
            gesture_buttons.append(initial_button)
    end_time = time.time()
    if gesture_buttons != []:
        delta = end_time - start_time
        #print(f"since last button: {delta}")
        if delta > 0.15 and len(gesture_buttons) > 2:
            direction = gesture_to_direction(gesture_buttons)
            print("moving", direction)
            previous_area = list(area)
            move(direction)
            lp.Reset()
            draw_numbers()
            light_menu_keys()
            gesture_buttons = []
    
