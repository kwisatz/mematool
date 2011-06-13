import logging

from pylons import request, response, session, tmpl_context as c, url
from pylons.controllers.util import abort, redirect

from mematool.lib.base import BaseController, render
from pylons.decorators.secure import https
from mematool.lib.syn2cat.auth.auth_ldap import LDAPAuthAdapter
from mematool.lib.syn2cat.crypto import encodeAES, decodeAES


log = logging.getLogger(__name__)

class AuthController(BaseController):

	def index(self,environ):
		if self.identity is not None:
			redirect(url(controller='members', action='showAllMembers'))
		else:
			redirect(url(controller='auth', action='login'))
	
		#if notAuthenticated:
		#	abort(401, 'You are not authenticated')
		
		#if isForbidden:
		#	abort(403, 'You don\'t have rights to accesss this page')


	@https()
	def login(self):
		if self.identity is not None:
			if 'came_from' in request.params:
				#redirect(request.params['came_from'])
				redirect(url(controller='members', action='showAllMembers'))
			else:
				redirect(url(controller='members', action='showAllMembers'))

		c.heading = 'MeMaTool'

		return render('/auth/login.mako')


	def doLogin(self):
		if not 'login' in request.params or request.params['login'] == '' or not 'password' in request.params or request.params['password'] == '':
			print "crap"
		else:
			authAdapter = LDAPAuthAdapter()
			ret = authAdapter.authenticate_ldap(request.params['login'], request.params['password'])

			if ret:
				session['identity'] = request.params['login']
				session['secret'] = encodeAES( request.params['password'] )
				session['groups'] = authAdapter.getUserGroups()
				session.save()

				if 'after_login' in session:
					print session["after_login"]
					redirect(session["after_login"])

		redirect(url(controller='auth', action='login'))


	def logout(self):
		if self.identity is not None:
			session['identity'] = None
			session.invalidate()
			session.save()
			session.delete()
			request.environ["REMOTE_USER"] = ""

		redirect(url(controller='auth', action='login'))

	def _require_auth(self):
		return False
