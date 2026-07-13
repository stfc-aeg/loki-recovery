from carrier.carrier import LokiCarrier_self_test


from tornado.ioloop import IOLoop
from tornado.escape import json_decode
from odin.adapters.adapter import ApiAdapter, ApiAdapterResponse, request_types, response_types, wants_metadata
from odin.adapters.parameter_tree import ParameterTreeError


import logging

class CarrierAdapter(ApiAdapter):

    def initialize(self, adapters):
        """Initialize the ApiAdapter after it has been registered by the API Route.
        This is an abstract implementation of the initialize mechinism that allows
        an adapter to receive a list of loaded adapters, for Inter-adapter communication.

        :param adapters: a dictionary of the adapters loaded by the API route.
        """
        self.adapters['odin_sequencer'].add_context('selftest', self.carrier)
        
        logging.debug("THIS IS THE END OF CARRIER ADAPTER INIT")

    def __init__(self, **kwargs):

        # Init superclass
        super(CarrierAdapter, self).__init__(**kwargs)

        self.carrier = LokiCarrier_self_test(**kwargs)

    @response_types('application/json', default='application/json')
    def get(self, path, request):
        """Handle an HTTP GET request.
        This method handles an HTTP GET request, returning a JSON response.
        :param path: URI path of request
        :param request: HTTP request object
        :return: an ApiAdapterResponse object containing the appropriate response
        """
        try:
            response = self.carrier.get(path, wants_metadata(request))
            status_code = 200
        except ParameterTreeError as e:
            response = {'error': str(e)}
            status_code = 400

        content_type = 'application/json'

        return ApiAdapterResponse(response, content_type=content_type,
                                    status_code=status_code)

    @request_types('application/json')
    @response_types('application/json', default='application/json')
    def put(self, path, request):
        """Handle an HTTP PUT request.
        This method handles an HTTP PUT request, returning a JSON response.
        :param path: URI path of request
        :param request: HTTP request object
        :return: an ApiAdapterResponse object containing the appropriate response
        """

        content_type = 'application/json'
        data=0
        try:
            data = json_decode(request.body)
            print("path, data: ", path, ", ", data)
            self.carrier.set(path, data)
            response = self.carrier.get(path)
            status_code = 200
        except (TypeError, ValueError) as e:
            response = {'error': 'Failed to decode PUT request body: {}'.format(str(e))}
            status_code = 400

        logging.debug(data)
        #logging.debug(response)

        return ApiAdapterResponse(response, content_type=content_type,
                                    status_code=status_code)

    def delete(self, path, request):
        """Handle an HTTP DELETE request.
        This method handles an HTTP DELETE request, returning a JSON response.
        :param path: URI path of request
        :param request: HTTP request object
        :return: an ApiAdapterResponse object containing the appropriate response
        """
        response = 'CarrierAdapter: DELETE on path {}'.format(path)
        status_code = 200

        logging.debug(response)

        return ApiAdapterResponse(response, status_code=status_code)

    def cleanup(self):
        self.carrier.cleanup()