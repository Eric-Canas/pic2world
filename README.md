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


1. `Camera` is used to model the **Camera**. It receives its intrinsics through the constructor ( _Pixel Size_, _Focal Length_ and, optionally, _Sensor Shape_), and internally calculates and store the rest of intrinsics. For example, if we would want to analize images taken from a **Canon R6** mounting a **50 mm** lens, we would set it as follows: 
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


2. `Ruler` is used to calculate real world distances from pixel measures and camera intrinsics:

##### Calculating Distance between the lens and the object when the Real Length is known


```python
from pic2world.camera_utils.ruler import Ruler
# Create a Ruler object
ruler = Ruler(camera=CANON_EOS_R6_CAMERA)
distance_to_img = ruler.distance_to_object_cm(object_length_px=2320, # Length of the object in pixels
                                              real_object_length_cm=3*30.0, # Real Length of 3 DIN-A4 papers.
                                              angle_degrees=60) # Angle with which the image was taken (0 would mean zenith).
```

```python
# Print the distance in cm.
>>> Distance to object -> Calculated: 118.5608 cm [Real: 118.0 cm]
```

##### Calculating Real Length of an object when the distance between it and the camera lens is known

```python
# Assume the same camera as above
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
