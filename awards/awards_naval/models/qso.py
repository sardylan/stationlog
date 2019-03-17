from odoo import models, fields

SELECTION_BAND = [
    ("160m", "160m"),
    ("80m", "80m"),
    ("40m", "40m"),
    ("30m", "30m"),
    ("20m", "20m"),
    ("17m", "17m"),
    ("15m", "15m"),
    ("12m", "12m"),
    ("10m", "10m")
]

SELECTION_MODE = [
    ("CW", "CW"),
    ("SSB", "SSB"),
    ("DIGI", "DIGI")
]


class QSO(models.Model):
    _name = "award_naval.qso"
    _order = "ts ASC"

    _sql_constraints = [
        ("callsign_ts_mode_uniq", "UNIQUE(callsign, ts, mode)", "Record already present")
    ]

    callsign = fields.Char(
        string="Callsign",
        required=True
    )

    ts = fields.Datetime(
        string="Date & Time",
        required=True
    )

    band = fields.Selection(
        string="Band",
        selection=SELECTION_BAND,
        required=True
    )

    mode = fields.Selection(
        string="Mode",
        selection=SELECTION_MODE,
        required=True
    )

    reference = fields.Char(
        string="Reference"
    )

    operator = fields.Char(
        string="Operator",
        required=True
    )

    rawdata = fields.Char(
        string="Raw data"
    )
