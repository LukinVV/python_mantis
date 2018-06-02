import random
from model.project import Project


def test_project_delete(app, orm, check_ui):
    if len(orm.get_project_list()) == 0:
        project = Project(name="new")
        app.project.add_project(project)
    old_project_list = orm.get_project_list()
    # print("страрый список %s" %len(old_project_list))
    project = random.choice(old_project_list)
    app.project.delete_project_by_id(project.id)
    new_project_list = orm.get_project_list()
    # print("новый список %s" %len(new_project_list))
    # assert len(new_project_list) == len(old_project_list) - 1
    old_project_list.remove(project)
    assert sorted(old_project_list, key=Project.id_or_max) == sorted(new_project_list, key=Project.id_or_max)
    if check_ui:
        print("Проверка пользовательского интерфейса")
        project_from_ui = app.project.get_project_list()
        project_from_db = orm.get_project_list()
        assert sorted(project_from_ui, key=Project.id_or_max) == sorted(project_from_db, key=Project.id_or_max)