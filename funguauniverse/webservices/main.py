from flask import Flask, Response

class EndpointAction(object):
    def __init__(self, action):
        self.action = action


    def __call__(self, *args):
        # Perform the action
        answer = self.action()
        # Create the answer (bundle it in a correctly formatted HTTP answer)
        self.response = Response(answer, status=200, headers={})
        # Send it
        return self.response


class FlaskAppWrapper(object):
    app = None

    def __init__(self, name):
        self.app = Flask(name)
    
    def run(self):
        self.app.run()

    def add_endpoint(self, endpoint=None, endpoint_name=None, handler=None):
        self.app.add_url_rule(endpoint, endpoint_name, EndpointAction(handler))

    def add_all_endpoints(self):
        # Add root endpoint
        self.add_endpoint(endpoint="/", endpoint_name="/", handler=self.action)

        # Add action endpoints
        # self.add_endpoint(endpoint="/add_X",
        #                 endpoint_name="/add_X", handler=self.add_X)
        # you can add more ...
        # You can also add options here : "... , methods=['POST'], ... "

    # # ==================== ------ API Calls ------- ====================


    # def action(self):
    #     # Dummy action
    #     return "action"  # String that will be returned and display on the webpage
    #     # Test it with curl 127.0.0.1:5000


    # def add_X(self):
    #     # Dummy action
    #     return "add_X"
    #     # Test it with curl 127.0.0.1:5000/add_X
