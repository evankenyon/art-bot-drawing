# art-bot-drawing

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
