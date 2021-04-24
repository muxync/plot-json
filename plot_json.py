#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Simple plotting of JSON lines from a file or stdin"""

from __future__ import unicode_literals

__author__ = "Mark Mulligan"
__email__ = "muxync@muxync.net"
__copyright__ = "Copyright 2018, Mark Mulligan"
__license__ = "MIT"

import argparse
from datetime import datetime
import json
import logging
import sys

import matplotlib.pyplot as plt
import numpy as np

# BASIC_FORMAT is defined as "%(levelname)s:%(name)s:%(message)s"
LOG_FORMAT = "[%(asctime)s] %(module)s %(levelname)8s: %(message)s"
DATE_FORMAT = "%Y-%m-%d %H:%M:%S"


def get_args():
    """Get passed arguments"""
    parser = argparse.ArgumentParser(
        description="Simple plotting of JSON lines from stdin or an input file")
    parser.add_argument(
        "parents", type=lambda x: x.split(','),
        help="parent key(s) of JSON to plot (comma separated)")
    parser.add_argument(
        "children", type=lambda x: x.split(','),
        help="child key(s) of JSON to plot (comma separated)")
    parser.add_argument(
        "-i", "--input", dest='json_file', help="JSON input file")
    parser.add_argument(
        "-d", "--datefmt", default=DATE_FORMAT, dest='date_format',
        help="JSON date format (default: %s)" % (DATE_FORMAT.replace('%', '%%')))
    parser.add_argument(
        "-v", "--verbose", default=logging.INFO, action="store_const",
        dest="loglevel", const=logging.DEBUG, help="show verbose debug output")

    args = parser.parse_args()
    logging.basicConfig(datefmt=args.date_format,
                        format=LOG_FORMAT, level=args.loglevel)

    return args


def get_json(json_file=None, **kwargs):
    """Returns a merged dict from provided JSON lines"""
    # pylint: disable=W0613

    json_dict = {}
    logging.info("Parsing JSON lines")

    # Get JSON lines from a file or stdin
    if json_file:
        with open(json_file) as jsf:
            json_lines = jsf.read().splitlines()
    else:
        json_lines = sys.stdin.readlines()

    # Load JSON lines into a dict allowing duplicate datetimes
    for line in json_lines:
        temp = json.loads(line)
        json_dict.setdefault(list(temp.keys())[0], {}).update(list(temp.values())[0])

    logging.debug("JSON dict loaded:\n%s", json_dict)

    return json_dict


def plot_json(json_dict, parents, children, date_format=DATE_FORMAT, **kwargs):
    """Displays the requested plot(s) filtered by parents and children"""
    # pylint: disable=W0613

    # Show a plot for each parent
    for par in parents:
        logging.debug("Creating plot for %s", par)

        # Only add datetimes that contain the parent
        logging.debug("Creating datetime list for %s", par)
        dt_list = [datetime.strptime(x, date_format) for x in sorted(json_dict.keys())
                   if par in json_dict[x].keys()]

        # Draw a line for each child (x: datetime, y: datapoint)
        xdt = np.array(dt_list)
        for chi in children:
            ydp = np.array([d[par][chi] for d in json_dict.values() if d.get(par, False)])
            plt.plot(xdt, ydp, label=chi)
            logging.debug("Drawing line for %s", chi)
            plt.draw()

        logging.info("Showing plot for %s", par)
        plt.title(par)
        plt.legend()
        plt.show()


def main():
    """Parse arguments and plot JSON"""
    args = get_args()
    json_dict = get_json(**vars(args))
    plot_json(json_dict, **vars(args))


if __name__ == "__main__":
    main()
