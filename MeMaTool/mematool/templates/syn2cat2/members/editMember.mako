<%inherit file="/base.mako" />

<%!
def getFormVar(s, c, var):
  if 'reqparams' in s:
    if var in s['reqparams']:
      return s['reqparams'][var]

  if hasattr(c, 'member'):
    if var in vars(c.member):
      return vars(c.member)[var]

  if var is 'gidNumber':
    return 100
  elif var is 'loginShell':
    return '/bin/false'
  elif var is 'homeDirectory':
    return '/home/'

  return ''
%>

<h3>${c.heading}</h3>

<form method="post" action="${url(controller='members', action='doEditMember')}" class="form-horizontal">
  ${parent.all_messages()}
  <div class="control-group">
    <label class="control-label">${_('Username')} ${_('(3-20chars, lowercase, alphanumeric only)')}</label>
    <div class="controls">
    % if c.mode is 'add':
    ${h.text('member_id', value=getFormVar(session, c, 'member_id'), class_='text')}
    % else:
    ${c.member.uid}
    % endif
    </div>
  </div>
  % if c.mode is 'edit':
  <div class="control-group">
    <label class="control-label">${_('User ID')}</label>
    <div class="controls">
    ${c.member.uidNumber}
    </div>
  </div>
  % endif
  <div class="control-group">
    <label class="control-label">${_('Additional groups')}</label>
    <div class="controls">
      ${h.checkbox('full_member', value='1', checked=getFormVar(session, c, 'full_member'), class_='text')}${_('full member')}<br>
      ${h.checkbox('locked_member', value='1', checked=getFormVar(session, c, 'locked_member'), class_='text')}${_('locked member')}

        <%
          i = 0
          first = True
        %>
        % if len(c.groups) > 0:
        <br><br>
          % for g in c.groups:
            % if i == 4:
        <br>
              <% i = 0 %>
            % endif
            % if first:
            <% first = False %>
            % else:
        ,
            % endif
        ${g}
            <% i += 1 %>
          % endfor
        % endif
    </div>
  </div>
  <div class="control-group">
    <label class="control-label">${_('Common name')}</label>
    <div class="controls">
    ${getFormVar(session, c, 'cn')}
    </div>
  </div>
  <div class="control-group">
    <label class="control-label">${_('Surname')}</label>
    <div class="controls">
    ${h.text('sn', value=getFormVar(session, c, 'sn'), class_='text')}
    </div>
  </div>
  <div class="control-group">
    <label class="control-label">${_('Given name')}</label>
    <div class="controls">
    ${h.text('givenName', value=getFormVar(session, c, 'givenName'), class_='text')}
    </div>
  </div>
  <div class="control-group">
    <label class="control-label">${_('Nationality (2 char iso-code)')}</label>
    <div class="controls">
    ${h.text('nationality', value=getFormVar(session, c, 'nationality'), class_='text')}
    </div>
  </div>
  <div class="control-group">
    <label class="control-label">${_('Convention signer')}</label>
    <div class="controls">
    ${h.text('conventionSigner', value=getFormVar(session, c, 'conventionSigner'), class_='text')}
    </div>
  </div>
  <div class="control-group">
    <label class="control-label">${_('Birth Date')} (YYYY-MM-DD)</label>
    <div class="controls">
    ${h.text('birthDate', value=getFormVar(session, c, 'birthDate'), class_='text')}
    </div>
  </div>
  <div class="control-group">
    <label class="control-label">${_('Address')}</label>
    <div class="controls">
    ${h.textarea('homePostalAddress', content=getFormVar(session, c, 'homePostalAddress'), rows='10', cols='60', class_='text')}
    </div>
  </div>
  <div class="control-group">
    <label class="control-label">${_('Phone')} (+xxx.yyyyyyyyy)</label>
    <div class="controls">
    ${h.text('homePhone', value=getFormVar(session, c, 'homePhone'), class_='text')}
    </div>
  </div>
  <div class="control-group">
    <label class="control-label">${_('Mobile')} (+xxx.yyyyyyyyy)</label>
    <div class="controls">
    ${h.text('mobile', value=getFormVar(session, c, 'mobile'), class_='text')}
    </div>
  </div>
  <div class="control-group">
    <label class="control-label">${_('E-Mail')}</label>
    <div class="controls">
    ${h.text('mail', value=getFormVar(session, c, 'mail'), class_='text')}
    </div>
  </div>
  <div class="control-group">
    <label class="control-label">${_('XMPP/Jabber/GTalk ID')}</label>
    <div class="controls">
    ${h.text('xmppID', value=getFormVar(session, c, 'xmppID'), class_='text')}
    </div>
  </div>
  <div class="control-group">
    <label class="control-label">${_('Login Shell')}</label>
    <div class="controls">
    ${h.text('loginShell', value=getFormVar(session, c, 'loginShell'), class_='text')}
    </div>
  </div>
  <div class="control-group">
    <label class="control-label">${_('Member since')} (YYYY-MM-DD)</label>
    <div class="controls">
    ${h.text('arrivalDate', value=getFormVar(session, c, 'arrivalDate'), class_='text')}
    </div>
  </div>
  <div class="control-group">
    <label class="control-label">${_('Membership canceled')} (YYYY-MM-DD)</label>
    <div class="controls">
    ${h.text('leavingDate', value=getFormVar(session, c, 'leavingDate'), class_='text')}
    </div>
  </div>
  <div class="control-group">
    <label class="control-label">${_('PGP Key')}</label>
    <div class="controls">
    ${h.text('pgpKey', value=getFormVar(session, c, 'pgpKey'), class_='text')}
    </div>
  </div>
  <div class="control-group">
    <label class="control-label">${_('iButton UID')}</label>
    <div class="controls">
    ${h.text('iButtonUID', value=getFormVar(session, c, 'iButtonUID'), class_='text', autocomplete='off')}
    </div>
  </div>
  <div class="control-group">
    <label class="control-label">${_('Has space key')}</label>
    <div class="controls">
    ${h.checkbox('spaceKey', value='1', checked=getFormVar(session, c, 'spaceKey'), class_='text')}
    </div>
  </div>
  <div class="control-group">
    <label class="control-label">${_('Is NPO member')}</label>
    <div class="controls">
    ${h.checkbox('npoMember', value='1', checked=getFormVar(session, c, 'npoMember'), class_='text')}
    </div>
  </div>
  <div class="control-group">
    <label class="control-label">${_('SSH Public Key')}</label>
    <div class="controls">
    ${h.textarea('sshPublicKey', content=getFormVar(session, c, 'sshPublicKey'), rows='10', cols='60', class_='text')}
    </div>
  </div>
  <div class="control-group">
    <label class="control-label">${_('Password')} (min 8)</label>
    <div class="controls">
    ${h.password('userPassword', value='', class_='text', autocomplete='off')}
    </div>
  </div>
  <div class="control-group">
    <label class="control-label">${_('Repeat Password')} (min 8)</label>
    <div class="controls">
    ${h.password('userPassword2', value='', class_='text', autocomplete='off')}
    </div>
  </div>

  <div class="control-group">
    <div class="controls">
      <button type="submit" class="btn">Submit</button>
    </div>
  </div>

% if c.mode is 'edit':
${h.hidden('member_id', value=c.member.uid)}
% endif
${h.hidden('mode', value=c.mode)}
</form>

<%
if 'reqparams' in session:
  del session['reqparams']
  session.save()
%>
