from odoo import models, fields


class Logbook(models.Model):
    _name = "station_log.logbook"
    _inherit = "mail.thread"

    name = fields.Char(
        string="Name",
        required=True,
        track_visibility="onchange"
    )

    active = fields.Boolean(
        string="Active",
        default=True,
        required=True,
        track_visibility="onchange"
    )

    res_users_ids = fields.Many2many(
        string="Users",
        help="Enabled users",
        comodel_name="res.users",
        relation="station_log_logbook_res_users_rel",
        column1="logbook_id",
        column2="res_users_id",
        domain=lambda self: [("groups_id", "in", [self.env.ref("station_log.group_user").id])],
        track_visibility="onchange"
    )

    read_res_users_ids = fields.Many2many(
        string="Read only users",
        help="Read-only enabled users",
        comodel_name="res.users",
        relation="station_log_logbook_res_users_read_rel",
        column1="logbook_id",
        column2="res_users_id",
        domain=lambda self: [("groups_id", "in", [self.env.ref("station_log.group_user").id])],
        track_visibility="onchange"
    )
