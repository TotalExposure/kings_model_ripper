#!/usr/bin/env python2.7

import urllib2
import json
import os
import errno
from PIL import Image

foo = urllib2.urlopen("http://api.erg.kcl.ac.uk/AirQuality/Hourly/Map/Json").read()

meta = json.loads(foo)
meta_maps = meta["Maps"]["Map"]


def is_valid_image(filename):
    try:
        im=Image.open(filename)
                # do stuff
        return True
    except IOError:
        return False
        print("Failed. "+filename+" is not an image")


def mkdir_p(path):
    """ 'mkdir -p' in Python """
    try:
        os.makedirs(path)
    except OSError as exc:  # Python >2.5
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else:
            raise

for meta_map in meta_maps:
    baseurl = meta_map["@MapURL"]
    speciesCode = meta_map["@SpeciesCode"]
    actual_map_url = baseurl+"/export?bbox=-0.59196709334786%2C51.1825635408232%2C0.387768324998984%2C51.7851860998837&bboxSR=&layers=&layerdefs=&size=&imageSR=&format=png&transparent=false&dpi=&time=&layerTimeOptions=&f=pjson"
    urllib2.urlopen(actual_map_url).read()

    start_date = meta_map["@EndDate"]
    start_date_dirname = start_date.replace(" ", "-")

    lonmin = -0.59196709334786
    lonmax = 0.387768324998984
    latmin = 51.2234680800641
    latmax = 51.7442815606427

    n_tiles = 22;

    for ti in range(0,n_tiles):
        for tj in range(0,n_tiles):

            r_min = float(ti)/float(n_tiles);
            r_max = float(ti+1)/float(n_tiles);
            s_min = float(tj)/float(n_tiles);
            s_max = float(tj+1)/float(n_tiles);

            subset_lonmin = lonmin*r_min+lonmax*(1-r_min)
            subset_lonmax = lonmin*r_max+lonmax*(1-r_max)
            subset_latmin = latmin*s_min+latmax*(1-s_min)
            subset_latmax = latmin*s_max+latmax*(1-s_max)


            map_png_url = "{}/export?bbox={}%2C{}%2C{}%2C{}&bboxSR=&layers=&layerdefs=&size=&imageSR=&format=png&transparent=false&dpi=&time=&layerTimeOptions=&f=image".format(baseurl, subset_lonmin, subset_latmin, subset_lonmax, subset_latmax)
            image = urllib2.urlopen(map_png_url).read()

            dirname = "data/images/{}/{}/x{}/y{}".format(speciesCode, start_date_dirname, ti, tj);
            filename = dirname+"/map.png";

            if is_valid_image(filename):
                print("Skipping "+filename)
            else:
                print("Downloading "+filename)

                mkdir_p(dirname);
                f = open(filename, 'w')
                f.write(image)
                f.close()
