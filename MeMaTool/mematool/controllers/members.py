#
#	MeMaTool (c) 2010 Georges Toth <georges _at_ trypill _dot_ org>
#
#
#	This file is part of MeMaTool.
#
#
#	MeMaTool is free software: you can redistribute it and/or modify
#	it under the terms of the GNU General Public License as published by
#	the Free Software Foundation, either version 3 of the License, or
#	(at your option) any later version.
#
#	Foobar is distributed in the hope that it will be useful,
#	but WITHOUT ANY WARRANTY; without even the implied warranty of
#	MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#	GNU General Public License for more details.
#
#	You should have received a copy of the GNU General Public License
#	along with MeMaTool.  If not, see <http://www.gnu.org/licenses/>.


import logging

from pylons import request, response, session, tmpl_context as c, url
from pylons.controllers.util import abort, redirect
from pylons import config

from mematool.lib.base import BaseController, render, Session
from mematool.model import Member

log = logging.getLogger(__name__)

from mematool.lib.syn2cat.ldapConnector import LdapConnector
from sqlalchemy.orm.exc import NoResultFound
import re
from mematool.lib.syn2cat import regex

from webob.exc import HTTPUnauthorized

import gettext
_ = gettext.gettext



class MembersController(BaseController):

	def __init__(self):
		super(MembersController, self).__init__()
		self.ldapcon = LdapConnector()


	def __before__(self):
		super(MembersController, self).__before__()

		if not self.identity or not self.authAdapter.user_in_group('office', self.identity):
			print 'wualla'
			redirect(url(controller='error', action='unauthorized'))


	def _require_auth(self):
		return True


	def index(self):
		return self.showAllMembers()


	def addMember(self):
		if not ('office' in session['groups'] or 'sysops' in session['groups']):
			redirect(url(controller='members', action='showAllMembers'))

		c.heading = 'Add member'
		c.mode = 'add'


		return render('/members/editMember.mako')


	def editMember(self):
		if (not 'member_id' in request.params):
			redirect(url(controller='members', action='showAllMembers'))

		#member_q = Session.query(Member).filter(Member.dtusername == request.params['member_id'])

		try:
			#member = member_q.one()
			member = Member()
			member.uid = request.params['member_id']

			c.heading = 'Edit member'
			c.mode = 'edit'

			try:
				member.loadFromLdap()

				c.member = member

				return render('/members/editMember.mako')

			except LookupError:
				print 'No such ldap user !'

		except NoResultFound:
			print 'No such sql user !'


		return 'ERROR 4x0'


	def checkMember(f):
		def new_f(self):
			# @TODO request.params may contain multiple values per key... test & fix
			if (not 'member_id' in request.params):
				redirect(url(controller='members', action='showAllMembers'))
			else:
				formok = True
				errors = []

				if not 'mode' in request.params or (request.params['mode'] != 'add' and request.params['mode'] != 'edit'):
					formok = False
					errors.append(_('Invalid form data'))

				if not 'cn' in request.params or request.params['cn'] == '' or len(request.params['cn']) > 40:
					formok = False
					errors.append(_('Invalid common name'))

				if not 'sn' in request.params or request.params['sn'] == '' or len(request.params['sn']) > 20:
					formok = False
					errors.append(_('Invalid surname'))

				if not 'gn' in request.params or request.params['gn'] == '' or len(request.params['gn']) > 20:
					formok = False
					errors.append(_('Invalid given name'))

				if not 'birthDate' in request.params or not re.match(regex.date, request.params['birthDate'], re.IGNORECASE):
					formok = False
					errors.append(_('Invalid birth date'))

				if not 'address' in request.params or request.params['address'] == '' or len(request.params['address']) > 100:
					formok = False
					errors.append(_('Invalid address'))

				if 'phone' in request.params and request.params['phone'] != '' and not re.match(regex.phone, request.params['phone'], re.IGNORECASE):
					formok = False
					errors.append(_('Invalid phone number'))

				if not 'mobile' in request.params or not re.match(regex.phone, request.params['mobile'], re.IGNORECASE):
					formok = False
					errors.append(_('Invalid mobile number'))

				if not 'mail' in request.params or not re.match(regex.email, request.params['mail'], re.IGNORECASE):
					formok = False
					errors.append(_('Invalid e-mail address'))

				if not 'gidNumber' in request.params or not re.match('^\d+$', request.params['gidNumber']) or len(request.params['gidNumber']) > 5:
					formok = False
					errors.append(_('Invalid group'))					

				if not 'loginShell' in request.params or not re.match(regex.loginShell, request.params['loginShell'], re.IGNORECASE):
					formok = False
					errors.append(_('Invalid login shell'))

				if not 'homeDirectory' in request.params or not re.match(regex.homeDirectory, request.params['homeDirectory'], re.IGNORECASE):
					formok = False
					errors.append(_('Invalid home directory'))

				if not 'arrivalDate' in request.params or not re.match(regex.date, request.params['arrivalDate'], re.IGNORECASE):
					formok = False
					errors.append(_('Invalid "member since" date'))

				if 'leavingDate' in request.params and request.params['leavingDate'] != '' and not re.match(regex.date, request.params['leavingDate'], re.IGNORECASE):
					formok = False
					errors.append(_('Invalid "membership canceled" date'))

				if 'userPassword' in request.params and 'userPassword2' in request.params:
					if request.params['userPassword'] != request.params['userPassword2']:
						formok = False
						errors.append(_('Passwords don\'t match'))
					elif len(request.params['userPassword']) > 0 and len(request.params['userPassword']) <= 6:
						formok = False
						errors.append(_('Password too short'))

					if request.params['mode'] == 'add' and request.params['userPassword'] == '':
						formok = False
						errors.append(_('No password set'))

				if not formok:
					session['errors'] = errors
					session['reqparams'] = {}

					# @TODO request.params may contain multiple values per key... test & fix
					for k in request.params.iterkeys():
						session['reqparams'][k] = request.params[k]
						
					session.save()

					if request.params['mode'] == 'add':
						redirect(url(controller='members', action='addMember'))
					else:
						redirect(url(controller='members', action='editMember', member_id=request.params['member_id']))

			return f(self)
		return new_f


	@checkMember
	def doEditMember(self):
		member = Member()
		member.uid = request.params['member_id']


		try:
			if request.params['mode'] is 'edit': 
				member.loadFromLdap()

			member.gidNumber = request.params['gidNumber']
			member.cn = request.params['cn']
			member.sn = request.params['sn']
			member.gn = request.params['gn']
			member.birthDate = request.params['birthDate']
			member.address = request.params['address']
			member.phone = request.params['phone']
			member.mobile = request.params['mobile']
			member.mail = request.params['mail']
			member.loginShell = request.params['loginShell']
			member.homeDirectory = request.params['homeDirectory']
			member.arrivalDate = request.params['arrivalDate']
			member.leavingDate = request.params['leavingDate']

			if 'sshPublicKey' in request.params and request.params['sshPublicKey'] != '':
				# @TODO don't blindly save it
				member.sshPublicKey = request.params['sshPublicKey']
			elif 'sshPublicKey' in vars(member) and request.params['mode'] is 'edit':
				member.sshPublicKey = 'removed'

			if 'userPassword' in request.params and request.params['userPassword'] != '':
				member.setPassword(request.params['userPassword'])

			if request.params['mode'] is 'edit':
				member.save()
			else:
				member.add()

			session['flash'] = 'Member details successfully edited'
			session.save()

			redirect(url(controller='members', action='showAllMembers'))

		except LookupError:
			print 'No such ldap user !'

		# @TODO make much more noise !
		redirect(url(controller='members', action='showAllMembers'))



	def getAllMembers(self):
		'''This methods retireves all members from LDAP and returns a list object containing them all'''
		ldapcon = LdapConnector()
		memberlist = ldapcon.getMemberList()
		members = []

		for key in memberlist:
			member = Member()
			member.uid = key
			member.loadFromLdap()

			members.append(member)

		return members


	def showAllMembers(self):
		try:
			c.heading = 'All members'

			members = self.getAllMembers()

			# make sure to clean out some vars
			for m in members:
				if m.sambaNTPassword != '':
					m.sambaNTPassword = '******'
				if m.userPassword != '':
					m.userPassword = '******'

			c.members = members

			return render('/members/viewAll.mako')

		except LookupError:
			print 'Lookup error!'
			pass
		except NoResultFound:
			print 'No such sql user !'



		return 'ERROR 4x0'
