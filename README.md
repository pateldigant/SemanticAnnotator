# Sementic Annotator

This is a python script to be used with [VGG image annotator](www.robots.ox.ac.uk/~vgg/software/via/) in order to generate masks(ground truth) for sementic segmentation.

#### Dependencies
  - pandas
  - cv2
  - numpy

#### Usage

  - Annotate multiple images with VGG image annotator. Give attriibute names while annotating to differentiate classes.
  - Download the annotation as csv file.
  - Place the input image and csv files in the same directory
  - run the python script as `python SementicAnnotator.py input_dir/csvfile.csv output_dir`
  