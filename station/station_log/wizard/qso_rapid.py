from datetime import datetime

from odoo import models, fields


class QSORapidWizard(models.TransientModel):
    _name = "station_log.wizard_qso_rapid"

    logbook_id = fields.Many2one(
        string="Logbook",
        comodel_name="station_log.logbook",
        required=True,
        domain=lambda self: self.env["station_log.logbook"].get_users_logbook_domain(self.env.uid),
        default=lambda self: self.env["station_log.logbook"].default_logbook_id(self.env.uid),
    )

    session_id = fields.Many2one(
        string="Session",
        help="Session",
        comodel_name="station_log.session",
    )

    frequency = fields.Integer(
        string="Frequency",
        help="Frequency (Hz)",
        required=True,
    )

    modulation_id = fields.Many2one(
        string="Modulation",
        help="Modulation",
        comodel_name="hamutility.modulation",
        required=True,
    )

    power = fields.Float(
        string="Power",
        help="Power (W)",
        required=True,
    )

    ts_start = fields.Datetime(
        string="Start datetime",
        help="Start datetime",
        required=True,
        default=lambda self: datetime.utcnow().replace(microsecond=0),
    )

    callsign = fields.Char(
        string="Callsign",
        help="Callsign",
        required=True,
        copy=False,
    )

    operator = fields.Char(
        string="Op.",
        help="Operator name",
        copy=False,
    )

    qth = fields.Char(
        string="QTH",
        help="QTH",
        copy=False,
    )

    ts_end = fields.Datetime(
        string="End datetime",
        help="End datetime",
    )

    rx_r = fields.Selection(
        string="Received Readability",
        help="Received Readability",
        selection=lambda self: self.env["station_log.utility_qso"].prepare_selection_readability(),
    )

    rx_s = fields.Selection(
        string="Received Strenght",
        help="Received Strenght",
        selection=lambda self: self.env["station_log.utility_qso"].prepare_selection_signal_tone(),
    )

    rx_t = fields.Selection(
        string="Received Tone",
        help="Received Tone",
        selection=lambda self: self.env["station_log.utility_qso"].prepare_selection_signal_tone(),
    )

    tx_r = fields.Selection(
        string="Sent Readability",
        help="Sent Readability",
        selection=lambda self: self.env["station_log.utility_qso"].prepare_selection_readability(),
    )

    tx_s = fields.Selection(
        string="Sent Strenght",
        help="Sent Strenght",
        selection=lambda self: self.env["station_log.utility_qso"].prepare_selection_signal_tone(),
    )

    tx_t = fields.Selection(
        string="Sent Tone",
        help="Sent Tone",
        selection=lambda self: self.env["station_log.utility_qso"].prepare_selection_signal_tone(),
    )

    qrm = fields.Boolean(
        string="QRM",
        help="QRM",
    )

    qrn = fields.Boolean(
        string="QRN",
        help="QRN",
    )

    qsb = fields.Boolean(
        string="QSB",
        help="QSB",
    )

    note = fields.Html(
        string="Note"
    )

