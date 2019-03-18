import logging

from odoo import models, fields, api

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

_logger = logging.getLogger(__name__)


class QSO(models.Model):
    _name = "award_naval.qso"
    _order = "ts ASC"

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
        string="Raw data",
        readonly=True
    )

    reference_auto = fields.Char(
        string="Automatic reference",
        readonly=True
    )

    @api.model
    def action_update_reference_auto(self):
        _logger.info("Updating Auto Reference")

        armi_obj = self.env["awards_naval.armi"]
        qso_obj = self.env["award_naval.qso"]

        armi_ids = armi_obj.search([])
        _logger.info("ARMI records count: %d" % len(armi_ids))

        qso_ids = qso_obj.search([])
        qso_count = len(qso_ids)
        _logger.info("QSO count: %d" % qso_count)

        count = 0
        for qso_id in qso_ids:
            qso_callsign = qso_id.callsign.upper()

            for armi_id in armi_ids:
                armi_callsign = armi_id.callsign.upper()

                if armi_callsign in qso_callsign:
                    reference = armi_id.reference
                    qso_id.reference_auto = reference
                    _logger.info("Found %s for %s" % (reference, qso_callsign))
                    count += 1
                    continue

        _logger.info("Registered %d references in %d QSO" % (count, qso_count))
