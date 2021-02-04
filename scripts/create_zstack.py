#!/usr/bin/env python

from sys import exit
from os import path
import argparse
import numpy as np
import ffmpeg
from datetime import datetime
from matplotlib import cm
from matplotlib.pyplot import imshow, figure, savefig, axis
gray = cm.gray

version = 1.0

# filename="/Users/aspierer/Documents/Postdoc/Publications/PLoS_Genetics_flight/proof approval/figure_revisions/far_796_good_gif.gif"
# filename="/Volumes/SPIERER/Flight/high_speed_videos/far_796_good_gif.gif"
# filename="/Users/aspierer/FreeClimber/example/w1118_m_2_1.h264"
# plot_path="/Users/aspierer/Documents/Postdoc/Publications/PLoS_Genetics_flight/proof approval/figure_revisions/"
# plot_file=plot_path+"test.tiff"

def define_argument_parser():
    '''Parses out arguments
    ----
    Inputs:
      None
    ----
    Returns:
      args (list): list of arguments passed to program
    '''
    parser = argparse.ArgumentParser(prog='z_stacker',
                                    description="Visualizes an object's motion from a video to an image",
                                    usage='%(prog)s [options] path',
                                    epilog='For documentation and a tutorial, see https://github.com/adamspierer/z_stacker',
                                    allow_abbrev=False)

    ## Specify input file
    parser.add_argument('--input_file', 
                        type=str, 
                        required=True, 
                        help="Path to input file")

    ## Specify save path
    parser.add_argument('--output_file', 
                        type=str, 
                        required=True, 
                        help="Path to output file")
    
    ## Specify z-stack method
    parser.add_argument('--method', 
                        type=str, 
                        required=False,
                        choices=['min','max'], 
                        help="Method to construct z-stack. Must be either 'min' or 'max'")

    ## Debug printing
    parser.add_argument('--interval', 
                        type=int, 
                        required=True, 
                        default=False, 
                        help="Number of frames to skip between frames to consider.")

    ## Specify z-stack method
    parser.add_argument('--grayscale', 
                        default=False, 
                        action='store_true', 
                        required=False, 
                        help="Method to construct z-stack. Must be either 'min' or 'max'")

    ## Final parser specifications
    parser.version = version ## Program version
    parser.add_argument('-v','--version', 
                        action='version')
    args = parser.parse_args()
    return args

## Check video argument arguments
def check_args(args):
    '''Confirms video path is valid, and if not checks arguments passed to parser and kills program if invalid path.
    ----
    Inputs:
      args (list): Arguments passed to parsed
    ----
    Returns:
      args.input_file (str): Video file path if valid, or None if not.
    '''
    if path.isfile(args.input_file):
        return args.input_file
    else:
        exit("!! Error: invalid input file path --"+args.input_file)

def startup():
    '''Function prints top line and runs argument parsing function.'''
    line_length = 72
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def print_line(line,line_length):
        '''Formats line to print'''
        if len(line) <= line_length: string = line + '#'*(line_length-len(line))
        else: string = line
        print(string)
        return

    ## Lines to print
    line0 = '#'*line_length
    line1 = '## z_stacker v.%s ' % str(version)
    line2 = '## Please cite: https://github.com/adamspierer/z_stacker'
    line3 = "## Beginning program @ %s " % str(now)
    line4 = line0
    
    ## Printing formated lines
    print('\n')
    for item in range(5):
        print_line(eval('line'+str(item)),line_length)
    return      
       
def video_to_array(File, **kwargs):
    '''Converts video into an nd-array using ffmpeg-python module.
    ----
    Inputs:
      file (str): Path to video file
      kwargs: Can be used with the ffmpeg.output() argument.
    ----
    Returns:
      image_stack (nd-array): nd-array of the video
    '''
    print("2 | 6 : Reading input")
    ## Extracting video meta-data
    try:
        try:
            probe = ffmpeg.probe(File)
        except:
            print('ERROR')
            raise SystemExit
        video_info = next(x for x in probe['streams'] if x['codec_type'] == 'video')
        width = int(video_info['width'])
        height = int(video_info['height'])
    except:
        print('!! Could not read in video file metadata')

    ## Converting video to nd-array    
    try:
        out,err = (ffmpeg
                   .input(File)
                   .output('pipe:',format='rawvideo', pix_fmt='rgb24',**kwargs)
                   .run(capture_stdout=True))
        n_frames = int(len(out)/height/width/3)
        image_stack = np.frombuffer(out, np.uint8).reshape([-1, height, width, 3])
    except:
        print('!! Could not read in video file to an array. Error message (if any):', err)

    return image_stack


def get_interval(stack,n=1):
    '''Selects a stack of frames spaced some interval (n) apart
    ----
    Input:
    stack (ndarray): numpy array of images
    n (int): interval
    ----
    Returns:
    stack (ndarray): numpy array of images, but only includes every n-th frame
    '''
    print("3 | 6 : Slicing by designated interval {}".format(n))
    return stack[::n]


def crop_and_grayscale(video_array,
                     x = 0 ,x_max = None,
                     y = 0 ,y_max = None,
                     first_frame = None,
                     last_frame = None,
                     grayscale = False):
    '''Crops imported video array to region of interest and converts it to grayscale
    ----
    Inputs:
      video_array (nd-array): image_stack generated from video_to_array function
      x (int): left-most x-position
      x_max (int): right-most x-position
      y (int): lowest y-position
      y_max (int): highest y-position
      first_frame (int): first frame to include
      last_frame (int): last frame to include
      grayscale (bool): True to convert to gray, False to leave in color. 
    ----
    Returns:
      clean_stack (nd-array): Cropped and grayscaled (if indicated) video as nd-array'''
    print("4 | 6 : Cropping frames and converting to grayscale")
    ## Conditionals for cropping frames and video length
    if first_frame == None: first_frame = 0
    if last_frame == None: last_frame = video_array.shape[0]
    if y_max == None: y_max = video_array.shape[1]
    if x_max == None: x_max = video_array.shape[2]

    ## Setting only frames and ROI to grayscale
    if grayscale:
        ch_1 = 0.2989 * video_array[first_frame:last_frame,y : y_max,x : x_max,0]
        ch_2 = 0.5870 * video_array[first_frame:last_frame,y : y_max,x : x_max,1]
        ch_3 = 0.1140 * video_array[first_frame:last_frame,y : y_max,x : x_max,2]
        clean_stack = ch_1.astype(float) + ch_2.astype(float) + ch_3.astype(float)

    ## Only cropping, no grayscaling
    else:
        clean_stack = video_array[first_frame:last_frame,y : y_max,x : x_max,:]
    return clean_stack


def z_stack(stack, method = "min"):
    '''Create a z-stack from stack provided
    ----
    Input:
    stack (ndarray): numpy array of images
    ----
    Returns:
    stack (ndarray): '''
    print("5 | 6 : Flattening image stack using method:", method)    
    if method == "min":
        stack = np.amin(stack,axis=0)
    elif method == "max":
        stack = np.amax(stack,axis=0)
    return stack

def visualize_stack(stack, save_file):
    print("6 | 6 : Visualizing z-stack")
    imshow(stack,cmap=cm.gray)
    axis('off')
    savefig(save_file, dpi = 300)
    print(save_file)
    return 

startup()

## Get arguments
print("1 | 6 : Check command line arguments")
arg = define_argument_parser()
check_args(arg)
filename = arg.input_file
save_file = arg.output_file
method = arg.method
interval = arg.interval

## Read input file into an nd-array
stack = video_to_array(filename,loglevel='panic')
# stack.shape

## Slice nd-array by interval
short_stack = get_interval(stack,interval)
# short_stack.shape

## Convert nd-array to grayscale
short_stack_gray = crop_and_grayscale(short_stack, grayscale = arg.grayscale)
# short_stack_gray.shape

## Flatten nd-array to array
z_short_stack = z_stack(short_stack_gray, method = method)
# z_short_stack_gray.shape

## Create visualization
visualize_stack(z_short_stack, save_file=save_file)