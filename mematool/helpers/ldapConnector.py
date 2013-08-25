# -*- coding: utf-8 -*-
#
# Copyright (c) 2013 Georges Toth <georges _at_ trypill _dot_ org>
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


import ldap
from mematool.helpers.exceptions import InvalidCredentials, ServerError
from mematool import Config


class LdapConnector(object):
  def __init__(self, username=None, password=None):
    """ Bind to server """
    ldap.set_option(ldap.OPT_X_TLS_REQUIRE_CERT, ldap.OPT_X_TLS_ALLOW)
    self.con = ldap.initialize(Config.get('ldap', 'server'))

    try:
      self.con.start_tls_s()
      try:
        binddn = 'uid=' + username + ',' + Config.get('ldap', 'basedn_users')
        self.con.simple_bind_s(binddn, password)
      except ldap.INVALID_CREDENTIALS:
        raise InvalidCredentials()
    except ldap.LDAPError, e:
      raise ServerError(str(e))

  def get_connection(self):
    return self.con
