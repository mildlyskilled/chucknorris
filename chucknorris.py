import urllib2
import json
import sys
from getopt import getopt, GetoptError


class ChuckNorris():

    """Library for interacting with the chuck norris API"""

    base_url = "http://api.icndb.com/jokes/{0}"

    def __init__(self, opts=None, args=None):
    	if not opts:
    		return self.get_random_jokes()

        for opt, arg in opts:
            if opt in ("-r", "--random"):
                if opt == "--random":
                    return self.get_random_jokes(arg)

                return self.get_random_jokes()

            elif opt == '-h':
                self.usage()
                return None

            elif opt == "--id":
                return self.get_joke_by_id(arg)
            else:
            	self.usage()

    def _call(self, url):
        try:
            response = urllib2.urlopen(url)
            return json.loads(response.read())
        except urllib2.HTTPError as e:
            return "{0}: {1}".format(e.code, e.read())

    def _output(self, data):
        if type(data) is dict:
        	if type(data["value"]) is list:
        		for joke in data["value"]:
        			print "- {0}".format(joke['joke'])
        	else:
        		print "- {0}".format(data["value"]["joke"])
            
        else:
            print data

    def get_random_jokes(self, count=1):
        url = self.base_url.format("random")
        if count > 1:
            url += "/{0}".format(count)
        d = self._call(url)
        self._output(d)

    def get_joke_by_id(self, id):
        if id:
    		url = self.base_url.format(id)
        d = self._call(url)
        self._output(d)

    def usage(self):
    	print """ My little Chuck Norris joke Library basically retrieves jokes from the 
    	Internet Chuck Norris Database (go figure). I will not waste any more time on this
    	so you may copy and modify as you wish
    	Kwabena Aning kwabena.aning@gmail.com
    	"""
        print "-h: Display this help"
        print "-r: Get random joke"
        print "--random=<number>: Get random <number> jokes"
        print "--id=<number>: Get joke with <id>"


if __name__ == '__main__':
    try:
        opts, args = getopt(sys.argv[1:], "hr", ["id=", "random="])
        cn = ChuckNorris(opts, args)
    except GetoptError as e:
        print e.read()
    	print "Invalid option"
        ChuckNorris.usage(ChuckNorris())
        sys.exit(2)
