from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import pickle
import traceback

from http.server import SimpleHTTPRequestHandler, HTTPServer
from socketserver import ThreadingMixIn
from funguauniverse.utils.web.threadpoolmixin import ThreadPoolMixIn


class ThreadedService(ThreadPoolMixIn, HTTPServer):
    def __init__(self, fun_service, address, port):
        # Create a service that
        handler = _make_handler(fun_service)
        HTTPServer.__init__(self, (address, port), handler)


def _make_handler(external_env):
    class Handler(SimpleHTTPRequestHandler):
        def do_POST(self):
            content_len = int(self.headers.get("Content-Length"), 0)
            raw_body = self.rfile.read(content_len)
            parsed_input = pickle.loads(raw_body)
            try:
                response = self.execute_command(parsed_input)
                self.send_response(200)
                self.end_headers()
                self.wfile.write(pickle.dumps(response))
            except Exception:
                self.send_error(500, traceback.format_exc())

        def execute_command(self, args):
            command = args["command"]
            arguments = args["args"]
            keywords = args["kwargs"]
            response = {}

            # print(args)
            # Create a method that allows us to determine executed command and associated action. 
            # Perhaps create a parser for this 
            if hasattr(external_env, command):
                command_resposne = getattr(external_env, command)(*arguments, **keywords)
                if command_resposne is not None:
                    response['data'] = command_resposne
            else:
                raise Exception("Unknown command: {}".format(command))
            return response

    return Handler



def start_service(env, host, port):
    service = ThreadedService(env, host, port)
    print(f"Serving Service on Port: {host}:{port}")
    service.serve_forever()


