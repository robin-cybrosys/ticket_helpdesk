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
from odoo import models, fields, api, _


class Helpdesk(models.TransientModel):
    _inherit = 'res.config.settings'

    create_task = fields.Boolean(string="Create Task")

    def set_values(self):
        super(Helpdesk, self).set_values()
        ICPSudo = self.env['ir.config_parameter'].sudo()
        ICPSudo.set_param("website_ticket_helpdesk.create_task", self.create_task)

    @api.model
    def get_values(self):
        res = super(Helpdesk, self).get_values()
        ICPSudo = self.env['ir.config_parameter'].sudo()
        create_task = ICPSudo.get_param('website_ticket_helpdesk.create_task')

        res.update(
            create_task=create_task,
        )
        return res
