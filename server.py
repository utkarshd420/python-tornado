import tornado.ioloop
import tornado.web
import tornado.websocket
from tornado import template
from random import randint
from tornado.options import define, options, parse_command_line

define("port",default=8888, help="run on the given port", type=int)
clients = dict()
class Indexhandler(tornado.web.RequestHandler):
	@tornado.web.asynchronous
	def get(self):
		print "awesome"
		temp_id = randint(10000,100000)
		self.render('index.html',id=temp_id)

class WebSocketHandler(tornado.websocket.WebSocketHandler):
    def open(self, *args):
    	print 'open'
        self.id = self.get_argument("Id")
        self.stream.set_nodelay(True)
        clients[self.id] = {"id": self.id, "object": self}
        #print clients

    def on_message(self, message):        
        """
        when we receive some message we want some message handler..
        for this example i will just print message to console
        """
        print "Client %s received a message : %s" % (self.id, message)
        for client,value in clients.iteritems():
        	value['object'].write_message(message)
        
    def on_close(self):
        if self.id in clients:
            del clients[self.id]

app=tornado.web.Application([
	(r'/',Indexhandler),
	(r'/mk/',WebSocketHandler),
	])

if __name__ == '__main__':
	parse_command_line()
	app.listen(options.port)
	tornado.ioloop.IOLoop.instance().start()