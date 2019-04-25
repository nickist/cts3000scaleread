from tornado import websocket
import tornado.ioloop

class EchoWebSocket(websocket.WebSocketHandler):
    def check_origin(self, origin):
        return True
    def open(self):
        print ("Websocket Opened")

    def on_message(self, message):
        i = 0
        if(message == "Start"):
            self.write_message(u"%s" % message)
            i+=1
        elif (message == "Stop"):
            self.on_close()



    def on_close(self):
        print ("Websocket closed")


if __name__ == "__main__":
    application = tornado.web.Application([(r"/", EchoWebSocket),])
    application.listen(9000)
    try:
        tornado.ioloop.IOLoop.instance().start()
    except KeyboardInterrupt:
        tornado.ioloop.IOLoop.instance().Stop()