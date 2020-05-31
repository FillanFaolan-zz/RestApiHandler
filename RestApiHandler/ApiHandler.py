import requests
from requests.cookies import cookiejar_from_dict

from .ResponseType import ResponseType
from .HttpMethod import HttpMethod


class ApiHandler:
    _base = None
    _path = None
    _params = None
    # auto parse dot or not
    autoParseDot = True
    # if you need to add headers or
    _session = None

    headers = {
        "User-Agent": "Mozilla/5.0 (X11; Linux i686; rv:73.0) Gecko/20100101 Firefox/73.0"
    }

    def _ParseResponse(self, resp: requests.Response, respType: ResponseType):
        if respType == ResponseType.Json:
            return resp.json()
        elif respType == ResponseType.Xml:
            raise Exception("Cannot parse xml currently, but you can use Bytes response and parse it by yourself.")
        elif respType == ResponseType.Bytes:
            return resp.content
        else:
            raise Exception("This kind of response cannot be auto-parse, use Bytes response and parse it by yourself.")

    # base: the base url of the website itself
    # path: the api path, from begin to end, the path go deeper
    # params: the params that will provide to the website
    def __init__(self, base: str, path: list = None, params: dict = None):
        self._base = base[0:len(base) - 1] if base.endswith('/') else base
        self._path = path if path is not None else []
        self._params = params if params is not None else {}
        self._session = requests.session()

    def __call__(self, **kwargs):
        params = self._params
        # iterate the arg list, along with import them to self arg list
        for key in kwargs.keys():
            params[key] = kwargs[key]
        return ApiHandler(self._base, self._path, params)

    def __getattr__(self, item):
        newPath = self._path + [item]
        return ApiHandler(self._base, newPath, self._params)

    def __str__(self):
        return self._BuildGetStyleUrI()

    def _BuildUrl(self):
        pathList = self._path
        if self.autoParseDot:
            index = 1
            end = len(pathList) - 1
            while index < end:
                if pathList[index] == "dot":
                    subPath = pathList[index - 1] + "." + pathList[index + 1]
                    pathList = pathList[0:index - 1] + [subPath] + pathList[index + 2:len(pathList)]
                    end = len(pathList) - 1
                index += 1

        urlResult = self._base
        # add path url
        for item in pathList:
            urlResult += '/' + item
        return urlResult

    def _BuildGetStyleUrI(self):
        urlResult = self._BuildUrl()
        paramResult = ''
        # add params
        for key in self._params:
            # if param is a array,it has to process separate
            value = self._params[key]
            if isinstance(value, list):
                for item in value:
                    paramResult += str(key) + '[]=' + str(item) + '&'
            else:
                paramResult += str(key) + '=' + str(value) + '&'
        # remove the last "&" and append "?" if there are params
        if len(self._params) > 0:
            paramResult = '?' + paramResult
            paramResult = paramResult[0:len(paramResult) - 1]
        return urlResult + paramResult

        # manually append path to void the situation of the path will collide the method in this class

    def SetCookies(self, cookies: dict):
        self._session.cookies = cookiejar_from_dict(cookies)

    def GetCookies(self):
        return self._session.cookies.get_dict()

    def AppendPath(self, append: str):
        newPath = self._path + [append]
        return ApiHandler(self._base, newPath, self._params)

    def AppendPaths(self, append: list):
        newPath = self._path + append
        return ApiHandler(self._base, newPath, self._params)

        # send request while invoke detail automatically determined by the method

    def _SendRequest(self, url: str, method: HttpMethod, params: dict) -> requests.Response:
        _functionMapping = {
            HttpMethod.GET: self._session.get,
            HttpMethod.POST: self._session.post,
            HttpMethod.HEAD: self._session.head,
            HttpMethod.PUT: self._session.put,
            HttpMethod.DELETE: self._session.delete,
            HttpMethod.PATCH: self._session.patch,
            HttpMethod.OPTIONS: self._session.options
        }
        reqSender = _functionMapping[method]
        response = None
        if method == HttpMethod.GET:
            response = reqSender(url=url, headers=self.headers, params=params)
        elif method == HttpMethod.POST or method == HttpMethod.PUT or method == HttpMethod.PATCH:
            response = reqSender(url=url, headers=self.headers, data=params)
        else:
            response = reqSender(url=url, headers=self.headers)
        return response

    def Get(self, respType=ResponseType.Json):
        url = self._BuildUrl()
        resp = self._SendRequest(url, HttpMethod.GET, self._params)
        return self._ParseResponse(resp, respType)

    def Post(self, respType=ResponseType.Json):
        url = self._BuildUrl()
        resp = self._SendRequest(url, HttpMethod.POST, self._params)
        return self._ParseResponse(resp, respType)

    def Put(self, respType=ResponseType.Json):
        url = self._BuildUrl()
        resp = self._SendRequest(url, HttpMethod.PUT, self._params)
        return self._ParseResponse(resp, respType)

    def Patch(self, respType=ResponseType.Json):
        url = self._BuildUrl()
        resp = self._SendRequest(url, HttpMethod.PATCH, self._params)
        return self._ParseResponse(resp, respType)

    def Head(self, respType=ResponseType.Json):
        url = self._BuildUrl()
        resp = self._SendRequest(url, HttpMethod.HEAD, self._params)
        return self._ParseResponse(resp, respType)

    def Delete(self, respType=ResponseType.Json):
        url = self._BuildUrl()
        resp = self._SendRequest(url, HttpMethod.DELETE, self._params)
        return self._ParseResponse(resp, respType)

    def Options(self, respType=ResponseType.Json):
        url = self._BuildUrl()
        resp = self._SendRequest(url, HttpMethod.OPTIONS, self._params)
        return self._ParseResponse(resp, respType)
