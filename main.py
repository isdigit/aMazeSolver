from time import sleep
from tkinter import CENTER, Tk, BOTH, Canvas, messagebox
import random

class Window:
    def __init__(self, width, height, background_color):
        self.width = width
        self.height = height
        self.root = Tk()
        self.title = "aMazeSolver"
        self.root.title(self.title)
        self.canvas = Canvas(
            self.root,
            height = self.height,
            width = self.width,
            cursor="cross",
            bg = background_color)
        self.canvas.pack(fill = "both", expand=True)
        self.window_running = False
        self.root.protocol("WM_DELETE_WINDOW", self.close)

    def redraw(self):
            self.root.update_idletasks()
            self.root.update()

    def wait_for_close(self):
        self.window_running = True
        while self.window_running:
            self.redraw()

    def close(self):
        result = messagebox.askokcancel(f"Close {self.title}","Do you want to exit?")
        if result:
            self.window_running = False
            self.root.destroy()
            exit()
        else:
            return

class Point:
    def __init__(self, x, y):
        self.x = x #where 0 is the left of the screen
        self.y = y #where 0 is the top of the screen
    
    def __repr__(self) -> str:
        return str([self.x, self.y])


class Line:
    def __init__(self, win, x1, y1, x2, y2, line_color, width = 2):
        if win is not None:
            self.canvas = win.canvas
        else:
            self.canvas = None
        self.pnt_1 = Point(x1, y1)
        self.pnt_2 = Point(x2, y2)
        self.line_color = line_color
        self.width = width

    def draw(self):
        if self.canvas is not None:
            self.canvas.create_line(self.pnt_1.x, self.pnt_1.y,
                                self.pnt_2.x, self.pnt_2.y,
                                fill=self.line_color, width=self.width)
        #else:
            #print("Cannot Line.draw()! Canvas is None!")


class Center_Mark:
    def __init__(self, win, x, y, size, line_color):
        self.win = win
        self.x = x
        self.y = y
        self.size = size / 2
        self.line_color = line_color

    def draw(self):
        Line(self.win, self.x - self.size, self.y - self.size, self.x + self.size, self.y + self.size, self.line_color).draw()
        Line(self.win, self.x - self.size, self.y + self.size, self.x + self.size, self.y - self.size, self.line_color).draw()


class Cell():
    def __init__(self, win = None, x = 0, y = 0, width = 0, height = 0,
                line_color = "white", background_color = "black", line_width = 3,
                left_wall = True, right_wall = True,
                top_wall = True, bottom_wall = True, col = 0, row = 0):

        self.win = win
        self.center_point = Point(x, y) #center point of cell
        self.width = width
        self.height = height
        self.line_color = line_color
        self.background_color = background_color
        self.line_width = line_width
        self.has_left_wall = left_wall
        self.has_right_wall = right_wall
        self.has_top_wall = top_wall
        self.has_bottom_wall = bottom_wall
        self.visited = False
        self.col = col
        self.row = row
    
    def __repr__(self):
        return str([self.row,self.col])
    
    #Parses and input string or list of strings for sides and sets the _has_<side>_wall to True by default or False if specified for each side specified
    #If has_<side>_wall changed from True to False, redraws the line to match the canvas background color
    #If has_<side>_wall changed from False to True, redraws the line to match the line color
    def set_wall(self, sides, has_wall = True):
        if "left" in sides:
            if self.has_left_wall != has_wall:
                self.has_left_wall = has_wall
                if has_wall:
                    self.left_wall.line_color = self.line_color
                else:
                    self.left_wall.line_color = self.background_color
        if "right" in sides:
            if self.has_right_wall != has_wall:
                self.has_right_wall = has_wall
                if has_wall:
                    self.right_wall.line_color = self.line_color
                else:
                    self.right_wall.line_color = self.background_color
        if "top" in sides:
            if self.has_top_wall != has_wall:
                self.has_top_wall = has_wall
                if has_wall:
                    self.top_wall.line_color = self.line_color
                else:
                    self.top_wall.line_color = self.background_color
        if "bottom" in sides:
            if self.has_bottom_wall != has_wall:
                self.has_bottom_wall = has_wall
                if has_wall:
                    self.bottom_wall.line_color = self.line_color
                else:
                    self.bottom_wall.line_color = self.background_color
        self.draw()

    def __calculate_walls(self):
        self.half_width = self.width / 2
        self.half_height = self.height / 2
        self.pnt_1 = Point(self.center_point.x - self.half_width, self.center_point.y - self.half_height) #upper left point of cell
        self.pnt_2 = Point(self.center_point.x + self.half_width, self.center_point.y + self.half_height) #lower right point of cell
        self.left_wall = Line(self.win, self.pnt_1.x, self.pnt_1.y, self.pnt_1.x, self.pnt_2.y, self.line_color, self.line_width)
        self.right_wall = Line(self.win, self.pnt_2.x, self.pnt_1.y, self.pnt_2.x, self.pnt_2.y, self.line_color, self.line_width)
        self.top_wall = Line(self.win, self.pnt_1.x, self.pnt_1.y, self.pnt_2.x, self.pnt_1.y, self.line_color, self.line_width)
        self.bottom_wall = Line(self.win, self.pnt_1.x, self.pnt_2.y, self.pnt_2.x, self.pnt_2.y, self.line_color, self.line_width)

    def draw(self):
        self.__calculate_walls()
        if self.win is not None:
            if self.has_left_wall:
                self.left_wall.line_color = self.line_color
            else:
                self.left_wall.line_color = self.background_color
            
            if self.has_right_wall:
                self.right_wall.line_color = self.line_color
            else:
                self.right_wall.line_color = self.background_color
            
            if self.has_top_wall:
                self.top_wall.line_color = self.line_color
            else:
                self.top_wall.line_color = self.background_color

            if self.has_bottom_wall:
                self.bottom_wall.line_color = self.line_color
            else:
                self.bottom_wall.line_color = self.background_color
            
            self.left_wall.draw()
            self.right_wall.draw()            
            self.top_wall.draw()
            self.bottom_wall.draw()
        #else:
            #print("Cannot Cell.draw()! Window is None!")

    def draw_move(self, to_cell, undo=False):
        if undo:
            line_color = "red"
        else:
            line_color = "green"
        line = Line(self.win, self.center_point.x, self.center_point.y, to_cell._center_point.x, to_cell._center_point.y, line_color)
        line.draw()


class Maze:
    def __init__(self,
        win = None,
        x = 0,
        y = 0,
        num_rows = 0,
        num_cols = 0,
        cell_width = 0,
        cell_height = 0,
        line_color = "black",
        background_color = "white",
        seed = None):

        self.win = win
        self.x = x + cell_width / 2 #center x position of upper left cell
        self.y = y + cell_height / 2 #center y position of upper left cell
        self.num_rows = num_rows
        self.num_cols = num_cols
        self.cell_width = cell_width
        self.cell_height = cell_height
        self.line_color = line_color
        self.background_color = background_color
        self.seed = seed
        if seed is not None:
            random.seed(seed)
        self.cells = []
        self.__create_cells()
        self.start_cell = self.cells[0][0]
        self.end_cell = self.cells[-1][-1]
        print(self)
        self.__break_entrance_and_exit()
        self.__break_walls_r(self.start_cell.col,self.start_cell.row)
        self.__reset_cells_visted()

    def __repr__(self):
        to_print = ""
        for j in range(0,self.num_rows):
            for i in range(0,self.num_cols):
                to_print += str(self.cells[i][j])
            to_print += "\n"
        return to_print

    def __create_cells(self):
        #build an array of cells [columns[rows]]
        i = 0
        while i < self.num_cols:
            j = 0
            self.cells.append(list())
            while j < self.num_rows:
                self.cells[i].append(Cell(self.win))
                j += 1
            i += 1

        #draw each cell
        i = 0
        while i < self.num_cols:
            j = 0
            while j < self.num_rows:
                self.__draw_cell(i,j)
                j += 1
            i += 1

    def __draw_cell(self,i,j):
            x = self.x + i * self.cell_width
            y = self.y + j * self.cell_height
            c = self.cells[i][j]
            c.col = j
            c.row = i
            c.center_point = Point(x,y)
            c.width = self.cell_width
            c.height = self.cell_height
            c.line_color = self.line_color
            c.background_color = self.background_color
            c.draw()
            #Center_Mark(self.win, x, y, 6, "violet").draw()
            #self.__animate()

    def __animate(self):
        if self.win is not None:
            self.win.redraw()
            sleep(.01)
        #else:
            #print("Cannot Maze.__animate()! Window is None!")

    def __break_entrance_and_exit(self):
        self.start_cell.has_top_wall = False
        self.start_cell.draw()
        self.__animate()
        self.end_cell.has_bottom_wall = False
        self.end_cell.draw()

    def __break_walls_r(self, i, j):
        current = self.cells[i][j]
        current.visited = True
        up = None
        down = None
        left = None
        right = None

        while True:
            to_visit = []

            if j > 0:
                up = self.cells[i][j-1]
                if not up.visited:
                    to_visit.append(up)
            
            if j < self.num_rows-1:
                down = self.cells[i][j+1]
                if not down.visited:
                    to_visit.append(down)

            if i > 0:
                left = self.cells[i-1][j]
                if not left.visited:
                    to_visit.append(left)

            if i < self.num_cols-1:
                right = self.cells[i+1][j]
                if not right.visited:
                    to_visit.append(right)

            if not to_visit:
                current.draw()
                return
            else:
                print(f"visiting: {current}")
                print(f"possible moves: {to_visit}")
                move_to = random.choice(to_visit)
                print(f"moving: {current} -> {move_to}")
                
                if move_to is up:
                    current.has_top_wall = False
                    current.draw()
                    move_to.has_bottom_wall = False
                    self.__animate()

                if move_to is down:
                    current.has_bottom_wall = False
                    current.draw()
                    move_to.has_top_wall = False
                    self.__animate()
                
                if move_to is left:
                    current.has_left_wall = False
                    current.draw()
                    move_to.has_right_wall = False
                    self.__animate()
                                
                if move_to is right:
                    current.has_right_wall = False
                    current.draw()
                    move_to.has_left_wall = False
                    self.__animate()
                
                self.__break_walls_r(move_to.row, move_to.col)
    
    def __reset_cells_visted(self):
        for i in self.cells:
            for j in i:
                j.visited = False

def main():
        maze_height = 20 #measured in cells
        maze_width = 20 #measured in cells
        cell_size = 25
        win_width = 800
        win_height = 600
        background_color = "black"
        seed = None
        line_color = "gray"
        min_border = 25
    #try:
        win = Window(win_width, win_height, background_color)
        Maze(win, min_border, min_border, maze_height, maze_width, cell_size, cell_size, line_color, background_color, seed)
        win.wait_for_close()

    #except Exception as exc:
    #   messagebox.showerror(message=f"!!SOMETHING WENT WRONG!!\n {exc}")

if __name__ == '__main__':
    main()


