<h1>time_stacker Tutorial</h1>

<h3>Overview</h3>

`time_stacker` creates a time-stack image show from a video or animated gif. This type of picture is best used to showcase the passage of time where the background is static and the focal object moves in a non-overlapping trajectory (e.g. ball bouncing down a hallway).

<h3>Setting up</h3>

After following the installation instructions on README.md, navigate to the `time\_stacker` working directory

	cd <path_to_time_stacker>

<h3>Starting from a video</h3>

`time\_stacker` can read animated gifs and most video formats and output most image file formats.

<p align="center">
<img src="https://github.com/adamspierer/time_stacker/blob/main/example/drosophila.gif" width="256" height="192">
</p>


<b>Basic functionality</b>: Running the script without extra arguments.

	python ./script/time_stacker.py --input_file ./example/drosophila.mov --output_file ./output/drosophila_basic.png

<p align="center">
<img src="https://github.com/adamspierer/time_stacker/blob/main/output/drosophila_basic.png" width="256" height="192">
</p>


<b>Adding an interval</b>: Space out the images selected to allow for better resolution between objects.

	python ./script/time_stacker.py --input_file ./example/drosophila.mov --output_file ./output/drosophila_interval_10.png --interval 10

<p align="center">
<img src="https://github.com/adamspierer/time_stacker/blob/main/output/drosophila_interval_10.png" width="256" height="192">
</p>


<b>Interval with grayscale</b>: Same image as above, but in grayscale.

	python ./script/time_stacker.py --input_file ./example/drosophila.mov --output_file ./output/drosophila_interval_10_grayscale.png --interval 10 --grayscale

<p align="center">
<img src="https://github.com/adamspierer/time_stacker/blob/main/output/drosophila_interval_10_grayscale.png" width="256" height="192">
Time stack of flies dropping into a flight column
</p>


<h4>Options for processing video</h4>

[Required]

	1. `--input\_file` - Path to movie (most formats) or animated gif file
	2. `--output\_file` - Path to output file, including desired file type as the file suffix

[Optional]

	3. `--method` - Method for flattening frames into a single frame. `min` is better for darker objects on a lighter background (default). `max` is better for lighter objects on a darker background
	4. `--interval` - Use every <n-th/interval> frame for final image (default is 1). Higher interval numbers decrease processing time.
	5. `--grayscale` - Option to output image in grayscale. This option significantly increases processing time
	6. `--dpi` - Resolution to save final image in drops per inch (dpi)
	
	--> `--help` - Provides help text in the command line to aid in what inputs are permissible


<h3>Starting from a stack of images</h3>

`time\_stacker` requires a video or animated gif, rather than a series of images. If you are beginning with a series of images, you can convert them to a video using `FFmpeg`. Depending on how the images are named, the following command will be different. 

Assuming a series of images with a common prefix (`img_`), images named with three digits (`000`,`001`...`999`), and a common suffix (`.png`):

	ffmpeg -i <path_to_image_folder>/img\_%03d.png ./example/output.mov

A video file (`output.mov`) will be created in `time_stacker`'s example folder. The video's frame rate is not important, though there may be discrepancies in the video quality depending on the end type of video you try converting. `FFmpeg` is well documented and can be used to create videos and animated gifs (among other things) with relative ease. 

<h3>Troubleshooting and errors</h3>

- Following the basic example, an error like the following: `TypeError: Invalid shape (8, 960, 1280, 3) for image data` may be caused by all packages being installed, but not having the conda virtual environment activated. Type: `conda activate python36` or `source activate python36` and re-run the command.