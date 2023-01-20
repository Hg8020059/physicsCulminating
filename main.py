import tkinter as tk
import tkinter.messagebox
import math

# Variables
boxes = []
boxSize = []
boxMass = []
boxNumberDisplay = []
boxSpeedY = []
boxSpeedX = []
boxHeight = []
frictionCoefficient = []
frictionAccel = []
boxNumber = 0
boxHeld = None
holdingBox = False
simulating = False
gravityAccel = 0.1225
gValue = 9.8
simulTime = 0
selectedTab = None
selectedBox = None
xStartSpeed = 0
yStartSpeed = 0

def create_box():
    global boxNumber
    boxSize.append(massSlider.get() * 20)
    boxMass.append(massSlider.get())
    frictionCoefficient.append(frictionCoeffSlider.get())
    frictionAccel.append(frictionCoefficient[boxNumber] * gValue * 0.0125)
    boxSpeedY.append(0)
    boxSpeedX.append(0)
    update_option_menu(boxNumber)
    boxes.append(canvas.create_rectangle(canvasWidth / 2, canvasHeight / 2, canvasWidth / 2 + boxSize[boxNumber],
                                         canvasHeight / 2 + boxSize[boxNumber], fill="grey"))
    boxNumberDisplay.append(canvas.create_text(canvas.coords(boxes[boxNumber])[0] + boxSize[boxNumber] / 2,
                                               canvas.coords(boxes[boxNumber])[1] + boxSize[boxNumber] / 2,
                                               text=boxNumber + 1, fill="White", font="lucida 15"))
    boxHeight.append(round((canvasHeight - canvas.coords(boxes[boxNumber])[3])/20, 2))
    boxNumber += 1

def update_option_menu(boxNumber):
    global selectedTab
    global selectedBox
    boxNumber += 1
    menu.add_command(label='Box ' + str(boxNumber), command=lambda: menu_label_change(boxNumber))

def menu_label_change(boxNumber):
    global selectedBox
    menubutton.config(text="Box" + str(boxNumber))
    selectedBox = boxNumber - 1
    update_speedY_label()
    update_speedX_label()
    update_speed_label()
    update_height_label()
    update_mass_label()
    update_coeff_label()
    update_kinetic_label()
    update_grav_label()
    addXSpeed.config(bg="Red")
    addYSpeed.config(bg="Red")

def delete_boxes():
    global boxNumber
    global selectedBox
    for j in range(len(boxes)):
        canvas.delete(boxes[j])
        canvas.delete(boxNumberDisplay[j])
    menu.delete(2, "end")
    menubutton.config(text="Select Box")
    boxSize.clear()
    boxMass.clear()
    boxes.clear()
    boxNumberDisplay.clear()
    boxSpeedY.clear()
    boxSpeedX.clear()
    boxHeight.clear()
    boxNumber = 0
    selectedBox = None

def move_box(event):
    global holdingBox
    global boxHeld
    if holdingBox:
        canvas.moveto(boxes[boxHeld], event.x - boxSize[boxHeld] / 2,
                      event.y - boxSize[boxHeld] / 2)  # Box held starts as a none, will be assigned later
        canvas.moveto(boxNumberDisplay[boxHeld], event.x - 7, event.y - 7)
        boxHeight[boxHeld] = round((canvasHeight - canvas.coords(boxes[boxHeld])[3])/20, 2)

        if selectedBox == boxHeld:
            update_height_label()
            update_grav_label()


def grab_box(event):
    global holdingBox
    global boxHeld
    holdingBox = True
    for i in range(len(boxes)):
        if canvas.coords(boxes[i])[0] <= event.x <= canvas.coords(boxes[i])[2]:
            if canvas.coords(boxes[i])[1] <= event.y <= canvas.coords(boxes[i])[3]:
                boxHeld = i


def drop_box(event):
    global holdingBox
    global boxHeld
    holdingBox = False
    boxHeld = None

def x_speed_entered(event):
    try:
        if event.keysym == "Return":
            addXSpeed.config(bg="Green")
            boxSpeedX[selectedBox] = float(addXSpeed.get())/2
            update_speedX_label()
        else:
            addXSpeed.config(bg="Red")
    except TypeError:
        tk.messagebox.showerror(title="Error", message="No Box Selected")
        addXSpeed.config(bg="Red")
    except ValueError:
        tk.messagebox.showerror(title="Error", message="Not a number")
        addXSpeed.config(bg="Red")

def y_speed_entered(event):
    try:
        if event.keysym == "Return":
            addYSpeed.config(bg="Green")
            boxSpeedY[selectedBox] = float(addYSpeed.get())/-2
            update_speedY_label()
        else:
            addYSpeed.config(bg="Red")
    except TypeError:
        tk.messagebox.showerror(title="Error", message="No Box Selected")
        addXSpeed.config(bg="Red")
    except ValueError:
        tk.messagebox.showerror(title="Error", message="Not a number")
        addXSpeed.config(bg="Red")

def update_speedX_label():
    boxXSpeedLabel.config(text=f"Box Speed X: {boxSpeedX[selectedBox] * 2:.2f} m/s")
def update_speedY_label():
    boxYSpeedLabel.config(text=f"Box Speed Y: {boxSpeedY[selectedBox] * -2:.2f} m/s")
def update_speed_label():
    boxSpeedLabel.config(text=f"Total Speed: {math.sqrt(abs((boxSpeedX[selectedBox]*2)**2) + abs((boxSpeedY[selectedBox] * 2)**2)):.2f}")
def update_height_label():
    boxHeightLabel.config(text=f"Box Height: {boxHeight[selectedBox]:.2f} m")
def update_mass_label():
    boxMassLabel.config(text=f"Box Mass: {boxMass[selectedBox]:.2f} kg")
def update_kinetic_label():
    boxKineticLabel.config(text=f"Kinetic Energy: {0.5 * boxMass[selectedBox] * (boxSpeedY[selectedBox] * 2) ** 2:.2f} J")
def update_grav_label():
    boxGravLabel.config(text= f"Gravitational Energy: {boxMass[selectedBox] * gValue * boxHeight[selectedBox]:.2f} J")
def update_coeff_label():
    boxFricLabel.config(text= f"Friction Coefficient: {frictionCoefficient[selectedBox]:.2f}")

def space_check(event):
    if event.keysym == "space":
        toggle_simul()

def toggle_simul():
    global simulating
    global simulTime
    global xStartSpeed
    global yStartSpeed
    if simulating:  # Stop simulation
        runTimeLast.config(text= "Previous Run: " + f'{simulTime:.2f}' + " s")
        simulTime = 0
        simulating = False
        toggleSimulButton.config(text="Start Simulation")
    elif not simulating:  # start simulation
        simulTime = 0
        simulating = True
        toggleSimulButton.config(text="Stop Simulation")
        addXSpeed.config(bg="Red")
        addYSpeed.config(bg="Red")
        mainloop()

def mainloop():
    global simulTime
    global selectedBox
    for i in range(len(boxes)):
        canvas.move(boxes[i], boxSpeedX[i], boxSpeedY[i])
        canvas.move(boxNumberDisplay[i], boxSpeedX[i], boxSpeedY[i])
        if round(canvas.coords(boxes[i])[3]) - 1 == canvasHeight:
            if boxSpeedX[i] > 0:
                boxSpeedX[i] -= frictionAccel[i]
                boxSpeedX[i] = max(boxSpeedX[i], 0)
                canvas.move(boxes[i], boxSpeedX[i], 0)
                canvas.move(boxNumberDisplay[i], boxSpeedX[i], 0)
            elif boxSpeedX[i] < 0:
                boxSpeedX[i] += frictionAccel[i]
                boxSpeedX[i] = min(boxSpeedX[i], 0)
                canvas.move(boxes[i], boxSpeedX[i], 0)
                canvas.move(boxNumberDisplay[i], boxSpeedX[i], 0)
        elif canvas.coords(boxes[i])[3] + boxSpeedY[i] > canvasHeight:  # Hit ground
            canvas.moveto(boxes[i], canvas.coords(boxes[i])[0]-1, canvasHeight - boxSize[i])
            canvas.moveto(boxNumberDisplay[i], canvas.coords(boxes[i])[0]-1 + boxSize[i] / 2 - 7, canvas.coords(boxes[i])[1] + boxSize[i] / 2 - 7)
            boxSpeedY[i] = 0
        else:
            boxSpeedY[i] += gravityAccel
        # Hit right wall
        if canvas.coords(boxes[i])[2] + boxSpeedX[i] > canvasWidth:
            canvas.moveto(boxes[i], canvasWidth - boxSize[i], round(canvas.coords(boxes[i])[1]) - 1)
            canvas.moveto(boxNumberDisplay[i], canvas.coords(boxes[i])[0]-1 + boxSize[i] / 2 - 7, canvas.coords(boxes[i])[1] + boxSize[i] / 2 - 7)
            boxSpeedX[i] = 0
        # Hit left wall
        if canvas.coords(boxes[i])[0] + boxSpeedX[i] < 0:
            canvas.moveto(boxes[i], 0, round(canvas.coords(boxes[i])[1]) - 1)
            canvas.moveto(boxNumberDisplay[i], canvas.coords(boxes[i])[0] - 1 + boxSize[i] / 2 - 7, canvas.coords(boxes[i])[1] + boxSize[i] / 2 - 7)
            boxSpeedX[i] = 0
        # Hit roof
        if canvas.coords(boxes[i])[1] + boxSpeedY[i] < 0:
            canvas.moveto(boxes[i], canvas.coords(boxes[i])[0]-1, 0)
            canvas.moveto(boxNumberDisplay[i], canvas.coords(boxes[i])[0] - 1 + boxSize[i] / 2 - 7, canvas.coords(boxes[i])[1] + boxSize[i] / 2 - 7)
            boxSpeedY[i] = 0

    # This lets the program simulate properly without having a box selected
    try:
        update_speedX_label()
        update_speedY_label()
        update_speed_label()
        update_height_label()
        update_kinetic_label()
        update_grav_label()
    except:
        pass
    runTimeLabel.config(text="Running Time: " + f'{simulTime:.2f}' + " s")
    simulTime += 0.025
    if simulating:
        root.after(25, mainloop)


# Initialize window
root = tk.Tk()
screenWidth = root.winfo_screenwidth()
screenHeight = root.winfo_screenheight()
root.attributes('-fullscreen', True)

# Canvas
canvasWidth = screenWidth - 250
canvasHeight = screenHeight
canvas = tk.Canvas(root, bg='Black', width=canvasWidth, height=canvasHeight)
canvas.pack(side=tk.LEFT)

# Exit button
exitButton = tk.Button(root, text="Exit", relief='solid', borderwidth=2, command=lambda: quit())
exitButton.pack(side=tk.TOP, anchor=tk.E, fill=tk.X, padx=5, pady=2)
# Create Box
boxButton = tk.Button(root, text="New Box", relief='solid', borderwidth=2, command=create_box)
boxButton.pack(side=tk.TOP, anchor=tk.E, fill=tk.X, padx=5, pady=2)
# Mass Slider Label
massSliderLabel = tk.Label(root, text="Box Mass", font="lucida 12")
massSliderLabel.pack(side=tk.TOP, anchor=tk.E, fill=tk.X, padx=5)
# Mass slider
massSlider = tk.Scale(root, from_=1, to=10, orient=tk.HORIZONTAL)
massSlider.pack(side=tk.TOP, anchor=tk.E, fill=tk.X, padx=5)
# Friction coefficient Label
frictionCoeffLabel = tk.Label(root, text="Friction Coefficient", font="lucida 12")
frictionCoeffLabel.pack(side=tk.TOP, anchor=tk.E, fill=tk.X, padx=5)
# Friction Coefficient Slider
frictionCoeffSlider = tk.Scale(root, from_=0, to=1, orient=tk.HORIZONTAL, resolution=0.01)
frictionCoeffSlider.pack(side=tk.TOP, anchor=tk.E, fill=tk.X, padx=5)

# Delete Boxes
deleteBoxesButton = tk.Button(root, text="Delete Boxes", relief='solid', borderwidth=2, command=delete_boxes)
deleteBoxesButton.pack(side=tk.TOP, anchor=tk.E, fill=tk.X, padx=5, pady=4)
# Start Simulation Button
toggleSimulButton = tk.Button(root, text="Start Simulation", relief='solid', borderwidth=2, command=toggle_simul)
toggleSimulButton.pack(side=tk.TOP, anchor=tk.E, fill=tk.X, padx=5, pady=4)

# menubutton
menubutton = tk.Menubutton(root, text='Select Box', relief='solid', borderwidth=2)
menubutton.pack(side=tk.TOP, anchor=tk.E, fill=tk.X, padx=5, pady=2)
menu = tk.Menu(menubutton)
menubutton.config(menu=menu)
menu.add_command(label='Select Box', command= update_option_menu)

# Enter speed
# XSpeed
addXSpeedLabel = tk.Label(root, text="Enter X Speed", font="lucida 12")
addXSpeedLabel.pack(side=tk.TOP, anchor=tk.E, fill=tk.X, padx=5, pady=2)
addXSpeed = tk.Entry(root, font = "lucida 10", bg="Red")
addXSpeed.pack(side=tk.TOP, anchor=tk.E, fill=tk.X, padx=5, pady=2)
# YSpeed
addYSpeedLabel = tk.Label(root, text="Enter Y Speed", font="lucida 12")
addYSpeedLabel.pack(side=tk.TOP, anchor=tk.E, fill=tk.X, padx=5, pady=2)
addYSpeed = tk.Entry(root, font = "lucida 10", bg="Red")
addYSpeed.pack(side=tk.TOP, anchor=tk.E, fill=tk.X, padx=5, pady=2)

# Box information
# SpeedXY
boxXSpeedLabel = tk.Label(root, text="Box Speed Y: ", font="lucida 10")
boxXSpeedLabel.pack(side=tk.TOP, anchor=tk.E, pady=2, fill= tk.X)
boxYSpeedLabel = tk.Label(root, text="Box Speed X: ", font="lucida 10")
boxYSpeedLabel.pack(side=tk.TOP, anchor=tk.E, pady=2, fill= tk.X)
# total Speed
boxSpeedLabel = tk.Label(root, text="Total Speed: ", font="lucida 10")
boxSpeedLabel.pack(side=tk.TOP, anchor=tk.E, pady=2, fill= tk.X)
# Distance from ground
boxHeightLabel = tk.Label(root, text="Box Height: ", font="lucida 10")
boxHeightLabel.pack(side=tk.TOP, anchor=tk.E, pady=2, fill= tk.X)
# Mass
boxMassLabel = tk.Label(root, text="Box Mass: ", font="lucida 10")
boxMassLabel.pack(side=tk.TOP, anchor=tk.E, pady=2, fill= tk.X)
# Friction Coefficient
boxFricLabel = tk.Label(root, text="Friction Coefficient: ", font="lucida 10")
boxFricLabel.pack(side=tk.TOP, anchor=tk.E, pady=2, fill= tk.X)
# Kinetic Energy
boxKineticLabel = tk.Label(root, text="Kinetic Energy: ", font="lucida 10")
boxKineticLabel.pack(side=tk.TOP, anchor=tk.E, pady=2, fill= tk.X)
# Gravitational Energy
boxGravLabel = tk.Label(root, text="Gravitational Energy: ", font="lucida 10")
boxGravLabel.pack(side=tk.TOP, anchor=tk.E, pady=2, fill= tk.X)

# Running time
runTimeLabel = tk.Label(root, text = "Running Time: ", font="lucida 10")
runTimeLabel.pack(side=tk.BOTTOM, anchor=tk.E, pady=2, fill= tk.X)
# Last run
runTimeLast = tk.Label(root, text= "Previous Run: ", font="lucida 10")
runTimeLast.pack(side=tk.BOTTOM, anchor=tk.E, pady=2, fill= tk.X)

canvas.bind('<Button>', grab_box)
canvas.bind('<ButtonRelease>', drop_box)
canvas.bind('<Motion>', move_box)
addXSpeed.bind('<KeyPress>', x_speed_entered)
addYSpeed.bind('<KeyPress>', y_speed_entered)
root.bind('<KeyPress>', space_check)

root.mainloop()
