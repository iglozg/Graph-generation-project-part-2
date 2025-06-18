#Reporting
import matplotlib.pyplot as plt
def plotting(woods, rocks, fires):
    """Function that plots number of woods, rocks and fires on a graph."""
    plt.figure()
    plt.plot( woods, linestyle = "-", color = "g", label= "Trees population")
    plt.plot( rocks, linestyle = "-", color = "0.8", label = "Non Combustible Land")
    plt.plot( fires, linestyle = "-", color = "r", label = "Wildfires")
    plt.xticks(range(len(woods)))
    plt.legend()
    plt.show()
    
