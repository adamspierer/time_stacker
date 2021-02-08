#!/usr/bin/env python

from sys import exit
from os import path
import argparse
import numpy as np
import ffmpeg
from datetime import datetime
from matplotlib import cm
from matplotlib.pyplot import imshow, figure, savefig, axis, tight_layout
gray = cm.gray

version = 1.0


def define_argument_parser():
	'''Parses out command line arguments
	----
	Inputs:
	  None
	----
	Returns:
	  args (list): list of arguments passed to program
	'''
	parser = argparse.ArgumentParser(prog='time_stacker',
									description="Create time-stack images from movies or animated gifs!",
									usage='%(prog)s [options] path',
									epilog='For documentation and a tutorial, see https://github.com/adamspierer/time_stacker',
									allow_abbrev=False)
	## Version information
	parser.version = version ## Program version
	parser.add_argument('-v','--version', 
						action='version')

	## Specify input file
	parser.add_argument('--input_file', 
						type=str, 
						required=True, 
						help='Path to input file')

	## Specify save path
	parser.add_argument('--output_file', 
						type=str, 
						required=True, 
						help='Path to output file')
																		
	## Specify z-stack method
	parser.add_argument('--method', 
						type=str,
						default='min', 
						required=False,
						choices=['min','max'], 
						help="Method to construct z-stack. Must be either 'min' or 'max'")

	## Specify interval value
	parser.add_argument('--interval', 
						type=int, 
						required=False, 
						default=1, 
						help='Number of frames to skip between frames to consider.')

	## Specify z-stack method
	parser.add_argument('--grayscale', 
						default=False, 
						action='store_true', 
						required=False, 
						help='Makes final image grayscale')

	## Specify output file type
	parser.add_argument('--dpi', 
						type=int, 
						required=False,
						help='Output file resolution in DPI')

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
		exit('!! Error: invalid input file path --'+args.input_file)

def startup():
		'''Function prints top line and runs argument parsing function.'''
		line_length = 72
		now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

		def print_line(line,line_length):
			'''Formats line to print'''
			if len(line) <= line_length: string = line + '#'*(line_length-len(line))
			else: string = line
			print(string)
			return

		## Lines to print
		line0 = '#'*line_length
		line1 = '## time_stacker v.%s ' % str(version)
		line2 = '## Please cite: https://github.com/adamspierer/time_stacker '
		line3 = '## Beginning program @ %s '  % str(now)
		line4 = line0
	
		## Printing formated lines
		print('\n')
		for item in range(5):
			print_line(eval('line'+str(item)),line_length)
		return      		

class stacker(object):
	def __init__(self, arg):
		## Set up input arguments
		self.filename = arg.input_file
		self.method = arg.method
		self.interval = arg.interval
		self.save_file = arg.output_file
		self.dpi = arg.dpi
		self.grayscale = arg.grayscale

		
	def video_to_array(self,File, **kwargs):
		'''Converts video into an nd-array using ffmpeg-python module.
		----
		Inputs:
		  file (str): Path to video file
		  kwargs: Can be used with the ffmpeg.output() argument.
		----
		Returns:
		  image_stack (nd-array): nd-array of the video
		'''
		print('2 | 6 : Reading input')
		## Extracting video meta-data
		try:
			try:
				probe = ffmpeg.probe(File)
			except:
				raise exit('ERROR: Could not read in input file')
			video_info = next(x for x in probe['streams'] if x['codec_type'] == 'video')
			width = int(video_info['width'])
			height = int(video_info['height'])
		except:
			exit('EROR: Could not read in video file metadata') ## Delete

		## Converting video to nd-array    
		try:
			out,err = (ffmpeg
					   .input(File)
					   .output('pipe:',format='rawvideo', pix_fmt='rgb24',**kwargs)
					   .run(capture_stdout=True))
			n_frames = int(len(out)/height/width/3)
			image_stack = np.frombuffer(out, np.uint8).reshape([-1, height, width, 3])
		except:
			exit('ERROR: Could not read in video file to an array. Error message (if any):', err) ## Delete

		## Check number of channels in video is correct
		if image_stack.shape[3] not in [1,3]:
			exit('ERROR: incorrect number of channels at %s. Requires a one or three channel image' % video_array.shape[3])

		return image_stack
		
	def get_interval(self, stack, n=1):
		'''Selects a stack of frames spaced some interval (n) apart
		----
		Input:
		stack (ndarray): numpy array of images
		n (int): interval
		----
		Returns:
		stack (ndarray): numpy array of images, but only includes every n-th frame
		'''
		print('3 | 6 : Slicing by designated interval: {}'.format(n))
		return stack[::n]


	def crop_and_grayscale(self, video_array, grayscale = False):
		'''Converts three-channel input to grayscale
		----
		Inputs:
		  video_array (nd-array): image_stack generated from video_to_array function
		  grayscale (bool): True to convert to gray, False to leave in color. 
		----
		Returns:
		  clean_stack (nd-array): Cropped and grayscaled (if indicated) video as nd-array'''
		print('4 | 6 : Converting to grayscale:',self.grayscale)

		## Setting only frames and ROI to grayscale
		if grayscale:
			ch_1 = 0.2989 * video_array[:,:,:,0]
			ch_2 = 0.5870 * video_array[:,:,:,1]
			ch_3 = 0.1140 * video_array[:,:,:,2]
			video_array = ch_1.astype(float) + ch_2.astype(float) + ch_3.astype(float)
		return video_array


	def flatten_stack(self, stack, method = 'min'):
		'''Create a z-stack from stack provided
		----
		Input:
		stack (ndarray): numpy array of images
		method (str): Options for how nd-array is collapsed. 'min' is better for light background and dark background; 'max' is the opposite.
		----
		Returns:
		stack (ndarray): '''
		print('5 | 6 : Flattening image stack using method:', method)    
		if method == 'min':
			stack = np.amin(stack,axis=0)
		elif method == 'max':
			stack = np.amax(stack,axis=0)
		return stack

	def visualize_stack(self, stack, save_file, dpi = 100):
		'''Create time-stack image
		----
		Input:
		stack (array): Flattened array of selected images
		save_file (str): Path to save final output
		dpi (int): Image resolution in drops per inch (dpi)
		----
		Output:
		None, but image is automatically saved to --output_file path
		'''
		print('6 | 6 : Visualizing time stack')
		imshow(stack,cmap=cm.gray)
		axis('off')
		tight_layout()
		savefig(save_file, dpi = dpi, bbox_inches='tight')
		return 


def main():
	## Print startup text
	startup()

	## Get arguments
	print('1 | 6 : Check command line arguments')
	arg = define_argument_parser()
	check_args(arg)

	ts = stacker(arg)
	## Read input file into an nd-array
	stack = ts.video_to_array(ts.filename,loglevel='panic')
	# stack.shape

	## Slice nd-array by interval
	stack = ts.get_interval(stack,ts.interval)
	# short_stack.shape

	## Convert nd-array to grayscale
	stack = ts.crop_and_grayscale(stack, grayscale = ts.grayscale)
	# short_stack_gray.shape

	## Flatten nd-array to array
	stack = ts.flatten_stack(stack, method = ts.method)
	# z_short_stack_gray.shape

	## Create visualization
	ts.visualize_stack(stack, 
						save_file=ts.save_file, 
						dpi = ts.dpi)

if __name__ == '__main__':
	main()