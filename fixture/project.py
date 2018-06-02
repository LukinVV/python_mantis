from model.project import Project
from selenium.webdriver.support.ui import Select
import time


class ProjectHelper:

    def __init__(self, app):
        self.app = app

    project_cach = None

    def open_project_page(self):
        wd = self.app.wd
        if not (wd.current_url.endswith("/manage_proj_page.php")):
            wd.find_element_by_link_text("Manage").click()
            wd.find_element_by_link_text("Manage Projects").click()

    def change_field_value(self, field_name, text):
        wd = self.app.wd
        if text is not None:
            wd.find_element_by_name(field_name).click()
            wd.find_element_by_name(field_name).clear()
            wd.find_element_by_name(field_name).send_keys(text)

    def change_list_value(self, select_name, text):
        wd = self.app.wd
        if text is not None:
            select = Select(wd.find_element_by_name(select_name))
            select.select_by_visible_text(text)

    def change_checkbox_value(self, checkbox_name, bool):
        wd = self.app.wd
        if bool is not None:
            checkbox = wd.find_element_by_name(checkbox_name)
            if not bool:
                checkbox.click()

    def fill_project_form(self, project):
        wd = self.app.wd
        self.change_field_value("name", project.name)
        self.change_list_value("status", project.status)
        self.change_checkbox_value("inherit_global", project.inherit_gl_categories)
        self.change_list_value("view_state", project.view_status)
        self.change_field_value("description", project.description)

    def add_project(self, project):
        wd = self.app.wd
        self.open_project_page()
        wd.find_element_by_css_selector("input[value='Create New Project']").click()
        # заполнение формы
        self.fill_project_form(project)
        wd.find_element_by_xpath("//input[@value='Add Project']").click()
        self.project_cach = None

    def get_project_list(self):
        wd = self.app.wd
        self.open_project_page()
        if self.project_cach is None:
            self.project_cach = []
            table = wd.find_elements_by_css_selector(".width100")[1]
            rows = table.find_elements_by_tag_name("tr")
            for row in rows[2:len(rows)]:
                cells = row.find_elements_by_tag_name("td")
                name = cells[0].find_element_by_tag_name("a").text
                status = cells[1].text
                enabled = cells[2].text
                view_status = cells[3].text
                description = cells[4].text
                id = cells[0].find_element_by_tag_name("a").get_attribute("href").split("id=")[1]
                self.project_cach.append(
                    Project(name=name, status=status, id=id, enabled=enabled,
                            view_status=view_status, description=description))
        return list(self.project_cach)

    def delete_project_by_id(self, id):
        wd = self.app.wd
        self.open_project_page()
        self.open_project_by_id(id)
        wd.find_element_by_css_selector("input[value='Delete Project']").click()
        wd.find_element_by_css_selector("input[value='Delete Project']").click()
        self.open_project_page()
        self.project_cach = None

    def open_project_by_id(self, id):
        wd = self.app.wd
        wd.find_element_by_xpath("//a[contains(@href, 'manage_proj_edit_page.php?project_id=%s')]" %id).click()
