from suds.client import Client
from suds import WebFault
from model.project import Project


class SoapHelper:

    def __init__(self, app):
        self.app = app

    def can_login(self, username, password):
        client = Client(self.app.config['soap']['url'])
        try:
            client.service.mc_login(username, password)
            return True
        except WebFault:
            return False

    def get_project_list(self, username, password):
        client = Client(self.app.config['soap']['url'])
        try:
            projects = client.service.mc_projects_get_user_accessible(username, password)
            self.projects_list = []
            for element in projects:
                id = element.id
                name = element.name
                self.projects_list.append(Project(id=str(id), name=name))
            return self.projects_list
        except WebFault:
            return False