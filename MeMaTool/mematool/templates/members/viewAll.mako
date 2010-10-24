<%inherit file="/base.mako" />

<%def name="css()">
	${parent.css()}
	${self.css_link('/css/viewAll.css', 'screen')}
</%def>

<table class="table_content" width="95%">
        <tr>
                <th class="table_title">
                        ${_('Username')}
                </th>
                <th class="table_title">
                        ${_('Common name')}
                </th>
                <th class="table_title">
                        ${_('Surname')}
                </th>
                <th class="table_title">
                        ${_('Given name')}
                </th>
                <th class="table_title">
                        ${_('Home directory')}
                </th>
                <th class="table_title">
                        ${_('Mobile')}
                </th>
		<th class="table_title">
			${_('PEAP enabled')}
		</th>
		<th class="table_title">
			${_('SSH Key')}
		</th>
		<th colspan="3" class="table_title">
			${_('Tools')}
		</th>
        </tr>
<%
	x = 0
%>
% for m in c.members:
	<%
			x += 1
			color = "#99ffcc" if x % 2 else "white"
			peapPossible = h.literal('<font color="red">no</font>') if not m.sambaNTPassword else h.literal('<font color="green">yes</font>')
			sshPublicKey = 'no' if not m.sshPublicKey else h.literal('<font color="green">yes</font>')
	%>
	<tr style="background-color:${color};" class="table_row">
		<td>${m.dtusername}</td>
                <td>${m.cn}</td>
	        <td>${m.sn}</td>
	        <td>${m.gn}</td>
		<td>${m.homeDirectory}</td>
		<td>${m.mobile}</td>
		<td>${peapPossible}</td>
		<td>${sshPublicKey}</td>
		<td><a href="${url(controller='members', action='editMember', member_id=m.idmember)}">edit</a></td>
		<td><a href="${url(controller='payments', action='showPayments', member_id=m.idmember)}">payments</a></td>
        </tr>
% endfor

</table>
