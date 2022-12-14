import os
from urllib.request import urlopen
import ssl
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
import json
from scipy.optimize import curve_fit

#Define constants
MU = 1.66053906660E-27  #kg
C = 2.9979245800E10     #cm / s
EH = 4.359744722207E-18 #J

def welcome_message():
    print("----------------")
    print("Triatomic Energy Plotter and Calculator")

def commands():
    print("----------------")
    print("Available commands:\n")
    print("local\tinput data from files stored locally")
    print("web\tinput data retrieved from a specified URL")
    print("help\tdisplay this list of commands")
    print("quit\texits the program")

def command_input(default=False):

    #Shortcut for debugging purposes
    if default:
        return values_from_local_file(default=True)

    #Parse user command
    valid = False
    while not valid:
        command = input("").lower().strip()
        if command == "local":
            return values_from_local_file()
        elif command == "web":
            return values_from_web_file()
        elif command == "help":
            commands()
        elif command == "quit":
            exit()
        else:
            print("Invalid command")

def values_from_local_file(default=False):

    #Display list of found directories
    files = os.listdir(os.getcwd() + "\outfiles")
    print("----------------")
    print("Found the following subdirectories in the \outfiles directory:")
    for file in files:
        print(file)
    print("Please enter the name of the molecule you would like to process:")
    print("(e.g. 'H2O', 'H2S. do NOT include the 'outfiles' part)")

    #Get user input and check it is valid
    if not default:
        while True:
            s = input("").strip()
            if (s + "outfiles") in files:
                break
            else:
                print("Subdirectory not found")
    else:
        s="H2O"     #Default for testing purposes
    
    """
    Generate a 2-dimensional array of energy values by parsing the appropriate
    file.
    """
    get_parameter_ranges(s)
    e_array = np.empty((RSIZE, TSIZE))

    for i in range(RSIZE):
        r = R_RANGE[i]
        for j in range(TSIZE):
            theta = T_RANGE[j]
            directory = os.getcwd()+"\\outfiles\\"+s+"outfiles\\"+s+\
                ".r%.2ftheta%.1f.out" % (r, theta)
            with open(directory, "r") as f:
                e = extract_energy_from_file(f)
                e_array[i][j] = e
    return e_array

def values_from_web_file():
    
    #I have no idea what this does but I was getting errors without it
    context = ssl._create_unverified_context()

    print("----------------")

    input_complete = False
    while not input_complete:
        try:
            print("Please enter the URL of the directory \
                containing the input files")
            print("This URL should end in, for example, .../H2Ooutfiles")
            directory = input()
            
            print("Please enter the name of the molecule \
                you would like to process:")
            print("(e.g. 'H2O', 'H2S. do NOT include the 'outfiles' part)")
            s = input()


            """
            Generate a 2-dimensional array of energy values by retrieving the
            appropriate web file and parsing to find the energy value. 
            """
            get_parameter_ranges(s)
            e_array = np.empty((RSIZE, TSIZE))

            for i in range(RSIZE):
                r = R_RANGE[i]
                for j in range(TSIZE):
                    theta = T_RANGE[j]
                    url = directory +"/"+s+".r%.2ftheta%.1f.out" % (r, theta)
                    f = urlopen(url, context=context)
                    e = extract_energy_from_file(f)
                    e_array[i][j] = e
                    print("Succesfully read %s" % url)
            input_complete = True


        except:
            print("Unable to find the following file: ")
            print(url)
            print("Please try again")
    
    return e_array
        
def extract_energy_from_file(f):
    #Parses file to find line with energy value and return this value
    lines = f.read().splitlines()
    for line in lines:
        if line[:4] == " SCF" or line[:4] == b' SCF':
            l = line.split()
            e = float(l[4])
            return e

def get_parameter_ranges(molecule):
    #Load the parameter ranges for r and theta from the config file.

    with open("config.json","r") as f:
        data = json.load(f)

    rmin = data[molecule]["r_min"]
    rmax = data[molecule]["r_max"]
    rstep = data[molecule]["r_step"]
    tmin = data[molecule]["theta_min"]
    tmax = data[molecule]["theta_max"]
    tstep = data[molecule]["theta_step"]

    #This gets the limits of the energy axis for the 3-d plot
    global ERANGE
    emin = data[molecule]["e_min"]
    emax = data[molecule]["e_max"]
    ERANGE = [emin, emax]

    #This gets the range around the equillibrium where the quadratics should be
    #fit, and whether to plot the graphs
    global R_FIT_RANGE, T_FIT_RANGE, PLOT_R_FIT, PLOT_T_FIT
    R_FIT_RANGE = data[molecule]["r_fit_range"]
    T_FIT_RANGE = data[molecule]["t_fit_range"]
    PLOT_R_FIT = data[molecule]["plot_r_fit"]
    PLOT_T_FIT = data[molecule]["plot_t_fit"]
    
    """
    Create global 1-d arrays of r and theta values from min to max values, used 
    in various places. The 'RSTEP * 0.5' is to account for possible floating 
    point errors as without this np.arange sometimes behaves strangely and 
    sometimes includes the max value and sometimes doesn't.
    """
    global R_RANGE, T_RANGE, RSIZE, TSIZE
    R_RANGE = np.arange(rmin, rmax + rstep * 0.5, rstep)
    T_RANGE = np.arange(tmin, tmax + tstep * 0.5, tstep)
    RSIZE = len(R_RANGE)
    TSIZE = len(T_RANGE)

def show_equillibrium_values(values):
    print("----------------")
    print("Equillibrium geometry parameters:")
    print("r\t=\t%.2f Angstrom" % values[0])
    print("theta\t=\t%.1f deg" % values[1])
    print("E\t=\t%.3f Hartree" % values[2])

def plot(energy_array):
    #Display the 3-dimensional plot of energy against r and theta

    R, T = np.meshgrid(T_RANGE, R_RANGE)

    ax = plt.axes(projection='3d')
    ax.plot_surface(R, T, energy_array, cmap=cm.coolwarm, antialiased=True)
    ax.plot_wireframe(R, T, energy_array, color='black', linewidth=0.5)

    ax.set_zlim(ERANGE)

    ax.set_ylabel(r'$r\ /\ \AA$')
    ax.set_xlabel(r'$\theta\ /\ \degree$')
    ax.set_zlabel(r'Energy / Hartrees')
    ax.set_title(r"Plot of energy against r and $\theta$")

    plt.show()

def get_equillibrium_geometry(energy_array):
    #Find lowest energy value and corresponding r and theta
    emin = energy_array[0][0]
    rmin = R_RANGE[0]
    tmin = T_RANGE[0]
    for i in range(RSIZE):
        for j in range(TSIZE):
            if energy_array[i][j] < emin:
                emin = energy_array[i][j]
                rmin = R_RANGE[i]
                tmin = T_RANGE[j]
    
    values = [rmin, tmin, emin]
    return values

def get_vib_frequencies(eq_geom, energy_array):
    """
    From the equillibrium bond length and angle, get the index of these entries
    in the range of r and theta values so that the corresponding rows and
    columns in the array of energy values can be referred to.
    """
    r_eq = eq_geom[0]
    t_eq = eq_geom[1]
    r_index = np.where(R_RANGE == r_eq)[0][0]
    t_index = np.where(T_RANGE == t_eq)[0][0]
    
    kr = fit(
        x_range=R_RANGE,
        x_eq=r_eq,
        y_range=energy_array[:, t_index],
        y_eq=eq_geom[2],
        fit_range=(r_index - R_FIT_RANGE, r_index + R_FIT_RANGE),
        xlab=r'$r\ -\ r_{eq}\ /\ \AA$',
        ylab=r'$E\ -\ E_{eq}$ / Hartrees',
        plot_title=r"Potential energy curve along stretching mode",
        plot=PLOT_R_FIT,
        )

    kt = fit(
        x_range=T_RANGE,
        x_eq=t_eq,
        y_range=energy_array[r_index, :],
        y_eq=eq_geom[2],
        fit_range=(t_index - T_FIT_RANGE, t_index + T_FIT_RANGE),
        xlab=r'$\theta \ -\ \theta_{eq}\ /\ \degree$',
        ylab=r'$E\ -\ E_{eq}$ / Hartrees',
        plot_title=r"Potential energy curve along bending mode",
        plot=PLOT_T_FIT,
        )

    #Convert to SI units
    kr = kr * EH / ((1E-10)**2)
    kt = kt * EH / ((np.pi / 180)**2)
    print("----------------")
    print("k_r\t=\t%.3e N m-1" % kr)
    print("k_theta\t=\t%.3e N rad-1" % kt)

    #Calculate vibration frequencies
    nu_stretch = np.sqrt(kr / (2 * MU)) / (2 * np.pi * C)
    nu_bend = np.sqrt(kt / ((r_eq * 1E-10)**2 * 0.5 * MU)) / (2 * np.pi * C)

    print("Stretching frequency\t=\t%.0f cm-1" % nu_stretch)
    print("Bending frequency\t=\t%.0f cm-1" % nu_bend)
    return (nu_stretch, nu_bend)

def fit(x_range,x_eq,y_range,y_eq,fit_range,plot=False,xlab="",ylab="",
        plot_title=""):
    X = x_range - x_eq
    Y = y_range - y_eq
    lower = max(fit_range[0],0)
    upper = min(fit_range[1], len(x_range) - 1)
    
    popt, pcov = curve_fit(f, X[lower:upper], Y[lower:upper])
    k = popt[0]

    if plot:
        x_arr = np.linspace(x_range[lower] - x_eq, x_range[upper] - x_eq, 100)
        fit = f(x_arr, k)
        plt.scatter(X, Y, marker="x", color="black", linewidths=0.5)
        plt.plot(x_arr, fit, color="red", linewidth=2)
        plt.xlabel(xlab)
        plt.ylabel(ylab)
        plt.ylim((0 - np.amax(Y)*0.05,min(np.amax(Y)*1.05, ERANGE[1] - y_eq)))
        plt.title(plot_title)
        plt.show()

    return k

def f(x, k):
    #Function to be fit
    return 0.5 * k * x**2


#Main Program Loop
while True:
    welcome_message()
    commands()

    energy_array = command_input(default=True) #Set default=True for testing

    eq_geom = get_equillibrium_geometry(energy_array)
    show_equillibrium_values(eq_geom)
    get_vib_frequencies(eq_geom, energy_array)

    plot(energy_array)

    input("Press enter to continue...")
exit()
