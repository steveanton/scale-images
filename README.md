# scale-images
Python script for scaling all images in a directory by a factor of 2.  Useful for adapting programs
that do not natively support GUI scaling on 4k machines by making the icons larger.

## Setup
Install the Python [Pillow](http://pillow.readthedocs.org/en/3.0.x/) library.
`pip install pillow`

## Usage
`$ python scale-images.py [--dry-run] path/to/directory`
Pass `--dry-run` to print out the intended changes without actually modifying any files.

## Features
Recursively descends all directories, modifying every square jpg and png image.  Maintains a
journal of modified files in the root directory so it can resume if cancelled or does not
accidentally enlarge multiple times.
