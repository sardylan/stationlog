{
    "name": "Station Log",
    "version": "12.0.0.10.0",
    "category": "Extra Tools",
    "summary": "HAM Station log",
    "depends": [
        "base",
        "mail",
        "hamutility",
        "widget_datetime_tz",
        "widget_googlemaps",
        "station",
        "web_responsive"
    ],
    "data": [
        "security/groups.xml",

        "security/access/logbook.xml",
        "security/access/qso.xml",
        "security/access/session.xml",
        "security/access/qsl.xml",

        "views/logbook.xml",
        "views/qso.xml",
        "views/session.xml",
        "views/qsl.xml",

        "reports/qso.xml",

        "wizard/dashboard.xml",
        "wizard/import_cabrillo.xml",
        "wizard/import_adif.xml",

        "menu/action.xml",
        "menu/items.xml"
    ],
    "application": True
}
