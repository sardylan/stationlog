from odoo import models, api

SELECTION_READABILITY = [
    ("1", "1"),
    ("2", "2"),
    ("3", "3"),
    ("4", "4"),
    ("5", "5")
]

SELECTION_SIGNAL_TONE = [
    ("1", "1"),
    ("2", "2"),
    ("3", "3"),
    ("4", "4"),
    ("5", "5"),
    ("6", "6"),
    ("7", "7"),
    ("8", "8"),
    ("9", "9")
]


class QSOUtility(models.AbstractModel):
    _name = "station_log.utility_qso"
    _description = "QSO utilities"

    @api.model
    def prepare_selection_readability(self):
        return SELECTION_READABILITY

    @api.model
    def prepare_selection_signal_tone(self):
        return SELECTION_SIGNAL_TONE
