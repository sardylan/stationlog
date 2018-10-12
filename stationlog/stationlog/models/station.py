from odoo import models, fields


class Station(models.Model):
    _name = "stationlog.station"
    _inherit = "mail.thread"

    callsign = fields.Char(
        string="Name",
        required=True,
        track_visibility="onchange"
    )

    note = fields.Html(
        string="Note"
    )
