from odoo import models, fields


class Contest(models.Model):
    _name = "stationlog.contest"
    _inherit = "mail.thread"
    _description = "QSO"
    _order = "ts_start DESC, ts_end DESC"

    name = fields.Char(
        string="Name",
        help="Contest name",
        track_visibility="onchange"
    )

    ts_start = fields.Datetime(
        string="Start",
        track_visibility="onchange"
    )

    ts_end = fields.Datetime(
        string="End",
        track_visibility="onchange"
    )

    note = fields.Html(
        string="Note"
    )
