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
from odoo.exceptions import UserError

_logger = logging.getLogger(__name__)

PRIORITIES = [
    ('0', 'Very Low'),
    ('1', 'Low'),
    ('2', 'Normal'),
    ('3', 'High'),
    ('4', 'Very High')]


class HelpDeskTicket(models.Model):
    _name = 'help.ticket'
    _description = 'Helpdesk Ticket'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char('Name', default=lambda self: self.env['ir.sequence'].
                       next_by_code('help.ticket') or _('New'))

    customer_id = fields.Many2one('res.partner', string='customer')
    customer_name = fields.Char('Customer Name')
    subject = fields.Text('Subject', required=True)
    description = fields.Text('Description')
    email = fields.Char('Email')
    phone = fields.Char('Phone')
    team_id = fields.Many2one('help.team', string='Helpdesk Team')
    product_id = fields.Many2one('product.product', string='Product')
    project_id = fields.Many2one('project.project', string='Project',
                                 related='team_id.project_id', store=True)
    task_count = fields.Integer("count", compute='_compute_task_count',
                                store=True)
    invoice_count = fields.Integer("count", compute='_compute_invoice_count',
                                   store=True)
    create_task = fields.Boolean(string="Create Task",
                                 related='team_id.create_task', store=True)
    priority = fields.Selection(PRIORITIES, default='0')
    stage_id = fields.Many2one('ticket.stage', string='Stage', tracking=True)
    billable = fields.Boolean(string="Billable", default=False)
    cost = fields.Float('Cost per hour')
    service_product_id = fields.Many2one('product.product',
                                         string='Service Product',
                                         domain=[
                                             ('detailed_type', '=', 'service')])

    start_date = fields.Date('Start Date')
    end_date = fields.Date('End Date')
    public_ticket = fields.Boolean(string="Public Ticket")
    invoice_ids = fields.Many2many('account.move', string='Invoices')
    task_ids = fields.Many2many('project.task', string='Tasks')

    @api.model_create_multi
    def create(self, vals_list):

        return super(HelpDeskTicket, self).create(vals_list)

    def write(self, vals):
        result = super(HelpDeskTicket, self).write(vals)
        return result

    @api.depends('task_ids')
    def _compute_task_count(self):
        """getting task count"""
        for orders in self:
            orders.task_count = self.env['project.task']. \
                search_count([('ticket_id', '=', orders.id)])

    @api.depends('invoice_ids')
    def _compute_invoice_count(self):
        """getting task count"""
        for orders in self:
            orders.invoice_count = self.env['account.move']. \
                search_count([('ticket_id', '=', orders.id)])

    def create_invoice(self):
        var = {
            'name': self.name,
            'project_id': self.project_id.id,
            'company_id': self.env.company.id,
            'ticket_id': self.id,
        }

        tasks = self.env['project.task'].search(
            [('project_id', '=', self.project_id.id),
             ('ticket_id', '=', self.id)]).filtered(
            lambda line: line.ticket_billed == False)
        if not tasks:
            raise UserError('No Tasks to Bill')

        total = sum(x.effective_hours for x in tasks if x.effective_hours > 0)

        invoice = self.env['account.move'].create({
            'partner_id': self.customer_id.id,
            'ticket_id': self.id,
            'move_type': 'out_invoice',

        })
        invoice_lines = self.env['account.move.line'].with_context(
            check_move_validity=False).create({
            'product_id': self.service_product_id.id,
            'name': self.service_product_id.name,
            'move_id': invoice.id,
            'quantity': total,
            'product_uom_id': self.service_product_id.uom_id.id,
            'price_unit': self.cost,
            'account_id': self.service_product_id.categ_id.
            property_account_income_categ_id.id,
            'exclude_from_invoice_tab': False,

        })
        self.write({
            'invoice_ids': [(4, invoice.id)]
        })

        for task in tasks:
            task.ticket_billed = True

        invoice_lines._onchange_price_subtotal()
        # invoice._compute_invoice_taxes_by_group()
        invoice_lines._onchange_mark_recompute_taxes()
        invoice.with_context(
            check_move_validity=False)._onchange_recompute_dynamic_lines()

        # vals = {
        #     ''
        # }

    def create_tasks(self):

        task_id = self.env['project.task'].create({
            'name': self.name,
            'project_id': self.project_id.id,
            'company_id': self.env.company.id,
            'ticket_id': self.id,
        })
        self.write({
            'task_ids': [(4, task_id.id)]
        })

        return {
            'name': 'Tasks',
            # 'domain': [('ticket_id', '=', self.id)],
            'res_model': 'project.task',
            'view_id': False,
            'res_id': task_id.id,
            'view_mode': 'form',
            'type': 'ir.actions.act_window',
            'target': 'new',

        }

    def open_tasks(self):

        return {
            'name': 'Tasks',
            'domain': [('ticket_id', '=', self.id)],
            'res_model': 'project.task',
            'view_id': False,
            'view_mode': 'tree,form',
            'type': 'ir.actions.act_window',

        }

    def open_invoices(self):

        return {
            'name': 'Invoice',
            'domain': [('ticket_id', '=', self.id)],
            'res_model': 'account.move',
            'view_id': False,
            'view_mode': 'tree,form',
            'type': 'ir.actions.act_window',

        }


class StageTicket(models.Model):
    _name = 'ticket.stage'
    _description = 'Ticket Stage'

    name = fields.Char('Name')
    sequence = fields.Integer('Sequence')
    closing_stage = fields.Boolean('Closing Stage', default=False)
    # folded = fields.Boolean('Folded in Kanban', default=False)


class Tasks(models.Model):
    _inherit = 'project.task'

    ticket_billed = fields.Boolean('Billed', default=False)
