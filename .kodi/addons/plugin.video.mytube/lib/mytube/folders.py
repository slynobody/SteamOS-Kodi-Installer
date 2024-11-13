# -*- coding: utf-8 -*-


# folders ----------------------------------------------------------------------

__folders__ = {
    "folders": {
        "feed": {
            "title": 30100,
            "setting": "home.feed",
            "art": "icons/settings/network.png"
        },
        "search": {
            "title": 137,
            "art": "DefaultAddonsSearch.png"
        }
    }
}


class Folder(dict):

    def __init__(self, action, folder):
        return super(Folder, self).__init__(
            title=folder["title"],
            action=folder.get("action", action),
            setting=folder.get("setting"),
            art=dict.fromkeys(("poster", "icon"), folder.get("art")),
            properties=folder.get("properties"),
            kwargs=folder.get("kwargs", {})
        )

def getFolders(*paths):
    folders = __folders__["folders"]
    for path in paths:
        folders = folders.get(path, {}).get("folders", {})
    return [Folder(*item) for item in folders.items()]
