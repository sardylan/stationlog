import base64
import logging

from odoo import models, fields, api
from odoo.exceptions import ValidationError

_logger = logging.getLogger(__name__)


class CabrilloImport(models.TransientModel):
    _name = "station_log.wizard_import_cabrillo"
    _description = "Wizard for importing contest QSOs from Cabrillo format"

    import_file = fields.Binary(
        string="File",
        attachment=True,
        required=True
    )

    import_file_name = fields.Char(
        string="Filename"
    )

    contest_id = fields.Many2one(
        string="Contest",
        help="Select contest for imported QSOs",
        comodel_name="station_log.contest",
        required=True
    )

    power = fields.Float(
        string="Power",
        help="Power (W)",
        required=True,
    )

    file_size = fields.Integer(
        string="File size",
        readonly=True
    )

    qso_count = fields.Integer(
        string="QSO count",
        readonly=True
    )

    @api.onchange("import_file")
    def _onchange_import_file(self):
        self.ensure_one()

        if not self.import_file:
            self.file_size = 0
            self.qso_count = 0
            return

        file_content = base64.b64decode(self.import_file).decode()
        self.file_size = len(file_content)

        self._check_valid_format_cabrillo(file_content)

        rows = file_content.splitlines()

        qso_count = 0
        for row in rows:
            if row.startswith("QSO"):
                qso_count += 1

        self.qso_count = qso_count

    def action_import(self):
        self.ensure_one()

        modulation_obj = self.env["hamutility.modulation"]
        qso_obj = self.env["station_log.qso"]
        cabrillo_obj = self.env["hamutility.cabrillo"]

        if not self.import_file:
            return

        file_content = base64.b64decode(self.import_file).decode()

        self._check_valid_format_cabrillo(file_content)

        rows = file_content.splitlines()

        contest_name = list(filter(lambda x: x.startswith("CONTEST:"), rows))[0].split()[1]

        row_count = 0
        qso_count = 0
        qso_dupe_count = 0

        for row in rows:
            row_count += 1

            if row.startswith("QSO"):
                cabrillo_row = cabrillo_obj.parse_qso_line(row)

                modulation_string = None
                if cabrillo_row["mode"] == "CW":
                    modulation_string = "CW"
                elif cabrillo_row["mode"] == "PH":
                    modulation_string = "SSB"
                elif cabrillo_row["mode"] == "FM":
                    modulation_string = "FM"
                elif cabrillo_row["mode"] == "RY":
                    modulation_string = "RTTY"

                if not modulation_string:
                    raise ValidationError(
                        "Modulation \"%s\" not supported in row %d" % (cabrillo_row["mode"], row_count)
                    )

                modulation_id = modulation_obj.search([("name", "ilike", modulation_string)], limit=1)
                if not modulation_id:
                    raise ValidationError("Modulation \"%s\" not found in row %d" % (modulation_string, row_count))

                qso_ts_start = cabrillo_row["ts"].strftime(fields.DATETIME_FORMAT)
                callsign = cabrillo_row["rx_callsign"]

                values = {
                    "contest_id": self.contest_id.id,
                    "callsign": callsign,
                    "frequency": cabrillo_row["frequency"],
                    "modulation_id": modulation_id.id,
                    "power": self.power,
                    "ts_start": qso_ts_start,
                    "ts_end": qso_ts_start,
                    "rx_r": cabrillo_row["rx_r"],
                    "rx_s": cabrillo_row["rx_s"],
                    "rx_t": cabrillo_row["rx_t"],
                    "tx_r": cabrillo_row["tx_r"],
                    "tx_s": cabrillo_row["tx_s"],
                    "tx_t": cabrillo_row["tx_t"],
                    "note": "<p>Contest: %s<br />Information sent: %s<br />Information received: %s</p>" % (
                        contest_name,
                        cabrillo_row["tx_exchange"],
                        cabrillo_row["rx_exchange"]
                    )
                }

                qso_record_count = qso_obj.search([
                    ("callsign", "=", callsign),
                    ("ts_start", "=", qso_ts_start),
                ], count=True)

                if qso_record_count > 0:
                    _logger.warning("QSO rejected at row %d from cabrillo file \"%s\": %s" % (
                        row_count,
                        self.import_file_name,
                        values
                    ))

                    qso_dupe_count += 1
                    continue

                qso_obj.create(values)
                qso_count += 1

        _logger.info("QSO imported: %d, rejected: %d" % (qso_count, qso_dupe_count))

        return {
            "type": "ir.actions.client",
            "tag": "reload",
        }

    @staticmethod
    def _check_valid_format_cabrillo(file_content):
        rows = file_content.splitlines()

        if not rows[0].split(":")[0].startswith("START-OF-LOG"):
            raise ValidationError("First line doesn't start with \"START-OF-LOG\"")

        if not rows[len(rows) - 1].split(":")[0].startswith("END-OF-LOG"):
            raise ValidationError("Last line doesn't start with \"END-OF-LOG\"")
