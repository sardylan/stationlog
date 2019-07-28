from odoo import models, fields, api


class MassiveQSOCreationWizard(models.TransientModel):
    _name = "station_log.wizard_massive_qso_creation"
    _description = "Wizard for massive creation of QSOs"

    logbook_id = fields.Many2one(
        string="Logbook",
        comodel_name="station_log.logbook",
        required=True,
        domain=lambda self: self.env["station_log.logbook"].get_users_logbook_domain(self.env.uid),
        default=lambda self: self.env["station_log.logbook"].default_logbook_id(self.env.uid),
    )

    session_id = fields.Many2one(
        string="Contest",
        help="Contest",
        comodel_name="station_log.session",
    )

    frequency = fields.Integer(
        string="Frequency",
        help="Frequency (Hz)",
        required=True
    )

    modulation_id = fields.Many2one(
        string="Modulation",
        help="Modulation",
        comodel_name="hamutility.modulation",
        required=True
    )

    power = fields.Float(
        string="Power",
        help="Power (W)",
        required=True
    )

    item_ids_visible = fields.Boolean(
        string="item_ids_visible",
        default=False
    )

    item_ids = fields.One2many(
        string="Items",
        help="Items",
        comodel_name="station_log.wizard_massive_qso_creation_item",
        inverse_name="wizard_id"
    )

    def action_show_item_ids(self):
        self.ensure_one()

        self.item_ids_visible = True

        return {
            "type": "ir.actions.act_window",
            "res_model": self._name,
            "res_id": self.id,
            "view_type": "form",
            "view_mode": "form",
            "context": self.env.context,
            "target": "new"
        }

    def action_create(self):
        self.ensure_one()


class MassiveQSOCreationItemWizard(models.TransientModel):
    _name = "station_log.wizard_massive_qso_creation_item"
    _description = "Items for QSO massive creation wizard"

    wizard_id = fields.Many2one(
        string="Wizard",
        help="Wizard",
        comodel_name="station_log.wizard_massive_qso_creation",
        required=True
    )

    callsign = fields.Char(
        string="Callsign",
        help="Callsign",
        required=True
    )

    ts_start = fields.Datetime(
        string="Start datetime",
        help="Start datetime",
        required=True
    )

    ts_end = fields.Datetime(
        string="End datetime",
        help="End datetime"
    )

    rst_tx = fields.Char(
        string="TX RST",
        help="Sent RST",
        required=True
    )

    rst_rx = fields.Char(
        string="RX RST",
        help="Received RST",
        required=True
    )

    operator = fields.Char(
        string="Op.",
        help="Operator name"
    )

    qth = fields.Char(
        string="QTH",
        help="QTH"
    )

    @api.onchange("callsign")
    def _onchange_callsign(self):
        for rec in self:
            rec.callsign = rec.callsign and rec.callsign.strip().upper()
