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

{
    'name': "HelpDesk Support",
    'version': '15.0.1.0.0',
    'summary': """Helpdesk Module for community""",
    'description': """Can create ticket from website also and can manage it from backend.
    Bill can be created for ticket if it has service cost""",
    'author': "Cybrosys Techno Solutions",
    'company': 'Cybrosys Techno Solutions',
    'maintainer': 'Cybrosys Techno Solutions',
    'category': 'Website',
    'depends': ['website', 'project', 'sale_project', 'hr_timesheet'],
    'data': [
        'security/ir.model.access.csv',
        'views/helpdesk.xml',
        'views/team.xml',
        'views/res_config.xml',
        'views/help_menu.xml',
        'views/report.xml',
        'views/helpdesk.xml',
        'views/portal.xml',
        'data/ticket_sequence.xml',
        'reports/report.xml',
    ],

    'images': ['static/description/banner.png'],
    'license': 'LGPL-3',
    'installable': True,
    'auto_install': False,
    'application': False,
}
