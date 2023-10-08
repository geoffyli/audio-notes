from tkinter import *

root = Tk()
root.title("Profile Entry using Grid")
root.geometry("500x300")  # set starting size of window
root.maxsize(500, 300)  # width x height
root.config(bg="lightgrey")

# Enter specific information for your profile into the following widgets
enter_info = Label(root, text="Please enter your information: ", bg="lightgrey")
enter_info.grid(row=0, column=1, columnspan=4, padx=5, pady=5)

# Name label and entry widgets
Label(root, text="Name", bg="lightgrey").grid(row=1, column=1, padx=5, pady=5, sticky=E)

name = Entry(root, bd=3)
name.grid(row=1, column=2, padx=5, pady=5)

# Gender label and dropdown widgets
gender = Menubutton(root, text="Gender")
gender.grid(row=2, column=2, padx=5, pady=5, sticky=W)
gender.menu = Menu(gender, tearoff=0)
gender["menu"] = gender.menu

# choices in gender dropdown menu
gender.menu.add_cascade(label="Male")
gender.menu.add_cascade(label="Female")
gender.menu.add_cascade(label="Other")
gender.grid()

# Eyecolor label and entry widgets
Label(root, text="Eye Color", bg="lightgrey").grid(row=3, column=1, padx=5, pady=5, sticky=E)
eyes = Entry(root, bd=3)
eyes.grid(row=3, column=2, padx=5, pady=5)

# Height and Weight labels and entry widgets
Label(root, text="Height", bg="lightgrey").grid(row=4, column=1, padx=5, pady=5, sticky=E)
Label(root, text="inches", bg="lightgrey").grid(row=4, column=3, sticky=W)

height = Entry(root, bd=3)
height.grid(row=4, column=2, padx=5, pady=5)

Label(root, text="Weight", bg="lightgrey").grid(row=5, column=1, padx=5, pady=5, sticky=E)
Label(root, text="lbs", bg="lightgrey").grid(row=5, column=3, sticky=W)

weight = Entry(root, bd=3)
weight.grid(row=5, column=2, padx=5, pady=5)

root.mainloop()