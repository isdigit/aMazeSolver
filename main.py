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
        self.canvas.pack()#fill = "both")
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
        self.x = None #where 0 is the left of the screen
        self.y = None #where 0 is the top of the screen

class Line:
    def __init__(self):
        self.x1 = None
        self.y1 = None
        self.x2 = None
        self.y3 = None
        self.fill_color = None
        self.width = None

    def draw(self, canvas, x1, y1, x2, y2, fill_color = "black", width = 2):
        canvas.create_line(x1, y1, x2, y2, fill=fill_color, width=2)

def main():
    try:
        win = Window(800,600)
        Line().draw(win.canvas, 0, 0, 800, 600)
        Line().draw(win.canvas, 0, 600, 800, 0)
        Line().draw(win.canvas, 0,300,800,300)
        Line().draw(win.canvas, 400,0,400,600)
        win.wait_for_close()
    except Exception as exc:
        print(f"!!SOMETHING WENT WRONG!!/N{exc}")

main()


