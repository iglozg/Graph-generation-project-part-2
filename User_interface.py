#User interface
from opener import opener
import graph_forest as gh
def main_menu():
    """ Main menu of the program, users can select the random number or provided file graph generation
    or to terminate. """
    while True:
        option = input('''Select one of the following:
  1) Generate random simulation
  2) Generate simulation from provided connections
  9) Quit.
Enter your choice: ''').strip()
        if option == "1":
            menu_random() # display the menu for random simulation
            break 
        elif option == "2":
            menu_provided() # display the menu for provided connections
            break
        elif option == "9":
            print("Bye")
            exit(0) # quit the program 
        else:
            print("Option \"" + option + "\" not recognised, please enter a number that corresponds to one of the options displayed.")

def menu_random():
    """Submenu of the program, users define the minimal number of sites for the graph."""
    while True:
        sites_random = input('''Please specify the minimal number of sites for the graph (number needs to be bigger then 3)? ''').strip()
        try: #Try to convert this number to an integer
            edges_random = int(sites_random)
            if edges_random <= 3:
                print("Oops something went wrong, please provide a number that's bigger then 3")
            else:
                break
        except ValueError:
            print("Oops something went wrong, please provide a number that's bigger then 3")       
    pattern = menu_colors()
    firefighters = menu_firefighters(edges_random)
    fire = menu_fire()
    forest_respawn = menu_respawn()
    iteration_steps = menu_iteration()
    gh.random_graph(edges_random, pattern, firefighters, fire, forest_respawn, iteration_steps)

def menu_provided():
    """Submenu of the program, users define from which file they create the graph."""
    while True:
        option = input("""Is the file in the same folder as this python file (Yes or No)?: """).strip().lower()
        if option == "yes":
            file_yes = input("""Please type full name of the file with its extension (for example: my_txt.txt): """)
            try:
                graph = opener(file_yes)
                break
            except FileNotFoundError: # If the file is not in the same folder as the python file, it will print this message
                print("Oops it seems that this file is not in the same folder as the python file, please try again")            
        elif option == "no":
            file_no = input("""Please provide the whole path to that file (for example: C:/path/to/your/file/file_name.txt): """).strip()
            try:
                graph =opener(file_no)
                break
            except FileNotFoundError: # If the file is not in the same folder as the python file, it will print this message
                print("Oops it seems that this is incorrect path to the file, please try again")    
        else:
            print("Oops, I think you made a typo, please try again")
    
    edges = len(list(set().union(*graph)))
    pattern = menu_colors()
    firefighters = menu_firefighters(edges)
    fire = menu_fire()
    forest_respawn = menu_respawn()
    iteration_steps = menu_iteration()
    gh.provided_graph(graph, pattern, firefighters, fire, forest_respawn, iteration_steps)

def menu_colors():
    """Submenu of the program, user define the landscape pattern for the sites in the graph."""
    pattern_info = []
    info = input('''Select colors for the graph:
    1) All sites are woods
    2) All sites are rocks
    3) All sites are random with fixed ration in trees.
  Enter your choice: ''').strip()
    if info not in ["1", "2", "3"]:
        print("Option \"" + info + "\" not recognised, please enter a number that corresponds to one of the options displayed.")
        return menu_colors()
    else:
        pattern_info.append(info)
        if info == '3':
            while True: 
                ratio_info = input('''Please provide a fixed ratio for woods ( e.g. 80%) for a random initial configuration: ''').strip()
                try:
                    ratio_info = int(ratio_info)
                    if 0 < ratio_info <= 100:
                        break
                    else:
                        print("Oops, something went wrong. Please provide a ratio between 0% and 100%.")
                except ValueError:
                    print("Oops, something went wrong. Please provide a valid number ratio.")

            pattern_info.append(ratio_info)
        return pattern_info
    
def menu_firefighters(edges):
    """Submenu of the program in which user define the number of firefighters and their average skill level."""
    firefighters_info = []
    while True:
        number = input('''Please specify the number of firefighters (number needs to be bigger then 0)? ''').strip()
        try:
            number = int(number)
            if number <= 0:
                print("Oops something went wrong, please provide a number that's bigger then 0.")
            elif number >= edges:
                print(f"Oops somethin went wrong, please provide a number that's smaller then number of edges ({edges}).")
            else:
                firefighters_info.append(number)
                break
        except ValueError:
            print("Oops something went wrong, please provide a number")
    while True:
        skill = input('''Please provide an average skill of firefighters (number should be inbetween 0 and 100): ''').strip()
        try:
            skill = int(skill)
            if 0 < skill <= 100:
                firefighters_info.append(skill)
                break
            else:
                print("Oops something went wrong, please provide a ratio between 0% and 100%.")
        except ValueError:
            print("Oops something went wrong, please provide a number")
    return firefighters_info

def menu_fire():
    """Submenu in which user defines informations about fire such as the probability for ignition and transmission."""
    fire_info = []
    while True:
        info = input('''Please specify the probability for ignition (number should be inbetween 0 and 100): ''').strip()
        try:
            info = int(info)
            if 0 < info <= 100:
                fire_info.append(info)
                break
            else:
                print("Oops something went wrong, please provide a ratio between 0% and 100%.")
        except ValueError:
            print("Oops something went wrong, please provide a number")
    while True:
        transmission = input('''Please specify the probability for transmission (number should be inbetween 0 and 100): ''').strip()
        try:
            transmission = int(transmission)
            if 0 < transmission <= 100:
                fire_info.append(transmission)
                break
            else:
                print("Oops something went wrong, please provide a ratio between 0% and 100%.")
        except ValueError:
            print("Oops something went wrong, please provide a number")
    return fire_info

def menu_respawn():
    """Submenu in which user defines information about forest respawn."""
    while True:
        respawn = input('''Please specify the probability for forest respawn (number should be inbetween 0 and 100): ''').strip()
        try:
            respawn = int(respawn)
            if 0 <= respawn <= 100:
                break
            else:
                print("Oops something went wrong, please provide a ratio between 0% and 100%.")
        except ValueError:
            print("Oops something went wrong, please provide a number")
    return respawn

def menu_iteration():
    """Submenu in which user defines the amount of iteration steps for simulation."""
    while True:
        iteration = input('''Please provide a number of iteration steps for the simulation (should be bigger then 0): ''').strip()
        try:
            iteration = int(iteration)
            if iteration <= 0:
                print("Oops something went wrong, please provide a number bigger then 0")
            else:
                break
        except ValueError:
            print("Oops something went wrong, please provide a number")
    return iteration

if __name__ == "__main__":
    main_menu()
