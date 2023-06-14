#ARAM ISIKBAY

import pygame
import random
pygame.init()

class Draw_Properties:
    BLACK = 0, 0, 0
    WHITE = 255, 255, 255
    GREEN = 0, 255, 0
    RED = 255, 0, 0
    GRAY1 = 128, 128, 128
    GRAY2 = 160, 160, 160
    GRAY3 = 192, 192, 192
    BACKGROUND_COLOR = WHITE

    GRADIENT = [GRAY1, GRAY2, GRAY3]

    FONT = pygame.font.Font(pygame.font.get_default_font(), 20)
    LARGE_FONT = pygame.font.Font(pygame.font.get_default_font(), 30)


    SIDE_PADDING = 100
    TOP_PADDING = 150

    def __init__(self, width, height, lst):
        self.width = width
        self.height = height

        self.window = pygame.display.set_mode((width, height))
        pygame.display.set_caption("Algorithm Visualizer")
        self.set_list(lst)

    def set_list(self, lst):
        self.lst = lst
        self.min_val = min(lst)
        self.max_val = max(lst)
        #Height and width of bars
        self.bar_height = (int)((self.height - self.TOP_PADDING) / (self.max_val - self.min_val))
        self.bar_width = round((self.width - self.SIDE_PADDING) / len(lst))
        self.start_x = self.SIDE_PADDING // 2

def drawScreen(draw_info, sorting_name, ascending):
    draw_info.window.fill(draw_info.BACKGROUND_COLOR)
    #Controls text
    controls = draw_info.FONT.render("R: Reset | SPACE: Sort | A: Ascending | D: Descending", 1, draw_info.BLACK)
    draw_info.window.blit(controls, (draw_info.width/2 - controls.get_width()/2, 5))
    #Sorting algorithm text
    sorting = draw_info.FONT.render("B: Bubble | I: Insertion", 1, draw_info.BLACK)
    draw_info.window.blit(sorting, (draw_info.width/2 - sorting.get_width()/2, 35))
    #Current state text
    state = draw_info.LARGE_FONT.render(f"{sorting_name} | {'Ascending' if ascending else 'Descending'}", 1, draw_info.BLACK)
    draw_info.window.blit(state, (draw_info.width/2 - state.get_width()/2, 65))

    drawList(draw_info)
    pygame.display.update()

def drawList(draw_info, colored_positions={}, clear_bg=False):
    lst = draw_info.lst

    if clear_bg:
        clear_rect = (draw_info.SIDE_PADDING//2, draw_info.TOP_PADDING, draw_info.width - draw_info.SIDE_PADDING, draw_info.height - draw_info.TOP_PADDING)
        pygame.draw.rect(draw_info.window, draw_info.BACKGROUND_COLOR, clear_rect)

    for i, val in enumerate(lst):
        #Positions for bars
        x = draw_info.start_x + i * draw_info.bar_width
        y = draw_info.height - (val - draw_info.min_val) * draw_info.bar_height 
        #Alternate bar gray colors
        color = draw_info.GRADIENT[i % 3]
        #Overwrite color if bar is being swapped currently
        if i in colored_positions:
            color = colored_positions[i]
        #Draw bar
        pygame.draw.rect(draw_info.window, color, (x, y, draw_info.bar_width, draw_info.height))

    if clear_bg:
        pygame.display.update()


def generate_starting_list(n, min_val, max_val):
    lst = []
    for _ in range(n):
        value = random.randint(min_val, max_val)
        lst.append(value)

    return lst

#SORTING ALGORITHMS#################################################################
def bubble(draw_info, ascending=True):
    lst = draw_info.lst

    for i in range(len(lst) - 1):
        for j in range (len(lst) - 1 - i):
            num1 = lst[j]
            num2 = lst[j+1]

            if (num1 > num2 and ascending) or (num1 < num2 and not ascending):
                #If condition is met, swap values
                lst[j], lst[j+1] = lst[j+1], lst[j]
                drawList(draw_info, {j: draw_info.GREEN, j+1: draw_info.RED}, True)
                #Generator - allows user to continue to use controls while sorting
                yield True

    return lst

def insertion(draw_info, ascending=True):
    lst = draw_info.lst

    for i in range(1, len(lst)):
        current = lst[i]

        while True:
            ascending_sort = i > 0 and lst[i-1] > current and ascending
            descending_sort = i > 0 and lst[i-1] < current and not ascending

            if not ascending_sort and not descending_sort:
                break

            lst[i] = lst[i-1]
            i = i-1
            lst[i] = current
            drawList(draw_info, {i: draw_info.GREEN, i-1: draw_info.RED}, True)
            yield True

####################################################################################

def main():
    run = True
    clock = pygame.time.Clock()

    n = 50
    min_val = 20
    max_val = 100

    lst = generate_starting_list(n, min_val, max_val)
    draw_info = Draw_Properties(800,600,lst)
    sorting = False
    ascending = True

    sorting_algorithm = bubble
    sorting_name = "Bubble Sort"
    sorting_algorithm_gen = None

    #Driver loop
    while run:
        clock.tick(80)
        if sorting:
            try:
                next(sorting_algorithm_gen)
            except StopIteration:
                sorting = False
        else:
            drawScreen(draw_info, sorting_name, ascending)

        #Get events since last iteration
        for event in pygame.event.get():
            #If user closes window
            if event.type == pygame.QUIT:
                    run = False
            if event.type != pygame.KEYDOWN:
                continue
            #If user resets list
            if event.key == pygame.K_r:
                lst = generate_starting_list(n, min_val, max_val)
                draw_info.set_list(lst)
                sorting = False
            elif event.key == pygame.K_SPACE and not sorting:
                sorting = True
                #Generator for sorting
                sorting_algorithm_gen = sorting_algorithm(draw_info, ascending)
            elif event.key == pygame.K_a and not sorting:
                ascending = True
            elif event.key == pygame.K_d and not sorting:
                ascending = False
            elif event.key == pygame.K_b and not sorting:
                sorting_algorithm = bubble
                sorting_name = "Bubble sort"
            elif event.key == pygame.K_i and not sorting:
                sorting_algorithm = insertion
                sorting_name = "Insertion sort"

    pygame.quit()

if __name__ == "__main__":
    main()