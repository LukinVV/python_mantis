from pony.orm import *
from datetime import datetime
from model.project import Project
from pymysql.converters import decoders


class ORMFixture:
    db = Database()

    class ORMProject(db.Entity):
        _table_ = 'mantis_project_table'
        id = PrimaryKey(int, column="id")
        name = Optional(str, column="name")
        status = Optional(int, column="status")
        inherit_gl_categories = Optional(int, column="inherit_global")
        view_status = Optional(int, column="view_state")
        description = Optional(str, column="description")
        enabled = Optional(int, column="enabled")

    def __init__(self, host, name, user, password):
        self.db.bind('mysql', host=host, database=name, user=user, password=password, conv=decoders)
        self.db.generate_mapping()
        sql_debug(True)

    def convert_projects_to_model(self, projects):
        def convert(project):
            return Project(id=str(project.id), name=project.name,
                           status=self.convert_status(project.status),
                           view_status=self.convert_view_status(project.view_status), description=project.description,
                           inherit_gl_categories=self.convert_inherit_gl_categories(project.inherit_gl_categories),
                           enabled=self.convert_enabled(project.enabled))

        return list(map(convert, projects))

    @db_session
    def get_project_list(self):
        return self.convert_projects_to_model(select(g for g in ORMFixture.ORMProject))

    def convert_status(self, status):
        status_list = dict({50: "stable", 10: "development", 30: "release", 70: "obsolete"})
        return status_list[status]

    def convert_view_status(self, status):
        status_list = dict({10: "public", 50: "private"})
        return status_list[status]

    def convert_inherit_gl_categories(self, in_gl):
        status_list = dict({1: True, 0: False})
        return status_list[in_gl]

    def convert_enabled(self, enabled):
        status_list = dict({1: "X", 0: "0"})
        return status_list[enabled]
