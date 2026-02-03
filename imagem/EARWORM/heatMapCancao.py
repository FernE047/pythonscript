import matplotlib.pyplot as plt
import matplotlib.tri as tri
import numpy as np
import math
import shelve
import os


def main() -> None:
    BD = shelve.open(os.path.join(os.getcwd(), "dadosPreProcessados"))
    xHeat = BD["x"]
    yHeat = BD["y"]
    zHeat = BD["z"]
    maximo = BD["maximo"]
    print(maximo)
    numero = int(input())
    BD.close()
    colors = ["viridis", "plasma", "inferno", "hot", "Paired", "Dark2", "hsv", "gist_ncar"]
    for color in colors:
        plt.figure()
        ax = plt.gca()
        ax.set_aspect("equal")
        cmap = plt.get_cmap(color)
        level = []
        for a in range(0, maximo, int(maximo / numero)):
            level.append(a)
        level.append(maximo)
        CS = ax.tricontourf(xHeat, yHeat, zHeat, np.linspace(0, maximo, 256), cmap=cmap)
        cbar = plt.colorbar(
            CS,
            ticks=np.sort(np.array(level)),
            ax=ax,
            orientation="horizontal",
            shrink=0.75,
            pad=0.09,
            aspect=40,
            fraction=0.05,
        )
        cbar.ax.set_xticklabels(
            list(map(str, np.sort(np.array(level))))
        )  # horizontal colorbar
        cbar.ax.tick_params(labelsize=8)
        plt.title("Heat Map " + color)
        plt.xlabel("X Label")
        plt.ylabel("Y Label")
        plt.show()


if __name__ == "__main__":
    main()