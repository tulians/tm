# Partials module.
# ===================================

"""Provides the management of the file that keeps track of partial commits"""

# Built-in modules.
import os
import json


class Partials(object):
    def __init__(self, creation_path):
        if creation_path[-1] != "/":
            creation_path += "/"
        try:
            if not os.path.exists(creation_path):
                os.makedirs(creation_path)
        except OSError as detail:
            print("The partials file could not be created due to permission"
                  " issues. Exception detail: " + str(detail))

        self.partials_path = creation_path + ".status.txt"

        if not os.path.isfile(self.partials_path):
            self.status = False
            with open(self.partials_path, "w") as partials:
                partials.write(json.dumps(self.status))
        else:
            with open(self.partials_path, "r") as partials:
                self.status = json.loads(partials.read())["exist"]

    def _set_status(self, status):
        self.status["exist"] = status
        with open(self.partials_path, "w") as partials:
            partials.write(json.dumps(self.status))

    @property
    def status(self):
        return self._status

    @status.setter
    def status(self, value):
        self._status = {"exist": value}
        self._set_status(value)
