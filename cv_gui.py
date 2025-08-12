import tkinter as tk    
from tkinter import *
from tkinter import filedialog  #module to open files
from tkinter import messagebox  #allows for error messages/popups
import matplotlib.pyplot as plt #graph plotting
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np  
from cv_simulation import simulate  #imports simulation function

class CV_GUI():
    def __init__(self, root):
        self.root = root
        self.root.title("Cyclic Voltammetry GUI")
        self.root.geometry("750x500")

        # Create left and right frames, left frame for buttons/labels and right frame to contain graph
        #graph configurations
        self.left_frame = Frame(root)
        self.left_frame.pack(side=LEFT, padx=10, pady=10)

        self.right_frame = Frame(root)
        self.right_frame.pack(side=LEFT, padx=10, pady=10)

    
        self.figure = plt.Figure(figsize=(5, 4), dpi=100)
        self.ax = self.figure.add_subplot(111)
        self.ax.set_title("Cyclic Voltammetry")
        self.ax.set_xlabel("Potential (V vs Ag/Ag+)")
        self.ax.set_ylabel("Current (mA)")
        self.ax.grid(True)
        self.ax.legend(loc='upper left') #legend
        self.canvas = FigureCanvasTkAgg(self.figure, master=self.right_frame)
        self.canvas.get_tk_widget().pack(padx=10, pady=10)
        #end of graph configurations
        
        self.params = {}    #dictionary to store when you enter parameters
        self.entries = []   #list for temporarily storing entries when you use .get(), cleared every time new params are entered. makes it so dont need separate variable for each entry
        self.data_storage = []  #supposed to store plotted datasets

        # Menu bar setup
        self.menubar = tk.Menu(self.root)
        self.file_menu = tk.Menu(self.menubar, tearoff=0)
        self.file_menu.add_command(label="Set Parameters", command=self.param_menu)
        self.file_menu.add_separator()
        self.file_menu.add_command(label="Exit", command=self.root.quit)
        self.menubar.add_cascade(label="Files", menu=self.file_menu)

        self.root.config(menu=self.menubar)

        tk.Button(self.left_frame, text="Import", command=self.import_data).grid(row=5, column=0, pady=5)
        tk.Button(self.left_frame, text="Simulate", command=self.run_simulation).grid(row=4, column=0, pady=5) 
        tk.Button(self.left_frame, text="Delete Graph", command=self.clear_graph).grid(row=7, column=0, pady=5)

    def run_simulation(self):
        required_keys = ["E0", "Da", "Db", "k0", "alpha"]
        if not all(k in self.params for k in required_keys):
            messagebox.showerror("Missing parameters", "Please set all parameters first.")
            return

        fig = simulate(self.params["E0"], self.params["Da"], self.params["Db"], self.params["k0"], self.params["alpha"])

        # self.canvas.get_tk_widget().destroy()
        # self.figure = fig
        # self.canvas = FigureCanvasTkAgg(self.figure, master=self.right_frame)
        # self.canvas.get_tk_widget().pack(padx=10, pady=10)
        # self.canvas.draw()


    def param_menu(self):
        self.popup = Toplevel(self.root)
        self.popup.title("Set Parameters")

        labels = [
            "Standard potential (V)", "Diffusion concentration (oxidation)", "Diffusion concentration (reduction)", 
            "Standard rate constant (cm/s)",
            "Transfer coefficient (alpha)"]
        
        keys = ["E0", "Da", "Db", "k0", "alpha"]

        # Clear old entries list before adding new ones
        self.entries.clear()

        # Header row
        Label(self.popup, text="Parameter").grid(row=0, column=0, padx=5, pady=3)
        Label(self.popup, text="Current Value").grid(row=0, column=1, padx=5, pady=3)
        Label(self.popup, text="New Value").grid(row=0, column=2, padx=5, pady=3)

        # Fill in parameter rows
        for i, (label, key) in enumerate(zip(labels, keys), start=1):
            Label(self.popup, text=label).grid(row=i, column=0, sticky="e", padx=5, pady=3)

            # Show current value or "N/A" if not set
            current_val = self.params.get(key, "N/A")
            Label(self.popup, text=str(current_val)).grid(row=i, column=1, padx=5, pady=3)

            # Entry for new value
            entry = Entry(self.popup)
            entry.grid(row=i, column=2, padx=5, pady=3)
            self.entries.append((key, entry))  # store both key and entry for saving

        Button(self.popup, text="Save", command=self.store_params).grid(
            row=len(labels) + 1, column=0, columnspan=3, pady=10
        )


    def store_params(self):
        ranges = [(-0.5, 0.5), ((1*10^-9), 10*(10^-9)), ((1*10^-9), 10*(10^-9)), (1*(10^-2), 1*(10^-6)), (0, 1)]
        range_map = dict(zip(["E0", "Da", "Db", "k0", "alpha"], ranges))

        for key, entry in self.entries:
            new_val = entry.get().strip()
            if new_val == "":
                continue  # skip empty entries, keep old value

            try:
                value = float(new_val)
            except ValueError:
                messagebox.showerror("Invalid Input", f"Value for {key} must be a number.")
                return

            low, high = range_map[key]
            if not (low <= value <= high):
                messagebox.showerror("Invalid Range", f"{key} must be between {low} and {high}.")
                return


            self.params[key] = value

        self.popup.destroy()



    def import_data(self):
        filepath = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt")])  #opens files app
        if not filepath:    
            return

        try:
            data = np.loadtxt(filepath, skiprows=1)  #Skip the header row
            V, I = data[:, 0], data[:, 1]             #parses through columns
        except Exception as e:  #error popup if file doesn't load
            messagebox.showerror("Import Error", f"Failed to load file: {e}")
            return

        self.ax.plot(V, I, '--', label="Experimental")
        self.ax.legend()
        self.canvas.draw()
        self.data_storage.append((V, I))    #stores data for future fitting

    # def fit_data(self): butler volmer? //euler

    def clear_graph(self):  # clears grids as well (fix)
        self.ax.clear()
        self.canvas.draw() 
        self.data_storage.clear()   #clears any pre existing data so that you don't regraph it

   

root = tk.Tk()
app = CV_GUI(root)
root.mainloop()



# to do: figure out simulation graphing simulation on graph


# show theoreotical graph with experimental

#numerical method
# non-linear least squares 
# scipy.optimize least squares
# works with nonlinear least squares
# lavenberg

# for ML: use bayesian optimization, there is library for this

# learning bayesian optimization, implement in the code
# experimental to theoretical? 

# 11:30 meeting 8/20 