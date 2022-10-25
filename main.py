from tkinter import CENTER, Tk, BOTH, Canvas, messagebox

class Window:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.root = Tk()
        self.title = "aMazeSolver"
        self.root.title(self.title)
        self.canvas = Canvas(
            self.root,
            height = self.height,
            width = self.width,
            cursor="cross")
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


class Line:
    def __init__(self, win, x1, y1, x2, y2, line_color = "black", width = 2):
        self._win = win
        self.pnt_1 = Point(x1, y1)
        self.pnt_2 = Point(x2, y2)
        self._line_color = line_color
        self._width = width

    def draw(self):
        self._win.create_line(self.pnt_1.x, self.pnt_1.y,
                            self.pnt_2.x, self.pnt_2.y,
                            fill=self._line_color, width=self._width)

class Cell():
    def __init__(self, win, row, col, x1, y1, x2, y2,
                left_wall = True, right_wall = True,
                top_wall = True, bottom_wall = True,
                line_color="black", line_width = 2):
        
        self._win = win
        self.row = row
        self.col = col
        self._pnt_1 = Point(x1, y1)
        self._pnt_2 = Point(x2, y2)
        self._line_color = line_color
        self._line_width = line_width
        self._left_wall = Line(self._win, self._pnt_1.x, self._pnt_1.y, self._pnt_1.x, self._pnt_2.y, self._line_color, self._line_width)
        self._right_wall = Line(self._win, self._pnt_2.x, self._pnt_1.y, self._pnt_2.x, self._pnt_2.y, self._line_color, self._line_width)
        self._top_wall = Line(self._win, self._pnt_1.x, self._pnt_1.y, self._pnt_2.x, self._pnt_1.y, self._line_color, self._line_width)
        self._bottom_wall = Line(self._win, self._pnt_1.x, self._pnt_2.y, self._pnt_2.x, self._pnt_2.y, self._line_color, self._line_width)
        self.has_left_wall = left_wall
        self.has_right_wall = right_wall
        self.has_top_wall = top_wall
        self.has_bottom_wall = bottom_wall

    def draw(self):
        if self.has_left_wall:
            self._left_wall.draw()
        if self.has_right_wall:
            self._right_wall.draw()
        if self.has_top_wall:
            self._top_wall.draw()
        if self.has_bottom_wall:
            self._bottom_wall.draw()

def main():
    try:
        grid_width=20
        grid_height=20
        cell_size = 25
        win_width = 800
        win_height = 600
        min_border = cell_size
        win = Window(win_width,win_height)
        cells=[]

    #build a list of cells
        i = 0
        while i < grid_width:
            j = 0
            while j < grid_height:
                x1 = min_border+i*cell_size
                y1 = min_border+j*cell_size
                x2 = min_border+i*cell_size+cell_size
                y2 = min_border+j*cell_size+cell_size
                cells.append(Cell(win.canvas, j, i, x1, y1, x2, y2))
                j += 1
            i += 1

     #draw all cells
        for c in cells:
            c.draw()

        win.wait_for_close()

    except Exception as exc:
        messagebox.showerror(message=f"!!SOMETHING WENT WRONG!!\n {exc}")

main()


