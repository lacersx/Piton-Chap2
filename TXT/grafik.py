import tkinter as tk
 
# Sample data points (x, y)
data_points = [(10, 20), (20, 50), (30, 35), (40, 90), (50, 60), (60, 110)]
 
class LineGraphApp:
    def __init__(self, root, data):
        self.root = root
        self.root.title("Line Graph")
 
        self.canvas = tk.Canvas(root, width=400, height=300, bg="white")
        self.canvas.pack()
 
        self.data = data
 
        self.draw_line_graph()
 
    def draw_line_graph(self):
        x_scale = 4  # Scale for x-axis
        y_scale = 2  # Scale for y-axis
        x_offset = 30
        y_offset = 250
 
        # Draw x and y axes
        self.canvas.create_line(x_offset, y_offset, x_offset + 360, y_offset, width=2)
        self.canvas.create_line(x_offset, y_offset, x_offset, y_offset - 250, width=2)
 
        # Draw data points and lines
        for i in range(len(self.data) - 1):
            x1, y1 = self.data[i]
            x2, y2 = self.data[i + 1]
            x1_scaled, y1_scaled = x1 * x_scale + x_offset, y_offset - y1 * y_scale
            x2_scaled, y2_scaled = x2 * x_scale + x_offset, y_offset - y2 * y_scale
            self.canvas.create_oval(x1_scaled - 3, y1_scaled - 3, x1_scaled + 3, y1_scaled + 3, fill="green")
            self.canvas.create_line(x1_scaled, y1_scaled, x2_scaled, y2_scaled, fill="blue", width=2)
 
if __name__ == "__main__":
    root = tk.Tk()
    app = LineGraphApp(root, data_points)
    root.mainloop()
