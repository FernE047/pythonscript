# Morph Projects

there are two implementations of morphing algorithms in this folder. the first one you need to first open the source and target image and then draw using paint.net layers the corresponding points (red), or lines (blue) or areas (green) between the two images. then you can run the morphing script and it will create a morphing video between the two images. the lines and areas expand in layers. the script interpolates areas by interpolating layers by interpolating the points that form the layers.
the second implementation is one where you just input the source and target image and it tries to make the same configuration as if the first layer is the outside most layer of both images in clockwise direction from the top left corner, it's very hard to get a good result this way.

## Projects

- [Manual Morph](./manual_config) : the first implementation of the morphing algorithm. it is a very manual implementation, you have to manually draw the corresponding points, lines and areas between the two images. but it gives you a lot of control over the morphing process.
- [Lazy Morph](./lazy_morph) : the second implementation of the morphing algorithm. it is a very lazy implementation.