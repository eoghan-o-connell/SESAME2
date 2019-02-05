from django.core.files.staorage import default_storage

class Researcher():

    def __init__(self, researcher):
        self.filename = "/researcher_profiles/%i" % researcher
        self.values = dict()
        if default_storage.exists(filename):
            file = default_storage.open(self.filename, "r")
            researcher = self.file.read()
            file.close()
            researcher = researcher.split(";\n")
            for pair in researcher:
                key, value = pair.split(":", 2)
                if key not in self.values:
                    self.values[key] = list()
                self.values[key].append(value)

    def get_value(self, key, index):
        return self.values[key][index]

    def set_value(self, key, value, index):
        value.replace(";\n", "; \n")
        self.values[key].insert(index, value)

    def get_num(self, key):
        return len(self.values[key]))

    def save(self):
        file = default_storage.open(filename, "w")
        for key, values in self.values:
            for value in values:
                file.write("%s:%s;\n" % key, value)
        file.close()
