from odoo import models, fields


class Contest(models.Model):
    _name = "stationlog.contest"
    _inherit = "mail.thread"
    _description = "QSO"
    _order = "ts_start DESC, ts_end DESC"

    name = fields.Char(
        string="Name",
        help="Contest name",
        track_visibility="onchange",
        required=True
    )

    ts_start = fields.Datetime(
        string="Start",
        track_visibility="onchange",
        required=True
    )

    ts_end = fields.Datetime(
        string="End",
        track_visibility="onchange",
        required=True
    )

    qso_ids = fields.One2many(
        string="QSOs",
        help="QSOs related to this contest",
        comodel_name="stationlog.qso",
        inverse_name="contest_id"
    )

    note = fields.Html(
        string="Note"
    )

    qso_count = fields.Integer(
        string="QSOs number",
        help="Number of QSOs",
        readonly=True,
        compute="_compute_qso_count"
    )

    def _compute_qso_count(self):
        for rec in self:
            rec.qso_count = len(rec.qso_ids)
