<%inherit file="/base.mako" />

<div id="content" class="span-19 push-1 last ">
  <header style="background:#00ADEF; padding:5px; font-weight:bold; color:#fff;">${c.heading}</header>
  <article>
    <%include file="/pendingMemberValidations.mako" />
    <li><a href="${url(controller='members', action='exportList')}">${_('Export as CSV')}<img src="/images/icons/pencil.png"></a></li>
    <li><a href="${url(controller='members', action='exportList', listType='RCSL')}">${_('Export as RCSL CSV')}<img src="/images/icons/pencil.png"></a></li>
    <li>${parent.error_messages()}</li>
    <li>
      <table class="table_content"> 
        ${parent.flash()}
        <tr> 
          <th class="table_title">
            #
          </th>
          <th class="table_title">
            ${_('Username')}
          </th>
          <th class="table_title">
            ${_('Surname')}
          </th>
          <th class="table_title">
            ${_('Given name')}
          </th>
          <th class="table_title">
            ${_('E-Mail')}
          </th>
          <th class="table_title">
            ${_('SSH')}
          </th>
          <th colspan="3" class="table_title">
            ${_('Tools')}
          </th>
        </tr>
        <% i = 0 %>
        % for m in c.members:
        <%
          sshPublicKey = h.literal('<img src="/images/icons/notok.png">') if not m.sshPublicKey else h.literal('<img src="/images/icons/ok.png">')
          uid = '<font color="green"><b>' + m.uid + '</b></font>' if m.fullMember else '<font color="#0479FF">' + m.uid + '</font>'
          i += 1
        %>
        <tr class="table_row"> 
          <td>${i}</td>
          <td><img src="${m.getGravatar()}" alt="${_('user profile image')}"> ${uid|n}</td>
          <td>${m.sn}</td>
          <td>${m.gn}</td>
          <td>${m.mail}</td>
          <td>${sshPublicKey}</td>
          <td><a href="${url(controller='members', action='editMember', member_id=m.uid)}"><img src="/images/icons/pencil.png"></a></td>
          <td><a href="${url(controller='payments', action='listPayments', member_id=m.uid)}"><img src="/images/icons/payment.png"></a></td>
          <td><a href="${url(controller='members', action='deleteUser', member_id=m.uid)}" onClick="return confirm('Are you sure you want to delete \'${m.uid}\'?')"><img src="/images/icons/notok.png"></a></td>
          % if m.validate:
          <td><a href="${url(controller='members', action='viewDiff', member_id=m.uid)}">validation</a></td>
          % endif
        </tr>
        % endfor
      </table>

      <!--
      <ul class="list-horizontal right">
        <li><a href="/mematool/members/list=10" class="regular button">10</a></li>
        <li><a href="/mematool/members/list=25" class="regular button">25</a></li>
        <li><a href="/mematool/members/list=50" class="regular button">50</a></li>
        <li><a href="/mematool/members/list=75" class="regular button">75</a></li>
        <li><a href="/mematool/members/list=100" class="regular button">100</a></li>
      </ul>
      !-->
      <div class="clear">&nbsp;</div>
  </article>
</div>
