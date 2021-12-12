# art-bot-drawing

## MS Paint Algorithm (process_image.py)

Instructions on how to use:
1. Go into directory that contains this folder (i.e. Robot-Draw)
2. Run the command "python process_image.py *image file path* *blur* *xDim* *yDim* *output_type*"
Blur is an optional argument (it is 0 by default, and can be between 0 and 2)
The image file path needs to already exist, i.e. you should have an image
ready for processing. However, the gcode file path or destination directory does not have to exist.
If it already does, then it will be overwritten. If it doesn't, it will be
created. xDim and yDim are both optional arguments (in mm). The defaults for these are the x and y dimensions of the original CNC machine that we used. Finally, the algorithm can generate G-code to render the given image using three different artistic media techniques. To select which type of media output you want, set output_type to 0 for a pen outline, 1 for multiple colored pens, and 2 for watercolors.
Example usage for pen outline: python process_image.py ./source_images/aang.png 1 0
Example usage for pen colors (note: currently pen color needs to be changed manually): python process_image.py ./source_images/aang.png 1 1
Example usage for watercolors: python process_image.py ./source_images/aang.png 1 2
Example usage for pen outline on different sized machine (ex. string bot): python process_image.py ./source_images/aang.png 1 400 600 0
Example usage for pen colors on different sized machine (ex. string bot, also note: currently pen color needs to be changed manually): python process_image.py ./source_images/aang.png 1 400 600 1
The example usage would take in aang.png (given by relative path in the source_images subdirectory of this repository) and output an automatically named and created G-code file into the subdirectory for its specific type of artistic media (G-code for watercolor paintings is stored in Art-Bot-Drawing/watercolor/gcode/aang.gcode, etc.). These examples would use blur 1 (if you woanted blur to be 0,
then you would leave this argumentout completely).

## Paint CNC Library
### clean function
To clean the brush in between paint colors or before/after use

Method: 
Zeros the machine to the top of the water basin
Dips the bursh in water
Moves back and forth along the ridge 
Rezeros the brush

### refill
Designed to be called whenever the brush has traveled past defined threshold (in mm) [see THRESHOLD in Paint_CNC.py]. 

Method:
Calls clean method
Calls set_paint_color method with current color

### set_paint_color
To pick up the paint color you would like to use

Method: 
Impliments the clean function
Finds the coordinate of the specified paint color
Moves down to touch the paint
Impliments the move_brush_around_paint function
Zeros

### circle
Creates a circle, given x,y coordinates and radius

Method:
Goes to initial spot, where theta == 0, then puts brush down
Uses polar coordinates to create a circle, based on given origin coordinates and radius parameters
Lifts brush up at the end

### set_current_coordinates
Sets the return coordinates that are used in set_paint_color/refill to whatever is passed in parameter

### set_threshold
Set the length the brush will paint until it needs to be refilled

## Visualizing and Validating G-Code for Painting (visualizer.py)

Instructions for use:
1. Open command line/terminal from the project directory (ex. cd ~/art-bot-drawing)
2. Run program using Python using the command: "python ./visualizer.py" along with the following command line arguments/switches
* -v: Verbose setting--Include this flag to print debug statements
* gcode_file_path: Path to G-Code file you would like visualized
* output_type: The algorithm can generate G-code to render the given image using three different artistic media techniques. To select which type of media output you want, set output_type to 0 for a pen outline, 1 for multiple colored pens, and 2 for watercolors.
* resolution: conversion factor between millimeters declared in G-code and pixel resolution (recommended value between 50 and 200)

Example use: python ./visualizer.py ./watercolor/gcode/mike.gcode 100 2
With these command line arguments, the visualizer will run using color and watercolor settings (wider pen width and translucent alpha value), with a resolution conversion factor of 100. It will access the G-Code instructions contained in the file "mike.gcode" at the given relative path (absolute also works!) and create a digital rendering of what this G-Code would look like if painted by the CNC robot. This render will be stored as "mike_visualized.jpg" in the subdirectory folder for watercolor visualized_images and will be displayed immediately in your default photo viewing application.
