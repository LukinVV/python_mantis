import random
from model.project import Project


def test_project_delete(app):
    if len(app.project.get_project_list()) == 0:
        project = Project(name="new")
        app.project.add_project(project)
    old_project_list = app.project.get_project_list()
    # print("страрый список %s" %len(old_project_list))
    project = random.choice(old_project_list)
    app.project.delete_project_by_id(project.id)
    new_project_list = app.project.get_project_list()
    # print("новый список %s" %len(new_project_list))
    assert len(new_project_list) == len(old_project_list) - 1
    old_project_list.remove(project)
    assert sorted(old_project_list, key=Project.id_or_max) == sorted(new_project_list, key=Project.id_or_max)
