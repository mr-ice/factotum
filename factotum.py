#!Users/michaelrice/project/factotum/bin/python2.7


# factotum - a simple http REST like server for arbitrary commands
# Copyright (C) 2014-2015s Michael Rice <michael@riceclan.org>
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
import rtyaml


from twisted.internet import reactor
from twisted.web.server import Site
from twisted.web.resource import Resource
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

reactor.listenTCP(config['port'], factory)
reactor.run()
