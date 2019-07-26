from odoo import models, fields, api


class Station(models.Model):
    _name = "station.station"
    _description = "HAM radio stations"
    _inherit = "mail.thread"
    _rec_name = "callsign"
    _order = "callsign ASC"

    _sql_constraints = [
        ("callsign_uniq", "UNIQUE(callsign)", "Callsign already present")
    ]

    callsign = fields.Char(
        string="Name",
        required=True,
        translate=False,
        track_visibility="onchange"
    )

    owner_partner_id = fields.Many2one(
        string="Owner",
        help="Station owner",
        comodel_name="res.partner",
        track_visibility="onchange"
    )

    position = fields.Char(
        string="Position",
        help="Position on the world",
        required=True,
        default=lambda self: self.env["widget_googlemaps.utility_googlemaps"].compute_default_position_value(),
        track_visibility="onchange"
    )

    note = fields.Html(
        string="Note"
    )

    @api.onchange("callsign")
    @api.constrains("callsign")
    def check_callsign(self):
        for rec in self:
            value = rec.callsign and rec.callsign.strip().upper()
            if value and rec.callsign != value:
                rec.callsign = value
