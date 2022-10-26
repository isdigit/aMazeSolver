from textwrap import fill
from time import sleep
from tkinter import CENTER, Tk, BOTH, Canvas, messagebox
from turtle import color, fillcolor


class Window:
    def __init__(self, width, height, canvas_color):
        self._width = width
        self._height = height
        self._root = Tk()
        self._title = "aMazeSolver"
        self._root.title(self._title)
        self.canvas = Canvas(
            self._root,
            height = self._height,
            width = self._width,
            cursor="cross",
            bg = canvas_color)
        self.canvas.pack(fill = "both", expand=True)
        self._window_running = False
        self._root.protocol("WM_DELETE_WINDOW", self.close)

    def redraw(self):
        self._root.update_idletasks()
        self._root.update()

    def wait_for_close(self):
        self._window_running = True
        while self._window_running:
            self.redraw()

    def close(self):
        result = messagebox.askokcancel(f"Close {self._title}","Do you want to exit?")
        if result:
            self._window_running = False
            self._root.destroy()
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
        self._canvas = win.canvas
        self.pnt_1 = Point(x1, y1)
        self.pnt_2 = Point(x2, y2)
        self._line_color = line_color
        self._width = width

    def draw(self):
        self._canvas.create_line(self.pnt_1.x, self.pnt_1.y,
                            self.pnt_2.x, self.pnt_2.y,
                            fill=self._line_color, width=self._width)


class Center_Mark:
    def __init__(self, win, x, y, size, line_color):
        self._win = win
        self._x = x
        self._y = y
        self._size = size / 2
        self._line_color = line_color

    def draw(self):
        Line(self._win, self._x - self._size, self._y - self._size, self._x + self._size, self._y + self._size, self._line_color).draw()
        Line(self._win, self._x - self._size, self._y + self._size, self._x + self._size, self._y - self._size, self._line_color).draw()


class Cell():
    def __init__(self, win, x = 0, y = 0, width = 0, height = 0,
                line_color = "white", line_width = 3,
                left_wall = True, right_wall = True,
                top_wall = True, bottom_wall = True):

        self._win = win
        self._pnt_cntr = Point(x, y) #center point of cell
        self._width = width
        self._height = height
        self._line_color = line_color
        self._line_width = line_width
        self._has_left_wall = left_wall
        self._has_right_wall = right_wall
        self._has_top_wall = top_wall
        self._has_bottom_wall = bottom_wall

    def set_center(self, center_point):
        self._pnt_cntr = center_point
    
    def set_width(self, width):
        self._width = width

    def set_height(self, height):
        self._height = height

    def set_line_color(self, line_color):
        self._line_color = line_color

    def set_line_width(self, line_width):
        self._line_width = line_width

    def get_center(self):
        return self._pnt_cntr

    def _calculate_walls(self):
        self._half_width = self._width / 2
        self._half_height = self._height / 2
        self._pnt_1 = Point(self._pnt_cntr.x - self._half_width, self._pnt_cntr.y - self._half_height) #upper left point of cell
        self._pnt_2 = Point(self._pnt_cntr.x + self._half_width, self._pnt_cntr.y + self._half_height) #lower right point of cell
        self._left_wall = Line(self._win, self._pnt_1.x, self._pnt_1.y, self._pnt_1.x, self._pnt_2.y, self._line_color, self._line_width)
        self._right_wall = Line(self._win, self._pnt_2.x, self._pnt_1.y, self._pnt_2.x, self._pnt_2.y, self._line_color, self._line_width)
        self._top_wall = Line(self._win, self._pnt_1.x, self._pnt_1.y, self._pnt_2.x, self._pnt_1.y, self._line_color, self._line_width)
        self._bottom_wall = Line(self._win, self._pnt_1.x, self._pnt_2.y, self._pnt_2.x, self._pnt_2.y, self._line_color, self._line_width)

    def draw(self):
        self._calculate_walls()
        if self._has_left_wall:
            self._left_wall.draw()
        if self._has_right_wall:
            self._right_wall.draw()
        if self._has_top_wall:
            self._top_wall.draw()
        if self._has_bottom_wall:
            self._bottom_wall.draw()
    
    def draw_move(self, to_cell, undo=False):
        if undo:
            line_color = "red"
        else:
            line_color = "green"
        line = Line(self._win, self._pnt_cntr.x, self._pnt_cntr.y, to_cell._pnt_cntr.x, to_cell._pnt_cntr.y, line_color)
        line.draw()


class Maze:
    def __init__(self,
        win,
        x1,
        y1,
        num_rows,
        num_cols,
        cell_width,
        cell_height,
        line_color):

        self._win = win
        self._x1 = x1 + cell_width / 2 #center x position of upper left cell
        self._y1 = y1 + cell_height / 2 #center y position of upper left cell
        self._num_rows = num_rows
        self._num_cols = num_cols
        self._cell_width = cell_width
        self._cell_height = cell_height
        self._line_color = line_color
        self._cells = []
        self.__create_cells()

    def __create_cells(self):
        #build an array of cells [columns[rows]]
        i = 0
        while i < self._num_cols:
            j = 0
            self._cells.append(list())
            while j < self._num_rows:
                self._cells[i].append(Cell(self._win))
                j += 1
            i += 1

        i = 0
        while i < self._num_cols:
            j = 0
            self._cells.append(list())
            while j < self._num_rows:
                self._draw_cell(i,j)
                j += 1
            i += 1

    def _draw_cell(self,i,j):
        x = self._x1 + i * self._cell_width
        y = self._y1 + j * self._cell_height
        c = self._cells[i][j]
        c.set_center(Point(x,y))
        c.set_width(self._cell_width)
        c.set_height(self._cell_height)
        c.set_line_color(self._line_color)
        c.draw()
        #Center_Mark(self._win, x, y, 6, "violet").draw()
        self._animate()


    def _animate(self):
        self._win.redraw()
        sleep(.1)

class Main():
    #try:
        maze_width=10 #measured in cells
        maze_height=10 #measured in cells
        cell_size = 50
        win_width = 800
        win_height = 600
        canvas_color = "black"        
        line_color = "gray"
        min_border = cell_size
        win = Window(win_width, win_height, canvas_color)
    
        Maze(win, min_border, min_border, maze_width, maze_height, cell_size, cell_size, line_color)

        win.wait_for_close()

    #except Exception as exc:
    #   messagebox.showerror(message=f"!!SOMETHING WENT WRONG!!\n {exc}")

Main()


