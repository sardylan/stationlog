from odoo import models, fields

SELECTION_DIRECTION = [
    ("tx", "Sent"),
    ("rx", "Received"),
]

SELECTION_MODE = [
    ("direct", "Direct"),
    ("bureau", "Bureau")
]


class QSL(models.Model):
    _name = "station_log.qsl"
    _description = "HAM Station QSL Card"
    _inherit = "mail.thread"
    _rec_name = "name"
    _order = "create_date DESC"

    qso_id = fields.Many2one(
        string="QSO",
        help="Related QSO",
        comodel_name="station_log.qso",
        required=True,
        track_visibility="onchange"
    )

    partner_id = fields.Many2one(
        string="Partner",
        help="Sender/Receiver",
        comodel_name="res.partner",
        required=True,
        track_visibility="onchange"
    )

    direction = fields.Selection(
        string="Direction",
        help="Sent or Received",
        selection=SELECTION_DIRECTION,
        required=True,
        track_visibility="onchange"
    )

    mode = fields.Selection(
        string="Mode",
        help="QSL mode",
        selection=SELECTION_MODE,
        required=True,
        track_visibility="onchange"
    )

    ts = fields.Datetime(
        string="Date & Time",
        help="Date & Time",
        track_visibility="onchange"
    )

    name = fields.Char(
        string="Name",
        help="Name",
        compute="_compute_name"
    )

    def _compute_name(self):
        for rec in self:
            direction_item = [x[1] for x in SELECTION_DIRECTION if x[0] == rec.direction]
            direction_string = direction_item and direction_item[0]

            rec.name = "%s - %s" % (
                rec.qso_id.short_desc,
                direction_string
            )
