# Sprites Heat Map

This project is a script to generate a heat map of the sprites in a folder. so you can see which areas are more common in the sprites. both implementations do the same thing, but each one outputs the heat map in a different way.

## Projects

- [Generate Image](./generate_image) : This implementation generates a heat map image where the intensity of each pixel represents the frequency of that pixel being used in the sprites. the more intense the pixel, the more common it is in the sprites.
- [Plot Heat Map](./plot_heatmap) : This implementation generates a heat map using matplotlib. it creates a plot where the color of each pixel represents the frequency of that pixel being used in the sprites. the more intense the color, the more common it is in the sprites. it uses all the possible heatmap colors