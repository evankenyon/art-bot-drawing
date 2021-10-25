# art-bot-drawing

## MS Paint Algorithm (process_image.py)

Instructions on how to use:
1. Go into directory that contains this folder (i.e. Robot-Draw)
2. Run the command "python process_image.py *image file path* *gcode file path* *blur* *usecolor*"
Blur is an optional argument (it is 0 by default, and can be between 0 and 2)
The image file path needs to already exist, i.e. you should have an image
ready for processing. However, the gcode file path does not have to exist.
If it already does, then it will be overwritten. If it doesn't, it will be
created. The usercolor argument is just a flag, "--usecolor" that you include if you want to use
color, and don't include if you  don't (i.e. you just want an outline).
Example usage: python process_image.py ./aang.png ./aang.gcode 1 --usecolor
The example usage would take in aang.png (located in the Robot-Draw folder
as denoted by the "./") and output the gcode into the aang.gcode file (
also in the Robot-Draw folder). This would use blur 1 (if you woanted blur to be 0,
then you would leave this argumentout completely) and make it with color instead of
an outline (if you wanted it to just be the outline, you would leave out --usecolor entirely).

## Paint CNC Library
### clean function
To clean the brush in between paint colors or before/after use

Method: 
Zeros the machine to the top of the water basin
Dips the bursh in water
Moves back and forth along the ridge 
Rezeros the brush

### set_paint_color
To pick up the paint color you would like to use

Method: 
Impliments the clean function
Finds the coordinate of the specified paint color
Moves down to touch the paint
Impliments the move_brush_around_paint function
Zeros

### move_brush_around_paint
To move the bursh back and forth in a paint well to pick up more of the color

Method:
Moves back and forth along the x and y axes in assorted increments 
