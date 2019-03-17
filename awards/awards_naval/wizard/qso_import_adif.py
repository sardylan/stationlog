import base64
import datetime
import json
import logging

from odoo import models, fields, api

_logger = logging.getLogger(__name__)


def json_converter(o):
    if isinstance(o, datetime.datetime):
        return o.__str__()
    elif isinstance(o, datetime.date):
        return o.__str__()
    elif isinstance(o, datetime.time):
        return o.__str__()
    else:
        return o


class QSOImportAdifWizard(models.TransientModel):
    _name = "award_naval.wizard_qso_import_adif"

    file_binary = fields.Binary(
        string="File",
        attachment=True,
        required=True
    )

    file_name = fields.Char(
        string="File name"
    )

    file_size = fields.Integer(
        string="File size",
        readonly=True
    )

    operator = fields.Char(
        string="Operator",
        required=True
    )

    reference_field = fields.Char(
        string="Reference field",
        required=True
    )

    raw_content = fields.Text(
        string="Raw content",
        readonly=True
    )

    @api.onchange("file_binary")
    def onchange_file_binary(self):
        for rec in self:
            file_raw = rec.file_binary and base64.b64decode(rec.file_binary) or ""
            rec.file_size = len(file_raw)
            rec.raw_content = file_raw[:1000]

    @api.onchange("operator")
    def onchange_operator(self):
        for rec in self:
            rec.operator = rec.operator and rec.operator.strip().upper() or ""

    @api.onchange("reference_field")
    def onchange_reference_field(self):
        for rec in self:
            rec.reference_field = rec.reference_field and rec.reference_field.strip().upper() or ""

    def action_import(self):
        self.ensure_one()

        if not self.file_binary:
            raise ValueError("Empty file")

        adif_utility = self.env["hamutility.adif"]
        qso_obj = self.env["award_naval.qso"]

        file_raw = base64.b64decode(self.file_binary).decode("latin")
        adif = adif_utility.parse_file_adif(file_raw)

        reference_field = self.reference_field.strip().upper()

        for qso in adif["qso"]:
            ts = datetime.datetime(
                year=qso["QSO_DATE"].year,
                month=qso["QSO_DATE"].month,
                day=qso["QSO_DATE"].day,
                hour=qso["TIME_ON"].hour,
                minute=qso["TIME_ON"].minute,
                second=qso["TIME_ON"].second
            )

            band = qso["BAND"].lower()

            if qso["MODE"] in ["CW"]:
                mode = "CW"
            elif qso["MODE"] in ["SSB", "USB", "LSB"]:
                mode = "SSB"
            elif qso["MODE"] in ["FT8"]:
                mode = "DIGI"
            else:
                raise ValueError("Mode %s not recognized" % qso["MODE"])

            reference = reference_field in qso and qso[reference_field] or False

            values = {
                "callsign": qso["CALL"],
                "ts": ts,
                "band": band,
                "mode": mode,
                "reference": reference,
                "operator": self.operator,
                "rawdata": json.dumps(qso, default=json_converter, indent=4)
            }

            qso_id = qso_obj.search([
                ("callsign", "=", values["callsign"]),
                ("ts", "=", values["ts"]),
                ("mode", "=", values["mode"])
            ])

            if not qso_id:
                qso_obj.create(values)
            else:
                qso_id.write(values)

        _logger.info(adif)
