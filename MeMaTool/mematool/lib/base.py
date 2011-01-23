"""The base Controller API

Provides the BaseController class for subclassing.
"""
from pylons.controllers import WSGIController
from pylons.templating import render_mako as render

from mematool.model.meta import Session
from mematool.lib.syn2cat.auth.auth_ldap import LDAPAuthAdapter


class BaseController(WSGIController):
    def __init__(self):
	self.authAdapter = LDAPAuthAdapter()

    def __call__(self, environ, start_response):
        """Invoke the Controller"""
        # WSGIController.__call__ dispatches to the Controller method
        # the request is routed to. This routing information is
        # available in environ['pylons.routes_dict']
        try:
            self.identity = environ.get('repoze.who.identity')

            return WSGIController.__call__(self, environ, start_response)
        finally:
            Session.remove()
