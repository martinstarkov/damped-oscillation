import numpy as np
import matplotlib.pyplot as plt

# note on variable usage in the script
# I know that usually it would not be the best practice to use non alphanumeric characters for variable names
# however, since this project contains lots of equations, everything becomes easier to understand when using ω_0 and γ
# and besidesssssssss, what doesn't support UTF-8 anyways.. (*cough* the default code page of windows 7 console *cough*)

def input_ask(question):
    answer = input(question)
    try:
        # we want only questions that ask for integers to try the evaluation
        if question[0] != "A":
            # check if user input can be evaluated 
            return eval(answer)
        # question[0] == "A" checks if "Are the initial conditions.." was asked, which has a true or false answer so always go to exception
        else: 
            1 / 0
    except:
        # initial conditions are x = 1, ẋ = 0, t = 0
        # this is just a cheap hack for not having to write another function parameter. I recognize your complaint ( ͡° ͜ʖ ͡°)
        # i.e. answer is yes or true
        if question[0] == "A" and (answer[0].capitalize() == "Y" or answer[0].capitalize() == "T"):
            # array with initial conditions
            return [1, 0, 0]
        # user wants to enter their own initial displacement, velocity and time
        # i.e. answer is no or false
        elif question[0] == "A" and (answer[0].capitalize() == "N" or answer[0].capitalize() == "F"):
            try:
                x = eval(input("Please enter the initial value of x (displacement): "))
                ẋ = eval(input("Please enter the initial value of ẋ (velocity): "))
                t = eval(input("Please enter the initial value of t (time): "))
                return [x, ẋ, t]
            except:
                print("Could not understand the state of an intial condition")
                return input_ask(question)
        else:
            print("One of the inputs could not be understood")
            return input_ask(question)

def oscillation_type(ω_0, γ):
    if γ > 2 * ω_0:
        return "Damped"
    elif γ == 2 * ω_0:
        return "Critically Damped"
    else:
        return "Under Damped"

def shm(ω_0, γ, time, conditions):
    # initial variable declarations (for scope)
    # these a and b values are only used if the initial conditions are default
    a = 1
    # γ / 2 appears so often later that I substitute it with variable c
    c = γ / 2
    # for default initial conditions
    b = c
    p = np.sqrt(abs(γ ** 2 / 4 - ω_0 ** 2))
    ω = np.sqrt((ω_0 ** 2 - γ ** 2 / 4))
    # this array contains initial conditions [x, ẋ, t], it's simpler to work with one letter for each
    x = conditions[0]
    v = conditions[1]
    t = conditions[2]
    default_initial_conditions = False

    # initial conditions are default, this check saves a bit of computing since a and b are given for these conditions
    if x == 1 and v == 0 and t == 0:
        default_initial_conditions = True

    if oscillation_type(ω_0, γ) == "Damped":
        if default_initial_conditions:
            b /= p
        else:
            # arbitrary values make the damped expressions for a and b more readable (still a mess xD), use ctrl + h find and replace if you prefer reading it without arbitrary variables 
            def1 = np.exp(t * (p - c))
            def1_5 = (p - c) * def1
            def2 = np.exp(-t * (p + c))
            def2_5 = (p + c) * def2
            # these expressions are obtained by taking the given smh equation for displacement and its derivative (velocity) in terms of a and b for each of the given types of damping
            b = (2 * x - 2 * v * (def1 + def2) / (def1_5 - def2_5)) / (def1 - def2 - (def1_5 + def2_5) * (def1 + def2) / (def1_5 - def2_5))
            a = 2 * (v - b * (def1_5 + def2_5) / 2) / (def1_5 - def2_5)

        displacement = np.exp(-γ * time / 2) * (a * np.cosh(p * time) + b * np.sinh(p * time))

    elif oscillation_type(ω_0, γ) == "Critically Damped":
        if not default_initial_conditions:
            # ” ditto comment
            b = np.exp(c * t) * (v + c * x)
            a = np.exp(c * t) * (x - b * t / np.exp(c * t))

        displacement = np.exp(-γ * time / 2) * (a + b * time)

    elif oscillation_type(ω_0, γ) == "Under Damped":
        if default_initial_conditions:
            b /= ω
        else:
            # ” ditto comment
            b = (np.exp(c * t) * (v + x * (c + ω * np.sin(ω * t) / np.cos(ω * t)))) / (c * np.sin(ω * t) + ω * np.sin(ω * t) ** 2 / np.cos(ω * t) - c * np.sin(ω * t) + ω * np.cos(ω * t))
            a = np.exp(c * t) * (x - b * np.sin(ω * t) / np.exp(c * t)) / np.cos(ω * t)

        displacement = np.exp(-γ * time / 2) * (a * np.cos(ω * time) + b * np.sin(ω * time))

    return displacement

def main():
    amplitudes = []
    times = []
    # ask for inputs
    ω_0 = input_ask("Please enter the value of ω_0 (omega_0): ")
    γ = input_ask("Please enter the value of γ (gamma): ")
    points = int(np.ceil(input_ask("Please enter the amount of points you'd like to plot: ")))
    init_conditions = input_ask("Are the initial conditions x = 1 (displacement), ẋ = 0 (velocity), t = 0 (time)? (yes/no): ")
    # divide range by amount of points to get step-length
    print("Plotted graph with ω_0 = " + str(ω_0) + ", γ = " + str(γ) + ", " + str(points) + " points, x_init = " + str(init_conditions[0]) + ", ẋ_init = " + str(init_conditions[1]) + ", t_init = " + str(init_conditions[2]))
    t_interval = (5 * np.pi / ω_0) / points
    # add values to time and amplitude arrays
    for i in range(points):
        x = i * t_interval
        times.append(x)
        amplitudes.append(shm(ω_0, γ, x, init_conditions))

    # plot display, formatting and such..
    plt.figure()
    plt.title('Behaviour of a ' + oscillation_type(ω_0, γ) + ' Simple Harmonic Oscillator')
    plt.xlabel('Time (s)')
    plt.ylabel('Displacement (m)')
    plt.plot(times, amplitudes, c='b') 
    plt.show()

    # recursion
    main()

# initial call
main()