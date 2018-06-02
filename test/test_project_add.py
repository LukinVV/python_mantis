from model.project import Project
import string
import random

def test_add_project(app, json_projects, orm, check_ui):
    old_project_list = orm.get_project_list()
    project = json_projects
    app.project.add_project(project)
    new_project_list = orm.get_project_list()
    # assert len(new_project_list) == len(old_project_list) + 1
    old_project_list.append(project)
    assert sorted(old_project_list, key=Project.id_or_max) == sorted(new_project_list, key=Project.id_or_max)
    if check_ui:
        print("Проверка пользовательского интерфейса")
        project_from_ui = app.project.get_project_list()
        project_from_db = orm.get_project_list()
        assert sorted(project_from_ui, key=Project.id_or_max) == sorted(project_from_db, key=Project.id_or_max)
