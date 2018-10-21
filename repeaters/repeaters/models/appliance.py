from odoo import fields, api
from odoo import models

SELECTION_TYPE = [
    ("beacon", "Beacon"),
    ("simplex", "Simplex"),
    ("repeater", "Repeater"),
    ("transponder", "Transponder")
]

SELECTION_SQUELCH_TYPE = [
    ("none", "None"),
    ("ctcss", "CTCSS"),
    ("dcs", "DCS")
]

NAME_REPEATER = {
    145575000: "RV",
    145600000: "R0",
    145612500: "R0a",
    145625000: "R1",
    145627500: "R1a",
    145650000: "R2",
    145662500: "R2a",
    145675000: "R3",
    145687500: "R3a",
    145700000: "R4",
    145712500: "R4a",
    145725000: "R5",
    145737500: "R5a",
    145750000: "R6",
    145767500: "R6a",
    145775000: "R7",
    145787500: "R7a",
    430000000: "RU0",
    430012500: "RU0a",
    430025000: "RU1",
    430037500: "RU1a",
    430050000: "RU2",
    430062500: "RU2a",
    430075000: "RU3",
    430087500: "RU3a",
    430100000: "RU4",
    430112500: "RU4a",
    430125000: "RU5",
    430137500: "RU5a",
    430150000: "RU6",
    430162500: "RU6a",
    430175000: "RU7",
    430187500: "RU7a",
    430200000: "RU8",
    430212500: "RU8a",
    430225000: "RU9",
    430237500: "RU9a",
    430250000: "RU10",
    430262500: "RU10a",
    430275000: "RU11",
    430287500: "RU11a",
    430300000: "RU12",
    430312500: "RU12a",
    430325000: "RU13",
    430337500: "RU13a",
    430350000: "RU14",
    430362500: "RU14a",
    430375000: "RU15",
    430387500: "RU15a",
    431225000: "RU16",
    431237500: "RU16a",
    431250000: "RU17",
    431262500: "RU17a",
    431275000: "RU18",
    431287500: "RU18a",
    431300000: "RU19",
    431312500: "RU19a",
    431325000: "RU20",
    431337500: "RU20a",
    431350000: "RU21",
    431362500: "RU21a",
    431375000: "RU22",
    431387500: "RU22a",
    431400000: "RU23",
    431412500: "RU23a",
    431425000: "RU24",
    431437500: "RU24a",
    431450000: "RU25",
    431462500: "RU25a",
    431475000: "RU26",
    431487500: "RU26a",
    431500000: "RU27",
    431512500: "RU27a",
    431525000: "RU28",
    431537500: "RU28a",
    431550000: "RU29",
    431562500: "RU29a",
    431575000: "RU30",
    431587500: "RU30a",
    431600000: "RU31"
}


class Appliance(models.Model):
    _name = "repeaters.appliance"
    _inherit = "mail.thread"
    _description = "Appliance"
    _rec_name = "frequency_tx"
    _order = "frequency_tx ASC"

    station_id = fields.Many2one(
        string="Station",
        help="Station",
        comodel_name="repeaters.station",
        required=True,
        track_visibility="onchange"
    )

    type = fields.Selection(
        stirng="Type",
        help="Type",
        selection=SELECTION_TYPE,
        required=True,
        track_visibility="onchange"
    )

    frequency_tx = fields.Integer(
        string="TX Frequency",
        help="TX Frequency",
        required=True,
        track_visibility="onchange"
    )

    frequency_rx = fields.Integer(
        string="RX Frequency",
        help="RX Frequency",
        track_visibility="onchange"
    )

    modulation_id = fields.Many2one(
        string="Modulation",
        help="Modulation",
        comodel_name="hamutility.modulation",
        required=True,
        track_visibility="onchange"
    )

    aux_modulation_ids = fields.Many2many(
        string="Auxiliary Modulations",
        help="Auxiliary Modulations",
        relation="repeaters_appliance_hamutility_modulation_rel_aux",
        comodel_name="hamutility.modulation",
        column1="appliance_id",
        column2="modulation_id",
        track_visibility="onchange"
    )

    squelch_tx_type = fields.Selection(
        string="TX Squelch type",
        help="TX Squelch type",
        selection=SELECTION_SQUELCH_TYPE,
        required=True,
        default="none",
        track_visibility="onchange"
    )

    squelch_tx_value = fields.Char(
        string="TX Squelch value",
        help="TX Squelch value",
        track_visibility="onchange"
    )

    squelch_rx_type = fields.Selection(
        string="RX Squelch type",
        help="RX Squelch type",
        selection=SELECTION_SQUELCH_TYPE,
        required=True,
        default="none",
        track_visibility="onchange"
    )

    squelch_rx_value = fields.Char(
        string="RX Squelch value",
        help="RX Squelch value",
        track_visibility="onchange"
    )

    conference_id = fields.Many2one(
        string="Conference",
        help="Conference",
        comodel_name="repeaters.conference",
        track_visibility="onchange"
    )

    note = fields.Html(
        string="Note",
        help="Note",
        track_visibility="onchange"
    )

    @api.onchange("type")
    def _onchange_type(self):
        for rec in self:
            if rec.type == "beacon":
                rec.frequency_rx = False
            if rec.type == "simplex":
                rec.frequency_rx = rec.frequency_tx

    @api.onchange("frequency_tx")
    def _onchange_frequency_tx(self):
        for rec in self:
            if rec.type == "simplex":
                rec.frequency_rx = rec.frequency_tx
