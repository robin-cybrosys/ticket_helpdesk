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

import logging
import psycopg2
from odoo import models, fields, api, tools, _
_logger = logging.getLogger(__name__)


PRIORITIES = [
    ('0', 'Very Low'),
    ('1', 'Low'),
    ('2', 'Normal'),
    ('3', 'High'),
    ('4', 'Very High')]

class TicketReport(models.Model):
    _name = "ticket.report"
    _description = "HelpDesk Report"
    _auto = False
    # _rec_name = 'create_date'
    # _order = 'create_date desc'

    customer_id = fields.Many2one('res.partner', string='customer')
    customer_name = fields.Char('Customer Name')
    # subject = fields.Text('Subject')
    # description = fields.Text('Description')
    email = fields.Char('Email')
    phone = fields.Char('Phone')
    team_id = fields.Many2one('help.team', string='Helpdesk Team')
    # product_id = fields.Many2one('product.product', string='Product')
    project_id = fields.Many2one('project.project', string='Project', related='team_id.project_id', store=True)
    task_count = fields.Integer("count", compute='_compute_task_count')
    invoice_count = fields.Integer("count", compute='_compute_task_count')
    create_task = fields.Boolean(string="Create Task", related='team_id.create_task', store=True)
    priority = fields.Selection(PRIORITIES, default='0')
    stage_id = fields.Many2one('ticket.stage', string='Stage', tracking=True)
    billable = fields.Boolean(string="Billable", default=False)
    cost = fields.Float('Cost per hour')
    service_product_id = fields.Many2one('product.product', string='Service Product',
                                         domain=[('detailed_type', '=', 'service')])

    analytic_account_id = fields.Many2one('account.analytic.account', 'Analytic Account', readonly=True)

    start_date = fields.Date('Start Date')
    end_date = fields.Date('End Date')
    create_date = fields.Date('Create Date')

    ticket_id = fields.Many2one('help.ticket', 'Ticket #', readonly=True)
    public_ticket = fields.Boolean(string="Public Ticket")

    def init(self):
        # self._table = sale_report
        tools.drop_view_if_exists(self.env.cr, self._table)
        self._cr.execute("""CREATE or REPLACE VIEW %s as  SELECT l.id as id,
            l.service_product_id as service_product_id,
            l.customer_name as customer_name,
            l.public_ticket as public_ticket,
            l.customer_id as customer_id,
            l.team_id as team_id,
            l.project_id as project_id,
            l.billable as billable,
            l.email as email,
            l.phone as phone, 
            l.stage_id as stage_id,
            l.id as ticket_id, 
            l.create_task as create_task,
            l.task_count as task_count,
            proj_tsk.analytic_account_id as analytic_account_id,
            
            l.invoice_count as invoice_count,
            l.priority as priority,
            l.cost as cost, 
            l.start_date as start_date,
            l.end_date as end_date, 
            l.create_date as create_date
            FROM help_ticket l
            join res_partner partner on l.customer_id = partner.id
            left join product_product p on (l.service_product_id=p.id)
            left join product_template t on (p.product_tmpl_id=t.id)
            left join project_project proj on (l.project_id=proj.id)
            left join project_task proj_tsk on (l.project_id=proj_tsk.project_id)
            
                    
            
            
    
            """ % (self._table))