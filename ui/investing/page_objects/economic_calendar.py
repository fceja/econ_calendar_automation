
import os
import time
import csv

from datetime import datetime, timezone

from framework.ui.page_object import PageObject


class EconomicCalendar(PageObject):
    """
    This class contains tests for Direct Bookings

    """
    def __init__(self, driver):
        super(EconomicCalendar, self).__init__(driver)

    # region Clickers
    def click_close_banner(self):
        self._wait_for_element_visible('banner', wait_time=1)
        self._click_element('banner_close_btn')

    def click_close_signup_modal(self):
        self._wait_for_element_visible('sign_up_modal', wait_time=30)
        self._click_element('sign_up_modal_close_btn')

    def click_this_weeks_btn(self):
        self._wait_for_element_visible('time_frame_this_weeks_btn')
        self._click_element('time_frame_this_weeks_btn')
        self.wait_for_econ_cal_spinner_invisible()

    def click_tomorrow_btn(self):
        self._click_element('time_frame_tomorrow_btn')
        self.wait_for_econ_cal_spinner_invisible()

    def click_btn_icon_calendar(self):
        self._move_to_element('btn_icon_date_picker')
        self._wait_for_element_visible('btn_icon_date_picker')
        self._click_element('btn_icon_date_picker')
    # endregion Clickers

    # region Getters
    def get_calendar_table(self):
        return self._get_element_text('economic_calendar_table')

    def get_calendar_table_header(self):
        elems = self._get_elements_text('economic_calendar_header_items')
        elems.remove("")

        return elems

    def get_calendar_table_date(self):
        return self._get_elements_text('economic_calendar_date')

    def get_calendar_table_date_ids(self):
        return self._get_elements_attribute('economic_calendar_date', 'id')

    def get_calendar_row_time(self, index):
        # offset, starts at 2
        return self._get_dynamic_element_text('economic_calendar_row_time', index+2)

    def get_calendar_row_time_by_id_date_time(self, id, date_time, index):
        # offset, starts at 2
        return self._get_dynamic_element_text('economic_calendar_row_event_time_by_date_time', id, date_time, str(index+1))

    def get_calendar_row_flag_by_id_date_time(self, id, date_time, index):
        # offset, starts at 2
        return self._get_dynamic_element_text('economic_calendar_row_event_flag_by_date_time', id, date_time, str(index+1))

    def get_calendar_row_time_by_id(self, index, date_time):
        # offset, starts at 2
        self.logger.debug(f"\n\ntest index -> {index}")
        self.logger.debug(f"\n\ntest date_time -> {date_time}")

        return self._get_dynamic_element_text('economic_calendar_row_time_by_id', index+1, date_time)

    def get_calendar_row_flag(self, index):
        # offset, starts at 2
        return self._get_dynamic_element_attribute('economic_calendar_row_flag_attr', 'data-img_key', index+2)

    def get_calendar_row_event(self, index):
        # offset, starts at 2
        elems = self._get_dynamic_elements('economic_calendar_row_event_no_data', index+2)

        if len(elems) == 1:
            return self._get_dynamic_element_text('economic_calendar_row_event_no_data', index+2)
        else:
            return self._get_dynamic_element_text('economic_calendar_row_event_data', index+2)

    def get_calendar_row_actual(self, index):
        # offset, starts at 2
        if self._wait_for_dynamic_element_visible('economic_calendar_row_actual', index+2, wait_time=0.5):
            return self._get_dynamic_element_text('economic_calendar_row_actual', index+2)

        return None

    def get_calendar_row_forecast(self, index):
        # offset, starts at 2
        if self._wait_for_dynamic_element_visible('economic_calendar_row_forecast', index+2, wait_time=0.5):
            return self._get_dynamic_element_text('economic_calendar_row_forecast', index+2)
        else:
            return None

    def get_calendar_row_previous(self, index):
        # offset, starts at 2
        if self._wait_for_dynamic_element_visible('economic_calendar_row_previous', index+2, wait_time=0.5):
            return self._get_dynamic_element_text('economic_calendar_row_previous', index+2)
        else:
            return None

    def get_calendar_row_stars_by_id_date_time(self, id, date_time, index):
        selected=0

        # sentiment = self._get_dynamic_element_text('economic_calendar_row_sentiment', index+1)
        sentiment = self._get_dynamic_element_text('economic_calendar_row_event_sentiment_by_id_date_time', id, date_time,index+1)
        self.logger.debug(f"\n\ntest sentiment-> {sentiment}")

        if sentiment == 'Holiday':
            return sentiment

        else:
            # stars = self._get_dynamic_elements_attribute('economic_calendar_row_stars', 'class', index+2)
            stars = self._get_dynamic_elements_attribute('economic_calendar_row_event_sentiment_stars_by_id_date_time', 'class', id, date_time, index+1)
            self.logger.debug(f"\n\ntest stars-> {stars}")

        for star in stars:
            if 'grayFullBullishIcon' == star:
                selected += 1
            elif 'grayEmptyBullishIcon' == star:
                pass
            else:
                raise IOError(f'Expected a valid star input but got -> [{star}]')

        return f'{selected} out of {len(stars)}'

    def get_calendar_row_event_by_id_date_time(self, id, date_time, index):
        # offset, starts at 2
        elems = self._get_dynamic_elements('economic_calendar_row_event_no_data_by_id_date_time', id, date_time, index+1)
        self.logger.debug(f"\n\ntest elems-> {elems}")

        if len(elems) == 1:
            return self._get_dynamic_element_text('economic_calendar_row_event_no_data_by_id_date_time', id, date_time, index+1)
        else:
            return self._get_dynamic_element_text('economic_calendar_row_event_data_by_id_date_time', id, date_time, index+1)

    def get_calendar_row_actual_by_id_date_time(self, id, date_time, index):
        # offset, starts at 2
        if self._wait_for_dynamic_element_visible('economic_calendar_row_event_actual_by_id_date_time', id, date_time, index+1, wait_time=0.5):
            result = self._get_dynamic_element_attribute('economic_calendar_row_event_actual_font_color_by_id_date_time', 'title', id, date_time, index+1)
            self.logger.debug(f"\n\ntest this class result-> {result}")

            orig = self._get_dynamic_element_text('economic_calendar_row_event_actual_by_id_date_time', id, date_time, index+1)
            self.logger.debug(f"\n\ntest orig-> {orig}")

            if 'Better Than Expected' in result:
                return {
                    'current': orig,
                    'expected': {
                        'color': 'green',
                        'text': result
                    }
                }

            elif 'Worse Than Expected' in result:
                return {
                    'current': orig,
                    'expected': {
                        'color': 'red',
                        'text': result
                    }
                }

            return orig
        else:
            return None

    def get_calendar_row_forecast_by_id_date_time(self, id, date_time, index):
        # offset, starts at 1
        if self._wait_for_dynamic_element_visible('economic_calendar_row_event_forecast_by_id_date_time', id, date_time, index+1, wait_time=0.5):
            return self._get_dynamic_element_text('economic_calendar_row_event_forecast_by_id_date_time', id, date_time, index+1)
        else:
            return None

    def get_calendar_row_previous_by_id_date_time(self, id, date_time, index):
        # offset, starts at 1
        if self._wait_for_dynamic_element_visible('economic_calendar_row_event_previous_by_id_date_time', id, date_time, index+1, wait_time=0.5):
            # TODO: if red font or green
            result = self._get_dynamic_element_attribute('economic_calendar_row_event_previous_font_color_by_id_date_time', 'class', id, date_time, index+1)

            orig = self._get_dynamic_element_text('economic_calendar_row_event_previous_by_id_date_time', id, date_time, index+1)

            if 'redFont' in result:
                result = self._get_dynamic_element_attribute('economic_calendar_row_event_previous_by_id_date_time', 'title', id, date_time, index+1)
                self.logger.debug(f"\n\ntest -> 1.1 result -> {result}")

                return {
                    'current': orig,
                    'revised': {
                        'color': 'red',
                        'text': result
                    }
                }

            elif 'greenFont' in result:
                self.logger.debug(f"\n\ntest -> 1.2")

                result = self._get_dynamic_element_attribute('economic_calendar_row_event_previous_by_id_date_time', 'title', id, date_time, index+1)
                self.logger.debug(f"\n\ntest -> 1.1 result -> {result}")

                return {
                    'current': orig,
                    'revised': {
                        'color': 'green',
                        'text': result
                    }
                }

            return orig
        else:
            return None

    def get_date_time_format(self, date):
        self.logger.debug(f"\n\ntest date in-> {date}")

        date = date.split(',')
        date.pop(0)
        date_str = ''.join(date).strip()

        return datetime.datetime.strptime(date_str, "%B %d %Y")

    def get_date_row_events(self, id, date_time):
        self.logger.debug(f"\n\ntest date_time in-> {date_time}")
        self.logger.debug(f"\n\ntest date_time in year -> {date_time.year}")
        self.logger.debug(f"\n\ntest date_time in month -> {date_time.month}")
        self.logger.debug(f"\n\ntest date_time in day -> {date_time.day}")
        self.logger.debug(f"\n\ntest id in-> {id}")
        date = f'{date_time.year}/{date_time.month}/{date_time.day}'

        self.logger.debug(f"\n\ntest date-> {date}")

        elems = self._get_dynamic_elements('economic_calendar_row_events_by_date_time', id, date)

        event_rows={}
        i=0
        for _ in elems:
            event_rows.update({
                # f'row_{i}':{
                f'row_{i} - {date}':{
                    'time': self.get_calendar_row_time_by_id_date_time(id, date, i),
                    'country': self.get_calendar_row_flag_by_id_date_time(id, date, i),
                    'importance': self.get_calendar_row_stars_by_id_date_time(id, date, i),
                    'event': self.get_calendar_row_event_by_id_date_time(id, date, i),
                    'actual': self.get_calendar_row_actual_by_id_date_time(id, date, i),
                    'forecast': self.get_calendar_row_forecast_by_id_date_time(id, date, i),
                    'previous': self.get_calendar_row_previous_by_id_date_time(id, date, i)
                }
            })
            i+=1

        return event_rows

    def get_todays_calendar(self):
        """
        This method returnds today's economic calendar
        """
        todays_caldenar = {
            "header": self.get_calendar_table_header(),
            "date": self.get_calendar_table_date(),
            "rows": self.get_calendar_table_rows()
        }

        return todays_caldenar

    def get_row_date(self, row_index):
        if not self._wait_for_dynamic_element_visible('row_date', row_index, wait_time=0.5):
            raise Exception('Next date row does not exist')

        self._move_to_dynamic_element('row_date', row_index)

        return self._get_dynamic_element_text('row_date', row_index)

    def get_row_event(self, date, row_index):
        if not self._wait_for_dynamic_element_present('row_event', date, row_index, wait_time=0.5):
            raise Exception('Next row does not exist')

        self._move_to_dynamic_element('row_event', date, row_index)

        return {
            'time': self._get_dynamic_element_text('row_event_time', date, row_index),
            'country': self._get_dynamic_element_text('row_event_flag', date, row_index),
            'sentiment': len(self._get_dynamic_elements('row_event_sentiment', date, row_index)),
            'event_title': self._get_dynamic_element_text('row_event_title', date, row_index),
            'actual': self._get_dynamic_element_text('row_event_actual', date, row_index),
            'forecast': self._get_dynamic_element_text('row_event_forecast', date, row_index),
            'prev': self._get_dynamic_element_text('row_event_prev', date, row_index),
        }

    def get_date_events(self, date):
        events = {}

        completed = False
        event_row_index = 1
        while not completed:
            try:
                event = self.get_row_event(date, event_row_index)
                events.update({event_row_index - 1 : event})
            except:
                completed = True

            event_row_index += 1

        return events

    def get_table_data(self):
        date_events= {}
        completed = False
        date_row_index = 1
        while not completed:
            try:
                # get first row and parse date from html attribute
                today = self.get_row_date(date_row_index)
                today_list = today.replace(',', '').split(' ')
                month = today_list[1]
                day = today_list[2]
                year = today_list[3]

                date_obj = datetime.strptime(f'{month} {day} {year}', '%B %d %Y')
                curr_date = date_obj.strftime('%Y/%m/%d')
                events = self.get_date_events(curr_date)

                date_events.update({curr_date: events})

            except:
                completed = True

            date_row_index += 1

        return date_events

    def create_dir_file(self):
        today_dt = datetime.today()
        folder_path = f'mation-scan_out/{today_dt.year}-{today_dt.month}-{today_dt.day}'
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)

        return open(f'{folder_path}/output.csv', 'w', newline='')

    def get_csv_header_row(self, countries):
        header_currency_list = []
        for currency in countries.values():
            header_currency_list.append(f'{currency.lower()}_event')

        header_row = ['date_time', 'importance'] +  header_currency_list + ['previous', 'forecast', 'actual']
        return header_row, header_currency_list

    def reset_values(self, my_dic):
        for i in my_dic:
            my_dic[i]=None

        return my_dic

    def table_data_to_csv(self, countries):
        csv_file = self.create_dir_file()
        csv_writer = csv.writer(csv_file)
        header_row, header_country_event_list = self.get_csv_header_row(countries)
        csv_writer.writerow(header_row)

        table_data = self._get_elements('econ_table_rows')

        temp_event_dic = {}

        for item in header_country_event_list:
            temp_event_dic[item] = None

        holiday_id_count=0
        for i, row in enumerate(table_data):
            temp_event_dic = self.reset_values(temp_event_dic)
            assert temp_event_dic is not None
            if row.get_attribute("id") is None:

                # NOTE - if row attribute id is none, row is a date
                # dont need to do anything with row date, already considered with event, pass
                pass

            else:
                # parse date
                date_str = self._get_dynamic_element_attribute('econ_table_row_by_event_id', 'data-event-datetime', row.get_attribute("id"))
                iso_datetime_str = None
                if date_str is not None:
                    date_obj = datetime.strptime(date_str, "%Y/%m/%d %H:%M:%S")
                    iso_datetime_str = date_obj.strftime("%Y-%m-%dT%H:%M:%SZ")
                else:
                    date_text = self._get_dynamic_element_text('econ_table_row_date_text_by_event_id', row.get_attribute("id"))
                    if date_text == 'All Day':
                        date_str = self._get_dynamic_element_text('econ_table_row_date_by_event_id', row.get_attribute("id"))

                        date_obj = datetime.strptime(date_str, "%A, %B %d, %Y")

                        iso_datetime_str = date_obj.strftime("%Y-%m-%dT%H:%M:%SZ")

                    else:
                        raise Exception(f'Logic error date_text: {date_text}')

                # parse importance
                try:
                    importance = self._get_dynamic_element_attribute('econ_table_row_importance_by_event_id', 'data-img_key', row.get_attribute("id"))[-1]

                except:
                    importance = self._get_dynamic_element_text('econ_table_row_importance_holiday_by_event_id', row.get_attribute("id"))
                    assert importance == 'Holiday', f'Expected imporance to be Holiday but was not -> {importance}'

                if importance == 'Holiday':
                    importance = 0
                    currency, holiday_id_count = self. get_currency_holiday(row, holiday_id_count, date_str)

                    event = self.get_holiday_event(row, currency)
                    previous = None
                    forecast = None
                    actual = None
                else:
                    event = self._get_dynamic_element_text('econ_table_row_event_by_event_id', row.get_attribute("id"))
                    currency = self._get_dynamic_element_text('econ_table_row_currency_by_event_id', row.get_attribute("id"))
                    previous = self._get_dynamic_element_text('econ_table_row_previous_by_event_id', row.get_attribute("id"))
                    forecast = self._get_dynamic_element_text('econ_table_row_forecast_by_event_id', row.get_attribute("id"))
                    actual = self._get_dynamic_element_text('econ_table_row_actual_by_event_id', row.get_attribute("id"))

                if currency == 'EUR':
                    if self._wait_for_dynamic_element_present('econ_table_row_currency_combined_country_by_event_id', row.get_attribute("id"), 'Germany', wait_time=.01):
                        currency = 'EUR/GER'

                tValues = []
                header_row = f'{currency.lower()}_event'
                temp_event_dic[f'{header_row}'] = event

                for value in temp_event_dic.values():
                    if value is not None:
                        tValues.append(value)
                    else:
                        tValues.append(None)
                header_row = [iso_datetime_str, importance ] +  tValues + [previous, forecast, actual]

                csv_writer.writerow(header_row)

        csv_file.close()

    COUNTRY_CURRENCY = {
        "Australia": "AUD",
        "Canada": "CAD",
        "Europe": "EUR",
        "Germany": "EUR/GER",
        "Japan": "JPY",
        "New_Zealand": "NZD",
        "Switzerland": "CHF",
        "United_Kingdom": "GBP",
        "USA": "USD"
    }

    def get_holiday_event(self, row, currency):
        if '/' in currency:
            currency=currency.split('/')[1].title()
        elif currency == 'CHF' :
            currency = 'Switzerland'
        elif currency == 'GBP' :
            currency = 'United Kingdom'
        elif currency == 'JPY' :
            currency = 'Japan'
        else:
            currency=currency.title()

        country = self._get_dynamic_element_text('econ_table_row_event_holiday_currency_by_event_id_country', row.get_attribute("id"), currency)
        country = country.split(' ')[0]

        country_event = self._get_dynamic_element_text('econ_table_row_event_holiday_country_by_event_id_country', row.get_attribute("id"), country)
        return country_event

    def get_currency(self, parsed_country):
        return self.COUNTRY_CURRENCY[parsed_country]

    def get_currency_holiday(self, row, holiday_id_counter, date_str):

        holiday_count_len = len(self._get_dynamic_elements('econ_table_row_event_holiday_count', row.get_attribute("id"), date_str))
        country = self._get_dynamic_element_attribute('econ_table_row_event_holiday_country_by_event_id_country_index', 'data-img_key',row.get_attribute("id"), holiday_id_counter+1)
        holiday_id_counter += 1

        if holiday_id_counter >= holiday_count_len:
            holiday_id_counter = 0

        result = self.get_currency(country)

        return result, holiday_id_counter

    def get_tomorrows_economic_calendar(self):
        """
        This method returns tomrrows economic calendar
        """
        self.click_tomorrow_btn()

        assert self._wait_for_element_visible('time_frame_tomorrow_btn_toggled') is True, \
            'Expected Tomorrow time frame button to be selected but was not'

        tomorrows_caldenar = {
            "header": self.get_calendar_table_header(),
            "date": self.get_calendar_table_date(),
            "rows": self.get_calendar_table_rows()
        }

        self.logger.debug(f'\n\ntomorrows_calendar -> {tomorrows_caldenar}')

    def get_this_weeks_economic_calendar(self):
        """
        This method returns tomrrows economic calendar
        """
        self.click_this_weeks_btn()

        assert self._wait_for_element_visible('time_frame_this_weeks_btn_toggled') is True, \
            'Expected This weeks time frame button to be selected but was not'

        header= self.get_calendar_table_header()
        self.logger.debug(f"\n\ntest header-> {header}")

        rows= self.get_calendar_table_rows()
        self.logger.debug(f"\n\ntest rows -> {rows}")

        assert 1 == 0


        this_weeks_caldenar = {
            "header": self.get_calendar_table_header(),
            "date": self.get_calendar_table_date(),
            "rows": self.get_calendar_table_rows()
        }

        self.logger.debug(f'\n\ntomorrows_calendar -> {this_weeks_caldenar}')
        assert 1 == 0

    def get_calendar_table_rows(self):
        dates= self.get_calendar_table_date()
        self.logger.debug(f"\n\ntest date-> {dates}")

        date_ids = self.get_calendar_table_date_ids()
        self.logger.debug(f"\n\ntest date_ids-> {date_ids}")


        time_events = {}
        i=0
        # for id in date_ids:
        for date in dates:
            self.logger.debug(f"\n\ntest this loop date -> {date}")
            date_time = self.get_date_time_format(date)
            self.logger.debug(f"\n\ntest date_time1-> {date_time}")

            date_events = self.get_date_row_events(date_ids[i], date_time)
            self.logger.debug(f"\n\ntest date_events1-> {date_events}")

            time_events.update({
                    # 'date': date,
                    # 'event_rows': date_events

                f'event_{i}':{
                    'date': date,
                    'event_rows': date_events
                }
            })

            i+=1

            self.logger.debug(f"\n\ntest time_events in loop-> {time_events}")
            # assert 1 == 0

        self.logger.debug(f"\n\ntest time_events out loop -> {time_events}")

    def set_time(self, timezone):
        self._click_element('economic_calendar_curr_time_dropdown_chevron')

        self._wait_for_dynamic_element_visible('economic_calendar_curr_time_timezone_menu', timezone)
        self._click_dynamic_element('economic_calendar_curr_time_timezone_menu', timezone)

        self.wait_for_econ_cal_spinner_invisible()

    # endregion Setters

    # region Waiters
    def wait_for_econ_cal_spinner_invisible(self):
        self._wait_for_element_invisible('econ_cal_load_spinner', wait_time=1)
    # endregion Wait

    # region Macros
    def close_onload_popups(self):
        """
        This method closes banners / notifcation / modals that display when landing on page
        """
        self.click_close_banner()
        """
        This method returns tomrrows economic calendar
        """
        self.click_this_weeks_btn()

        assert self._wait_for_element_visible('time_frame_this_weeks_btn_toggled') is True, \
            'Expected This weeks time frame button to be selected but was not'

        header= self.get_calendar_table_header()
        self.logger.debug(f"\n\ntest header-> {header}")

        rows= self.get_calendar_table_rows()
        self.logger.debug(f"\n\ntest rows -> {rows}")

        assert 1 == 0


        this_weeks_caldenar = {
            "header": self.get_calendar_table_header(),
            "date": self.get_calendar_table_date(),
            "rows": self.get_calendar_table_rows()
        }

        self.logger.debug(f'\n\ntomorrows_calendar -> {this_weeks_caldenar}')
        assert 1 == 0
    # endregion Macros