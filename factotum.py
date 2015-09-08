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
import pwd
import os
import argparse
import rtyaml
import yaml
import subprocess
import socket
import time
from flask import Flask, render_template, make_response

execdir = os.path.dirname(os.path.realpath(__file__))
workdir = os.getcwd()
parser = argparse.ArgumentParser('factotum - your handy jack of all web services')
parser.add_argument('--config','-c', 
                    help='load application configuration from file',
                    default=workdir + '/factotum.conf')

args = parser.parse_args()
args.config = os.path.realpath(args.config)

config = rtyaml.load(file(args.config))

if config['debug']:
    print(workdir)
    print(args.config)
    print(os.path.dirname(args.config))

workdir = os.path.dirname(args.config)

if os.path.isabs(config['commandfile']):
    configfile = config['commandfile']
else:
    configfile = workdir + "/" + config['commandfile']

t0 = time.strftime("%Y%m%d-%H%M%S") # timestamp
factotum = Flask(__name__)


if config['debug']:
    print("got interface as {}".format(config['interface']))

@factotum.route('/<command>', methods = ['POST', 'GET'])
def handler(command):

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
        if isinstance(run,basestring):
            run = run.split(" ")
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
        out = subprocess.check_output(run, stderr=subprocess.STDOUT)
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
    response = make_response("factotum running\r\n" \
           "    run at: {time}\r\n" \
           "    run by: {uid}@{host} (pid {pid})\r\n" \
           "    run in: cd {cwd}\r\n" \
           "    run as: {argv}\r\n" \
           "    script: {file}\r\n" \
           "    config: {config}\r\n" \
           "    commands: {command}\r\n" \
           "".format(
        time= t0,
        file= os.path.realpath(__file__),
        host= socket.gethostname(),
        uid= pwd.getpwuid(os.getuid())[0],
        pid= os.getpid(),
        cwd= workdir,
        config= args.config,
        command= configfile,
        argv=' '.join(sys.argv)
        ), 200)
    response.headers['Content-type'] = 'text/plain'
    return response

@factotum.route('/id')
def Id():
    return subprocess.check_output('/usr/bin/id', stderr=subprocess.STDOUT)

@factotum.route('/env')
def Env():
    return subprocess.check_output('/usr/bin/env', stderr=subprocess.STDOUT)

@factotum.route('/config')
def ConfigFile():
    return file(args.config).read()

@factotum.route('/commands')
def CommandFile():
    return file(configfile).read()

if __name__ == '__main__':
    factotum.run(host = config['interface'], port = config['port'], debug=config['debug'])
