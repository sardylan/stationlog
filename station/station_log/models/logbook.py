from odoo import models, fields, api


class Logbook(models.Model):
    _name = "station_log.logbook"
    _description = "Station LogBook"
    _inherit = "mail.thread"
    _order = "create_date DESC"

    name = fields.Char(
        string="Name",
        required=True,
        track_visibility="onchange"
    )

    callsign = fields.Char(
        string="Callsign",
        help="Callsign",
        required=True,
        copy=False,
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

    @api.model
    def create(self, vals):
        if "callsign" in vals and vals["callsign"]:
            vals["callsign"] = vals["callsign"].strip().upper()

        return super().create(vals)

    @api.multi
    def write(self, vals):
        if "callsign" in vals and vals["callsign"]:
            vals["callsign"] = vals["callsign"].strip().upper()

        return super().write(vals)

    @api.onchange("callsign")
    def _onchange_callsign(self):
        for rec in self:
            if rec.callsign:
                rec.callsign = rec.callsign.strip().upper()

    @api.model
    def get_users_logbook_domain(self, uid):
        return [
            ("active", "=", True),
            ("res_users_ids", "in", [uid])
        ]

    @api.model
    def default_logbook_id(self, uid):
        logbook_domain = self.get_users_logbook_domain(uid)
        logbook_id = self.search(logbook_domain, limit=1)

        if not logbook_id:
            return False

        return logbook_id
