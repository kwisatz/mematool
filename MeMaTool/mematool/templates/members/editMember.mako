<%inherit file="/base.mako" />

<form method="post" action="${url(controller='members', action='doEditMember')}" name="recordform">

<table class="table_content" width="95%">
        <tr>
                <td class="table_title">
                        ${_('Username')}
                </td>
		<td>
			${c.member.dtusername}
		</td>
	</tr>
	<tr>
                <td class="table_title">
                        ${_('Common name')}
                </td>
                <td>
                        <input type="text" name="cn" value="${c.member.cn}" class="input">
                </td>
	</tr>
	<tr>
                <td class="table_title">
                        ${_('Surname')}
                </td>
                <td>
                        <input type="text" name="sn" value="${c.member.sn}" class="input">
                </td>
        </tr>
	<tr>
                <td class="table_title">
                        ${_('Given name')}
                </td>
                <td>
                        <input type="text" name="gn" value="${c.member.gn}" class="input">
                </td>
        </tr>
	<tr>
                <td class="table_title">
                        ${_('Home directory')}
                </td>
                <td>
                        <input type="text" name="homeDirectory" value="${c.member.homeDirectory}" class="input">
                </td>
        </tr>
	<tr>
                <td class="table_title">
                        ${_('Mobile')}
                </td>
                <td>
                        <input type="text" name="mobile" value="${c.member.mobile}" class="input">
                </td>
        </tr>
	<tr>
		<td>
			&nbsp;
		</td>
                <td>
                        <input type="submit" name="" value="Submit" class="input">
                </td>
        </tr>
</table>


<input type="hidden" name="member_id" value="${c.member.dtusername}">
</form>
