from setuptools import setup, find_packages

# Get the long description from the relevant file
with open('README.md','r') as f:
    long_description = f.read()

setup(name='time_stacker',
      version='1.0',
      description='time_stacker is a Python program to create time stack images from movies or animated gifs.',
      long_description=long_description,
      long_description_content_type="text/markdown",
      url='http://github.com/adamspierer/time_stacker',
      
      author='Adam Spierer',
      author_email='anspierer+Github_setup_py@gmail.com',
      license='MIT',

      classifiers=[
      'Development Status :: 4 - Beta',
      'Intended Audience :: Developers',
      'License :: OSI Approved :: MIT License',
      'Programming Language :: Python :: 3.6',
      'Programming Language :: Python :: 3.7'],

      keywords='Drosophila time-stack python3 time-visualization scientific-visualization image-processing',

      packages=find_packages(),
      install_requires=['ffmpeg-python==0.2.0',"argparse==1.1",
                        'numpy','pip','matplotlib==3.1.3'],
      zip_safe=False)
