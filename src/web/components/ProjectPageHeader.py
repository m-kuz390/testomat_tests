from playwright.sync_api import Page, expect


class ProjectPageHeader:
    def __init__(self, page: Page):
        self.page = page

    def is_loaded(self):
        expect(self.page.locator(".common-page-header")).to_be_visible()
        expect(self.page.locator(".common-page-header h2")).to_have_text("Projects")

    def get_selected_company(self):
        return self.page.locator("#company_id")

    def get_plan_name(self):
        return self.page.locator(".tooltip-project-plan span").last

    def select_company(self, company_name: str):
        self.page.locator("#company_id").select_option(label=company_name)

    def search_project(self, project_name: str):
        self.page.locator("#content-desktop #search").fill(project_name)

    def click_create(self):
        self.page.locator(".common-page-header-right").get_by_role("link", name="Create").click()

    def switch_to_grid_view(self):
        self.page.locator("#grid-view").click()

    def switch_to_table_view(self):
        self.page.locator("#table-view").click()

    def is_grid_view_active(self):
        expect(self.page.locator("#grid-view")).to_have_class("tablinks active_list_type")

    def is_table_view_active(self):
        expect(self.page.locator("#table-view")).to_have_class("tablinks active_list_type")
