# -*- coding: utf-8 -*-
#############################################################################
#
#    Cybrosys Technologies Pvt. Ltd.
#
#    Copyright (C) 2022-TODAY Cybrosys Technologies(<https://www.cybrosys.com>)
#    Author: Cybrosys Techno Solutions(<https://www.cybrosys.com>)
#
#    You can modify it under the terms of the GNU LESSER
#    GENERAL PUBLIC LICENSE (LGPL v3), Version 3.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU LESSER GENERAL PUBLIC LICENSE (LGPL v3) for more details.
#
#    You should have received a copy of the GNU LESSER GENERAL PUBLIC LICENSE
#    (LGPL v3) along with this program.
#    If not, see <http://www.gnu.org/licenses/>.
#
#############################################################################

import base64
import json
from odoo import http, SUPERUSER_ID, _

from odoo import http
from odoo.http import request
from odoo.tools import is_html_empty
from werkzeug.exceptions import BadRequest
from odoo.exceptions import ValidationError, UserError
from odoo.addons.portal.controllers.portal import CustomerPortal, pager as portal_pager
from odoo.exceptions import AccessError, MissingError
from collections import OrderedDict
from odoo.http import request
from markupsafe import Markup

from odoo.osv.expression import OR, AND


class PortalAccountInherit(CustomerPortal):

    def _prepare_home_portal_values(self, counters):
        values = super()._prepare_home_portal_values(counters)
        if 'ticket_count' in counters:
            ticket_count = request.env['help.ticket'].search_count([('customer_id', '=', request.env.user.partner_id.id)])
            values['ticket_count'] = ticket_count
        return values

    def _ticket_get_search_domain(self, search_in, search):

        search_domain = []
        if search_in in ('content', 'all'):
            search_domain.append([('name', 'ilike', search)])

        if search_in in ('stage_id', 'all'):
            search_domain.append([('stage_id.name', 'ilike', search)])
        if search_in in ('priority', 'all'):
            if search in 'Very Low':
                search_domain.append([('priority', '=', '0')])
            elif search in 'Low':
                search_domain.append([('priority', '=', '1')])
            elif search in 'Normal':
                search_domain.append([('priority', '=', '2')])
            elif search in 'High':
                search_domain.append([('priority', '=', '3')])
            elif search in 'Very High':
                search_domain.append([('priority', '=', '4')])
            else:
                search_domain.append([('priority', 'ilike', search)])

        return OR(search_domain)

    def _ticket_get_searchbar_inputs(self):
        values = {
            'all': {'input': 'all', 'label': _('Search in All'), 'order': 1},
            'content': {'input': 'content', 'label': _('Search Name'), 'order': 1},
            'stage': {'input': 'stage', 'label': _('Search in Stages'), 'order': 4},
            'priority': {'input': 'priority', 'label': _('Search in Priority'), 'order': 6},
        }
        return dict(sorted(values.items(), key=lambda item: item[1]["order"]))

    @http.route(['/my_tickets'], type='http', auth="user", website=True)
    def portal_my_tickets(self, page=1, date_begin=None, date_end=None, sortby=None, filterby=None, search=None, search_in='content', groupby=None, **kw):
        values = self._prepare_portal_layout_values()
        partner = request.env.user.partner_id
        Tickets = request.env['help.ticket']

        # domain = self._prepare_orders_domain(partner)
        domain = [('customer_id', '=', request.env.user.partner_id.id)]
        searchbar_inputs = self._ticket_get_searchbar_inputs()

        searchbar_sortings = {
            'date': {'label': _('Create Date'), 'order': 'create_date desc'},
            'name': {'label': _('Name'), 'order': 'name'},
            'stage': {'label': _('Stage'), 'order': 'stage_id'},
        }
        # default sortby order
        if not sortby:
            sortby = 'date'
        sort_order = searchbar_sortings[sortby]['order']

        searchbar_filters = {
            'all': {'label': _('All'), 'domain': []},

        }

        # default filter by value
        if not filterby:
            filterby = 'all'
        domain += searchbar_filters[filterby]['domain']

        # search
        if search and search_in:
            domain += self._ticket_get_search_domain(search_in, search)




        # if date_begin and date_end:
        #     domain += [('create_date', '>', date_begin), ('create_date', '<=', date_end)]

        # count for pager
        order_count = Tickets.search_count(domain)
        # pager
        pager = portal_pager(
            url="/my_tickets",
            url_args={'sortby': sortby, 'search_in': search_in, 'search': search},
            total=order_count,
            page=page,
            step=self._items_per_page
        )
        # content according to pager
        orders = Tickets.search(domain, order=sort_order, limit=self._items_per_page, offset=pager['offset'])
        # request.session['my_orders_history'] = orders.ids[:100]

        values.update({
            # 'date': date_begin,
            'orders': orders.sudo(),
            'page_name': 'Tickets',
            'pager': pager,
            'default_url': '/my_tickets',
            'searchbar_sortings': searchbar_sortings,
            'sortby': sortby,
            'searchbar_filters': OrderedDict(sorted(searchbar_filters.items())),
            'filterby': filterby,
            'search_in': search_in,
            'search': search,
            'searchbar_inputs': searchbar_inputs,
        })
        return request.render("website_ticket_helpdesk.portal_my_tickets", values)

    @http.route([
        '/my_ticket/<int:order_id>',
    ], type='http', auth="public", website=True)
    def my_ticket(self, **kw):

        domain = [('customer_id', '=', request.env.user.partner_id.id), ('id', '=', kw.get('order_id'))]
        tickets = request.env['help.ticket'].search(domain)

        values = {
            'tickets': tickets,

        }
        return request.render("website_ticket_helpdesk.ticket_portal_template", values)


class Websitedesk(http.Controller):


    @http.route(['/helpdesk_ticket'], type='http', auth="public", website=True, sitemap=True)
    def helpdesk_ticket(self, **kwargs):

        return request.render('website_ticket_helpdesk.ticket_form')
