#type: ignore

#plt doesn't have good type hints for strict mode, so we ignore all type errors in this file

import matplotlib.pyplot as plt
import numpy as np
import shelve

MAX_TICKS = 7
TICK_SIZE = 127
TICK_ARRAY = np.sort(np.array([TICK_SIZE * i for i in range(MAX_TICKS + 1)]))
ALL_PLOT_COLORS = (
    "viridis",
    "plasma",
    "inferno",
    "magma",
    "Greys",
    "Purples",
    "Blues",
    "Greens",
    "Oranges",
    "Reds",
    "YlOrBr",
    "YlOrRd",
    "OrRd",
    "PuRd",
    "RdPu",
    "BuPu",
    "GnBu",
    "PuBu",
    "PuBuGn",
    "BuGn",
    "YlGn",
    "binary",
    "gist_yarg",
    "gist_gray",
    "gray",
    "bone",
    "pink",
    "spring",
    "summer",
    "autumn",
    "winter",
    "cool",
    "Wistia",
    "hot",
    "afmhot",
    "gist_heat",
    "copper",
    "PiYG",
    "PRGn",
    "BrBG",
    "PuOr",
    "RdGy",
    "RdBu",
    "RdYlBu",
    "RdYlGn",
    "Spectral",
    "coolwarm",
    "bwr",
    "seismic",
    "Pastel1",
    "Pastel2",
    "Paired",
    "Accent",
    "Dark2",
    "Set1",
    "Set2",
    "Set3",
    "tab10",
    "tab20",
    "tab20b",
    "tab20c",
    "flag",
    "prism",
    "ocean",
    "gist_earth",
    "terrain",
    "gist_stern",
    "gnuplot",
    "gnuplot2",
    "CMRmap",
    "cubehelix",
    "brg",
    "hsv",
    "gist_rainbow",
    "rainbow",
    "jet",
    "nipy_spectral",
    "gist_ncar",
)


def main() -> None:
    with shelve.open("./dadosPreProcessados") as database:
        xHeat = database["x"]
        yHeat = database["y"]
        zHeat = database["z"]

    plt.figure()
    ax = plt.gca()
    ax.set_aspect("equal")
    color = "hsv"
    cmap = plt.get_cmap(color)
    cs = ax.tricontourf(xHeat, yHeat, zHeat, np.linspace(0, 762, 256), cmap=cmap)
    cbar = plt.colorbar(
        cs,
        ticks=TICK_ARRAY,
        ax=ax,
        orientation="horizontal",
        shrink=0.75,
        pad=0.09,
        aspect=40,
        fraction=0.05,
    )
    cbar.ax.set_xticklabels(list(map(str, TICK_ARRAY)))  # horizontal colorbar
    cbar.ax.tick_params(labelsize=8)
    plt.title(f"Heat Map {color}")
    plt.xlabel("X Label")
    plt.ylabel("Y Label")
    plt.show()
    for color in ALL_PLOT_COLORS:
        plt.figure()
        ax = plt.gca()
        ax.set_aspect("equal")
        cmap = plt.get_cmap(color)
        cs = ax.tricontourf(xHeat, yHeat, zHeat, np.linspace(0, 762, 256), cmap=cmap)
        cbar = plt.colorbar(
            cs,
            ticks=TICK_ARRAY,
            ax=ax,
            orientation="horizontal",
            shrink=0.75,
            pad=0.09,
            aspect=40,
            fraction=0.05,
        )
        cbar.ax.set_xticklabels(list(map(str, TICK_ARRAY)))  # horizontal colorbar
        cbar.ax.tick_params(labelsize=8)
        plt.title(f"Heat Map {color}")
        plt.xlabel("X Label")
        plt.ylabel("Y Label")
        plt.show()


if __name__ == "__main__":
    main()
