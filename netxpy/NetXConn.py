import random
import requests
import json
import time

class SettingsError(Exception):
    """
    Exception used when backend settings are not configured.
    """
    pass


class ResponseError(Exception):
    """
    Exception used when we receive unexpected response from origin server.
    """
    def __init__(self, message):
        if isinstance(message, requests.exceptions.ConnectTimeout):
            self.response = json.loads('{"result": "Connection timeout", "code": 10001, "data": null, "message": "Connection timeout"}')
            super().__init__(self.response)
        else:
            # https://netx.artic.edu/external/api/json returned {'result': 'Access not allowed to object for the given caller', 'code': 3004, 'data': None, 'message': 'Access not allowed to object for the given caller'}, self.user=kford1, self.session_key=w8BYlsxDAuvfDJcTR3iLGQjjE
            # print(message)
            self.response = message[message.find('{'):message.rfind('}')] + '}'
            self.response = self.response.replace("'", '"')
            self.response = self.response.replace('None', 'null')
            # print(self.response)
            self.response = json.loads(self.response)
            super().__init__(self.response)

class NetXConn:
    
    def __init__(self, config):
        self.config = config
        self.timeout = 5
        self.sess = requests.Session()
        return
    
    @property
    def session_key(self):
        if not getattr(self, '_session_key', None):
            self._session_key = self.login()
        return self._session_key
        
    def _restore_connection(self):
        delattr(self, '_session_key')
        _ = self.session_key
    
    def execute(self, context):
        try:
            response = self.request(context)
            result = response.get('result', None)
            return result
        except ResponseError as err:
            raise
            # return err.response
        
    def login(self):
        """
        Sends authenticate command to authenticate a user based on the supplied
        credential and returns the session key for use by subsequent API calls.
        """
        context = {
            'method': 'authenticate',
            'params': [self.config["user"], self.config["pass"]],
        }
        response = self.request(context=context)
        session_key = response.get('result', None)
        if session_key is None or session_key == "-1":
            raise SettingsError("Invalid USERNAME or PASSWORD in settings.")
        self._session_key = session_key["sessionKey"]
        return self._session_key
        
    
    # Thank you:
    # https://github.com/ic-labs/python-netx/blob/master/netx/netx.py
    def request(self, context, retries=0):
        """
        Wraps HTTP POST request with the specified data. Returns dict decoded
        from the JSON response.
        """
        
        self._nonce = str(random.getrandbits(64))

        data = {
            'id': self._nonce,
            'dataContext': 'json',
            'jsonrpc': '2.0',
        }
        data.update(context)
        data = json.dumps(data)  # Origin server expects JSON-encoded POST data
        url = self.config["apibase"]
        if (context["method"] == "facetedSearch"):
            url = self.config["appbase"] + '/' + context["method"]
        headers = {
            'user-agent': 'netxpy',
            'content-type': 'application/json',
        }

        # Retry if we get intermittent connection error
        # self._requests_limiter()
        #print("trying post")
        #print(data)
        try:
            response = self.sess.post(url, headers=headers, data=data, verify=True, timeout=self.timeout)
        except requests.exceptions.ConnectionError as err:
            if context['method'] != 'authenticate' and retries > 1:
                # LOGGER.info('retry (%d): %s', retries - 1, context)
                self.request(context, retries=retries - 1)
            else:
                raise ResponseError(err)


        if response.status_code != 200:
            raise ResponseError('%s returned HTTP%d' % (url, response.status_code))
        self.last_request = int(time.time() * 1000)
        response = response.json()
        
        nonce = response.get('id', None)
        if nonce != self._nonce:
            raise ResponseError(
                'Mismatched nonce: %s != %s\n'
                'Request: %s\n'
                'Response: %s' % (nonce, self._nonce, data, response))
        # Reraise exception returned by origin server
        error = response.get('error', None)
        if error:
            # print(error)
            msg = '%s returned %s, self.user=%s, self.session_key=%s' % (
                url, error, self.config["user"], self.session_key)
            # Retry if we have a stale connection
            if context['method'] != 'authenticate' and retries > 1:
                self._restore_connection()
                return self.request(context, retries=retries - 1)
            else:
                raise ResponseError(msg)

        return response