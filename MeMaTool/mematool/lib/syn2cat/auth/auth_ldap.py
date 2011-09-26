# -*- coding: utf-8 -*-
##############################################################################
#
# Copyright (c) 2011, Georges Toth <georges@trypill.org>.
# All Rights Reserved.
#
##############################################################################

"""The groups and permission adapters for LDAP sources"""


from mematool.lib.syn2cat.ldapConnector import LdapConnector
from pylons import config


class LDAPAuthAdapter(object):
	"""The base class for LDAP source adapters"""
	
	def __init__(self, **kwargs):
		super(LDAPAuthAdapter, self).__init__(**kwargs)
		self.baseDN = 'dc=hackerspace,dc=lu'
		self.userDN = 'ou=People,' + self.baseDN
		self.groupDN = 'ou=Group,' + self.baseDN
		self.ldapcon = LdapConnector()
		self.con = self.ldapcon.getLdapConnection()

	def authenticate_ldap(self, username, password):
		"""Authenticate a user via LDAP and return his/her LDAP properties.

		 Raises AuthenticationError if the credentials are rejected, or
		 EnvironmentError if the LDAP server can't be reached.
		 """

		import ldap

		dn = "uid=" + username + ',' + self.userDN

		""" Bind to server """
		con = ldap.initialize(config.get('ldap.server'))
		print 'init'

		try:
			con.start_tls_s()
			print 'tls'
			try:
				con.simple_bind_s(dn, password)
				self.ldapcon.setLdapConnection(con)

				self.groups = self.ldapcon.getMemberGroups(username)
				print 'simple bind'
				return True

			except ldap.INVALID_CREDENTIALS:
				print "Your username or password is incorrect."
		except ldap.LDAPError, e:
			''' @TODO better handle errors and don't use "sys.exit" ;-) '''
			print e.message['info']
			if type(e.message) == dict and e.message.has_key('desc'):
				print e.message['desc']
			else:
				print e
				sys.exit

		return False
