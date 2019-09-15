from datetime import datetime

from odoo import models, fields, api


class QSO(models.Model):
    _name = "station_log.qso"
    _description = "QSO"
    _inherit = "mail.thread"
    _rec_name = "short_desc"
    _order = "ts_start DESC, callsign ASC"

    _sql_constraints = [
        (
            "callsign_ts_start_uniq",
            "UNIQUE(callsign, ts_start)",
            "QSO already registered"
        )
    ]

    logbook_id = fields.Many2one(
        string="Logbook",
        comodel_name="station_log.logbook",
        required=True,
        domain=lambda self: self.env["station_log.logbook"].get_users_logbook_domain(self.env.uid),
        default=lambda self: self.env["station_log.logbook"].default_logbook_id(self.env.uid),
        track_visibility="onchange"
    )

    session_id = fields.Many2one(
        string="Session",
        help="Session",
        comodel_name="station_log.session",
        track_visibility="onchange"
    )

    callsign = fields.Char(
        string="Callsign",
        help="Callsign",
        required=True,
        copy=False,
        track_visibility="onchange"
    )

    my_callsign = fields.Char(
        string="My Callsign",
        help="My Callsign",
        required=True,
        track_visibility="onchange"
    )

    station_id = fields.Many2one(
        string="Station",
        help="Station",
        comodel_name="station.station",
        track_visibility="onchange"
    )

    operator = fields.Char(
        string="Op.",
        help="Operator name",
        copy=False,
        track_visibility="onchange"
    )

    qth = fields.Char(
        string="QTH",
        help="QTH",
        copy=False,
        track_visibility="onchange"
    )

    ts_start = fields.Datetime(
        string="Start datetime",
        help="Start datetime",
        required=True,
        default=lambda self: datetime.utcnow().replace(microsecond=0),
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
        comodel_name="hamutility.modulation",
        required=True,
        track_visibility="onchange"
    )

    power = fields.Float(
        string="Power",
        help="Power (W)",
        required=True,
        track_visibility="onchange"
    )

    rapid_tx_rst = fields.Char(
        string="TX RST",
        help="TX RST"
    )

    rapid_rx_rst = fields.Char(
        string="RX RST",
        help="RX RST"
    )

    rx_r = fields.Selection(
        string="Received Readability",
        help="Received Readability",
        selection=lambda self: self.env["station_log.utility_qso"].prepare_selection_readability(),
        track_visibility="onchange"
    )

    rx_s = fields.Selection(
        string="Received Strenght",
        help="Received Strenght",
        selection=lambda self: self.env["station_log.utility_qso"].prepare_selection_signal_tone(),
        track_visibility="onchange"
    )

    rx_t = fields.Selection(
        string="Received Tone",
        help="Received Tone",
        selection=lambda self: self.env["station_log.utility_qso"].prepare_selection_signal_tone(),
        track_visibility="onchange"
    )

    tx_r = fields.Selection(
        string="Sent Readability",
        help="Sent Readability",
        selection=lambda self: self.env["station_log.utility_qso"].prepare_selection_readability(),
        track_visibility="onchange"
    )

    tx_s = fields.Selection(
        string="Sent Strenght",
        help="Sent Strenght",
        selection=lambda self: self.env["station_log.utility_qso"].prepare_selection_signal_tone(),
        track_visibility="onchange"
    )

    tx_t = fields.Selection(
        string="Sent Tone",
        help="Sent Tone",
        selection=lambda self: self.env["station_log.utility_qso"].prepare_selection_signal_tone(),
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

    qsl_ids = fields.One2many(
        string="QSL",
        help="QSL cards",
        comodel_name="station_log.qsl",
        inverse_name="qso_id"
    )

    mobile = fields.Boolean(
        string="Mobile",
        help="Mobile",
        track_visibility="onchange",
        required=True,
        default=False
    )

    note = fields.Html(
        string="Note"
    )

    short_desc = fields.Char(
        string="Short description",
        compute="_compute_short_desc"
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

    disturbs = fields.Char(
        string="Disturbs",
        help="Disturbs like QRM, QRN or QSB",
        compute="_compute_disturbs"
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

        if "rapid_tx_rst" in vals and vals["rapid_tx_rst"]:
            r, s, t = self._parse_rst_rapid(vals["rapid_tx_rst"])
            vals["tx_r"] = r
            vals["tx_s"] = s
            vals["tx_t"] = t

        if "rapid_rx_rst" in vals and vals["rapid_rx_rst"]:
            r, s, t = self._parse_rst_rapid(vals["rapid_rx_rst"])
            vals["rx_r"] = r
            vals["rx_s"] = s
            vals["rx_t"] = t

        if "ts_start" not in vals or not vals["ts_start"]:
            vals["ts_start"] = datetime.utcnow().replace(microsecond=0)

        if "ts_end" not in vals or not vals["ts_end"]:
            vals["ts_end"] = vals["ts_start"]

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

    @api.model
    def name_search(self, name="", args=None, operator="ilike", limit=100):
        if args is None:
            args = []

        domain = []
        if args:
            domain.append("|")

        domain.extend([
            ("callsign", operator, name)
        ])

        return super().search(domain, limit=limit).name_get()

    @api.onchange("callsign")
    def _onchange_callsign(self):
        for rec in self:
            if rec.callsign:
                rec.callsign = rec.callsign.strip().upper()

    # @api.onchange("ts_start")
    # def _onchange_start(self):
    #     for rec in self:
    #         rec.ts_end = rec.ts_start

    @api.onchange("logbook_id")
    def _onchange_logbook_id(self):
        for rec in self:
            rec.my_callsign = rec.logbook_id.callsign

    @api.depends("callsign", "frequency", "modulation_id")
    def _compute_short_desc(self):
        for rec in self:
            rec.short_desc = "%s %.03f %s" % (
                rec.callsign,
                float(rec.frequency / 1000000),
                rec.modulation_id.complete_name
            )

    @api.depends("rx_r", "rx_s", "rx_t")
    def _compute_received_rst(self):
        for rec in self:
            rec.rx_rst = self._rst_string(rec.rx_r, rec.rx_s, rec.rx_t)

    @api.depends("tx_r", "tx_s", "tx_t")
    def _compute_sent_rst(self):
        for rec in self:
            rec.tx_rst = self._rst_string(rec.tx_r, rec.tx_s, rec.tx_t)

    @api.depends("qrm", "qrn", "qsb")
    def _compute_disturbs(self):
        for rec in self:
            disturbs = []
            rec.qrm and disturbs.append("QRM")
            rec.qrn and disturbs.append("QRN")
            rec.qsb and disturbs.append("QSB")

            rec.disturbs = "-".join(disturbs)

    @api.depends("qsl_ids")
    def _compute_qsl_status(self):
        for rec in self:

            value = []

            if [x for x in rec.qsl_ids if x.direction == "tx"]:
                value.append("TX")

            if [x for x in rec.qsl_ids if x.direction == "rx"]:
                value.append("RX")

                rec.qsl_status = "-".join(value)

    def action_station_qrz_com(self):
        self.ensure_one()

        return {
            "type": "ir.actions.act_url",
            "target": "new",
            "url": "https://qrz.com/db/%s" % self.callsign
        }

    def action_create_similar(self):
        self.ensure_one()

        return {
            "type": "ir.actions.act_window",
            "name": "Create similar QSO",
            "res_model": self._name,
            "view_type": "form",
            "view_mode": "form",
            "context": {
                "default_logbook_id": self.logbook_id.id,
                "default_session_id": self.session_id.id,
                "default_my_callsign": self.my_callsign,
                "default_ts_start": self.ts_start,
                "default_ts_end": self.ts_end,
                "default_frequency": self.frequency,
                "default_modulation_id": self.modulation_id.id,
                "default_power": self.power,
                "default_mobile": self.mobile,
                "default_rx_r": self.rx_r,
                "default_rx_s": self.rx_s,
                "default_rx_t": self.rx_t,
                "default_tx_r": self.tx_r,
                "default_tx_s": self.tx_s,
                "default_tx_t": self.tx_t,
                "default_qrm": self.qrm,
                "default_qrn": self.qrn,
                "default_qsb": self.qsb,
                "default_note": self.note
            }
        }

    def action_continue(self):
        self.ensure_one()

        return {
            "type": "ir.actions.act_window",
            "name": "Rapid",
            "view_type": "form",
            "view_mode": "form",
            "res_model": "station_log.qso",
            "target": "new",
            "views": [(self.env.ref("station_log.view_qso_form_rapid").id, "form")],
            "context": {
                "default_logbook_id": self.logbook_id.id,
                "default_frequency": self.frequency,
                "default_session_id": self.session_id.id,
                "default_modulation_id": self.modulation_id.id,
                "default_power": self.power,
                "default_ts_start": False,
                "default_ts_end": False
            }
        }

    @staticmethod
    def _rst_string(r, s, t):
        return "%s-%s-%s" % (r or "X", s or "X", t or "X")

    @staticmethod
    def _parse_rst_rapid(rst=""):
        if rst:
            if len(rst) == 1:
                return "5", rst, False
            elif len(rst) == 2:
                return rst[0], rst[1], False
            elif len(rst) == 3:
                return rst[0], rst[1], rst[2]

        return "5", "9", "9"
