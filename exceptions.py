from flask import make_response

class CustomExceptions(Exception):
    def __init__(self, msg = "Generic Msg", statusCode = 500):
        self.message = msg
        self.statusCode = statusCode
    
    def response(self):
        return make_response({
            "message": self.message
        }, self.statusCode)