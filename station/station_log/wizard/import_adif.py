import base64
import datetime
import json
import logging

from odoo import models, fields, api
from odoo.exceptions import ValidationError

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


SELECTION_ENCODING = [
    ("latin", "ISO-8859-1"),
    ("utf8", "UTF-8")
]


class ImportAdifWizard(models.TransientModel):
    _name = "station_log.wizard_import_adif"
    _description = "Wizard for importing QSOs from ADIF file"

    file_binary = fields.Binary(
        string="File",
        attachment=True,
        required=True
    )

    file_name = fields.Char(
        string="File name"
    )

    encoding = fields.Selection(
        string="Encoding",
        selection=SELECTION_ENCODING,
        required=True,
        default="utf8"
    )

    file_size = fields.Integer(
        string="File size",
        readonly=True,
        compute="_compute_infos"
    )

    raw_content = fields.Text(
        string="Raw content",
        readonly=True,
        compute="_compute_infos"
    )

    @api.onchange("file_binary")
    @api.depends("file_binary")
    def _compute_infos(self):
        for rec in self:
            file_string = self.get_file_content()
            rec.file_size = len(file_string)
            rec.raw_content = file_string[:10000]

    def get_file_content(self):
        self.ensure_one()

        file_b64 = self.with_context(bin_size=False).file_binary
        file_raw = file_b64 and base64.b64decode(file_b64) or b""
        file_string = file_raw and file_raw.decode(self.encoding) or ""

        return file_string

    def action_import(self):
        self.ensure_one()

        if not self.file_binary:
            raise ValueError("Empty file")

        logbook_obj = self.env["station_log.logbook"]
        qso_obj = self.env["station_log.qso"]
        modulation_obj = self.env["hamutility.modulation"]

        adif_utility = self.env["hamutility.adif"]

        file_string = self.get_file_content()
        adif = adif_utility.parse_file_adif(file_string)

        qso_total = len(adif["qso"])

        _logger.info("ADIF header: %s" % json.dumps(adif["headers"], default=json_converter, indent=4))
        _logger.info("ADIF QSO count: %d" % qso_total)

        count_new = 0
        count_updated = 0

        logbook_id = logbook_obj.default_logbook_id(self.env.uid)

        for qso in adif["qso"]:
            ts_start = datetime.datetime(
                year=qso["QSO_DATE"].year,
                month=qso["QSO_DATE"].month,
                day=qso["QSO_DATE"].day,
                hour=qso["TIME_ON"].hour,
                minute=qso["TIME_ON"].minute,
                second=qso["TIME_ON"].second
            )

            ts_end = datetime.datetime(
                year=qso["QSO_DATE_OFF"].year,
                month=qso["QSO_DATE_OFF"].month,
                day=qso["QSO_DATE_OFF"].day,
                hour=qso["TIME_OFF"].hour,
                minute=qso["TIME_OFF"].minute,
                second=qso["TIME_OFF"].second
            )

            modulation_id = modulation_obj.search([("name", "=", qso["MODE"])])
            if not modulation_id:
                raise ValidationError("Mode %s not recognized" % qso["MODE"])

            if qso["MODE"] == "FT8" \
                    and not qso["RST_RCVD"].startswith("5") \
                    and not qso["RST_SENT"].startswith("5"):
                rx_db = int(qso["RST_RCVD"])
                tx_db = int(qso["RST_SENT"])

                rx_r = 5
                rx_s = int((rx_db + 26) / 6)
                rx_t = 9
                tx_r = 5
                tx_s = int((tx_db + 26) / 6)
                tx_t = 9
            else:
                rx_r = qso["RST_RCVD"] != "-" and int(qso["RST_RCVD"][0]) or 5
                rx_s = qso["RST_RCVD"] != "-" and int(qso["RST_RCVD"][1]) or 9
                rx_t = len(qso["RST_RCVD"]) == 3 and qso["RST_RCVD"][2] != "-" and int(qso["RST_RCVD"][2]) or False
                tx_r = qso["RST_SENT"] != "-" and int(qso["RST_SENT"][0]) or 5
                tx_s = qso["RST_SENT"] != "-" and int(qso["RST_SENT"][1]) or 9
                tx_t = len(qso["RST_SENT"]) == 3 and qso["RST_SENT"][2] != "-" and int(qso["RST_SENT"][2]) or False

            if rx_r < 1:
                rx_r = "1"
            elif rx_r > 5:
                rx_r = "5"
            else:
                rx_r = "%d" % rx_r

            if rx_s < 1:
                rx_s = "1"
            elif rx_s > 9:
                rx_s = "9"
            else:
                rx_s = "%d" % rx_s

            if rx_t and rx_t < 1:
                rx_t = "1"
            elif rx_t and rx_t > 9:
                rx_t = "9"
            elif rx_t:
                rx_t = "%d" % rx_t
            else:
                rx_t = False

            if tx_r < 1:
                tx_r = "1"
            elif tx_r > 5:
                tx_r = "5"
            else:
                tx_r = "%d" % tx_r

            if tx_s < 1:
                tx_s = "1"
            elif tx_s > 9:
                tx_s = "9"
            else:
                tx_s = "%d" % tx_s

            if tx_t < 1:
                tx_t = "1"
            elif tx_t > 9:
                tx_t = "9"
            elif tx_t:
                tx_t = "%d" % tx_t
            else:
                tx_t = False

            values = {
                "logbook_id": logbook_id.id,
                "callsign": qso["CALL"],
                "station_id": False,
                "operator": "NAME" in qso and qso["NAME"] or False,
                "qth": "QTH" in qso and qso["QTH"] or False,
                "ts_start": ts_start,
                "ts_end": ts_end,
                "frequency": qso["FREQ"],
                "modulation_id": modulation_id.id,
                "power": qso["TX_PWR"],
                "rx_r": rx_r,
                "rx_s": rx_s,
                "rx_t": rx_t,
                "tx_r": tx_r,
                "tx_s": tx_s,
                "tx_t": tx_t,
                "note": "NOTES" in qso and qso["NOTES"] or False,
            }

            qso_id = qso_obj.search([
                ("logbook_id", "=", logbook_id.id),
                ("callsign", "=", values["callsign"]),
                ("ts_start", "=", values["ts_start"]),
                ("frequency", "=", values["frequency"]),
                ("modulation_id", "=", values["modulation_id"])
            ])

            if not qso_id:
                qso_id = qso_obj.create(values)
                count_new += 1
            else:
                qso_id.write(values)
                count_updated += 1

            _logger.info("QSO: %s - Total: %d - Number: %d" % (qso_id.callsign, qso_total, count_new + count_updated))

        _logger.info("QSO count: %d new - %d updated" % (count_new, count_updated))

        return {
            "type": "ir.actions.client",
            "tag": "reload"
        }
