<h1>time_stacker</h1>

<h3>Overview</h3>

`time_stacker` creates a time-stack image show from a video or animated gif. This type of picture is best used to showcase the passage of time where the background is static and the focal object moves in a non-overlapping trajectory (e.g. ball bouncing down a hallway).

<p align="center">
<img src="https://github.com/adamspierer/time_stacker/blob/main/outputs/flight_example.png" width="333" height="424">
</p>

<h3>Motivation</h3>

This program was designed to fill the void of Python-based programs that can generate a time-stack image, as well as address a personal issue I encountered trying to create time-stack images with a subset of images/frames in a video for a publication. May my effort save you time.

<h3>Requirements</h3>

General programs:

	- FFmpeg        [4.3.1 ]

	--> Download from here: https://ffmpeg.org/download.html
	--> May require the use of Homebrew: https://docs.brew.sh/Installation
	--> Install ffmpeg with Homebrew: https://formulae.brew.sh/formula/ffmpeg

Python modules:

    - argparse      [1.1   ]
    - ffmpeg-python [0.2.0 ]
    - matplotlib    [3.1.3 ]
    - numpy         [1.18.1]
    - pip           [20.0.2]
    - sys		[standard]
    - os		[standard]
	- datetime	[standard]

NOTE: time_stacker is tested in a Python3.6 virtual environment. Other programs have experienced difficulty with the `ffmpeg` in later Python versions, but may work.

NOTE: These are the package versions I know work, though future versions should work as well.

<h3>Installing</h3>

I recommend running this package in an Anaconda-based virtual environment. Anaconda can be downloaded [here](https://docs.anaconda.com/anaconda/install/).

**Make sure `conda` is installed** (should return something like `conda 4.7.11`):

	conda -V 

**Update conda if needed** (press `y` when prompted):

	conda update conda

**Create a Python 3 virtual environment** (replace `python36` with your name of choice):
	
	conda create -n python36 python=3.6 anaconda

*NOTE: See note above about Python 3.6 vs. 3.7*

**Activate your virtual environment**:

	conda activate python36
	
**OR** (if that doesn't work):

	source activate python36

For more details about creating a conda virtual environment, see [here](https://uoa-eresearch.github.io/eresearch-cookbook/recipe/2014/11/20/conda/). Once the environment is set up and activated, we can install the dependencies listed in the `Requirements` section above.


**Download the script files** (can be done with `git clone` if user is familiar with `git` or by directly downloading the `.py` files into a single folder)

**Cloning the git repository**:

	cd <folder of interest>
	git clone https://github.com/adamspierer/time_stacker.git
	
NOTE: As of now, the platform itself is <u>not</u> callable as a module and these steps merely download the dependencies. The script files must be directly referenced when running the program. See our [tutorial](https://github.com/adamspierer/time_stacker/blob/master/TUTORIAL.md) for usage instructions.


<h3>Examples</h3>

1. `drosophila.mov` - video of fruit flies climbing in vials

<h3>Outputs</h3>

1. `test.tiff` - output from `drosophila.mov`

<h3>Usage</h3>

The following is a general overview of the program's usage. For detailed instructions, please see our [tutorial page](https://github.com/adamspierer/time_stacker/blob/master/TUTORIAL.md).

Make sure the time\_stacker scripts are downloaded and in a folder on your computer. Navigate to the `time\_stacker` directory and type:

	cd <path_to_time_stacker>

Type and run (placeholder to generate the current `./outputs/test.tiff` file):

	python ./scripts/time_stacker.py --input_file ./examples/drosophila.mov --output_file ./outputs/test.tiff --method min --interval 20


<h3>Code Structure/Overview</h3>

`time_stacker.py` - Creates a time-stack photo from a video or animated gif

We encourage you to to visit our [Tutorial page]('https://github.com/adamspierer/time_stack/blob/master/TUTORIAL.md') for a more thorough walk-through, description, and various caveats.

<h3>Version releases</h3>

1.0 - Alpha release - Script works but the innards are not polished.

<h3>Deployment</h3>

This software has only been tested on a Mac OS X (Sierra 10.15.7) but is likely not limited to this OS.

<h3>Contributing</h3>

Contributors can fork from the repository and submit a pull request when modifications are ready. Please document the changes you made and any pertinent information that will help in the review of changes.

<h3>Release History</h3>

I plan to release maintenance updates as needed, though am unlikely to modify the platform's main functionality.

<h3>Citing this work</h3>

This script was written for generating figures for the following [manuscript](https://doi.org/10.1101/2020.05.27.118604)

<h3>License</h3>

This work is licensed under the MIT license.

<h3>Authors</h3>

Written by [Adam Spierer](https://github.com/adamspierer).