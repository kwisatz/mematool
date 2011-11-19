<%inherit file="/base.mako" />

<%!
def getFormVar(s, c, var):
	if hasattr(c, var):
		return getattr(c, var)

	if 'reqparams' in s:
		if var in s['reqparams']:
			return s['reqparams'][var]

	if var in vars(c.payment):
		return vars(c.payment)[var]

%>


<%def name="actions()" >
	<p id="actions">
		<a href="${url(controller='payments', action='listPayments', member_id=c.member_id)}">&lt;-- ${_('back to Payments')}</a>
	</p>
</%def>

${h.form(url(controller='payments', action='savePayment'), method='post', name='addpaymentform')}
<div id="content" class="span-19 push-1 last ">
<header style="background:#00ADEF; padding:5px; font-weight:bold; color:#fff;">${c.heading}</header>
<article>

<table class="table_content" width="95%">
	${parent.all_messages()}
        <tr>
                <td class="table_title"><label for="date">${_('Date payed')}</label></td>
		<td>${h.text('date', value=getFormVar(session, c, 'date'), class_='input text')}(YYYY-MM-DD)</td>
        </tr>
	<tr>
                <td class="table_title"><label for="Status">${_('Status')}</label></td>
		<td>
			${_('Normal payment')}${h.radio('status', value=0, checked=c.status_0, class_='input text')}
			${_('No payment')}${h.radio('status', value=1, checked=c.status_1, class_='input text')}
			${_('Not a member')}${h.radio('status', value=2, checked=c.status_2, class_='input text')}
		</td>
	</tr>
	<tr>
		<td class="table_title"/>
		<td style="text-align:left;">
		<% 
			if (c.payment.id == None):
				label = _('Add payment')
			else:
				label = _('Edit payment')
		%>
		${h.submit('send', label, class_='input text')}</td>
	</tr>
	<input type="hidden" name="member_id" value="${c.member_id}">
	<input type="hidden" name="idPayment" value="${c.payment.id}">
</table>
${h.end_form()}
