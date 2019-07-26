from odoo import models, fields


class ResUsers(models.Model):
    _inherit = "res.users"

    logbook_ids = fields.Many2many(
        string="Logbooks",
        help="Enabled logbook",
        comodel_name="station_log.logbook",
        relation="station_log_logbook_res_users_read_rel",
        column1="res_users_id",
        column2="logbook_id",
        readonly=True
    )

    read_logbook_ids = fields.Many2many(
        string="Read only logbooks",
        help="Read-only enabled logbooks",
        comodel_name="station_log.logbook",
        relation="station_log_logbook_res_users_read_rel",
        column1="res_users_id",
        column2="logbook_id",
        readonly=True
    )
