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


class HelpDeskTeam(models.Model):
    _name = 'help.team'
    _description = 'Helpdesk Team'

    name = fields.Char('Name')
    member_ids = fields.Many2many('res.users', string='Members')
    email = fields.Char('Email')
    project_id = fields.Many2one('project.project', string='Project')
    create_task = fields.Boolean(string="Create Task")

