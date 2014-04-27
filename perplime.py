#!/usr/bin/env python

import os
import errno
from time import time
from datetime import datetime
import dbm
import sys

try:
    from PIL import Image
except:
    print "No PIL no hashing!!"

def download_file(url, path):
    import urllib2
    the_file = urllib2.urlopen(url)
    write_to_file_in_dir(the_file.read(), path)


def write_to_file_in_dir(what, path):
    try:
        open(path, 'w').write(what)
    except IOError as e:
        if e.errno == errno.ENOENT:
            os.makedirs(os.path.dirname(path))
            open(path, 'w').write(what)
        else:
            raise


def parse_cmdline():
    import argparse

    parser = argparse.ArgumentParser(description='mi.perpli.me')
    parser.add_argument('-t', '--title', required=True,
                        help='The title of the image')
    parser.add_argument('-d', '--description',
                        default='',
                        help='Description of the post')
    parser.add_argument('-u', '--url', required=True,
                        help='The url of the entry')
    parser.add_argument('-i', '--images-directory',
                        default='content/images',
                        help='Where to store the images')
    parser.add_argument('-I', '--images-url',
                        default='/images',
                        help='The images directory absolute url')
    parser.add_argument('-e', '--entries-directory',
                        default='content',
                        help='Where to store the entry file')
    parser.add_argument('-l', '--hash-list',
                        default='hash',
                        help='Where to check/store image hashes')
    parser.add_argument('-D', '--datetime',
                        default=None,
                        help='Set a custom date and time for the post (YYYY-MM-DD hh:mm)')
    parser.add_argument('-f', '--force',
                        help='force image writing',
                        action="store_true")

    return parser.parse_args()


def hash_calc(im):
    if not isinstance(im, Image.Image):
        im = Image.open(im)
    im = im.resize((8, 8), Image.ANTIALIAS).convert('L')
    avg = reduce(lambda x, y: x + y, im.getdata()) / 64.
    return reduce(lambda x, (y, z): x | (z << y),
                  enumerate(map(lambda i: 0 if i < avg else 1, im.getdata())),
                  0)


def hash_check(hsh, filename):
    hashes = dbm.open(filename, "c")

    ret = str(hsh) in hashes and hashes[str(hsh)]

    hashes.close()
    return ret


def hash_write(hsh, filename, url):
    hashes = dbm.open(filename, "c")

    if str(hsh) in hashes:
        hashes[str(hsh)] = "%s %s" % (hashes[str(hsh)], url)
    else:
        hashes[str(hsh)] = url

    hashes.close()


def write_entry(title, date, description, entryfile, imageurl):
    what = '''Title: {}
Date: {}

![{}]({})'''.format(title,
                    date.strftime("%Y-%m-%d %H:%M:%S"),
                    len(description) and description or title,
                    imageurl)

    write_to_file_in_dir(what, entryfile)

if __name__ == '__main__':
    config = parse_cmdline()

    now = time()
    now_date = config.datetime and \
        datetime.strptime(config.datetime, "%Y-%m-%d %H:%M:%S") or \
        datetime.fromtimestamp(now)
    filename = str(now).replace(".", "_")
    entry_file = os.path.join(config.entries_directory, "%s.md" % filename)
    image_file = os.path.join(config.images_directory, filename)
    image_url = os.path.join(config.images_url, filename)
    hash_list = config.hash_list

    download_file(config.url, image_file)

    if 'Image' in dir():
        image_hash = hash_calc(image_file)
        check = hash_check(image_hash, hash_list)
    else:
        image_hash = None
        check = False

    if not check or config.force:
        write_entry(config.title.upper(),
                    now_date,
                    config.description,
                    entry_file,
                    image_url)

        if image_hash:
            hash_write(image_hash, hash_list, config.url)

        sys.exit(0)

    else:
        sys.stderr.write("COLLISION: %s\n" % check)
        sys.exit(1)
