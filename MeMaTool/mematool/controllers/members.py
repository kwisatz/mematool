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
from pylons.controllers.util import redirect
from pylons import config

from mematool.lib.base import BaseController, render, Session
from mematool.model import Member, TmpMember

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


	@BaseController.needAdmin
	def __before__(self):
		super(MembersController, self).__before__()


	def _require_auth(self):
		return True


	def index(self):
		return self.showAllMembers()


	@BaseController.needAdmin
	def addMember(self):
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

			c.actions = list()
			c.actions.append( ('Show all members', 'members', 'showAllMembers') )


			try:
				member.loadFromLdap()

				c.member = member

				if member.fullMember:
					c.member.full_member = 'checked'
				if member.lockedMember:
					c.member.locked_member = 'checked'

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

				if not 'sn' in request.params or request.params['sn'] == '' or len(request.params['sn']) > 20:
					formok = False
					errors.append(_('Invalid surname'))

				if not 'gn' in request.params or request.params['gn'] == '' or len(request.params['gn']) > 20:
					formok = False
					errors.append(_('Invalid given name'))

				if not 'birthDate' in request.params or not re.match(regex.date, request.params['birthDate'], re.IGNORECASE):
					formok = False
					errors.append(_('Invalid birth date'))

				if not 'homePostalAddress' in request.params or request.params['homePostalAddress'] == '' or len(request.params['homePostalAddress']) > 255:
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

				if not 'loginShell' in request.params or not re.match(regex.loginShell, request.params['loginShell'], re.IGNORECASE):
					formok = False
					errors.append(_('Invalid login shell'))

				if not 'arrivalDate' in request.params or not re.match(regex.date, request.params['arrivalDate'], re.IGNORECASE):
					formok = False
					errors.append(_('Invalid "member since" date'))

				if 'leavingDate' in request.params and request.params['leavingDate'] != '' and not re.match(regex.date, request.params['leavingDate'], re.IGNORECASE):
					formok = False
					errors.append(_('Invalid "membership canceled" date'))

				if 'sshPublicKey' in request.params and request.params['sshPublicKey'] != '' and not re.match(regex.sshKey, request.params['sshPublicKey'], re.IGNORECASE) or len(request.params['sshPublicKey']) > 1200:
					formok = False
					errors.append(_('Invalid SSH key'))

				if 'pgpKey' in request.params and request.params['pgpKey'] != '' and not re.match(regex.pgpKey, request.params['pgpKey'], re.IGNORECASE):
					formok = False
					errors.append(_('Invalid PGP key'))

				if 'conventionSigner' in request.params and request.params['conventionSigner'] != '' and not re.match(regex.username, request.params['conventionSigner']):
					formok = False
					errors.append(_('Invalid convention signer'))


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
						if (k == 'full_member' or k == 'locked_member')  and request.params[k] == 'on':
							session['reqparams'][k] = 'checked'
						else:
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
			if request.params['mode'] == 'edit': 
				member.loadFromLdap()

			# @TODO review: for now we don't allow custom GIDs
			#member.gidNumber = request.params['gidNumber']
			member.gidNumber = '100'
			member.cn = request.params['gn'].lstrip(' ').rstrip(' ') + ' ' + request.params['sn'].lstrip(' ').rstrip(' ')
			member.sn = request.params['sn'].lstrip(' ').rstrip(' ')
			member.gn = request.params['gn'].lstrip(' ').rstrip(' ')
			member.birthDate = request.params['birthDate']
			member.homePostalAddress = request.params['homePostalAddress']
			member.phone = request.params['phone']
			member.mobile = request.params['mobile']
			member.mail = request.params['mail']
			member.loginShell = request.params['loginShell']
			member.homeDirectory = '/home/' + request.params['member_id']
			member.arrivalDate = request.params['arrivalDate']
			member.leavingDate = request.params['leavingDate']

			if 'sshPublicKey' in request.params:
				if request.params['sshPublicKey'] == '' and 'sshPublicKey' in vars(member):
					member.sshPublicKey = 'removed'
				else:
					member.sshPublicKey = request.params['sshPublicKey']
			elif 'sshPublicKey' in vars(member) and request.params['mode'] == 'edit':
				member.sshPublicKey = 'removed'

			if 'pgpKey' in request.params:
				if request.params['pgpKey'] == '' and 'pgpKey' in vars(member):
					member.pgpKey = 'removed'
				else:
					member.pgpKey = request.params['pgpKey']
			elif 'pgpKey' in vars(member) and request.params['mode'] == 'edit':
				member.pgpKey = 'removed'

			if 'conventionSigner' in request.params:
				if request.params['conventionSigner'] == '' and 'conventionSigner' in vars(member):
					member.conventionSigner = 'removed'
				else:
					member.conventionSigner = request.params['conventionSigner']
			elif 'conventionSigner' in vars(member) and request.params['mode'] == 'edit':
				member.pgpKey = 'removed'

			if 'userPassword' in request.params and request.params['userPassword'] != '':
				member.setPassword(request.params['userPassword'])

			if 'full_member' in request.params:
				member.fullMember = True

			if 'locked_member' in request.params:
				member.lockedMember = True

			if request.params['mode'] == 'edit':
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
			member = Member(key)

			members.append(member)

		return members


	def showAllMembers(self, _filter='active'):
		try:
			c.heading = 'All members'

			members = self.getAllMembers()
			c.members = []

			# make sure to clean out some vars
			for m in members:
				if m.sambaNTPassword != '':
					m.sambaNTPassword = '******'
				if m.userPassword != '':
					m.userPassword = '******'

				if _filter == 'active' and not m.lockedMember:
					c.members.append(m)
				elif _filter == 'former' and m.lockedMember:
					c.members.append(m)
				elif _filter == 'all':
					c.members.append(m)

			c.actions = list()
			c.actions.append( ('Add member', 'members', 'addMember') )
			c.actions.append( ('Active members', 'members', 'showActiveMembers') )
			c.actions.append( ('Former members', 'members', 'showFormerMembers') )
			#c.actions.append( ('RCSL export', 'members', 'rcslExport') )

			return render('/members/viewAll.mako')

		except LookupError as e:
			print 'Lookup error!'
			print e
			pass
		except NoResultFound:
			print 'No such sql user !'

		return 'ERROR 4x0'

	def showActiveMembers(self):
		return self.showAllMembers(_filter='active')

	def showFormerMembers(self):
		return self.showAllMembers(_filter='former')

	def validateMember(self):
		if (not 'member_id' in request.params):
			redirect(url(controller='members', action='showAllMembers'))

		try:
			member = Member(request.params['member_id'])

			if member.validate:
				tm = Session.query(TmpMember).filter(TmpMember.id == member.uidNumber).first()
				member.cn = tm.gn + ' ' + tm.sn
				member.gn = tm.gn
				member.sn = tm.sn
				member.birthDate = tm.birthDate
				member.homePostalAddress = tm.homePostalAddress
				member.phone = tm.phone
				member.mobile = tm.mobile
				member.mail = tm.mail

				member.save()
				Session.delete(tm)
				Session.commit()
			else:
				session['flash'] = 'Nothing to validate!'

		except LookupError:
			session['flash'] = 'Member validation failed!'

		session.save()
		redirect(url(controller='members', action='showAllMembers'))


	def rejectValidation(self):
		if (not 'member_id' in request.params):
			redirect(url(controller='members', action='showAllMembers'))

		try:
			member = Member(request.params['member_id'])

			if member.validate:
				tm = Session.query(TmpMember).filter(TmpMember.id == member.uidNumber).first()
				Session.delete(tm)
				Session.commit()
			else:
				session['flash'] = 'Nothing to reject!'

		except LookupError:
			session['flash'] = 'Validation rejection failed!'

		session.save()
		redirect(url(controller='members', action='showAllMembers'))

