"""
The MIT License

Copyright (c) 2007 Leah Culver

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
"""

import argparse
import os
from PIL import Image
import sys

class Journal(object):
    def __init__(self, path):
        self.f = open(path, "a+")
        self.f.seek(0, os.SEEK_SET)
        self.converted_files = {line.strip() for line in self.f}

    def add_converted_file(self, path):
        if path in self.converted_files:
            return
        print(path, file=self.f)
        self.f.flush()
        self.converted_files.add(path)

    def has_converted_file(self, path):
        return path in self.converted_files

def scale_image(image_path, relpath, journal, dry_run=False):
    if journal.has_converted_file(relpath):
        #print("%s already converted" % (image_path,))
        return
    img = Image.open(image_path)
    if img.width != img.height:
        print("%s is not square -- skipping" % (image_path,))
        img.close()
        return
    # copy the image data to an in memory buffer so we can overwrite the original file
    img_copy = img.copy()
    img.close()
    img = img_copy
    new_width = img.width * 2
    new_height = img.height * 2
    print("%s scaling %dx%d -> %dx%d" % (image_path, img.width, img.height, new_width, new_height))
    if dry_run:
        print("Not performing operation due to dry run")
        return
    os.rename(image_path, image_path + ".bak")
    scaled_img = img.resize((new_width, new_height))
    scaled_img.save(image_path)
    journal.add_converted_file(relpath)

def scale_images(root_dir, journal_path, dry_run=False):
    journal = Journal(journal_path)
    for root, dirs, files in os.walk(root_dir):
        for filename in files:
            path = root + os.sep + filename
            relpath = os.path.relpath(path, root_dir)
            if path.endswith(".jpg") or path.endswith(".png"):
                scale_image(path, relpath, journal, dry_run)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=
            "Scales all images in a directory by a factor of two.")
    parser.add_argument("dir")
    parser.add_argument("--dry-run", action="store_true")

    args = parser.parse_args()

    if not os.path.isdir(args.dir):
        print("%s is not a directory" % (args.dir,), file=sys.stderr)
        sys.exit(1)
    scale_images(args.dir, "%s/scale-images.journal" % (args.dir,), args.dry_run)
