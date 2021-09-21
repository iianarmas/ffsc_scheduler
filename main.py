"""from kivy.config import Config

Config.set('graphics', 'width', '400')
Config.set('graphics', 'height', '740')"""

#from kivy.core.window import Window
from kivy.uix.screenmanager import ScreenManager
from kivymd.app import MDApp
#from kivy.lang import Builder
#from kivymd.uix import dialog
#from kivymd.uix.dialog import MDDialog
#from kivymd.uix.screen import MDScreen
from kivymd.uix.card import MDCard
#from kivy.metrics import dp, sp
#from kivy.properties import StringProperty, NumericProperty, BooleanProperty, ObjectProperty
from kivymd.uix.list import MDList, OneLineListItem
from kivymd.uix.snackbar import Snackbar
#from threading import *
from time import *
from kivy.clock import *
#from kivymd.uix.menu import MDDropdownMenu
from create_new import *
from kivymd.uix.spinner import MDSpinner
#from kivy.uix.boxlayout import BoxLayout
from connection import *
#from kivy.uix.scrollview import ScrollView
#from kivy.logger import Logger

from jnius import autoclass
from android.runnable import run_on_ui_thread

Color = autoclass("android.graphics.Color")
WindowManager = autoclass('android.view.WindowManager$LayoutParams')
activity = autoclass('org.kivy.android.PythonActivity').mActivity


screen_manager = ScreenManager()

date_now = datetime.now()

formatted_date = date_now.strftime('%Y-%m-%d')

title_list = []
body_list = []

Builder.load_file('contentscreen.kv')



class PreSplashScreen(MDScreen):
    def __init__(self, **kw):
        super().__init__(**kw)
        self.account_create = MDDialog(
                title='Creating',
                type='custom',
                content_cls=MySpinner()
            )

        self.account_created = MDDialog(
                title='Account Created!',
                text='Redirecting...',
                type='custom'
            )

    def create(self):
        self.account_create.open()
        Clock.schedule_once(self.create_dismiss, 5)
        Clock.schedule_once(self.created, 5)
        Clock.schedule_once(self.created_dismiss, 8.5)
        Clock.schedule_once(self.switch, 8.5)

    def create_dismiss(self, obj):
        self.account_create.dismiss()


    def created(self, obj):
        self.account_created.open()

    def created_dismiss(self, obj):
        self.account_created.dismiss()


    def switch(self, obj):
        screen_manager.switch_to(LoginScreen(name='loginscreen'))


class LoginScreen(MDScreen):

    def on_enter_button(self):
        # screen_manager.add_widget((HomeScreen(name='homescreen')))
        self.redirect = MDDialog(
                title='Redirecting...',
                type='custom',
                content_cls=MySpinner()
            )

        self.redirect.open()
        Clock.schedule_once(self.redirect_dismiss, 5)
        Clock.schedule_once(self.switch, 5)

    def redirect_dismiss(self, obj):
        self.redirect.dismiss()

    def switch(self, obj):
        screen_manager.switch_to(HomeScreen())

class HomeScreen(MDScreen):
    goal_title = connect.goal()[0]
    goal_body = connect.goal()[1]

    verse_title = connect.memory_verse()[0]
    verse_body = connect.memory_verse()[1]

    announcement_title = connect.announcements()[0].upper()
    announcement_body = connect.announcements()[1]
    announcement_date = connect.announcements()[2]

    CREATE = ['Main Service', 'Outreach Service', 'Event', 'Goal', 'Announcement']

    month = date_now.strftime('%B')
    year = date_now.year
    schedule_label = f'{month} {year}'

    def __init__(self):
        super(HomeScreen, self).__init__()
        # screen_manager.add_widget(MainContent())
        # screen_manager.add_widget(EventContent())

        self.create_menu_items = [{
            'viewclass': 'OneLineListItem',
            'divider': None,
            'text': i,
            'height': len(self.CREATE) * dp(10),
            'on_release': lambda x=i: self.create_new_callback(x),
        } for i in self.CREATE
        ]
        self.create_new_menu = MDDropdownMenu(
            items=self.create_menu_items,
            width_mult=2.7
        )

        # Goal Creation Dialog
        self.create_goal_dialog = MDDialog(
            title='Create New Goal',
            type='custom',
            content_cls=GoalContent(),
            buttons=[
                MDFlatButton(text='Save', font_style='Button', on_release=self.on_goal_send),
                MDFlatButton(text='Cancel', font_style='Button', on_release=self.on_goal_cancel)
            ],
            auto_dismiss=False
        )

        # Announcement Creation Dialog
        self.create_announcement_dialog = MDDialog(
            title='Create New Announcement',
            type='custom',
            content_cls=AnnouncementContent(),
            buttons=[
                MDFlatButton(text='Save', font_style='Button', on_release=self.on_announcement_send),
                MDFlatButton(text='Cancel', font_style='Button', on_release=self.on_announcement_cancel)
            ],
            auto_dismiss=False
        )

    # "Create" Menu
    def create_new(self, button):
        self.create_new_menu.caller = button
        self.create_new_menu.open()

    def create_new_callback(self, text_item):
        self.create_new_menu.dismiss()
        if text_item == self.CREATE[0]:
            screen_manager.switch_to(MainServiceCreate(), direction='left')
        elif text_item == self.CREATE[1]:
            screen_manager.switch_to(OutreachServiceCreate(), direction='left')
        elif text_item == self.CREATE[2]:
            screen_manager.switch_to(EventServiceCreate(), direction='left')
        elif text_item == self.CREATE[3]:
            self.create_goal_dialog.open()
        else:
            self.create_announcement_dialog.open()

    # goal dialog fxns
    def on_goal_send(self, button):
        if len(title_list) != 0 and len(body_list) != 0:
            Connection().on_goal_send(title_list[-1], body_list[-1], formatted_date)
            title_list.clear()
            body_list.clear()
            Snackbar(text='Done', duration=0.5).open()
            self.create_goal_dialog.dismiss()
        else:
            Snackbar(text='You must fill all the fields.', duration=0.5).open()

    def on_goal_cancel(self, button):
        self.create_goal_dialog.dismiss()

    # announcement dialog fxns
    def on_announcement_send(self, button):
        if len(title_list) != 0 and len(body_list) != 0:
            Connection().on_announcement_send(title_list[-1], body_list[-1], formatted_date)
            title_list.clear()
            body_list.clear()
            Snackbar(text='Done', duration=0.5).open()
            self.create_announcement_dialog.dismiss()
        else:
            Snackbar(text='You must fill all the fields.', duration=0.5).open()

    def on_announcement_cancel(self, button):
        self.create_announcement_dialog.dismiss()

    # goal button press
    def on_goal_press(self):
        self.goal_dialog = MDDialog(
            title=self.goal_title,
            text=self.goal_body,
            type='custom',
            size_hint_x=0.8,
            padding='24dp',
            auto_dismiss=False,
            buttons=[
                MDFlatButton(
                    text='Okay',
                    font_style='Button',
                    on_release=self.on_goal_dismiss
                )
            ]
        )
        self.goal_dialog.open()

    def on_goal_dismiss(self, button):
        self.goal_dialog.dismiss()

    # memory verse card press
    def on_memory_verse_press(self):
        self.memory_dialog = MDDialog(
            title=self.verse_title,
            text=self.verse_body,
            size_hint_x=0.8,
            type='custom',
            padding='24dp',
            auto_dismiss=False,
            buttons=[
                MDFlatButton(
                    text='Okay',
                    font_style='Button',
                    on_release=self.on_memory_dismiss
                )
            ]
        )
        self.memory_dialog.open()

    def on_memory_dismiss(self, button):
        self.memory_dialog.dismiss()

    # announcent card press
    def on_announcement_press(self):
        self.announcement_dialog = MDDialog(
            title=self.announcement_title,
            text=self.announcement_body,
            type='custom',
            size_hint_x=0.8,
            padding='24dp',
            auto_dismiss=False,
            buttons=[
                MDFlatButton(
                    text='Okay',
                    font_style='Button',
                    on_release=self.on_announcement_dismiss
                )
            ]
        )
        self.announcement_dialog.open()

    def on_announcement_dismiss(self, button):
        self.announcement_dialog.dismiss()


class GoalContent(MDBoxLayout):
    Window.keyboard_anim_args = {'d': 0.2, 't': 'in_out_expo'}
    Window.softinput_mode = 'below_target'

    def goal_text(self):
        global title_list

        title_list.clear()
        title_list.append(self.ids.goal_title.text)

    def goal_body_text(self):
        global body_list

        body_list.clear()
        body_list.append(self.ids.goal_body.text)


class AnnouncementContent(MDBoxLayout):
    Window.keyboard_anim_args = {'d': 0.2, 't': 'in_out_expo'}
    Window.softinput_mode = 'below_target'

    def announcement_text(self):
        global title_list

        title_list.clear()
        title_list.append(self.ids.announcement_title.text)

    def announcement_body(self):
        global body_list

        body_list.clear()
        body_list.append(self.ids.announcement_body.text)


# main content view
class MainContent(MDScreen):
    title = StringProperty('Main Schedule')

    def on_pre_enter(self, *args):
        self.dialog = MDDialog(
            title='Please Wait...',
            type='simple',
            size_hint=(.45, None),

        )
        self.dialog.open()

    def on_enter(self):
        SCHEDULE = connect.get_latest_main_service()

        for i in range(SCHEDULE[0]):
            self.ids.schedules.add_widget(ScheduleViewCard(
                preacher_name=SCHEDULE[6][i],
                date=str(SCHEDULE[3][i]),
                time=str(SCHEDULE[4][i]),
                year=str(SCHEDULE[5][i]),
                topic=SCHEDULE[8][i],
                topic_details=SCHEDULE[9][i],
                substitute_preacher=SCHEDULE[7][i],
                opening_prayer=SCHEDULE[12][i],
                scripture_reading=SCHEDULE[13][i],
                offertory=SCHEDULE[14][i],
                closing_prayer=SCHEDULE[15][i],
                event=SCHEDULE[10][i],
                event_details=SCHEDULE[11][i],
                status=SCHEDULE[16][i]
            ))

        self.dialog.dismiss()

    def on_pre_leave(self, *args):
        self.ids.schedules.clear_widgets()


# outreach content view
class OutreachContent(MDScreen):
    title = StringProperty('')

    outreach = StringProperty('')

    def on_pre_enter(self, *args):
        self.dialog = MDDialog(
            title='Please Wait...',
            type='simple',
            size_hint=(.45, None),
        )
        self.dialog.open()

    def on_enter(self):
        SCHEDULE = connect.get_latest_outreach_service(self.outreach)

        for i in range(SCHEDULE[0]):
            self.ids.schedules.add_widget(ScheduleViewCard(
                preacher_name=SCHEDULE[7][i],
                date=str(SCHEDULE[4][i]),
                time=str(SCHEDULE[5][i]),
                year=str(SCHEDULE[6][i]),
                topic=SCHEDULE[9][i],
                topic_details=SCHEDULE[10][i],
                substitute_preacher=SCHEDULE[8][i],
                opening_prayer=SCHEDULE[13][i],
                scripture_reading=SCHEDULE[14][i],
                offertory=SCHEDULE[15][i],
                closing_prayer=SCHEDULE[16][i],
                event=SCHEDULE[11][i],
                event_details=SCHEDULE[12][i],
                status=SCHEDULE[17][i]
            ))

        self.dialog.dismiss()

    def on_pre_leave(self, *args):
        self.ids.schedules.clear_widgets()


# Dialog Outreach Selection
class OutreachDialogContent(MDBoxLayout):
    OUTREACH_NAMES = connect.get_outreach_names()

    def __init__(self):
        super(OutreachDialogContent, self).__init__()

        self.container = self.ids.container_list

        for i in self.OUTREACH_NAMES:
            self.container.add_widget(OneLineListItem(text=i, divider=None,
                                                      on_release=self.on_outreach_select))

    def on_outreach_select(self, text_item):

        for i in self.OUTREACH_NAMES:

            if text_item.text == i:
                screen_manager.add_widget(OutreachContent())
                screen_manager.switch_to(OutreachContent(
                    title=f'{i} Outreach Schedule',
                    outreach=i),
                    direction='left')


# events content view
class EventContent(MDScreen):
    title = StringProperty('Events Schedule')

    def on_pre_enter(self, *args):
        self.dialog = MDDialog(
            title='Please Wait...',
            type='simple',
            size_hint=(.45, None),
        )
        self.dialog.open()

    def on_enter(self):
        SCHEDULE = connect.get_latest_events()

        for i in range(SCHEDULE[0]):
            self.ids.schedules.add_widget(EventScheduleViewCard(
                preacher_name=SCHEDULE[7][i],
                date=str(SCHEDULE[4][i]),
                time=str(SCHEDULE[5][i]),
                year=str(SCHEDULE[6][i]),
                topic=SCHEDULE[9][i],
                topic_details=SCHEDULE[10][i],
                substitute_preacher=SCHEDULE[8][i],
                opening_prayer=SCHEDULE[12][i],
                scripture_reading=SCHEDULE[13][i],
                offertory=SCHEDULE[14][i],
                closing_prayer=SCHEDULE[15][i],
                event=SCHEDULE[2][i],
                event_details=SCHEDULE[11][i],
                event_organizer=SCHEDULE[16][i],
                event_contact=SCHEDULE[17][i],
                status=SCHEDULE[18][i]
            ))

        self.dialog.dismiss()

    def on_pre_leave(self, *args):
        self.ids.schedules.clear_widgets()


# schedules on main and outreach view
class ScheduleViewCard(MDCard):
    preacher_name = StringProperty('')
    date = StringProperty('')
    time = StringProperty('')
    year = StringProperty('')
    topic = StringProperty('')
    topic_details = StringProperty('')
    substitute_preacher = StringProperty('')
    opening_prayer = StringProperty('')
    scripture_reading = StringProperty('')
    offertory = StringProperty('')
    closing_prayer = StringProperty('')
    event = StringProperty('')
    event_details = StringProperty('')
    status = StringProperty('')


# event schedules on main and outreach view
class EventScheduleViewCard(MDCard):
    event_name = StringProperty('')
    preacher_name = StringProperty('')
    date = StringProperty('')
    time = StringProperty('')
    year = StringProperty('')
    topic = StringProperty('')
    topic_details = StringProperty('')
    substitute_preacher = StringProperty('')
    opening_prayer = StringProperty('')
    scripture_reading = StringProperty('')
    offertory = StringProperty('')
    closing_prayer = StringProperty('')
    event = StringProperty('')
    event_details = StringProperty('')
    event_organizer = StringProperty('')
    event_contact = StringProperty('')
    status = StringProperty('')


class MySpinner(MDBoxLayout):
    pass



# Main
class FaithSchedulerApp(MDApp):
    back_button_counter = NumericProperty(0)

    def __init__(self, **kwargs):
        super(FaithSchedulerApp, self).__init__(**kwargs)
        self.outreach_dialog = MDDialog()

    def build(self):

        Window.bind(on_keyboard=self.key_input)

        if screen_manager.current == 'loginscreen':
            StatusBarColor().statusbar('#FFFFFF')
        else:
            StatusBarColor().statusbar('#5D15FE')

        # self.theme_cls.primary_palette = 'Purple'
        Builder.load_file('mainscreen.kv')

        screen_manager.add_widget((PreSplashScreen()))

        # screen_manager.add_widget(MainServiceCreate())

        self.screens = [PreSplashScreen(), HomeScreen()]

        return screen_manager

    # main content call1
    def on_main_card_press(self):

        screen_manager.switch_to(MainContent(), direction='left')

    # outreach dialog content call
    def on_outreach_card_press(self):

        self.outreach_dialog = MDDialog(
            title='Select Outreach',
            type='custom',
            content_cls=OutreachDialogContent()
        )

        self.outreach_dialog.open()

    # outreach dialog dismiss
    def on_outreach_dialog_close(self):
        self.outreach_dialog.dismiss()

    # events content call
    def on_event_card_press(self):

        screen_manager.switch_to(EventContent(), direction='left')

    # back button
    def home_screen(self):
        screen_manager.switch_to(self.screens[1], direction='right')

    # Android back button
    def key_input(self, window, key, scancode, codepoint, modifier):
        if key == 27:
            if screen_manager.current == 'loginscreen' or self.back_button_counter == 1:
                self.stop()
            else:
                screen_manager.switch_to(self.screens[1], direction='right')
                Snackbar(text='Press back twice to exit.', duration=0.5).open()
                self.back_button_counter += 1
                Clock.schedule_once(self.reset_back_button_counter, 0.5)
            return True
        else:
            return False

    def reset_back_button_counter(self, *args):
        self.back_button_counter = 0


class StatusBarColor:
    @run_on_ui_thread
    def statusbar(self,color):
        window = activity.getWindow()
        window.clearFlags(WindowManager.FLAG_TRANSLUCENT_STATUS)
        window.addFlags(WindowManager.FLAG_DRAWS_SYSTEM_BAR_BACKGROUNDS)
        window.setStatusBarColor(Color.parseColor(color)) 
        window.setNavigationBarColor(Color.parseColor(color))

if __name__ == '__main__':
    FaithSchedulerApp().run()
