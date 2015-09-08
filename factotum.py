#!Users/michaelrice/project/factotum/bin/python2.7


# factotum - a simple http REST like server for arbitrary commands
# Copyright (C) 2014-2015 Michael Rice <michael@riceclan.org>
# 
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
# 
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#

from __future__ import print_function
import sys
import os
import argparse
import rtyaml
import subprocess
import time
from flask import Flask, render_template

workdir = os.path.dirname(os.path.realpath(__file__))

factotum = Flask(__name__)

parser = argparse.ArgumentParser('factotum - your handy jack of all web services')
parser.add_argument('--config','-c', 
                    help='load application configuration from file',
                    default='factotum.conf')

args = parser.parse_args()

config = rtyaml.load(file(args.config))

if config['debug']:
    print("got interface as {}".format(config['interface']))

@factotum.route('/<command>', methods = ['POST', 'GET'])
def handler(command):

    configfile = workdir + "/" + config['commandfile']
    if config['debug']:
        print(configfile)
        print(command)
    # load commands data inside the loop -- this ensures changes are picked up immediately
    try:
        with open(configfile) as file:
            commands = rtyaml.load(file)
    except Exception as e:
        raise e # do something smart here later (open config)

    print(commands[command].__str__())

    if command not in commands:
        print("Command not found: {}".format(command))
        return "Command not found: {}".format(command)

    try:
        run = commands[command]['exec']
    except Exception as e:
        raise e # do something smart here later (set run string)

    try:
        chdir = commands[command]['chdir']
    except Exception as e:
        raise e # do something smart here later (set chdir string)

    try:
        t = time.strftime("%Y%m%d-%H%M%S") # timestamp
    except Exception as e:
        raise e # do something smart here later (set timestamp string)

    try:
        if config['debug']:
            print("About to run {} after chdir({})".format(run,chdir))
    except Exception as e:
        raise e # do something smart here later (print debugging info)

    try:
        os.chdir(chdir)
    except Exception as e:
        raise e # do something smart here later (chdir)

    try:
        out = subprocess.check_output(run, stderr=subprocess.STDOUT, shell=True)
        return out
    except Exception as e:
        raise e # do something smart here later (subprocess.check_output)

        # try:
        #     logdir = config.logdir
        #     if not os.path.exists(logdir):
        #         os.makedirs(logdir)
        #     try:
        #         f = open(config.logdir + "/" + command + "-" + t + ".log", 'wb+)
        #         f.write(out)
        #         f.close()
        #     except Exception as e:
        #         raise e # placeholder for error handling in the future
        #
        # except Exception as e:
        #     raise e # do something smart here later
    except Exception as e:
        raise e # do something smart here later (try run)

    return "Error: fell through"

@factotum.route('/status')
def Status():
    return "factotum running"
    
    
if __name__ == '__main__':
    factotum.run(host = config['interface'], port = config['port'], debug=config['debug'])
