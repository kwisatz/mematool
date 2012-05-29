#
# Copyright (c) 2012 Georges Toth <georges _at_ trypill _dot_ org>
#
# This file is part of MeMaTool.
#
# MeMaTool is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# MeMaTool is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with MeMaTool.  If not, see <http://www.gnu.org/licenses/>.

import logging

from pylons import request, response, session, tmpl_context as c, url
from pylons.controllers.util import redirect
from pylons import config
from pylons.i18n.translation import _, set_lang

from mematool.lib.base import BaseController, render, Session
from mematool.model import Member, TmpMember

log = logging.getLogger(__name__)

import re
from mematool.lib.syn2cat import regex
from mematool.lib.syn2cat.crypto import encodeAES
from mematool.model.ldapModelFactory import LdapModelFactory
from mematool.model.lechecker import ParamChecker, InvalidParameterFormat

from webob.exc import HTTPUnauthorized

from email.mime.text import MIMEText


class ProfileController(BaseController):

  def __init__(self):
    super(ProfileController, self).__init__()
    self.lmf = LdapModelFactory()

  def __before__(self):
    super(ProfileController, self).__before__()
    self._sidebar()

  def _print 'Edit :: No such user !'

    return 'ERROR 4x0'

  def checkMember(f):
    def new_f(self):
      # @TODO request.params may contain multiple values per key... test & fix
      formok = True
      errors = []

      m = self.lmf.getUser(session['identity'])

      for v in m.str_vars:
        if v in request.params:
          setattr(m, v, request.params.get(v, ''))

      try:
        m.check()
      except InvalidParameterFormat as ipf:
        formok = False
        errors += ipf.message

      if 'userPassword' in request.params and len(request.params['userPassword']) > 0:
        try:
          ParamChecker.checkPassword('userPassword', 'userPassword2')
        except InvalidParameterFormat as ipf:
          formok = False
          errors.append(ipf.message)

      if not formok:
        session['errors'] = errors
        session['reqparams'] = {}

        # @TODO request.params may contain multiple values per key... test & fix
        for k in request.params.iterkeys():
          session['reqparams'][k] = request.params[k]

        session.save()

        redirect(url(controller='profile', action='edit'))

      return f(self)
    return new_f

  @checkMember
  def doEdit(self):
    m = self.lmf.getUser(session['identity'])

    if m.validate:
      # member locked for validation
      redirect(url(controller='error', action='forbidden'))
    else:
      changes = False

      if request.params['sn'] != m.sn or\
        request.params['givenName'] != m.givenName or\
        request.params['birthDate'] != m.birthDate or\
        request.params['homePostalAddress'] != m.homePostalAddress or\
        ('homePhone' in request.params and len(request.params['homePhone']) > 0 and request.params['homePhone'] != m.homePhone) or\
        request.params['mobile'] != m.mobile or\
        request.params['mail'] != m.mail or\
        request.params['xmppID'] != m.xmppID:
        changes = True

      if changes:
        tm = TmpMember(m.uidNumber)
        tm.sn = str(request.params['sn'].encode('utf-8'))
        tm.gn = str(request.params['givenName'].encode('utf-8'))
        tm.birthDate = request.params['birthDate']
        tm.homePostalAddress = str(request.params['homePostalAddress'].encode('utf-8'))

        if 'homePhone' not in request.params or (request.params['homePhone'] == '' and not m.homePhone is ''):
          tm.phone = '>>REMOVE<<'
        else:
          tm.phone = request.params['homePhone']

        if 'xmppID' not in request.params or (request.params['xmppID'] == '' and not m.xmppID is ''):
          tm.xmppID = 'removed'
        else:
          tm.xmppID = request.params['xmppID']

        tm.mobile = request.params['mobile']
        tm.mail = request.params['mail']

        Session.add(tm)
        Session.commit()

        session['flash'] = _('Changes saved!')
        session['flash_class'] = 'success'

        self.mailValidationRequired()
      else:
        session['flash'] = _('Nothing to save!')
        session['flash_class'] = 'info'

      if 'userPassword' in request.params and 'userPassword2' in request.params and request.params['userPassword'] != '' and request.params['userPassword'] == request.params['userPassword2']:
        m.setPassword(request.params['userPassword'])
        self.lmf.saveMember(m, is_admin=False)
        session['secret'] = encodeAES(request.params['userPassword'])

        session['flash'] = _('Password updated!')
        session['flash_class'] = 'success'

    session.save()
    redirect(url(controller='profile', action='index'))

  def mailValidationRequired(self):
    body = 'Hi,\n'
    body += 'The following user has updated his profile which requires your approval:\n'
    body += session['identity'] + '\n'
    body += 'Please carefully review his changes and approve or reject them as required.\n\n'
    body += 'regards,\nMeMaTool'

    to = 'office@hackerspace.lu'
    subject = 'syn2cat mematool - request for validation'
    self.sendMail(to, subject, body)

  def setLang(self):
    if (not 'lang' in request.params):
      redirect(url(controller='members', action='showAllMembers'))

    if request.params['lang'] in ('en', 'lb', 'de'):
      session['lang'] = request.params['lang']
      session.save()
      set_lang(request.params['lang'])

    redirect(url(controller='members', action='showAllMembers'))
