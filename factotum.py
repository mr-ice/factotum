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
import sys
import json
import rtyaml
import subprocess
import time

config = rtyaml.load(file('config.yaml'))

class ClockPage(Resource):
    isLeaf = True
    def render_GET(self,request):
        return "<html><body>%s</body></html>" % (time.ctime(),)

class Action(Resource):
    isLeaf = True
    def render_GET(self,request):
        return "<html><body>%s</body></html>" %

root = Resource()

for url in config['actions'].keys():
    root.putChild()

resource = ClockPage()
factory = Site(resource)

factotum = Flask(__name__)

parser = argparse.ArgumentParser(description='factotum - run your commands with a web URI')

parser.add_argument('-c','--config',
                    help='load configuration from a file')
                    
args = parser.parse_args()

if args.config:
    config = rtyaml.load(args.config)
else:
    config = rtyaml.load('factotum.conf') # default configuration
    
@app.route('/<command>', methods = ['POST'])
def handler(command):
    
    
    # handle json passed in
    # load commands
    with open(config.commandfile) as file:
        commands = json.load(file)
        
    if commands[command]:
        run = commands[command]["command"]
        for arg in commands[command]["args"]:
            if arg == "time":
                run += "%s" % (time.ctime(),)
        failed = False
        t = time.strftime("%Y%m%d-%H%M%S") # timestamp
        out = check_output(run, stderr=subprocess.STDOUT)
        try: 
            logdir = config.logdir
            if not os.path.exists(logdir):
                os.makedirs(logdir)
            try:
                f = open(logdir + "/" + command + "-" + t + ".log", 'wb+)
                f.write(out)
                f.close()
            except Exception as e:
                raise e # placeholder for error handling in the future
                
        except Exception as e:
            raise e # placeholder for error handling in the future
    else:
        print "Command not found: " + command
        return "Command not found: " + command
        
@app.route('/status')
def Status():
    return "factotum running"
    
    
if __name__ == '__main__':
    app.run(host = config.host, port = config.port, debug=config.debug)
