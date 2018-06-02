from model.project import Project
import string
import random

def test_add_project(app, json_projects):
    old_project_list = app.project.get_project_list()
    project = json_projects
    app.project.add_project(project)
    new_project_list = app.project.get_project_list()
    assert len(new_project_list) == len(old_project_list) + 1
    old_project_list.append(project)
    assert sorted(old_project_list, key=Project.id_or_max) == sorted(new_project_list, key=Project.id_or_max)




# def random_string(max_len):
#     symbols = string.ascii_letters * 3 + string.digits * 3
#     return "".join([random.choice(symbols) for i in range(random.randrange(max_len))])
#
#
# def test_add_project_old(app, json_projects):
#     old_project_list = app.project.get_project_list()
#     project = Project(name=random_string(10),
#                       status="stable",
#                       inherit_gl_categories=True,
#                       view_status="public",
#                       description=random_string(10))
#     project = json_projects
#     app.project.add_project(project)
#     new_project_list = app.project.get_project_list()
#     assert len(new_project_list) == len(old_project_list) + 1
#     old_project_list.append(project)
#     assert sorted(old_project_list, key=Project.id_or_max) == sorted(new_project_list, key=Project.id_or_max)