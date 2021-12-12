# art-bot-drawing

## MS Paint Algorithm (process_image.py)

Instructions on how to use:
1. Go into directory that contains this folder (i.e. Robot-Draw)
2. Run the command "python process_image.py *image file path* *gcode file path* *blur* *xDim* *yDim* *usecolor/pencolor*"
Blur is an optional argument (it is 0 by default, and can be between 0 and 2)
The image file path needs to already exist, i.e. you should have an image
ready for processing. However, the gcode file path does not have to exist.
If it already does, then it will be overwritten. If it doesn't, it will be
created. xDim and yDim are both optional arguments (in mm). The defaults for these are the x and y dimensions of the original CNC machine that we used. The usercolor argument is just a flag, "--usecolor" that you include if you want to produce a G-code file suitable for watercolors (with the current CNC machine setup). The same goes for pencolor, which is the flag "--pencolor", that you can include if you want to produce a G-code file suitable for a pen coloring in an image. If you don't include a flag, it will produce a G-code file suitable for a pen outline.
Example usage for pen outline: python process_image.py ./aang.png ./aang.gcode 1
Example usage for pen colors (note: currently pen color needs to be changed manually): python process_image.py ./aang.png ./aang.gcode 1 --pencolor
Example usage for watercolors: python process_image.py ./aang.png ./aang.gcode 1 --usecolor
Example usage for pen outline on different sized machine (ex. string bot): python process_image.py ./aang.png ./aang.gcode 1 400 600
Example usage for pen colors on different sized machine (ex. string bot, also note: currently pen color needs to be changed manually): python process_image.py ./aang.png ./aang.gcode 1 400 600 --pencolor
The example usage would take in aang.png (located in the Robot-Draw folder
as denoted by the "./") and output the gcode into the aang.gcode file (
also in the Robot-Draw folder). These examples would use blur 1 (if you woanted blur to be 0,
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
* --usecolor: Colors for various lines are stored in gcode comments; if this flag is provided, colors in comments will be parsed, if not black will be used as default
* -v: Verbose setting--Include this flag to print debug statements
* gcode_file_path: Path to G-Code file you would like visualized
* artType: String indicating type of art the visualizer should render (choices: pen, watercolor)
* resolution: conversion factor between millimeters declared in G-code and pixel resolution (recommended value between 50 and 200)

Example use: python ./visualizer.py --usecolor ./mike.gcode watercolor 100
With these command line arguments, the visualizer will run using color and watercolor settings (wider pen width and translucent alpha value), with a resolution conversion factor of 100. It will access the G-Code instructions contained in the file "mike.gcode" in your current working directory and create a digital rendering of what this G-Code would look like if painted by the CNC robot. This render will be stored as "mike_visualized.jpg" in the same working directory folder and will be displayed immediately in your default photo viewing application.
