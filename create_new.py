#import threading

#from kivy.clock import mainthread
from connection import Connection
#from datetime import date
#import time
#from kivy.utils import strtotuple
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.dialog import MDDialog
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.picker import MDDatePicker, MDTimePicker
from kivy.metrics import dp
from kivy.lang import Builder
from kivymd.uix.screen import MDScreen
from kivy.core.window import Window
#from kivymd.uix.card import MDCard
from kivy.properties import StringProperty, NumericProperty, ObjectProperty
from kivymd.uix.button import MDFlatButton

#from threading import Thread

Builder.load_file('createnew.kv')

Window.keyboard_anim_args = {'d': 0.2, 't': 'in_out_expo'}
Window.softinput_mode = 'below_target'

PREACHERS = ['Ptr. William', 'Jayr', 'Lovely', 'Paul', 'Kim', 'Milca']

MONTHS = ['January', 'February', 'March', 'April',
          'May', 'June', 'July', 'August',
          'September', 'October', 'November', 'December', ]

sched_counter = 0

outreach_name_list = []

month_list = []
sched_num_list = []

date_list = []
time_list = []
year_list = []

preachers_list = []
sub_preacher_list = []

topic_list = []
topic_details_list = []

event_list = []
event_details_list = []
event_organizer_list = []
event_contact_list = []

opening_prayer_list = []
scripture_reading_list = []
offertory_list = []
closing_prayer_list = []

status = []

TO_SEND = []


# Main Schedule Creation
class MainServiceCreate(MDScreen):
    schedule_num = NumericProperty(1)

    def on_add_button_press(self):
        self.ids.create.add_widget(MainServiceCreateCard(schedule_num_text=f'Schedule #{self.schedule_num}'))
        self.schedule_num += 1

    def on_send_button_press(self, button):
        MainServiceCreateCard().send_dialog_open()


# Outreach Sched Creation
class OutreachServiceCreate(MDScreen):
    schedule_num = NumericProperty(1)

    def on_add_button_press(self):
        self.ids.create.add_widget(OutreachServiceCreateCard(schedule_num_text=f'Schedule #{self.schedule_num}'))
        self.schedule_num += 1

    def on_send_button_press(self, button):
        OutreachServiceCreateCard().send_dialog_open()


# Event Schedule Creation
class EventServiceCreate(MDScreen):
    schedule_num = NumericProperty(1)

    def on_add_button_press(self):
        self.ids.create.add_widget(EventServiceCreateCard(schedule_num_text=f'Schedule #{self.schedule_num}'))
        self.schedule_num += 1

    def on_send_button_press(self, button):
        EventServiceCreateCard().send_dialog_open()


# Create Cards
class MainServiceCreateCard(MDBoxLayout):
    schedule_num_text = StringProperty('')

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # Preachers Dropdown
        preachers_menu_items = [{
            'viewclass': 'OneLineListItem',
            'divider': None,
            'text': i,
            'height': dp(40),
            'on_release': lambda x=i: self.set_preachers_item(x),
        } for i in PREACHERS
        ]

        sub_preachers_menu_items = [{
            'viewclass': 'OneLineListItem',
            'divider': None,
            'text': i,
            'height': dp(40),
            'on_release': lambda x=i: self.set_sub_preachers_item(x),
        } for i in PREACHERS
        ]

        self.preachers_menu = MDDropdownMenu(
            caller=self.ids.preachers_drop_down,
            items=preachers_menu_items,
            position='auto',
            width_mult=2
        )

        self.sub_preachers_menu = MDDropdownMenu(
            caller=self.ids.sub_drop_down,
            items=sub_preachers_menu_items,
            position='auto',
            width_mult=2
        )

        # Months Dropdown
        months_menu_items = [{
            'viewclass': 'OneLineListItem',
            'divider': None,
            'text': i,
            'size_hint_y': None,
            'height': dp(40),
            'on_release': lambda x=i: self.set_months_item(x),
        } for i in MONTHS
        ]

        self.months_menu = MDDropdownMenu(
            caller=self.ids.months_drop_down,
            items=months_menu_items,
            position='auto',
            width_mult=2
        )

        # Toolbar button
        self.dialog = MDDialog(
            title='Are you sure ka na ba?',
            text=f'{sched_counter} schedule(s) to send.\nContinue?',
            type='simple',
            buttons=[
                MDFlatButton(text='Wait lang muna', font_style='Button', on_release=self.on_close_dialog),
                MDFlatButton(text='Send na dali', font_style='Button', on_release=self.on_send_press)

            ]

        )

    def set_preachers_item(self, text__item):
        self.preachers_menu.dismiss()
        self.ids.preachers.text = text__item

    def set_sub_preachers_item(self, text__item):
        self.sub_preachers_menu.dismiss()
        self.ids.sub_preachers.text = text__item

    def set_months_item(self, text__item):
        self.months_menu.dismiss()
        self.ids.months.text = text__item

    def on_date_picker(self):
        self.date_dialog = MDDatePicker()
        self.date_dialog.bind(on_save=self.on_date_save, on_cancel=self.on_date_cancel)
        self.date_dialog.open()

    def on_date_save(self, instance, value, date_range):
        self.ids.date_text_field.text = str(value)
        date_list.append(self.ids.date_text_field.text)

    def on_date_cancel(self, instance, value):
        self.date_dialog.dismiss()

    def show_time_picker(self):
        self.time_dialog = MDTimePicker()
        self.time_dialog.bind(on_save=self.get_time_save)
        self.time_dialog.open()

    def get_time_save(self, instance, value):
        self.ids.time_text_field.text = str(value)

    def on_time_save(self, instance, time):
        self.ids.time_text_field = str(time)

    # textfield functions
    def get_year(self):
        year_list.append(date_list[-1][0:4])

    def on_schedule_save(self):
        self.save_dialog = MDDialog(
            title='Save Schedule',
            text='You can no longer undo this.\nAre you sure?',
            type='simple',
            buttons=[
                MDFlatButton(
                    text='Save',
                    font_style='Button',
                    on_release=self.on_save
                ),
                MDFlatButton(
                    text='Cancel',
                    font_style='Button',
                    on_release=self.on_sched_dialog_dismiss
                )
            ]
        )
        if self.ids.preachers.disabled == False:
            self.save_dialog.open()
        else:
            self.save_dialog.disabled = True

    def on_check_text(self, text_input):
        if self.ids.months.text != '' and self.ids.preachers.text != '' \
                and self.ids.date_text_field.text != '' and self.ids.time_text_field.text != '' \
                and self.ids.topic.text != '' and self.ids.sub_preachers.text != '' \
                and self.ids.opening_prayer.text != '' and self.ids.scripture_reading.text != '' \
                and self.ids.offertory.text != '' and self.ids.closing_prayer.text != '':
            self.ids.save_button.disabled = False

    def save_button_change(self):
        self.ids.save_button.text = 'Saved'
        self.ids.save_button.md_bg_color = 254 / 255, 215 / 255, 46 / 255, 1

    def on_sched_dialog_dismiss(self, button):
        self.save_dialog.dismiss()

    def for_sending(self):
        send_list = (month_list[0], sched_counter, date_list[0], time_list[0], year_list[0],
                     preachers_list[0], sub_preacher_list[0], topic_list[0], topic_details_list[0],
                     event_list[0], event_details_list[0], opening_prayer_list[0], scripture_reading_list[0],
                     offertory_list[0], closing_prayer_list[0], status[0])

        TO_SEND.append(send_list)

    def clear_list(self):
        month_list.clear()
        preachers_list.clear()
        date_list.clear()
        time_list.clear()
        year_list.clear()
        sub_preacher_list.clear()
        topic_list.clear()
        topic_details_list.clear()
        event_list.clear()
        event_details_list.clear()
        opening_prayer_list.clear()
        scripture_reading_list.clear()
        offertory_list.clear()
        closing_prayer_list.clear()
        status.clear()

    def disable_fields(self):
        self.ids.months_drop_down.disabled = True
        self.ids.preachers.disabled = True
        self.ids.preachers_drop_down.disabled = True
        self.ids.date_text_button.disabled = True
        self.ids.time_text_button.disabled = True
        self.ids.topic.disabled = True
        self.ids.topic_details.disabled = True
        self.ids.sub_preachers.disabled = True
        self.ids.sub_drop_down.disabled = True
        self.ids.opening_prayer.disabled = True
        self.ids.scripture_reading.disabled = True
        self.ids.offertory.disabled = True
        self.ids.closing_prayer.disabled = True
        self.ids.event.disabled = True
        self.ids.event_details.disabled = True

    def on_save(self, button):
        global sched_counter
        self.save_dialog.dismiss()

        month_list.append(self.ids.months.text)
        preachers_list.append(self.ids.preachers.text)
        date_list.append(self.ids.date_text_field.text)
        time_list.append(self.ids.time_text_field.text)
        self.get_year()

        topic_list.append(self.ids.topic.text)

        sub_preacher_list.append(self.ids.sub_preachers.text)
        opening_prayer_list.append(self.ids.opening_prayer.text)
        scripture_reading_list.append(self.ids.scripture_reading.text)
        offertory_list.append(self.ids.offertory.text)
        closing_prayer_list.append(self.ids.closing_prayer.text)

        if self.ids.topic_details.text != '':
            topic_details_list.append(self.ids.topic_details.text)
        else:
            topic_details_list.append('No details provided.')

        if self.ids.event.text != '':
            event_list.append(self.ids.event.text)
        else:
            event_list.append('None')

        if self.ids.event_details.text != '':
            event_details_list.append(self.ids.event_details.text)
        else:
            event_details_list.append('None')

        sched_counter += 1

        sched_num_list.append(sched_counter)

        status.append('Pending')

        # Prepare to send
        self.for_sending()

        # clear list
        self.clear_list()

        # disable fields
        self.disable_fields()

        # change button
        self.save_button_change()

        # Toobar button

    def send_dialog_open(self):
        if sched_counter != 0:
            self.dialog.open()
        else:
            self.dialog.disabled = True

    def on_close_dialog(self, button):
        self.dialog.dismiss()

    # SEND BUTTON
    def on_send_press(self, obj):
        self.on_close_dialog(self)

        Connection().on_main_send(TO_SEND)
        self.send_status()

    def send_status(self):
        self.send_dialog = MDDialog(
            title='Sent',
            type='simple',
            size_hint=(.45, None),
            buttons=[
                MDFlatButton(
                    text='Okay',
                    font_style='Button',
                    on_release=self.send_spinner_close
                )
            ]
        )

        self.send_dialog.open()

    def send_spinner_close(self, button):
        self.send_dialog.dismiss()


# Outreach Card
class OutreachServiceCreateCard(MDBoxLayout):
    schedule_num_text = StringProperty('')

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        preachers_menu_items = [{
            'viewclass': 'OneLineListItem',
            'divider': None,
            'text': i,
            'height': dp(40),
            'on_release': lambda x=i: self.set_preachers_item(x),
        } for i in PREACHERS
        ]

        sub_preachers_menu_items = [{
            'viewclass': 'OneLineListItem',
            'divider': None,
            'text': i,
            'height': dp(40),
            'on_release': lambda x=i: self.set_sub_preachers_item(x),
        } for i in PREACHERS
        ]

        self.preachers_menu = MDDropdownMenu(
            caller=self.ids.preachers_drop_down,
            items=preachers_menu_items,
            position='auto',
            width_mult=2
        )

        self.sub_preachers_menu = MDDropdownMenu(
            caller=self.ids.sub_drop_down,
            items=sub_preachers_menu_items,
            position='auto',
            width_mult=2
        )

        # Months Dropdown
        months_menu_items = [{
            'viewclass': 'OneLineListItem',
            'divider': None,
            'text': i,
            'size_hint_y': None,
            'height': dp(40),
            'on_release': lambda x=i: self.set_months_item(x),
        } for i in MONTHS
        ]

        self.months_menu = MDDropdownMenu(
            caller=self.ids.months_drop_down,
            items=months_menu_items,
            position='auto',
            width_mult=2
        )

        # Toolbar button
        self.dialog = MDDialog(
            title='Are you sure ka na ba?',
            text=f'{sched_counter} schedule(s) to send.\nContinue?',
            type='simple',
            buttons=[
                MDFlatButton(text='Wait lang muna', font_style='Button', on_release=self.on_close_dialog),
                MDFlatButton(text='Send na dali', font_style='Button', on_release=self.on_send_press)

            ]

        )

    def set_preachers_item(self, text__item):
        self.preachers_menu.dismiss()
        self.ids.preachers.text = text__item

    def set_sub_preachers_item(self, text__item):
        self.sub_preachers_menu.dismiss()
        self.ids.sub_preachers.text = text__item

    def set_months_item(self, text__item):
        self.months_menu.dismiss()
        self.ids.months.text = text__item

    def on_date_picker(self):
        self.date_dialog = MDDatePicker()
        self.date_dialog.bind(on_save=self.on_date_save, on_cancel=self.on_date_cancel)
        self.date_dialog.open()

    def on_date_save(self, instance, value, date_range):
        self.ids.date_text_field.text = str(value)

    def on_date_cancel(self, instance, value):
        self.date_dialog.dismiss()

    def show_time_picker(self):
        self.time_dialog = MDTimePicker()
        self.time_dialog.bind(on_save=self.get_time_save)
        self.time_dialog.open()

    def get_time_save(self, instance, value):
        self.ids.time_text_field.text = str(value)

    def on_time_save(self, instance, time):
        self.ids.time_text_field = str(time)

    # textfield functions
    def get_year(self):
        year_list.append(date_list[-1][0:4])

    def on_schedule_save(self):
        self.save_dialog = MDDialog(
            title='Save Schedule',
            text='Please check all the fields before sending. This can no longer be undone.\nAre you sure?',
            type='simple',
            buttons=[
                MDFlatButton(
                    text='Save',
                    font_style='Button',
                    on_release=self.on_save
                ),
                MDFlatButton(
                    text='Cancel',
                    font_style='Button',
                    on_release=self.on_sched_dialog_dismiss
                )
            ]
        )
        if self.ids.preachers.disabled == False:
            self.save_dialog.open()
        else:
            self.save_dialog.disabled = True

    def on_check_text(self, text_input):
        if self.ids.outreach_name != '' and self.ids.months.text != '' and self.ids.preachers.text != '' \
                and self.ids.date_text_field.text != '' and self.ids.time_text_field.text != '' \
                and self.ids.topic.text != '' and self.ids.sub_preachers.text != '' \
                and self.ids.opening_prayer.text != '' and self.ids.scripture_reading.text != '' \
                and self.ids.offertory.text != '' and self.ids.closing_prayer.text != '':
            self.ids.save_button.disabled = False

    def save_button_change(self):
        self.ids.save_button.text = 'Saved'
        self.ids.save_button.md_bg_color = 254 / 255, 215 / 255, 46 / 255, 1

    def on_sched_dialog_dismiss(self, button):
        self.save_dialog.dismiss()

    def for_sending(self):
        send_list = (month_list[0], outreach_name_list[0], sched_counter, date_list[0], time_list[0], year_list[0],
                     preachers_list[0], sub_preacher_list[0], topic_list[0], topic_details_list[0],
                     event_list[0], event_details_list[0], opening_prayer_list[0], scripture_reading_list[0],
                     offertory_list[0], closing_prayer_list[0], status[0])

        TO_SEND.append(send_list)

    def clear_list(self):
        month_list.clear()
        outreach_name_list.clear()
        preachers_list.clear()
        date_list.clear()
        time_list.clear()
        year_list.clear()
        sub_preacher_list.clear()
        topic_list.clear()
        topic_details_list.clear()
        event_list.clear()
        event_details_list.clear()
        opening_prayer_list.clear()
        scripture_reading_list.clear()
        offertory_list.clear()
        closing_prayer_list.clear()
        status.clear()

    def disable_fields(self):
        self.ids.months_drop_down.disabled = True
        self.ids.outreach_name.disabled = True
        self.ids.preachers.disabled = True
        self.ids.preachers_drop_down.disabled = True
        self.ids.date_text_button.disabled = True
        self.ids.time_text_button.disabled = True
        self.ids.topic.disabled = True
        self.ids.topic_details.disabled = True
        self.ids.sub_preachers.disabled = True
        self.ids.sub_drop_down.disabled = True
        self.ids.opening_prayer.disabled = True
        self.ids.scripture_reading.disabled = True
        self.ids.offertory.disabled = True
        self.ids.closing_prayer.disabled = True
        self.ids.event.disabled = True
        self.ids.event_details.disabled = True

    def on_save(self, button):
        global sched_counter
        self.save_dialog.dismiss()

        month_list.append(self.ids.months.text)
        outreach_name_list.append(self.ids.outreach_name.text)
        preachers_list.append(self.ids.preachers.text)
        date_list.append(self.ids.date_text_field.text)
        time_list.append(self.ids.time_text_field.text)
        self.get_year()

        topic_list.append(self.ids.topic.text)

        sub_preacher_list.append(self.ids.sub_preachers.text)
        opening_prayer_list.append(self.ids.opening_prayer.text)
        scripture_reading_list.append(self.ids.scripture_reading.text)
        offertory_list.append(self.ids.offertory.text)
        closing_prayer_list.append(self.ids.closing_prayer.text)

        if self.ids.topic_details.text != '':
            topic_details_list.append(self.ids.topic_details.text)
        else:
            topic_details_list.append('No details provided.')

        if self.ids.event.text != '':
            event_list.append(self.ids.event.text)
        else:
            event_list.append('None')

        if self.ids.event_details.text != '':
            event_details_list.append(self.ids.event_details.text)
        else:
            event_details_list.append('None')

        sched_counter += 1

        sched_num_list.append(sched_counter)

        status.append('Pending')

        # Prepare to send
        self.for_sending()

        # clear list
        self.clear_list()

        # disable fields
        self.disable_fields()

        # change button
        self.save_button_change()

        # Toobar button

    def send_dialog_open(self):
        if sched_counter != 0:
            self.dialog.open()
        else:
            self.dialog.disabled = True

    def on_close_dialog(self, button):
        self.dialog.dismiss()

    # SEND BUTTON
    def on_send_press(self, obj):
        self.on_close_dialog(self)

        Connection().on_outreach_send(TO_SEND)
        self.send_status()

    def send_status(self):
        self.send_dialog = MDDialog(
            title='Sent',
            type='simple',
            size_hint=(.45, None),
            buttons=[
                MDFlatButton(
                    text='Okay',
                    font_style='Button',
                    on_release=self.send_spinner_close
                )
            ]
        )

        self.send_dialog.open()

    def send_spinner_close(self, button):
        self.send_dialog.dismiss()


# Events Card
class EventServiceCreateCard(MDBoxLayout):
    schedule_num_text = StringProperty('')

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        preachers_menu_items = [{
            'viewclass': 'OneLineListItem',
            'divider': None,
            'text': i,
            'height': dp(40),
            'on_release': lambda x=i: self.set_preachers_item(x),
        } for i in PREACHERS
        ]

        sub_preachers_menu_items = [{
            'viewclass': 'OneLineListItem',
            'divider': None,
            'text': i,
            'height': dp(40),
            'on_release': lambda x=i: self.set_sub_preachers_item(x),
        } for i in PREACHERS
        ]

        self.preachers_menu = MDDropdownMenu(
            caller=self.ids.preachers_drop_down,
            items=preachers_menu_items,
            position='auto',
            width_mult=2
        )

        self.sub_preachers_menu = MDDropdownMenu(
            caller=self.ids.sub_drop_down,
            items=sub_preachers_menu_items,
            position='auto',
            width_mult=2
        )

        # Months Dropdown
        months_menu_items = [{
            'viewclass': 'OneLineListItem',
            'divider': None,
            'text': i,
            'size_hint_y': None,
            'height': dp(40),
            'on_release': lambda x=i: self.set_months_item(x),
        } for i in MONTHS
        ]

        self.months_menu = MDDropdownMenu(
            caller=self.ids.months_drop_down,
            items=months_menu_items,
            position='auto',
            width_mult=2
        )

        # Toolbar button
        self.dialog = MDDialog(
            title='Are you sure ka na ba?',
            text=f'{sched_counter} schedule(s) to send.\nContinue?',
            type='simple',
            buttons=[
                MDFlatButton(text='Wait lang muna', font_style='Button', on_release=self.on_close_dialog),
                MDFlatButton(text='Send na dali', font_style='Button', on_release=self.on_send_press)

            ]

        )

    def set_preachers_item(self, text__item):
        self.preachers_menu.dismiss()
        self.ids.preachers.text = text__item

    def set_sub_preachers_item(self, text__item):
        self.sub_preachers_menu.dismiss()
        self.ids.sub_preachers.text = text__item

    def set_months_item(self, text__item):
        self.months_menu.dismiss()
        self.ids.months.text = text__item

    def on_date_picker(self):
        self.date_dialog = MDDatePicker()
        self.date_dialog.bind(on_save=self.on_date_save, on_cancel=self.on_date_cancel)
        self.date_dialog.open()

    def on_date_save(self, instance, value, date_range):
        self.ids.date_text_field.text = str(value)

    def on_date_cancel(self, instance, value):
        self.date_dialog.dismiss()

    def show_time_picker(self):
        self.time_dialog = MDTimePicker()
        self.time_dialog.bind(on_save=self.get_time_save)
        self.time_dialog.open()

    def get_time_save(self, instance, value):
        self.ids.time_text_field.text = str(value)

    def on_time_save(self, instance, time):
        self.ids.time_text_field = str(time)

    # textfield functions
    def get_year(self):
        year_list.append(date_list[-1][0:4])

    def on_schedule_save(self):
        self.save_dialog = MDDialog(
            title='Save Schedule',
            text='Please check all the fields before sending. This can no longer be undone.\nAre you sure?',
            type='simple',
            buttons=[
                MDFlatButton(
                    text='Save',
                    font_style='Button',
                    on_release=self.on_save
                ),
                MDFlatButton(
                    text='Cancel',
                    font_style='Button',
                    on_release=self.on_sched_dialog_dismiss
                )
            ]
        )
        if self.ids.preachers.disabled == False:
            self.save_dialog.open()
        else:
            self.save_dialog.disabled = True

    def on_check_text(self, text_input):
        if self.ids.event.text != '' and self.ids.months.text != '' and self.ids.preachers.text != '' \
                and self.ids.date_text_field.text != '' and self.ids.time_text_field.text != '' \
                and self.ids.topic.text != '' and self.ids.sub_preachers.text != '' \
                and self.ids.opening_prayer.text != '' and self.ids.scripture_reading.text != '' \
                and self.ids.offertory.text != '' and self.ids.closing_prayer.text != '':
            self.ids.save_button.disabled = False

    def save_button_change(self):
        self.ids.save_button.text = 'Saved'
        self.ids.save_button.md_bg_color = 254 / 255, 215 / 255, 46 / 255, 1

    def on_sched_dialog_dismiss(self, button):
        self.save_dialog.dismiss()

    def for_sending(self):
        send_list = (month_list[0], event_list[0], sched_counter, date_list[0], time_list[0], year_list[0],
                     preachers_list[0], sub_preacher_list[0], topic_list[0], topic_details_list[0], \
                     event_details_list[0], opening_prayer_list[0], scripture_reading_list[0], offertory_list[0], \
                     closing_prayer_list[0], event_organizer_list[0], event_contact_list[0], status[0])

        TO_SEND.append(send_list)

    def clear_list(self):
        month_list.clear()
        event_list.clear()
        preachers_list.clear()
        date_list.clear()
        time_list.clear()
        year_list.clear()
        sub_preacher_list.clear()
        topic_list.clear()
        topic_details_list.clear()
        event_details_list.clear()
        opening_prayer_list.clear()
        scripture_reading_list.clear()
        offertory_list.clear()
        closing_prayer_list.clear()
        event_organizer_list.clear()
        event_contact_list.clear()
        status.clear()

    def disable_fields(self):
        self.ids.months_drop_down.disabled = True
        self.ids.event.disabled = True
        self.ids.preachers.disabled = True
        self.ids.preachers_drop_down.disabled = True
        self.ids.date_text_button.disabled = True
        self.ids.time_text_button.disabled = True
        self.ids.topic.disabled = True
        self.ids.topic_details.disabled = True
        self.ids.sub_preachers.disabled = True
        self.ids.sub_drop_down.disabled = True
        self.ids.opening_prayer.disabled = True
        self.ids.scripture_reading.disabled = True
        self.ids.offertory.disabled = True
        self.ids.closing_prayer.disabled = True
        self.ids.event_details.disabled = True
        self.ids.event_organizer.disabled = True
        self.ids.event_contact.disabled = True

    def on_save(self, button):
        global sched_counter
        self.save_dialog.dismiss()

        month_list.append(self.ids.months.text)
        event_list.append(self.ids.event.text)
        preachers_list.append(self.ids.preachers.text)
        date_list.append(self.ids.date_text_field.text)
        time_list.append(self.ids.time_text_field.text)
        self.get_year()

        topic_list.append(self.ids.topic.text)

        sub_preacher_list.append(self.ids.sub_preachers.text)
        opening_prayer_list.append(self.ids.opening_prayer.text)
        scripture_reading_list.append(self.ids.scripture_reading.text)
        offertory_list.append(self.ids.offertory.text)
        closing_prayer_list.append(self.ids.closing_prayer.text)

        if self.ids.topic_details.text != '':
            topic_details_list.append(self.ids.topic_details.text)
        else:
            topic_details_list.append('No details provided.')

        if self.ids.event_details.text != '':
            event_details_list.append(self.ids.event_details.text)
        else:
            event_details_list.append('No details provided.')

        event_organizer_list.append(self.ids.event_organizer.text)
        event_contact_list.append(self.ids.event_contact.text)

        sched_counter += 1

        sched_num_list.append(sched_counter)

        status.append('Pending')

        # Prepare to send
        self.for_sending()

        # clear list
        self.clear_list()

        # disable fields
        self.disable_fields()

        # change button
        self.save_button_change()

        # Toobar button

    def send_dialog_open(self):
        if sched_counter != 0:
            self.dialog.open()
        else:
            self.dialog.disabled = True

    def on_close_dialog(self, button):
        self.dialog.dismiss()

    # SEND BUTTON
    def on_send_press(self, obj):
        self.on_close_dialog(self)

        Connection().on_events_send(TO_SEND)
        self.send_status()

    def send_status(self):
        self.send_dialog = MDDialog(
            title='Sent',
            type='simple',
            size_hint=(.45, None),
            buttons=[
                MDFlatButton(
                    text='Okay',
                    font_style='Button',
                    on_release=self.send_spinner_close
                )
            ]
        )

        self.send_dialog.open()

    def send_spinner_close(self, button):
        self.send_dialog.dismiss()