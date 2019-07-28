from odoo import models, fields

SELECTION_TYPE = [
    ("portable", "Portable"),
    ("field", "Field day"),
    ("award", "Award"),
    ("contest", "Contest")
]


class Session(models.Model):
    _name = "station_log.session"
    _inherit = "mail.thread"
    _description = "QSO"
    _order = "ts_start DESC, ts_end DESC"

    name = fields.Char(
        string="Name",
        help="Contest name",
        required=True,
        track_visibility="onchange",
    )

    type = fields.Selection(
        string="Type",
        help="Session type",
        selection=SELECTION_TYPE,
        required=True,
        default="portable",
        track_visibility="onchange"
    )

    ts_start = fields.Datetime(
        string="Start",
        required=True,
        track_visibility="onchange"
    )

    ts_end = fields.Datetime(
        string="End",
        required=True,
        track_visibility="onchange"
    )

    qso_ids = fields.One2many(
        string="QSOs",
        help="QSOs related to this contest",
        comodel_name="station_log.qso",
        inverse_name="session_id"
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
