import tkinter as tk

class ScrollableFrame(tk.Frame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        self.canvas = tk.Canvas(self)
        self.scrollbar = tk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = tk.Frame(self.canvas)

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )

        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")

        self.bind_arrow_keys()

    def scroll_up(self, event):
        self.canvas.yview_scroll(-1, "units")  # Scroll up by a small increment

    def scroll_down(self, event):
        self.canvas.yview_scroll(1, "units")  # Scroll down by a small increment

    def bind_arrow_keys(self):
        self.scrollable_frame.bind("<Up>", self.scroll_up)
        self.scrollable_frame.bind("<Down>", self.scroll_down)
        self.scrollable_frame.focus_set()  # Set focus to enable key bindings

# Usage
root = tk.Tk()
sf = ScrollableFrame(root)
sf.pack(fill="both", expand=True)

# Add some content to the frame
for i in range(50):
    tk.Label(sf.scrollable_frame, text="Sample Label " + str(i)).pack()

root.mainloop()
