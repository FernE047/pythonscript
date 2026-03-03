# type: ignore

# matplotlib missing strict type hints. YES, I like strict type hints.

import matplotlib.pyplot as plt
import numpy as np
import shelve
import os

AVAILABLE_COLORS = [
    "viridis",
    "plasma",
    "inferno",
    "hot",
    "Paired",
    "Dark2",
    "hsv",
    "gist_ncar",
]
MAX_BRIGHTNESS = 256
PARAMS_SIZE = 8


def main() -> None:
    with shelve.open(os.path.join(os.getcwd(), "dadosPreProcessados")) as database:
        xHeat = database["x"]
        yHeat = database["y"]
        zHeat = database["z"]
        maximum = database["maximum"]
        print(maximum)
        num_contour_levels = int(input())
        database.close()
        colors = AVAILABLE_COLORS
        for color in colors:
            plt.figure()
            ax = plt.gca()
            ax.set_aspect("equal")
            cmap = plt.get_cmap(color)
            level: list[int] = []
            for contour_level in range(0, maximum, int(maximum / num_contour_levels)):
                level.append(contour_level)
            level.append(maximum)
            cs = ax.tricontourf(
                xHeat, yHeat, zHeat, np.linspace(0, maximum, MAX_BRIGHTNESS), cmap=cmap
            )
            cbar = plt.colorbar(
                cs,
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
            cbar.ax.tick_params(labelsize=PARAMS_SIZE)
            plt.title(f"Heat Map {color}")
            plt.xlabel("X Label")
            plt.ylabel("Y Label")
            plt.show()


if __name__ == "__main__":
    main()
