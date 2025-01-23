import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import tkinter as tk

# Define the input variables
population_density = ctrl.Antecedent(np.arange(0, 101, 1), 'population_density')
target_importance = ctrl.Antecedent(np.arange(0, 11, 1), 'target_importance')
weapon_precision = ctrl.Antecedent(np.arange(0, 101, 1), 'weapon_precision')

# Define the output variable
risk = ctrl.Consequent(np.arange(0, 101, 1), 'risk')

population_density['low'] = fuzz.trimf(population_density.universe, [0, 0, 50])
population_density['medium'] = fuzz.trimf(population_density.universe, [30, 50, 70])
population_density['high'] = fuzz.trimf(population_density.universe, [50, 100, 100])

target_importance['low'] = fuzz.trimf(target_importance.universe, [0, 0, 5])
target_importance['medium'] = fuzz.trimf(target_importance.universe, [3, 5, 7])
target_importance['high'] = fuzz.trimf(target_importance.universe, [5, 10, 10])

weapon_precision['low'] = fuzz.trimf(weapon_precision.universe, [0, 0, 50])
weapon_precision['medium'] = fuzz.trimf(weapon_precision.universe, [30, 50, 70])
weapon_precision['high'] = fuzz.trimf(weapon_precision.universe, [50, 100, 100])

risk['low'] = fuzz.trimf(risk.universe, [0, 0, 50])
risk['medium'] = fuzz.trimf(risk.universe, [30, 50, 70])
risk['high'] = fuzz.trimf(risk.universe, [50, 100, 100])

# Rules
rule1 = ctrl.Rule(population_density['high'] & weapon_precision['low'], risk['high'])
rule2 = ctrl.Rule(population_density['medium'] & weapon_precision['medium'], risk['medium'])
rule3 = ctrl.Rule(population_density['low'] & weapon_precision['high'], risk['low'])
rule4 = ctrl.Rule(target_importance['high'] & weapon_precision['low'], risk['high'])
rule5 = ctrl.Rule(target_importance['low'] & weapon_precision['high'], risk['low'])
rule6 = ctrl.Rule(target_importance['high'] & population_density['high'], risk['high'])
rule7 = ctrl.Rule(target_importance['medium'] & population_density['medium'], risk['medium'])
rule8 = ctrl.Rule(weapon_precision['high'] & population_density['low'], risk['low'])
rule9 = ctrl.Rule((target_importance['medium'] | population_density['medium']) & weapon_precision['medium'], risk['medium'])
rule10 = ctrl.Rule(target_importance['low'] & population_density['low'], risk['low'])
rule11 = ctrl.Rule((target_importance['high'] | population_density['high']) & weapon_precision['medium'], risk['medium'])
rule12 = ctrl.Rule(target_importance['high'] & weapon_precision['high'], risk['medium'])
rule13 = ctrl.Rule(population_density['high'] & weapon_precision['medium'], risk['high'])
rule14 = ctrl.Rule(target_importance['medium'] & weapon_precision['low'], risk['high'])
rule15 = ctrl.Rule((population_density['medium'] | target_importance['medium']) & weapon_precision['high'], risk['low'])

# Control system
risk_control = ctrl.ControlSystem([rule1, rule2, rule3, rule4, rule5, rule6, rule7, rule8, rule9,rule10,rule11, rule12,rule13,rule14,rule15])
risk_simulation = ctrl.ControlSystemSimulation(risk_control)

def show_membership_functions():
    # Create a new window
    mf_window = tk.Toplevel(root)
    mf_window.title("Membership Functions Visualization")
    
    # Create a figure with subplots
    fig, axes = plt.subplots(2, 2, figsize=(10, 8))
    fig.suptitle('Membership Functions of All Variables')
    
    # Plot Population Density
    ax = axes[0, 0]
    for term in population_density.terms:
        ax.plot(population_density.universe, 
                population_density[term].mf,  # Access membership function directly
                label=term)
    ax.set_title('Population Density')
    ax.legend()
    
    # Plot Target Importance
    ax = axes[0, 1]
    for term in target_importance.terms:
        ax.plot(target_importance.universe, 
                target_importance[term].mf,  # Access membership function directly
                label=term)
    ax.set_title('Target Importance')
    ax.legend()
    
    # Plot Weapon Precision
    ax = axes[1, 0]
    for term in weapon_precision.terms:
        ax.plot(weapon_precision.universe, 
                weapon_precision[term].mf,  # Access membership function directly
                label=term)
    ax.set_title('Weapon Precision')
    ax.legend()
    
    # Plot Risk
    ax = axes[1, 1]
    for term in risk.terms:
        ax.plot(risk.universe, 
                risk[term].mf,  # Access membership function directly
                label=term)
    ax.set_title('Risk Level')
    ax.legend()
    
    # Embed in Tkinter
    canvas = FigureCanvasTkAgg(fig, master=mf_window)
    canvas.draw()
    canvas.get_tk_widget().pack()
    
    close_button = tk.Button(mf_window, text="Close", command=mf_window.destroy)
    close_button.pack(pady=10)

# Tkinter GUI
def update_plot():
    try:
        # Get values from sliders
        pop_density = population_slider.get()
        target_imp = target_slider.get()
        weapon_prec = weapon_slider.get()
        
        # Set fuzzy inputs
        risk_simulation.input['population_density'] = pop_density
        risk_simulation.input['target_importance'] = target_imp
        risk_simulation.input['weapon_precision'] = weapon_prec
        
        # Compute the fuzzy output
        risk_simulation.compute()
        computed_risk = risk_simulation.output['risk']
        
        # Update result label
        result_label.config(text=f"Computed Risk Level: {computed_risk:.2f}")
        
        # Clear the plot and redraw
        ax.clear()
        ax.set_title('Fuzzy Risk Evaluation')
        ax.set_ylabel('Membership')
        ax.set_xlabel('Risk Level')
        for term, mf in risk.terms.items():
            ax.plot(risk.universe, mf.mf, label=term)
        ax.axvline(computed_risk, color='red', linestyle='--', label='Output')
        ax.legend()
        canvas.draw()
    except KeyError as e:
        result_label.config(text=f"Error: Missing input data ({e}). Please adjust all sliders.")
    except ValueError as e:
        result_label.config(text=f"Error: Invalid input ({e}). Please check slider values.")

# Create the Tkinter window
root = tk.Tk()
root.title("Fuzzy Risk Evaluation")

# Create sliders for inputs
population_slider = tk.Scale(root, from_=0, to=100, orient=tk.HORIZONTAL, label="Population Density")
population_slider.set(50)
population_slider.pack(pady=10)

target_slider = tk.Scale(root, from_=0, to=10, orient=tk.HORIZONTAL, label="Target Importance")
target_slider.set(5)
target_slider.pack(pady=10)

weapon_slider = tk.Scale(root, from_=0, to=100, orient=tk.HORIZONTAL, label="Weapon Precision")
weapon_slider.set(50)
weapon_slider.pack(pady=10)

# Button to update plot
update_button = tk.Button(root, text="Update Risk", command=update_plot)
update_button.pack(pady=10)

# Label to display the computed risk
result_label = tk.Label(root, text="Computed Risk Level: 0.00", font=("Helvetica", 14))
result_label.pack(pady=10)

# Matplotlib Figure embedded in Tkinter
fig, ax = plt.subplots(figsize=(6, 4))
canvas = FigureCanvasTkAgg(fig, master=root)
canvas_widget = canvas.get_tk_widget()
canvas_widget.pack(pady=10)


mf_button = tk.Button(root, text="Show Membership Functions", command=show_membership_functions)
mf_button.pack(pady=10)


root.mainloop()

