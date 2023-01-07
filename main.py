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
    def __init__(self, win, x1, y1, x2, y2, line_color, width = 3):
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


class Center_Mark:
    def __init__(self, win, cell, size, line_color):
        self.win = win
        self.x = cell.center_point.x
        self.y = cell.center_point.y
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

    def draw_move(self, to_cell, undo=False):
        if undo:
            line_color = "red"
        else:
            line_color = "green"
        line = Line(self.win,
            self.center_point.x,
            self.center_point.y,
            to_cell.center_point.x,
            to_cell.center_point.y,
            line_color)

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
        #print(self)
        self.__break_entrance_and_exit()
        self.__break_walls_r(self.start_cell)
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
            c.col = i
            c.row = j
            c.center_point = Point(x,y)
            c.width = self.cell_width
            c.height = self.cell_height
            c.line_color = self.line_color
            c.background_color = self.background_color
            c.draw()
            #self.__animate()

    def __animate(self,time_interval = .005):
        
        
        if self.win is not None and time_interval > 0:
            self.win.redraw()
            sleep(time_interval)

    def __break_entrance_and_exit(self):
        self.start_cell.has_top_wall = False
        self.start_cell.draw()
        self.__animate()
        self.end_cell.has_bottom_wall = False
        self.end_cell.draw()

    def __break_walls_r(self, cell):
        current_cell = cell
        current_cell.visited = True

        while True:
            to_visit = []

            if current_cell.row > 0:
                up = self.cells[current_cell.col][current_cell.row-1]
                if not up.visited:
                    to_visit.append(up)
            else:
                up = None
            
            if current_cell.row < self.num_rows-1:
                down = self.cells[current_cell.col][current_cell.row+1]
                if not down.visited:
                    to_visit.append(down)
            else:
                down = None

            if current_cell.col > 0:
                left = self.cells[current_cell.col-1][current_cell.row]
                if not left.visited:
                    to_visit.append(left)
            else:
                left = None

            if current_cell.col < self.num_cols-1:
                right = self.cells[current_cell.col+1][current_cell.row]
                if not right.visited:
                    to_visit.append(right)
            else:
                right = None

            if not to_visit:
                current_cell.draw()
                return
            else:
                #print(f"visiting: {current_cell}")
                #print(f"possible moves: {to_visit}")
                move_to = random.choice(to_visit)
                #print(f"moving: {current_cell} -> {move_to}")

                if move_to is down:
                    current_cell.has_bottom_wall = False
                    current_cell.draw()
                    move_to.has_top_wall = False
                
                if move_to is left:
                    current_cell.has_left_wall = False
                    current_cell.draw()
                    move_to.has_right_wall = False

                if move_to is up:
                    current_cell.has_top_wall = False
                    current_cell.draw()
                    move_to.has_bottom_wall = False

                if move_to is right:
                    current_cell.has_right_wall = False
                    current_cell.draw()
                    move_to.has_left_wall = False

                self.__animate(.000001)                
                self.__break_walls_r(move_to)
    
    def __reset_cells_visted(self):
        for i in self.cells:
            for j in i:
                j.visited = False

    def __solve_r(self, cell):
        current_cell = cell
        current_cell.visited = True
        self.__animate()

        if current_cell is self.end_cell:
            Center_Mark(self.win,current_cell,min(current_cell.width,current_cell.height)/2,"green").draw()
            return True
        
        #Check outer boundaries
        if current_cell.row > 0:
            up = self.cells[current_cell.col][current_cell.row-1]
        else:
            up = None
        
        if current_cell.row < self.num_rows-1:
            down = self.cells[current_cell.col][current_cell.row+1]
        else:
            down = None
        
        if current_cell.col > 0:
            left = self.cells[current_cell.col-1][current_cell.row]
        else:
            left = None

        if current_cell.col < self.num_cols-1:
            right = self.cells[current_cell.col+1][current_cell.row]
        else:
            right = None

		#Check direction for obstructions then move if there are none
        if down is not None and not down.has_top_wall and not down.visited:
            current_cell.draw_move(down)
            #print(f"drawing down: {current_cell} -> {down}")
            if self.__solve_r(down):
                return True
            down.draw_move(current_cell, True)
                
        if right is not None and not right.has_left_wall and not right.visited:
            current_cell.draw_move(right)
            #print(f"drawing right: {current_cell} -> {right}")
            if self.__solve_r(right):
                return True
            right.draw_move(current_cell, True)

        if left is not None and not left.has_right_wall and not left.visited:
            current_cell.draw_move(left)
            #print(f"drawing left: {current_cell} -> {left}")
            if self.__solve_r(left):
                return True
            left.draw_move(current_cell, True)

        if up is not None and not up.has_bottom_wall and not up.visited:
            current_cell.draw_move(up)
            #print(f"drawing up: {current_cell} -> {up}")
            if self.__solve_r(up):
                return True
            up.draw_move(current_cell, True)
        
        return False

    def solve(self):
        return self.__solve_r(self.start_cell)
    

def main(maze_height = 40,
        maze_width = 40,
        cell_width = 15,
        cell_height = 15,
        win_width = 700,
        win_height = 700,
        background_color = "black",
        seed = None,
        line_color = "gray",
        min_border = 25,
        repeat = 5):
        
        maze_height = maze_height #measured in cells
        maze_width = maze_width #measured in cells
        cell_width = cell_width
        cell_height = cell_height
        win_width = win_width
        win_height = win_height
        background_color = background_color
        seed = seed
        line_color = line_color
        min_border = min_border
        repeat = repeat
        
        try:
            win = Window(win_width, win_height, background_color)
            for x in range(repeat):
                maze = Maze(win, min_border, min_border, maze_height, maze_width, cell_width, cell_height, line_color, background_color, seed)
                sleep(1)
                maze.solve()
                sleep(5)
                win.canvas.delete("all")
            	
            win.wait_for_close()
        except Exception as exc:
            messagebox.showerror(message=f"!!SOMETHING WENT WRONG!!\n {exc}")

if __name__ == '__main__':
    main()
