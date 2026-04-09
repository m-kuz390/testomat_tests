import re

from playwright.sync_api import expect

from src.web.Application import Application

TARGET_PROJECT = "Grocery, Outdoors & Shoes"
TARGET_PROJECT_URL = "/projects/grocery-outdoors-shoes-074f0/"


def test_projects_page_is_loaded(app: Application, login):
    app.projects_page.header.is_loaded()


def test_search_project(app: Application, login):
    app.projects_page.header.search_project(TARGET_PROJECT)

    card = app.projects_page.get_project_card(TARGET_PROJECT)
    card.is_visible()


def test_search_project_not_found(app: Application, login):
    app.projects_page.header.search_project("nonexistent project 12345")

    card = app.projects_page.get_project_card(TARGET_PROJECT)
    card.is_hidden()


def test_project_card_has_correct_badge(app: Application, login):
    card = app.projects_page.get_project_card(TARGET_PROJECT)
    card.is_visible()

    expect(card.get_badge()).to_have_text("Classical")


def test_open_project(app: Application, login):
    card = app.projects_page.get_project_card(TARGET_PROJECT)
    card.click()

    expect(app.page).to_have_url(re.compile(TARGET_PROJECT_URL))


def test_switch_company_to_free(app: Application, login):
    app.projects_page.header.select_company("Free Projects")

    card = app.projects_page.get_project_card(TARGET_PROJECT)
    card.is_hidden()


def test_create_project_button_navigates(app: Application, login):
    app.projects_page.header.click_create()

    expect(app.page).to_have_url(re.compile(r"/projects/new$"))
