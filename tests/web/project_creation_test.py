from faker import Faker

from src.web.application import Application


def test_new_project_creation(app: Application, login):
    target_project_name = Faker().company()

    (app.new_projects_page
     .open()
     .is_loaded()
     .fill_project_till(target_project_name)
     .click_create())

    (app.project_page
     .is_loaded()
     .empty_project_name_is(target_project_name)
     .close_read_me())

    (app.project_page.side_bar
     .is_loaded()
     .click_logo()
     .is_tab_active("Tests"))
