{
    "name": "Station Log",
    "version": "12.0.0.9.0",
    "category": "Extra Tools",
    "summary": "HAM Station log",
    "depends": [
        "base",
        "mail",
        "hamutility",
        "widget_datetime_tz"
        "widget_googlemaps"
    ],
    "data": [
        "security/groups.xml",

        "security/access/logbook.xml",
        "security/access/qso.xml",
        "security/access/contest.xml",

        "views/logbook.xml",
        "views/qso.xml",
        "views/contest.xml",

        "reports/qso.xml",

        "wizard/dashboard.xml",
        "wizard/cabrillo_import.xml",

        "menu/action.xml",
        "menu/items.xml"
    ],
    "application": True
}