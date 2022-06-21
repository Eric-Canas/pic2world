# Pic2World 🌍
<b>Pic2World</b> is a toolbox for inferring <b>Real World Information</b> such as <b>distances</b> from <b>Pictures</b> and <b>Camera Intrinsics</b>.
It also offers a set of <b>Geometry</b> and <b>Image Manipulation</b> tools, that help to deal with <b>Homographies</b>
and <b>Perspective</b> while maintaining the <b>Real World</b> coherence.

## ⬇️ Installation
You can install Pic2World [via pip](https://pypi.org/project/pic2world/), by running the following command:
```bash
pip install pic2world
```

## ⌨️ Usage
Pic2World includes 4 main modules:
1. [`pic2world.camera_utils`](#camera-utils): Tools based on [Thin-Lens Equation](https://en.wikipedia.org/wiki/Thin_lens) that allow to transform **Pixel Measures** into **Real World Distances**, when the _intrinsic parameters_ of the **camera** (_Inclination_, _Focal Length_ and _Pixel Size_) and the **scene** (one of _Real Object Lenght_ or _Distance to Object_) are **known**.
2. [`pic2world.homographies`](#homographies): Tools based on **Homographies** that help to deal with **Perspective Correction**. Designed to produce visualizations coherent with the **Real World** inferred information.
3. `pic2world.geometry`: **Geometry** tools that help to deal with _N-Dimensional_ polygon transformations.
4. `pic2world.interactive`: **Interactive Tools**, based on [matplotlib](https://matplotlib.org/), that can be used for **asking** information about the image to the user. For example, it include functions to let the user _define_ or _confirm_ a polygon over the image.


### Camera Utils
**Camera Utils** include two main classes, [`pic2world.camera_utils.camera`](./modules/camera_utils/camera.py') and [`pic2world.camera_utils.ruler`](./modules/camera_utils/ruler.py').


1. `Camera` is used to model the **Camera**. It receives its intrinsics through the constructor ( _Pixel Size_, _Focal Length_ and, optionally, _Sensor Shape_), and internally calculates and store the rest of intrinsics. For example, if we would want to analize images taken from a **Canon EOS R6** mounting a **50 mm** lens, we would set it as follows: 
    ```python
    from pic2world.camera_utils.camera import Camera
    # Build the Intrinsics of a Canon R6 
    CANON_EOS_R6_CAMERA = Camera(
        pixel_size_mm=8.18/1000.0, # Pixel size of the camera sensor. 8.18 μm
        focal_length_mm=50, # Focal length of the mounted lens
        sensor_shape_px=(5472, 3648) # (width, height) of the sensor. Default: None. Only used for inclinations close to 0º.
    )
    ```
    There are some preset _camera models_ that can be exported from [`pic2world.camera_utils.config`](./modules/camera_utils/config.py)


2. `Ruler` is the object used to transform **Pixel Measures** to **Real World Distances** using a defined `Camera` and some of the **Scene Intrinsics**. Let's build an example using the following image:
   <img src="./debug/resources/Distance-140cm-angle-60-deg-Height-90cm-1969px-CANON-EOS-R6.JPG" width="50%" align="left">

    That's the information we know for that image:
    * **Camera**: _Canon EOS R6_.
    * **3 DIN-A4 Height**: _3*30 cm_.
    * **Distance from lens to first DIN-A4**: _140 cm_.
    * **Angle of the camera**: _30 degrees_.

First, we create the Ruler object
```python
from pic2world.camera_utils.ruler import Ruler
# Create a Ruler object
ruler = Ruler(camera=CANON_EOS_R6_CAMERA)
``` 

Then, knowing how many pixels does the **3 DIN-A4** occuppy in our image we can make the following inferences:

```python
# Let's assume that we don't know the distance between the lens and the object and calculate it.
distance_lens_to_object = ruler.distance_to_object_cm(object_length_px=2320, # Length of the object in pixels
                                              real_object_length_cm=3*30.0, # Real Length of 3 DIN-A4 papers.
                                              angle_degrees=60) # Angle with which the image was taken (0 would mean zenith).
```

```python
object_height = ruler.object_length_in_cm(object_length_px=2320, # Length of a vertical of the object in pixels,
                                                  distance_to_object_cm=118.0, # Distance between the object and the camera lens in cm
                                                  angle_degrees=60) # Angle with which the image was taken (0 would mean zenith).
```

```python
# Print the real length in cm.
>>> Object height -> Calculated: 89.5742 cm [Real 90.0 cm]
```

### Homographies
Homographies module includes functions for changing the perspective of an image, while maintaining the real world coherence.

##### From original image to zenith view. Setting input interactively

```python
from pic2world.homographies.homography_utils import correct_perspective
correct_polygon_perspective(img,
                            origin_polygon=None, # We are not providing an input polygon because we want the user to define it.
                            interactive=True, # Ask the user to define the polygon.
                            angle_degrees=60.0, # Angle with which the image was originaly taken.
                            output_shape=(600, 300), # Output shape we want
                            pad= 0.05) # Padding between the limits of the rectangle and the border of the output image.
```

## Note

This library is a work in progress. It is not yet complete, and it is not meant to be used in production yet.
