<%inherit file="/base.mako" />

<%def name="actions()">
<p id="actions">
${h.form(url(controller='payments', action='editPayment'), method='post', name='addpayment')}
	${h.select('member_id', '1000', c.member_ids)}
	${h.submit('choose','Add payment')}
${h.end_form()}
</p>
</%def>

<table class="table_content" width="95%">
        <tr>
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
                        ${_('Payment good')}
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
                        paymentGood = h.literal('<font color="red">no</font>') if m.paymentGood == 'no' else h.literal('<font color="green">yes</font>')
        %>
        <tr style="background-color:${color};" class="table_row">
                <td>${m.uid}</td>
                <td>${m.sn}</td>
                <td>${m.gn}</td>
                <td>${paymentGood}</td>
                <td><a href="${url(controller='payments', action='listPayments', member_id=m.uid)}">payments</a></td>
        </tr>
% endfor
</table>
