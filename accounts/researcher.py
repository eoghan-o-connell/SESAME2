from django.core.files.storage import default_storage

class Researcher():

    def __init__(self, user_id):
        self.user = User.objects.get(id=user_id)
        self._filename = "/researcher_profiles/%i" % user_id
        self._values = dict()
        if default_storage.exists(filename):
            file = default_storage.open(self._filename, "r")
            researcher = file.read()
            file.close()
            researcher = researcher.split(";\n")
            for attribute in researcher:
                key, values = attribute.split(":", 2)
                self._values[key] = values.split(":")
        educations = self._get_objects("edu", "degree", "field", "institution", "location", "year")
        employments = self._get_objects("emp", "company", "location", "years")
        societies = self._get_objects("soc", "start", "end", "name", "type")
        awards = self._get_objects("award", "year", "awarding_body", "details", "team")
        fundings = self._get_objects("fund", "start", "end", "amount", "body", "programme", "attribution")
        team_members = self._get_objects("mem", "start", "end", "name", "position", "attribution")
        impacts = self._get_objects("imp", "title", "category", "beneficiary", "attribution")
        innovations = self.get_objects("inn", "year", "type", "title", "attribution")
        publications = self.get_objects("pub", "year", "type", "title", "journal", "status", "doi", "attribution")
        presentations = self.get_objects("pre", "year", "title", "event", "body", "location", "attribution")
        acedemic_collabs = self.get_objects("acd", "start", "end", "institution", "dept", "location", "name", "goal", "frequency", "attribution")
        non_acedemic_collabs = self.get_objects("non", "start", "end", "institution", "dept", "location", "name", "goal", "frequency", "attribution")
        conferences = self.get_objects("con", "start", "end", "title", "type", "role", "location", "attribution")
        comms_overviews = self.get_objects("com", "year", "lectures", "visits", "media")
        funding_ratios = self.get_objects("rat", "year", "percent")
        projects = self.get_objects("pro", "name", "start", "end", "type", "topic", "target", "attribution")

    def new_education(self):
        education = self._get_object("edu_", "degree", "field", "institution", "location", "year")
        educations.append(education)
        return education

    def new_employment(self):
        employment = self._get_object("emp", "company", "location", "years")
        employments.append(employment)
        return employment

    def new_society(self):
        society = self._get_object("soc", "start", "end", "name", "type")
        societies.append(society)
        return society

    def new_award(self):
        award = self._get_object("award", "year", "awarding_body", "details", "team")
        awards.append(award)
        return award

    def new_funding(self):
        funding = self._get_object("fund", "start", "end", "amount", "body", "programme", "attribution")
        fundings.append(funding)
        return funding

    def new_team_member(self):
        team_member = self._get_object("mem", "start", "end", "name", "position", "attribution")
        team_members.append(team_member)
        return team_member

    def new_impact(self):
        impact = self._get_object("imp", "title", "category", "beneficiary", "attribution")
        impacts.append(impact)
        return impact

    def new_innovation(self):
        innovation = self._get_object("inn", "year", "type", "title", "attribution")
        innovations.append(innovation)
        return innovation

    def new_publication(self):
        publication = self._get_object("pub", "year", "type", "title", "journal", "status", "doi", "attribution")
        publications.append(publication)
        return publication

    def new_presentation(self):
        presentation = self._get_object("pre", "year", "title", "event", "body", "location", "attribution")
        presentations.append(presentation)
        return presentation

    def new_acedemic_collab(self):
        acedemic_collab = self._get_object("acd", "start", "end", "institution", "dept", "location", "name", "goal", "frequency", "attribution")
        acedemic_collabs.append(acedemic_collab)
        return acedemic_collab

    def new_non_acedemic_collab(self):
        non_acedemic_collab = self._get_object("non", "start", "end", "institution", "dept", "location", "name", "goal", "frequency", "attribution")
        non_acedemic_collabs.append(non_acedemic_collab)
        return non_acedemic_collab

    def new_conference(self):
        conference = self._get_object("con", "start", "end", "title", "type", "role", "location", "attribution")
        conferences.append(conference)
        return conference

    def new_comms_overview(self):
        comms_overview = self._get_object("com", "year", "lectures", "visits", "media")
        comms_overviews.append(comms_overview)
        return comms_overview

    def new_funding_ratio(self):
        funding_ratio = self._get_object("rat", "year", "percent")
        funding_ratios.append(funding_ratio)
        return funding_ratio

    def new_project(self):
        project = self._get_object("pro", "name", "start", "end", "type", "topic", "target", "attribution")
        projects.append(project)
        return project

    def _get_object(self, prefix, *keys)
        return ResearcherObject(prefix, self, self._get_num("%s_private" % prefix), keys)

    def _get_objects(self, prefix, *keys):
        objects = []
        for i in range(self._get_num("%s_private" % prefix)):
            objects[i] = ResearcherObject(prefix, self, i, keys)
        return objects

    def _get_value(self, key, index):
        return self._values[key][index]

    def _set_value(self, key, value, index):
        if ":" in value or ";\n" in value:
            raise ValueError
        self._values[key].insert(index, value)

    def _get_num(self, key):
        return len(self._values[key]))

    def save(self):
        file = default_storage.open(filename, "w")
        for key, values in self._values:
            file.write(key)
            for value in values:
                file.write(":%s" % value)
            file.write(";\n")
        file.close()

    def delete(self):
        default_storage.delete(self._filename)
        del self._filename
        del self._values
        del self

class ResearcherObject():

    def __init__(self, prefix, researcher, index, keys):
        self._researcher = researcher
        is_private_key = "%s_private" % prefix
        format = "%s_%s" % prefix
        if index == None:
            self._index = researcher.get_num(is_private_key) + 1
        self.is_private = self._get_property(is_private_key)
        if index == None:
            self.is_private = true
        for keyname in keys:
            key = format % keyname
            self.__dict__[keyname] = self._get_property(key)

    def save(self):
        self._researcher.save()

    def _get_property(self, key):
        return property(lambda self: self._researcher.get_value(self.key, self._index),
        lambda self, value: self._researcher.set_value(key, value, self._index))
