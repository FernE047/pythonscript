import matplotlib.pyplot as plt
import matplotlib.tri as tri
import numpy as np
import math
import shelve
import os


def main() -> None:
    BD=shelve.open(os.path.join(os.getcwd(),"dadosPreProcessados"))
    xHeat=BD["x"]
    yHeat=BD["y"]
    zHeat=BD["z"]
    BD.close()

    """plt.figure()
    ax = plt.gca()
    ax.set_aspect("equal")
    color="hsv"
    cmap=plt.get_cmap(color)
    CS = ax.tricontourf(xHeat, yHeat, zHeat, np.linspace(0,762,256),cmap=cmap)
    cbar = plt.colorbar(CS, ticks=np.sort(np.array([0,127,254,381,508,635,762])),ax=ax, orientation="horizontal", shrink=.75, pad=.09, aspect=40,fraction=0.05)
    cbar.ax.set_xticklabels(list(map(str,np.sort(np.array([0,127,254,381,508,635,762])))))  # horizontal colorbar
    cbar.ax.tick_params(labelsize=8) 
    plt.title("Heat Map "+color)
    plt.xlabel("X Label")
    plt.ylabel("Y Label")
    plt.show()"""
    #"viridis","plasma","inferno","magma","Greys","Purples","Blues","Greens","Oranges","Reds","YlOrBr","YlOrRd","OrRd","PuRd","RdPu","BuPu","GnBu","PuBu","PuBuGn","BuGn","YlGn","binary","gist_yarg","gist_gray","gray","bone","pink","spring","summer","autumn","winter","cool","Wistia","hot","afmhot","gist_heat","copper",
    colors=["PiYG","PRGn","BrBG","PuOr","RdGy","RdBu","RdYlBu","RdYlGn","Spectral","coolwarm","bwr","seismic","Pastel1","Pastel2","Paired","Accent","Dark2","Set1","Set2","Set3","tab10","tab20","tab20b","tab20c","flag","prism","ocean","gist_earth","terrain","gist_stern","gnuplot","gnuplot2","CMRmap","cubehelix","brg","hsv","gist_rainbow","rainbow","jet","nipy_spectral","gist_ncar"]
    for color in colors:
        plt.figure()
        ax = plt.gca()
        ax.set_aspect("equal")
        cmap=plt.get_cmap(color)
        CS = ax.tricontourf(xHeat, yHeat, zHeat, np.linspace(0,762,256),cmap=cmap)
        cbar = plt.colorbar(CS, ticks=np.sort(np.array([0,127,254,381,508,635,762])),ax=ax, orientation="horizontal", shrink=.75, pad=.09, aspect=40,fraction=0.05)
        cbar.ax.set_xticklabels(list(map(str,np.sort(np.array([0,127,254,381,508,635,762])))))  # horizontal colorbar
        cbar.ax.tick_params(labelsize=8) 
        plt.title("Heat Map "+color)
        plt.xlabel("X Label")
        plt.ylabel("Y Label")
        plt.show()


if __name__ == "__main__":
    main()