import socket
import socketserver
import threading
from wsgiref.simple_server import WSGIRequestHandler, WSGIServer
from wsgiref.simple_server import make_server

import bottle
from bottle import Bottle
from utils import log_msg, log_exception, LOGDEBUG

STREAMING_TIMEOUT_IN_SECS = 600


def __bottle_stderr(*args):
    log_msg(f"{args}")


bottle._stderr = __bottle_stderr


class ThreadedWSGIServer(socketserver.ThreadingMixIn, WSGIServer):
    pass


# Need this copy of 'bottle.WSGIRefServer' to add a 'shutdown' method, so we can do a
# clean shutdown of the bottle app.
class MyWSGIRefServer(bottle.WSGIRefServer):
    def __init__(self, host: str = "", port: int = 0):
        super().__init__(host, port)
        self.__server = None

    def run(self, app) -> None:
        class FixedHandler(WSGIRequestHandler):
            # Prevent reverse DNS lookups.
            def address_string(self) -> str:
                return self.client_address[0]

            def log_request(*args, **kw):
                if not self.quiet:
                    return WSGIRequestHandler.log_request(*args, **kw)

        handler_cls = self.options.get("handler_class", FixedHandler)
        server_cls = self.options.get("server_class", ThreadedWSGIServer)

        if ":" in self.host:
            # Fix wsgiref for IPv6 addresses.
            if getattr(server_cls, "address_family") == socket.AF_INET:

                class AddressFamilyServerCls(server_cls):
                    address_family = socket.AF_INET6

                server_cls = AddressFamilyServerCls

        # CHANGE (1) TO THE ORIGINAL BOTTLE CLASS METHOD!
        server_cls.timeout = STREAMING_TIMEOUT_IN_SECS

        srv = make_server(self.host, self.port, app, server_cls, handler_cls)
        # CHANGE (2) TO THE ORIGINAL BOTTLE CLASS METHOD!
        self.__server = srv

        log_msg(f"Starting wsgiref web server, timeout = {self.__server.timeout}.")

        srv.serve_forever()

    # HERE'S THE ADDED SERVER SHUTDOWN METHOD.
    def shutdown(self) -> None:
        log_msg("Shutdown wsgiref server requested...")
        self.__server.shutdown()


__server: MyWSGIRefServer = MyWSGIRefServer()
__bottle_manager: Bottle = Bottle()
__manager_thread: threading.Thread = threading.Thread()


def route_all(app: object) -> None:
    for kw in dir(app):
        attr = getattr(app, kw)
        if hasattr(attr, "route"):
            __bottle_manager.route(attr.route)(attr)


def __begin_app() -> None:
    bottle.run(app=__bottle_manager, server=__server)


def start_thread(web_port: int) -> None:
    global __manager_thread
    global __server
    __server = MyWSGIRefServer(host="localhost", port=web_port)
    __manager_thread = threading.Thread(target=__begin_app)
    __manager_thread.start()


def stop_thread() -> None:
    log_msg("Closing bottle app and thread.", LOGDEBUG)
    try:
        __bottle_manager.close()
        __server.shutdown()
        __manager_thread.join()
    except Exception as exc:
        log_exception(exc, f"Bottle app closed with exception.")
