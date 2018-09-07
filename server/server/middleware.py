from django.utils.deprecation import MiddlewareMixin
from django.core.handlers.wsgi import WSGIRequest
from django.http.response import *
from wephoto.views import BaseJsonResponse
from server import tokens, settings


class DisableCSRF(MiddlewareMixin):
    def process_request(self, request):
        setattr(request, '_dont_enforce_csrf_checks', True)


class CheckToken(MiddlewareMixin):
    """
        检查请求
    """
    def process_request(self, req):
        print(req.path)
        if settings.CHECK_TOKEN and req.path.startswith("/api"):
            print("检查 user-agent")
            user_agent = req.META.get("HTTP_USER_AGENT", None)
            token = req.GET.get("token", None)
            print(user_agent, token, tokens, tokens.get(token))
            if user_agent is not None and user_agent.find("wephoto") >=0:
                print("user-agent checked")
            else:
                return JsonResponse(BaseJsonResponse("user-agent not allowed", "").error())

            if token is not None and tokens.get(token) is not None:
                print("token checked")
            else:
                return JsonResponse(BaseJsonResponse("token not allowed", "").error())
