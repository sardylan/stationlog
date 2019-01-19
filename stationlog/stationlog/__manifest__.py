{
    "name": "Station Log",
    "version": "12.0.0.9.0",
    "category": "Extra Tools",
    "summary": "HAM Station log",
    "depends": [
        "mail",
        "snailmail",
        "hamutility"
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

        "menu/action.xml",
        "menu/items.xml"
    ],
    "application": True
}
