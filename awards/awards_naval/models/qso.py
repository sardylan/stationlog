import datetime
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

SELECTION_DUPE = [
    ("normal", "Normal"),
    ("dupe", "DUPE")
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

    dupe = fields.Selection(
        string="DUPE",
        selection=SELECTION_DUPE,
        readonly=True,
        required=True,
        default="normal"
    )

    rst_tx = fields.Char(
        string="RST TX",
        compute="compute_rst",
        readonly=True
    )

    rst_rx = fields.Char(
        string="RST RX",
        compute="compute_rst",
        readonly=True
    )

    country_id = fields.Many2one(
        string="Country",
        comodel_name="hamutility.country",
        compute="compute_country",
        readonly=True,
        store=True
    )

    ts_date = fields.Date(
        string="Date",
        compute="compute_ts_date",
        readonly=True,
        store=True
    )

    ts_time = fields.Char(
        string="Time",
        compute="compute_ts_date_time",
        readonly=True,
        store=True
    )

    @api.depends("mode")
    def compute_rst(self):
        for rec in self:
            rst = rec.mode in ["CW", "DIGI"] and "599" or "59"
            rec.rst_tx = rst
            rec.rst_rx = rst

    @api.depends("callsign")
    def compute_country(self):
        utility_callsign_onj = self.env["hamutility.utility_callsign"]

        for rec in self:
            if rec and rec.callsign:
                rec.country_id = utility_callsign_onj.get_country(rec.callsign)

    @api.depends("ts")
    def compute_ts_date_time(self):
        for rec in self:
            rec.ts_date = rec.ts.strftime("%Y-%m-%d")
            rec.ts_time = rec.ts.strftime("%H%M%S")

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

    @api.model
    def action_update_missing_reference(self):
        _logger.info("Updating Missing Reference")

        qso_obj = self.env["award_naval.qso"]

        qso_ids = qso_obj.search([
            ("reference", "!=", None)
        ])

        ref_dict = {}
        for qso_id in qso_ids:
            ref_dict[qso_id.callsign] = qso_id.reference

        for callsign, reference in ref_dict.items():
            qso_ids = qso_obj.search([
                ("callsign", "ilike", callsign),
                "|",
                ("reference", "=", False),
                ("reference", "=", "")
            ])

            qso_ids.write({
                "reference": reference
            })

    @api.model
    def action_compute_dupe(self):
        qso_ids = self.search([])
        qso_ids.write({"dupe": "normal"})

        qso_first = self.search([], limit=1, order="ts ASC")
        qso_last = self.search([], limit=1, order="ts DESC")

        datetime_first = qso_first.ts.replace(hour=0, minute=0, second=0, microsecond=0)
        datetime_last = qso_last.ts.replace(hour=23, minute=59, second=59, microsecond=999999)

        datetime_interval = datetime_last - datetime_first
        days = datetime_interval.days + 1

        qso_ids_group = self.read_group(domain=[], fields=["callsign"], groupby=["callsign"])
        callsign_list = [x["callsign"] for x in qso_ids_group if x["callsign"]]

        for callsign in callsign_list:
            for i in range(0, days):
                datetime_day = datetime_first + datetime.timedelta(days=i)

                self.check_dupe(callsign, datetime_day, "CW")
                self.check_dupe(callsign, datetime_day, "SSB")
                self.check_dupe(callsign, datetime_day, "DIGI")

    def check_dupe(self, callsign, datetime_day, mode):
        ts_start = datetime_day.strftime("%Y-%m-%d 00:00:00")
        ts_end = datetime_day.strftime("%Y-%m-%d 23:59:59")

        qso_ids = self.search([
            ("callsign", "=", callsign),
            ("mode", "=", mode),
            ("ts", ">=", ts_start),
            ("ts", "<=", ts_end),
        ], order="ts ASC")

        if len(qso_ids) > 1:
            _logger.info("DUPE for %s on %s in %s with %d QSO" % (
                callsign, datetime_day.strftime("%Y-%m-%d"), mode, len(qso_ids)
            ))

            count = 0
            for qso_id in qso_ids:
                qso_id.dupe = "dupe" if count > 0 else "normal"
                count += 1
