from framework.ui.page_object import PageObject

class FilterCountrySelectionModal(PageObject):
    # region clickers
    def click_btn_apply(self):
        self._move_to_element('btn_apply')
        self._wait_for_element_visible('btn_apply')
        self._click_element('btn_apply')
        self._wait_for_element_invisible('container_filters')

    def click_btn_clear_selections(self):
        self._wait_for_element_visible('btn_clear_country_selections')
        self._click_element('btn_clear_country_selections')

    def click_btn_country_selection(self, country):
        self._move_to_dynamic_element('input_country_option', country)
        self._wait_for_dynamic_element_visible('input_country_option', country)
        self._click_dynamic_element('input_country_option', country)

    def click_btn_filter_country(self):
        self._wait_for_element_visible('btn_filter_countries')
        self._click_element('btn_filter_countries')

    # endregion clickers

    # region waiters
    def wait_for_container_countries(self):
        return self._wait_for_element_visible('container_countries')
    # endregion waiters