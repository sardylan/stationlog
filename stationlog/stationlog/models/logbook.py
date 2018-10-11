from odoo import models, fields


class Logbook(models.Model):
    _name = "stationlog.logbook"

    name = fields.Char(
        string="Name",
        required=True
    )

    active = fields.Boolean(
        string="Active",
        default=True,
        required=True
    )

    res_users_ids = fields.Many2many(
        string="Users",
        help="Enabled users",
        comodel_name="res.users",
        relation="stationlog_logbook_res_users_read_rel",
        column1="logbook_id",
        column2="res_users_id",
        domain=lambda self: [("groups_id", "in", [self.env.ref("stationlog.group_user").id])]
    )

    read_res_users_ids = fields.Many2many(
        string="Read only users",
        help="Read-only enabled users",
        comodel_name="res.users",
        relation="stationlog_logbook_res_users_read_rel",
        column1="logbook_id",
        column2="res_users_id",
        domain=lambda self: [("groups_id", "in", [self.env.ref("stationlog.group_user").id])]
    )
