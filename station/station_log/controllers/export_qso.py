from odoo import http
from odoo.http import route, request


class QSOExportController(http.Controller):
    @route(
        route="/station_log/api/v1/export/qso",
        type="http",
        auth="user",
        methods=["GET"],
        cors="*",
        csrf=False
    )
    def export_qso(self):
        qso_obj = request.env["station_log.qso"]

        qso_ids = qso_obj.search([], order="ts_start ASC")

        values = {
            "qso_ids": qso_ids
        }

        html_content = request.render("station_log.export_qso", qcontext=values, lazy=False)

        return html_content
