from odoo import models, fields, api

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


class QSO(models.Model):
    _name = "stationlog.qso"
    _inherit = "mail.thread"
    _description = "QSO"
    _order = "ts_start DESC, callsign ASC"

    callsign = fields.Char(
        string="Callsign",
        help="Callsign",
        required=True,
        track_visibility="onchange"
    )

    ts_start = fields.Datetime(
        string="Start datetime",
        help="Start datetime",
        required=True,
        track_visibility="onchange"
    )

    ts_end = fields.Datetime(
        string="End datetime",
        help="End datetime",
        track_visibility="onchange"
    )

    frequency = fields.Integer(
        string="Frequency",
        help="Frequency (Hz)",
        required=True,
        track_visibility="onchange"
    )

    modulation_id = fields.Many2one(
        string="Modulation",
        help="Modulation",
        comodel_name="stationlog.modulation",
        required=True,
        track_visibility="onchange"
    )

    power = fields.Float(
        string="Power",
        help="Power (W)",
        required=True,
        track_visibility="onchange"
    )

    rx_r = fields.Selection(
        string="Received Readability",
        help="Received Readability",
        selection=SELECTION_READABILITY,
        track_visibility="onchange"
    )

    rx_s = fields.Selection(
        string="Received Strenght",
        help="Received Strenght",
        selection=SELECTION_SIGNAL_TONE,
        track_visibility="onchange"
    )

    rx_t = fields.Selection(
        string="Received Tone",
        help="Received Tone",
        selection=SELECTION_SIGNAL_TONE,
        track_visibility="onchange"
    )

    tx_r = fields.Selection(
        string="Sent Radio",
        help="Sent Radio",
        selection=SELECTION_READABILITY,
        track_visibility="onchange"
    )

    tx_s = fields.Selection(
        string="Sent Strenght",
        help="Sent Strenght",
        selection=SELECTION_SIGNAL_TONE,
        track_visibility="onchange"
    )

    tx_t = fields.Selection(
        string="Sent Tone",
        help="Sent Tone",
        selection=SELECTION_SIGNAL_TONE,
        track_visibility="onchange"
    )

    qrm = fields.Boolean(
        string="QRM",
        help="QRM",
        track_visibility="onchange"
    )

    qrn = fields.Boolean(
        string="QRN",
        help="QRN",
        track_visibility="onchange"
    )

    qsb = fields.Boolean(
        string="QSB",
        help="QSB",
        track_visibility="onchange"
    )

    qsl_sent = fields.Boolean(
        string="QSL Sent",
        help="QSL Sent",
        track_visibility="onchange"
    )

    qsl_received = fields.Boolean(
        string="QSL Received",
        help="QSL Received",
        track_visibility="onchange"
    )

    note = fields.Html(
        string="Note"
    )

    rx_rst = fields.Char(
        string="Received RST",
        help="Received RST",
        compute="_compute_received_rst"
    )

    tx_rst = fields.Char(
        string="Sent RST",
        help="Sent RST",
        compute="_compute_sent_rst"
    )

    qsl_status = fields.Char(
        string="QSL Status",
        help="QSL Status",
        compute="_compute_qsl_status"
    )

    @api.model
    def create(self, vals):
        if "callsign" in vals and vals["callsign"]:
            vals["callsign"] = vals["callsign"].strip().upper()

        return super().create(vals)

    @api.multi
    def write(self, vals):
        if "callsign" in vals and vals["callsign"]:
            vals["callsign"] = vals["callsign"].strip().upper()

        return super().write(vals)

    def name_get(self):
        result = []

        for rec in self:
            result.append((rec.id, "%s (%s)" % (rec.callsign, rec.ts_start)))

        return result

    @api.onchange("ts_start")
    def _onchange_start(self):
        for rec in self:
            rec.ts_end = rec.ts_start

    @api.depends("rx_r", "rx_s", "rx_t")
    def _compute_received_rst(self):
        for rec in self:
            rec.rx_rst = self._rst_string(rec.rx_r, rec.rx_s, rec.rx_t)

    @api.depends("tx_r", "tx_s", "tx_t")
    def _compute_sent_rst(self):
        for rec in self:
            rec.tx_rst = self._rst_string(rec.tx_r, rec.tx_s, rec.tx_t)

    @api.depends("qsl_sent", "qsl_received")
    def _compute_qsl_status(self):
        for rec in self:
            value = []
            if rec.qsl_sent:
                value.append("TX")
            if rec.qsl_received:
                value.append("RX")
            rec.qsl_status = "-".join(value)

    @staticmethod
    def _rst_string(r, s, t):
        return "%s-%s-%s" % (r or "X", s or "X", t or "X")
