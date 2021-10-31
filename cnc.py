#!/usr/bin/env python3
# Borrowed from Tyler Bletsch

import sys,os,re
import random

# for text rendering
#from HersheyFonts import HersheyFonts

# for coordinate handling
import numpy as np

# for image processing
import PIL
from PIL import Image


def frange(lo,hi,delta):
    v=lo
    while v<=hi+.0001:
        yield(v)
        v += delta

def iff(c,a,b):
    if c: return a
    else: return b

def interp(v,a,b,c,d):
    return (v-a)/(b-a)*(d-c)+c
    
def pixel_order_yx(p_sx,p_sy):
    for py in range(p_sy):
        for px in range(p_sy):
            yield (px,py)
            
def pixel_order_yx_twoway(p_sx,p_sy):
    for py in range(p_sy):
        for px in iff(py%2==0,range(p_sx),reversed(range(p_sx))):
            yield (px,py)
            
def pixel_order_xy(p_sx,p_sy):
    for px in range(p_sx):
        for py in range(p_sy):
            yield (px,py)
            
def pixel_order_xy_twoway(p_sx,p_sy):
    for px in range(p_sx):
        for py in iff(px%2==0,range(p_sy),reversed(range(p_sy))):
            yield (px,py)

def pixel_order_diag(p_sx,p_sy):
    for u in range(p_sx + p_sy):
        for v in range(u+1):
            px = v
            py = u-v
            if px<p_sx and py<p_sy: yield(px,py)

def pixel_order_diag_twoway(p_sx,p_sy):
    for u in range(p_sx + p_sy):
        for v in iff(u%2==0,range(u+1),reversed(range(u+1))):
            px = v
            py = u-v
            if px<p_sx and py<p_sy: yield(px,py)

def pixel_order_diag2(p_sx,p_sy):
    for u in reversed(range(p_sx + p_sy)):
        for v in range(u+1):
            px = v
            py = u-v
            if px<p_sx and py<p_sy: yield(px,py)

def pixel_order_spacefill(p_sx,p_sy):
    from spacefill import spacefill
    for px,py in spacefill(p_sx,p_sy):
        yield (px-1,py-1) # spacefill is 1-origin, image is 0-origin, so we -1 to convert

# used to compose other pixel orders
def pixel_order_compose(*funcs):
    def f(p_sx,p_sy):
        for func in funcs:
            for px,py in func(p_sx,p_sy):
                yield px,py
        

class CNC(object):
    
    fp_gcode = None
    # Changed from 1 to 10
    pen_up_height = 10
    pen_down_height = 0
    enable_echo = False
    if __name__ == "main": 
        enable_echo = True
        
        
    def open(self,filename):
        self.fp_gcode = open(filename,"w")
        
    def close(self):
        self.fp_gcode.close()
        self.fp_gcode = None
    
    def cmd_str(self,str):
        if self.fp_gcode:
            self.fp_gcode.write(str + "\n")
        if self.enable_echo:
            sys.stdout.write(str + "\n")

    def cmd(self,base,**args):
        c = base.upper().strip() + " " + " ".join(k.upper().strip() + str(v).strip() for k,v in args.items() if v is not None)
        self.cmd_str(c)
        
    def _get_dt(self,distance,maxrate,accel):
        pass #TODO

    # internal state tracking for time/odometer"
    feedrate = None
    mode_abs = True
    cur_pos = np.array([0,0,0])
    maxrate = np.array([3000,3000,600]) ## mm/min
    acc = np.array([120,120,60]) # mm/s^2
    time = 0
    min_pos = np.array([ 99999, 99999, 99999])
    max_pos = np.array([-99999,-99999,-99999])
    
    # todo: differentiate g0 and g1 feedrates
    def internal_go(self,coord):
        if not isinstance(coord,np.ndarray):
            coord = np.array(coord)
        if self.mode_abs:
            p = np.array([iff(coord[i] is not None, coord[i], self.cur_pos[i]) for i in range(3)])
            dp = p - self.cur_pos
        else:
            dp = np.array([iff(coord[i] is not None, coord[i], 0) for i in range(3)])
            p = dp + self.cur_pos
        # todo: include acceleration in math
        time_per_dim = [iff(p[dim] is None,0, dp[dim]/self.maxrate[dim]*60) for dim in range(3)]
        self.min_pos = np.array([min(p[dim],self.min_pos[dim]) for dim in range(3)])
        self.max_pos = np.array([max(p[dim],self.max_pos[dim]) for dim in range(3)])
        dt = max(time_per_dim)
        self.time += dt
        #print("p=",p,"dp=",dp,"time_per_dim=",time_per_dim,"dt=",dt,"time=",time)
        self.cur_pos = p
        
    def g0(self,x=None,y=None,z=None): 
        self.internal_go([x,y,z])
        self.cmd("G0",x=x,y=y,z=z) # fast travel
    def g1(self,x=None,y=None,z=None,f=None): 
        self.internal_go([x,y,z])
        self.cmd("G1",x=x,y=y,z=z,f=f) # slow travel
    def g28(self,x=None,y=None,z=None): 
        self.cmd("G28",x=x,y=y,z=z) # home via the coords given
    def g53(self):
        self.cmd("G53")
    def g54(self):
        self.cmd("G54")
    def g55(self):
        self.cmd("G55")
    def g56(self):
        self.cmd("G56")
    def g90(self): 
        mode_abs = True
        self.cmd("G90") # abs mode
    abs=g90 #alias
    def g91(self): 
        mode_abs = False
        self.cmd("G91") # rel mode
    rel=g91 #alias
    def f(self,f): 
        self.cmd_str("F%d" % f) # feed rate set
    def comment(self,s): 
        self.cmd_str("; %s" % s)
        
    def get_size(self): 
        return self.max_pos - self.min_pos
    
    def print_stderr_report(self):
        sys.stderr.write("** Time: %f\n" % self.time)
        sys.stderr.write("** Min pos: %s\n" % str(self.min_pos))
        sys.stderr.write("** Max pos: %s\n" % str(self.max_pos))
        sys.stderr.write("** Size: %s\n" % str(self.get_size()))
        
    def render_text_string(self,text,font_height,font=None):
        thefont = HersheyFonts()
        thefont.load_default_font(font)
        thefont.normalize_rendering(font_height)
        base_y = 0
        for line in text.split("\n"):
            base_y -= font_height
            self.comment("[Y=%.1f] %s" % (base_y,line))
            for stroke in thefont.strokes_for_text(line):
                self.up()
                x,y = stroke[0]
                self.g0(x,y+base_y)
                self.down()
                for x,y in stroke:
                    self.g1(x,y+base_y)

    def render_text_file(self,fp,font_height,font=None):
        s = fp.read()
        self.render_text_string(s,font_height,font)
        
    def render_image_raster(self, filename, height_mm, black_z, white_z, up_z=None, two_way=True, mm_per_row=0.5, save_working_image_filename=None):
        if up_z is None:
            up_z = self.white_z
        im_orig = PIL.Image.open( filename )

        p_sy = int(height_mm/mm_per_row)
        p_sx = p_sy * im_orig.width // im_orig.height

        im = im_orig.resize((p_sx,p_sy),PIL.Image.BICUBIC)
        im = im.convert('L') # greyscale
        if save_working_image_filename is not None:
            im.save(save_working_image_filename)

        imm = im.load() # load pixels as array

        self.comment("Image: %s" % filename)
        self.g0(z=up_z)
        pen_down = False
        for py in range(p_sy):
            self.comment("[%s] Row %d of %d" % (filename,py,p_sy))
            ry = -py*mm_per_row
            #self.g0(x=0,y=ry,z=up_z)
            px_iter = list(range(p_sx))
            if two_way and py%2==1:
                px_iter.reverse()
            for px in px_iter:
                rx = px*mm_per_row
                value = imm[px,py]
                rz = interp(value,0,255,black_z,white_z)
                
                if value<255:
                    if not pen_down:
                        self.g0(x=rx,y=ry,z=up_z)
                    self.g1(x=rx,y=ry,z=rz)
                    pen_down = True
                else:
                    if pen_down:
                        self.g0(z=up_z)
                        pen_down = False
                
            if pen_down:
                self.g0(z=up_z)
                pen_down = False

    def render_image_raster_free(self, filename, height_mm, black_z, white_z, pixel_order, up_z=None, mm_per_row=0.5, save_working_image_filename=None):
        if up_z is None:
            up_z = white_z
        im_orig = PIL.Image.open( filename )

        p_sy = int(height_mm/mm_per_row)
        p_sx = p_sy * im_orig.width // im_orig.height

        im = im_orig.resize((p_sx,p_sy),PIL.Image.BICUBIC)
        im = im.convert('L') # greyscale
        if save_working_image_filename is not None:
            im.save(save_working_image_filename)

        imm = im.load() # load pixels as array

        self.comment("Image: %s" % filename)
        self.g0(z=up_z)
        pen_down = False
        old_px=-10
        old_py=-10
        for px,py in pixel_order(p_sx,p_sy):
            self.comment("[%s] (%d,%d)" % (filename,px,py))
            rx = px*mm_per_row
            ry = -py*mm_per_row
            value = imm[px,py]
            rz = interp(value,0,255,black_z,white_z)
            
            if value<255:
                if not pen_down:
                    self.g0(x=rx,y=ry,z=up_z)
                self.g1(x=rx,y=ry,z=rz)
                pen_down = True
            else:
                if pen_down:
                    self.g0(z=up_z)
                    pen_down = False
            
            # if pen is down and we need to seek elsewhere, pull pen up (e.g. at end of line in a simple raster)
            if pen_down and (abs(old_px-px)>1 or abs(old_py-py)>1):
                self.g0(z=up_z)
                pen_down = False
                
            old_px = px
            old_py = py

    def up(self): 
        self.g0(z=self.pen_up_height)
    def down(self): 
        self.g1(z=self.pen_down_height)
        
    def render_test_grid(self, size_x, size_y, z, num_lines=5, up_z=5):
        for i in range(num_lines):
            x = i*size_x/(num_lines-1)
            cnc.g0(z=up_z)
            cnc.g0(x=x,y=0)
            cnc.g1(z=z)
            cnc.g1(y=-size_y)
        for i in range(num_lines):
            y = -i*size_y/(num_lines-1)
            cnc.g0(z=up_z)
            cnc.g0(x=0,y=y)
            cnc.g1(z=z)
            cnc.g1(x=size_x)    
    

# if 1:
#     if len(sys.argv) < 2:
#         print("Syntax: %s <file>" % sys.argv[0])
#         sys.exit(1)
#     text_filename = sys.argv[1]
#     if text_filename=='-':
#         text_fp = sys.stdin
#     else:
#         text_fp = open(text_filename)



cnc = CNC()
cnc.g90() #abs
cnc.g0(z=5)
cnc.f(3000)

#cnc.render_test_grid(200,140,0.75)
if 0:
    cnc.render_image_raster_free(sys.argv[1], height_mm=50, black_z=0, white_z=0.6, pixel_order=pixel_order_spacefill, up_z=None, mm_per_row=0.6)


if 1:
    from spacefill import spacefill

    rsx=200
    rsy=150
    psx=200//0.5
    psy=150//0.5
    n=0
    for i in range(n):
        psx+=psx-1
        psy+=psy-1
    rdx=rsx/psx
    rdy=rsy/psy



    cnc.g1(z=0)
    for px,py in spacefill(psx,psy):
        px-=1
        py-=1
        rx = px/(psx-1)*rsx
        ry = py/(psy-1)*rsy
        ry = -ry # upper left is origin
        #sys.stderr.write(str((px,py))+"  "+str((rx,ry))+"\n")
        cnc.g1(rx,ry)
    if __name__ == "main": 
        sys.stderr.write("delta: "+str((rdx,rdy))+"\n")
    #cnc.render_text_file(text_fp,10,"cursive")
    #cnc.render_image_raster_free(text_filename, 150, 0, 1, pixel_order=pixel_order_diag2, mm_per_row=0.5, save_working_image_filename="yeah.png")

cnc.g0(z=5)
cnc.g0(0,0)

if __name__ == "main": 
    cnc.print_stderr_report()
