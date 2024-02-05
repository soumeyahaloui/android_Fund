from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.image import Image
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.graphics import Color, Rectangle, RoundedRectangle
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.dropdown import DropDown
from kivy.network.urlrequest import UrlRequest
from kivy.uix.boxlayout import BoxLayout
import json
from kivy.uix.scrollview import ScrollView
from kivy.core.window import Window
import logging
import traceback
from kivy.loader import Loader
from kivy.uix.image import AsyncImage
from kivy.clock import Clock
from kivy.metrics import dp
from kivymd.app import MDApp
from kivymd.uix.textfield import MDTextField
from kivymd.uix.button import MDRaisedButton
from kivy.lang import Builder
from kivymd.uix.button import MDFloatingActionButton
from kivy.uix.behaviors import ButtonBehavior
from kivy.graphics import Line
from kivy.core.text import LabelBase
from arabic_reshaper import reshape
from bidi.algorithm import get_display
from kivymd.uix.button import MDIconButton
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.button import MDFlatButton
from kivymd.icon_definitions import md_icons
from kivymd.uix.list import OneLineIconListItem
import json
from kivymd.uix.dialog import MDDialog
from kivymd.uix.datatables import MDDataTable
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.label import MDLabel
import requests


alpha_value = 0.5  
reshaped_text = reshape('تسجيل')
bidi_text = get_display(reshaped_text)

class PlanetButton(ButtonBehavior, Image):
    border_width = 3.5  

    def __init__(self, **kwargs):
        self.text_label = Label(text='', font_name='DejaVuSans', font_size='15sp')
        super(PlanetButton, self).__init__(**kwargs)
        self.add_widget(self.text_label)
        self.always_release = True
        self.keep_ratio = True
        self.allow_stretch = True
        self.source = './res/fdr.png'  
        
        Clock.schedule_once(self.init_graphics, 0)

    def init_graphics(self, *args):
    
        if getattr(self.canvas, 'before', None):
            self.canvas.before.clear()
            with self.canvas.before:
                
                Color(0, 0, 0, 1)  
                
                self.border = Line(ellipse=(self.x, self.y, self.width, self.height), width=self.border_width)
        self.update_text_label()

    def update_text_label(self):
        self.text_label.size = self.size
        self.text_label.pos = self.pos
        self.text_label.text =''


    def on_size(self, *args):
        self.init_graphics()
        self.update_text_label()


    def on_pos(self, *args):
        self.init_graphics()
        self.update_text_label()

    def on_press(self):
        
        pass

    def on_release(self):
        
        pass


class LabelB(Label):
    def __init__(self, **kwargs):
        self.bg_color = kwargs.pop(
            'bg_color', (1, 1, 1, 1))  
        super(LabelB, self).__init__(**kwargs)
        with self.canvas.before:
            Color(*self.bg_color)
            self.rect = Rectangle(pos=self.pos, size=self.size)
        self.bind(pos=self.update_rect, size=self.update_rect)

    def update_rect(self, *args):
        self.rect.pos = self.pos
        self.rect.size = self.size


class FirstScreen(Screen):
    def __init__(self, **kwargs):
        super(FirstScreen, self).__init__(**kwargs)

        bg = AsyncImage(source='https://cdn.glitch.global/53883c99-cc30-4656-9386-14bc8357b85c/fundra.png?v=1706453653572',
                allow_stretch=True,
                keep_ratio=False)
        self.add_widget(bg)

        
        layout = FloatLayout()
        self.add_widget(layout)

     
        donate_button = Button(
            text="Donate",
            font_size="20sp",
            background_color=(0.2, 0.5, 0.8, 1),  
            color=(1, 1, 1, 1),  
            size_hint=(None, None),
            size=(200, 60),
            pos_hint={'center_x': 0.5, 'center_y': 0.2}
        )

        
        donate_button.size_hint = (0.5, None)
        donate_button.height = '48dp'
        donate_button.pos_hint = {'center_x': 0.5, 'y': 0.1}

        donate_button.bind(on_press=self.go_to_second_screen)
        layout.add_widget(donate_button)

        login_signup_button = PlanetButton(
            size_hint=(None, None),
            size=(dp(56), dp(56)),  
            pos_hint={'center_x': 0.1, 'center_y': 0.06}
        )
        login_signup_button.bind(on_press=self.show_user_options)
        layout.add_widget(login_signup_button)

        self.planet_button = login_signup_button


    def show_user_options(self, instance):
        app = MDApp.get_running_app()
        if app.is_logged_in():
            self.show_logout_option(instance)
        else:
            self.show_login_signup_options(instance)

    def show_logout_option(self, instance):
        logout_menu_items = [
            {
                'text': 'Log Out',
                'viewclass': 'OneLineListItem',
                'on_release': lambda x='Log Out': self.logout_user(x)
            }
        ]

        self.logout_menu = MDDropdownMenu(
            caller=self.planet_button,
            items=logout_menu_items,
            position="auto",
            width_mult=4,
        )

        self.logout_menu.open()

    def logout_user(self, text_item):
        self.logout_menu.dismiss()
        if text_item == 'Log Out':
            
            app = MDApp.get_running_app()
            app.logout_user()

    def show_login_signup_options(self, instance):
        content = BoxLayout(orientation='vertical', padding=10, spacing=10, size_hint_y=None)
        
        content.height = dp(100)  

        login_btn = MDRaisedButton(text="Login", size_hint=(1, None), height=dp(40))
        signup_btn = MDRaisedButton(text="Signup", size_hint=(1, None), height=dp(40))
        
        content.add_widget(login_btn)
        content.add_widget(signup_btn)

        popup = Popup(content=content, size_hint=(None, None), size=(300, content.height), title_size=0)
        login_btn.bind(on_press=lambda x: self.go_to_login(popup))
        signup_btn.bind(on_press=lambda x: self.go_to_signup(popup))
        popup.open()

    def go_to_login(self, popup):
        popup.dismiss()
        self.manager.current = 'login'

    def go_to_signup(self, popup):
        popup.dismiss()
        self.manager.current = 'signup'

    def is_logged_in(self):
        logout_menu_items = [
            {
                'text': 'Log Out',
                'viewclass': 'OneLineListItem',
                'on_release': lambda x='Log Out': self.logout_user(x)
            }
        ]

        self.logout_menu = MDDropdownMenu(
            caller=self.planet_button,
            items=logout_menu_items,
            position="auto",
            width_mult=4,
        )

        self.logout_menu.open()

    def logout_user(self, text_item):
        self.logout_menu.dismiss()
        if text_item == 'Log Out':
            
            app = MDApp.get_running_app()
            app.logout_user()

    def show_login_signup_options(self):
        content = BoxLayout(orientation='vertical', padding=10, spacing=10, size_hint_y=None)
        
        content.height = dp(100)  

        login_btn = MDRaisedButton(text="Login", size_hint=(1, None), height=dp(40))
        signup_btn = MDRaisedButton(text="Signup", size_hint=(1, None), height=dp(40))
        
        content.add_widget(login_btn)
        content.add_widget(signup_btn)

        popup = Popup(content=content, size_hint=(None, None), size=(300, content.height), title_size=0)
        login_btn.bind(on_press=lambda x: self.go_to_login(popup))
        signup_btn.bind(on_press=lambda x: self.go_to_signup(popup))
        popup.open()


    def go_to_login(self, popup):
        popup.dismiss()
        self.manager.current = 'login'

    def go_to_signup(self, popup):
        popup.dismiss()
        self.manager.current = 'signup'

    def go_to_second_screen(self, instance):
        app = MDApp.get_running_app()

        # Check if the user is logged in before navigating to the second screen
        if app.is_logged_in():
            self.manager.current = 'second'
        else:
            self.show_login_signup_options()

    def is_logged_in(self):
        try:
            with open('login_state.json', 'r') as file:
                state = json.load(file)
                return state.get('logged_in', False)
        except (FileNotFoundError, json.JSONDecodeError):
            return False

class SecondScreen(Screen):
    def __init__(self, **kwargs):
        super(SecondScreen, self).__init__(**kwargs)

        self.widget_dict = {}  
        self.counters = {}  
        self.widget_ids = {}  

        self.fetch_data()
        self.available_frames = []
        self.processed_sets = []  

        self.next_index = 1
        self.last_fetched_family_id = 4  
        
        self.frame_data_map = {i: i for i in range(1, 5)}

        bg = AsyncImage(source='https://cdn.glitch.global/53883c99-cc30-4656-9386-14bc8357b85c/fundd.png?v=1706210860343',
                allow_stretch=True,
                keep_ratio=False)
        self.add_widget(bg)

        self.cols = 2  
        self.rows = 2  
        
        
        screen_width, screen_height = Window.size
        column_width = screen_width / self.cols
        row_height = screen_height / self.rows
        

        layout = GridLayout(cols=self.cols, spacing=dp(10), padding=dp(10), size_hint=(1, None))
        layout.bind(minimum_height=layout.setter('height'))
        self.add_widget(layout)

        
        layout.spacing = dp(2)
        layout.padding = dp(2)


        
        for i in range(1, 5):
            self.counters[f'counter_{i}'] = 0  

            framed_layout = FloatLayout(size_hint=(None, None), size=(
                column_width, row_height))  
            
            self.add_black_frame(framed_layout)

            image_layout = FloatLayout(size_hint=(1, 1), pos_hint={
                                       'center_x': 0.5, 'center_y': 0.5})

            top_text = LabelB(
                text='',
                bg_color=(0.2, 0.5, 0.8, 1),  
                color=(1, 1, 1, 1),  
                font_size='20sp',  
                bold=True,  
                size_hint=(None, None),
                size=(200, 50),
                pos_hint={'center_x': 0.5, 'top': 1},
                halign="center",  
                valign="middle"  
            )

            
            top_text.size_hint = (0.8, None)  
            top_text.height = dp(30)  
            top_text.pos_hint = {'center_x': 0.5, 'top': 0.99}  

            
            top_text.bind(size=top_text.setter('text_size'))
            self.widget_ids[f'top_text_{i}'] = top_text  
            image_layout.add_widget(top_text)

            
            image = AsyncImage(source='', size_hint=(0.8, 0.3), allow_stretch=True)
            image.pos_hint = {'center_x': 0.5, 'center_y': 0.5}
            self.widget_ids[f'image_{i}'] = image  
            image_layout.add_widget(image)

            
            image.size_hint = (0.8, 0.3)  
            image.allow_stretch = True  
            image.pos_hint = {'center_x': 0.5, 'center_y': 0.7}  

            
            button_container = GridLayout(rows=1, size_hint=(None, None),size=(200, 50),  
                pos_hint={'center_x': 0.5, 'y': 0.27}
            )
            
            button_container.size_hint = (0.8, None)
            button_container.height = dp(40)
            button_container.padding = [dp(2)] * 4  

            custom_amount_input = TextInput(
                hint_text='Enter Num',
                
                hint_text_color=[0.5, 0.5, 0.5, 1],
                multiline=False,
                size_hint=(None, None),
                size=(140, 50),
                pos_hint={'center_x': 0.4, 'y': 0.2}
            )

            for amount in ["1", "5", "50", "100"]:
                button = Button(text=amount, size_hint=(None, 1), width=dp(48))  
                button.bind(on_press=self.create_button_callback(amount, f'counter_{i}', custom_amount_input))
                button_container.add_widget(button)

            
            for button in button_container.children:
                button.size_hint_x = 1 / len(button_container.children)
                
            
            button.size_hint = (1 / len(button_container.children), 1)  

            
          
            
            custom_amount_input.size_hint = (0.6, None)
            custom_amount_input.height = dp(40)  
            custom_amount_input.pos_hint = {'center_x': 0.4, 'y': 0.4}

            self.widget_dict[f'custom_amount_{i}'] = custom_amount_input
            image_layout.add_widget(custom_amount_input)

            
            submit_button = Button(
                text="Sub",
                size_hint=(None, None),
                
                size=(60, 50), pos_hint={'x': custom_amount_input.pos_hint['center_x'] + 0.35, 'y': 0.2}

            )
            
            submit_button.size_hint = (0.2, None)
            submit_button.height = dp(40)  
            submit_button.pos_hint = {'right': custom_amount_input.pos_hint['center_x'] + 0.5, 'y': 0.4}
            
            submit_button.bind(on_press=lambda instance, x=custom_amount_input, counter_key=f'counter_{i}':
                               self.show_confirmation_from_input(x, counter_key))

            image_layout.add_widget(submit_button)

            
            
            

            image_layout.add_widget(button_container)
            
            bottom_text = Label(
                text=f'Bottom {i}',
                size_hint=(None, None),
                size=(200, 50),
                pos_hint={'center_x': 0.5, 'y': 0}
            )
            
            
            bottom_text.size_hint = (0.8, None)
            bottom_text.height = dp(30)  
            bottom_text.pos_hint = {'center_x': 0.5, 'y': 0.17}

            self.add_frame(bottom_text)
            image_layout.add_widget(bottom_text)
            self.widget_dict[f'bottom_text_{i}'] = bottom_text

            framed_layout.add_widget(image_layout)
            layout.add_widget(framed_layout)
        
        
        menu_button = Button(
            text='Menu',
            size_hint=(None, None),
            size=(100, 50),
            pos_hint={'center_x': 0.5, 'y': 0}
        )

        
        menu_button.size_hint = (0.5, None)
        menu_button.height = dp(40)  
        menu_button.pos_hint = {'center_x': 0.5, 'bottom': 1}

        menu_button.bind(on_release=self.open_menu)
        self.add_widget(menu_button)
        
        
        self.planet_button = PlanetButton(
            size_hint=(None, None),
            size=(dp(40), dp(40)),  
            pos_hint={'center_x': 0.1, 'center_y': 0.04}
        )
        self.add_widget(self.planet_button)
        self.planet_button.bind(on_release=self.show_user_options)
    
    def show_user_options(self, instance):
        app = MDApp.get_running_app()
        if app.is_logged_in():
            self.show_logout_option(instance)
        else:
            self.show_login_signup_options(instance)

    def show_logout_option(self, instance):
        logout_menu_items = [
            {
            'text': 'Profile',  # New option for the logged-in user
            'viewclass': 'OneLineListItem',
            'on_release': lambda x='Profile': self.view_profile(x)
        },
            {
                'text': 'Log Out',
                'viewclass': 'OneLineListItem',
                'on_release': lambda x='Log Out': self.logout_user(x)
            }
        ]

        self.logout_menu = MDDropdownMenu(
            caller=self.planet_button,
            items=logout_menu_items,
            position="auto",
            width_mult=4,
        )

        self.logout_menu.open()

    def view_profile(self, text_item):
        self.logout_menu.dismiss()
        if text_item == 'Profile':
            # Add the logic to navigate to the profile screen or perform any profile-related actions
            self.manager.current = 'profile'


    def logout_user(self, text_item):
        self.logout_menu.dismiss()
        if text_item == 'Log Out':
            
            app = MDApp.get_running_app()
            app.logout_user()

    def show_login_signup_options(self, instance):
        content = BoxLayout(orientation='vertical', padding=10, spacing=10, size_hint_y=None)
        
        content.height = dp(100)  

        login_btn = MDRaisedButton(text="Login", size_hint=(1, None), height=dp(40))
        signup_btn = MDRaisedButton(text="Signup", size_hint=(1, None), height=dp(40))
        
        content.add_widget(login_btn)
        content.add_widget(signup_btn)

        popup = Popup(content=content, size_hint=(None, None), size=(300, content.height), title_size=0)
        login_btn.bind(on_press=lambda x: self.go_to_login(popup))
        signup_btn.bind(on_press=lambda x: self.go_to_signup(popup))
        popup.open()

    def go_to_login(self, popup):
        popup.dismiss()
        self.manager.current = 'login'

    def go_to_signup(self, popup):
        popup.dismiss()
        self.manager.current = 'signup'

    def is_logged_in(self):
        logout_menu_items = [
            {
                'text': 'Log Out',
                'viewclass': 'OneLineListItem',
                'on_release': lambda x='Log Out': self.logout_user(x)
            }
        ]

        self.logout_menu = MDDropdownMenu(
            caller=self.planet_button,
            items=logout_menu_items,
            position="auto",
            width_mult=4,
        )

        self.logout_menu.open()

    def logout_user(self, text_item):
        self.logout_menu.dismiss()
        if text_item == 'Log Out':
            
            app = MDApp.get_running_app()
            app.logout_user()

    def go_to_first_screen(self):
        
        self.manager.current = 'first'

    def create_button_callback(self, amt, key, input_field):
        def button_callback(instance):
            self.show_confirmation(amt, key, input_field)
        return button_callback

    def fetch_data(self):
        url = 'https://fund-flask.onrender.com/get_data'
        UrlRequest(url, on_success=self.on_request_success, on_failure=self.on_request_failure, on_error=self.on_request_error, on_redirect=self.on_request_redirect)


    def on_request_failure(self, request, result):
        logging.error("Request failed with result: %s" % result)


    def on_request_redirect(self, request, result):
        logging.info("Request was redirected, final result: %s" % result)


    def on_request_success(self, request, result):
        Clock.schedule_once(lambda dt: self.update_ui_with_data(result))

        logging.info("Request to Flask server successful.")
        logging.info(f"Data received: {result}")

        
        if isinstance(result, list) and len(result) > 0:
            
            self.update_ui_with_data(result)
        else:
            logging.error("Data received is not in the expected format or is empty.")

    def update_ui_with_data(self, data):
    
        if isinstance(data, list) and len(data) > 0:
            for i, data_item in enumerate(data):
                logging.info(f"Updating UI for frame {i+1}")
                
                if i < 4:  
                    image_widget = self.widget_ids.get(f'image_{i+1}')
                    top_text_widget = self.widget_ids.get(f'top_text_{i+1}')

                    if image_widget and 'Image' in data_item:
                        logging.info(f"Setting image source to: {data_item['Image']}")
                        image_widget.source = data_item['Image']
                    if top_text_widget and 'Amount' in data_item:
                        top_text_widget.text = f"Goal: {data_item['Amount']}"
        else:
            logging.error("Data received is not in the expected format or is empty.")



    def open_menu(self, button):
        menu_items = [
            {
                'text': 'Beneficiary',
                'viewclass': 'OneLineIconListItem',  
                'icon': 'account-box',  
                'on_release': lambda x='Beneficiary': self.menu_callback(x)
            },
            {
                'text': 'Main',
                'viewclass': 'OneLineIconListItem',
                'icon': 'home',
                'on_release': lambda x='Main': self.menu_callback(x)
            },
            
        ]


        
        self.menu = MDDropdownMenu(
            caller=button,  
            items=menu_items,
            position="auto",
            width_mult=4,
        )

        self.menu.open()

    def menu_callback(self, text_item):
        if text_item == 'Beneficiary':
            self.go_to_beneficiary()
        elif text_item == 'Main':
            self.go_to_first_screen()
        
        self.menu.dismiss()

    def close_dropdown_and_navigate(self, dropdown, navigation_action):
            """Close dropdown and perform the specified navigation action."""
            dropdown.dismiss()
            navigation_action()

    def go_to_beneficiary(self):
        
        self.manager.current = 'beneficiary'

    def show_confirmation_from_input(self, custom_input, counter_key):
        try:
            amount_text = custom_input.text  
            amount = float(amount_text)  
        except ValueError:
            self.show_error_popup(f"Invalid amount: {amount}Please enter a valid number.")
            return
        
        self.show_confirmation(amount, counter_key, custom_input)

        dialog = MDDialog(
        title="Confirm Donation",
        text=f"Are you sure you want to donate {amount}?",
        buttons=[
            MDFlatButton(
                text="CANCEL",
                on_release=lambda _: dialog.dismiss()  
            ),
            MDFlatButton(
                text="DONATE",
                on_release=lambda _: self.confirm_donation(amount, counter_key, dialog)
            )
        ],
    )
        

    def show_error_popup(self, message):
        content = Label(text=message)
        popup = Popup(title="Error",
                      content=content,
                      size_hint=(None, None), size=(400, 200))
        popup.open()

    
    def add_black_frame(self, widget):
        with widget.canvas.before:
            Color(0.8667, 0.6157, 0.6196, alpha_value)  
            widget.frame = Rectangle(pos=widget.pos, size=widget.size)
        widget.bind(pos=self.update_frame, size=self.update_frame)

    def update_frame(self, instance, value):
        
        instance.frame.pos = (instance.pos[0] - 10, instance.pos[1] - 10)
        
        instance.frame.size = (instance.size[0] + 20, instance.size[1] + 20)

    def add_frame(self, widget):
        
        with widget.canvas.before:
            Color(0.2, 0.5, 0.8, 1)  
            widget.frame = Rectangle(pos=widget.pos, size=widget.size)

        
        widget.bind(pos=self.update_frame, size=self.update_frame)

    def update_frame(self, instance, value):
        instance.frame.pos = instance.pos
        instance.frame.size = instance.size

    def show_confirmation(self, amount, counter_key, custom_input):
        try:
            
            amount = float(amount)
        except ValueError:
            
            self.show_error_popup(f"Invalid amount: {amount}")
            return

        print(f"Showing confirmation for {amount}")  
        
        dialog = MDDialog(
        title="Confirm Donation",
        text=f"Are you sure you want to donate {amount}?",
        buttons=[
            MDFlatButton(text="CANCEL", on_release=lambda x: dialog.dismiss()),
            MDFlatButton(text="DONATE", on_release=lambda x: self.confirm_donation(amount, counter_key, dialog))
        ],
    )
        dialog.open()

    def confirm_donation(self, amount, counter_key, dialog):
        
        amount = float(amount)

        
        top_text_widget = self.widget_ids.get(f'top_text_{counter_key[-1]}')
        if top_text_widget:
            goal_text = top_text_widget.text
            
            try:
                completion_goal = float(goal_text.split(" ")[1])
            except (IndexError, ValueError):
                print("Error extracting goal amount from top_text")
                completion_goal = 0  
        else:
            completion_goal = 0  

        
        print(
            f"Confirming donation: {amount} for {counter_key} with goal {completion_goal}")

        self.update_counter(amount, counter_key)

        if self.counters[counter_key] >= completion_goal:
            print(f"Amount completed for {counter_key}")  
            completed_image_path = self.widget_ids[f'image_{counter_key[-1]}'].source

            completed_set = {
                'Image': completed_image_path,
                
                'Amount': self.counters[counter_key],
                'Details': ''
            }

            self.manager.get_screen(
                'beneficiary').add_completed_set(completed_set)
            self.show_thank_you_popup()

            self.reset_frame(counter_key)
            self.mark_frame_as_available(counter_key)
            frame_number = int(counter_key.split('_')[-1])
            self.fetch_next_family_set(frame_number)

        
        custom_amount_input = self.widget_dict.get(
            f'custom_amount_{counter_key[-1]}')
        if custom_amount_input:
            custom_amount_input.text = ''  

        dialog.dismiss()

    def mark_frame_as_available(self, counter_key):
        
        
        self.available_frames.append(counter_key[-1])  

    def reset_frame(self, counter_key):
        
        image_widget = self.widget_ids.get(f'image_{counter_key[-1]}')
        text_widget = self.widget_ids.get(f'top_text_{counter_key[-1]}')
        bottom_text_widget = self.widget_dict.get(
            counter_key.replace('counter', 'bottom_text'))
        custom_amount_input = self.widget_dict.get(
            f'custom_amount_{counter_key[-1]}')

        if image_widget:
            image_widget.source = ''  
        if text_widget:
            text_widget.text = 'Default Text'  
        if bottom_text_widget:
            bottom_text_widget.text = 'Total: 0.00'  
        if custom_amount_input:
            custom_amount_input.text = ''  

        self.counters[counter_key] = 0

    def update_frame_with_new_data(self, counter_key, data):

        image_widget = self.widget_ids.get(f'image_{counter_key[-1]}')
        top_text_widget = self.widget_ids.get(f'top_text_{counter_key[-1]}')
        bottom_text_widget = self.widget_dict.get(
            counter_key.replace('counter', 'bottom_text'))
        custom_amount_input = self.widget_dict.get(
            f'custom_amount_{counter_key[-1]}')

        if image_widget:
            image_widget.source = data['Image']

        if top_text_widget:
            top_text_widget.text = f"Goal: {data['Amount']}"

        if bottom_text_widget:
            bottom_text_widget.text = 'Total: 0.00'

        if custom_amount_input:
            custom_amount_input.text = ''

        self.counters[counter_key] = 0

        print(f"New family set fetched for frame {counter_key}: {data}")

    def on_request_error(self, request, error):
        logging.error(f"Request to Flask server error: {error}")
        traceback.print_exc()
        print("Error fetching total sets:", error)

    def update_counter(self, value, counter_key):
        self.counters[counter_key] += value
        updated_count = self.counters[counter_key]
        bottom_text_widget = self.widget_dict.get(
            counter_key.replace('counter', 'bottom_text'))
        if bottom_text_widget:
            bottom_text_widget.text = f"Total: {updated_count:.2f}"

    def get_numeric_value(self, text):
        try:
            return int(''.join(filter(str.isdigit, text)))
        except ValueError:
            return 0

    def show_thank_you_popup(self):
        dialog = MDDialog(
        title="Thank You",
        text="Thank you, the amount is completed",
        buttons=[MDFlatButton(text="CLOSE", on_release=lambda x: dialog.dismiss())],
    )
        dialog.open()

    def go_to_beneficiary(self):
        self.manager.current = 'beneficiary'

    def fetch_next_family_set(self, frame_number):
        self.last_fetched_family_id += 1  
        next_family_id = self.last_fetched_family_id

        base_url = 'https://fund-flask.onrender.com/'  

        UrlRequest(f'{base_url}/get_family_data/{next_family_id}', on_success=lambda req, res: self.update_frame_with_new_data(f'counter_{self.available_frames.pop(0)}', res), on_error=self.on_request_error, on_failure=self.on_request_error)
    
    def update_planet_button(self, initial):
        self.planet_button.text_label.text = initial

    def reset_planet_button_label(self):
        self.planet_button.text_label.text = ''

class BeneficiaryScreen(Screen):
    def __init__(self, **kwargs):
        super(BeneficiaryScreen, self).__init__(**kwargs)

        bg = AsyncImage(source='https://cdn.glitch.global/53883c99-cc30-4656-9386-14bc8357b85c/fundd.png?v=1706210860343',
                allow_stretch=True,
                keep_ratio=False)
        self.add_widget(bg)

        scroll_view = ScrollView(size_hint=(
            1, None), size=(Window.width, Window.height))
        self.layout = GridLayout(
            cols=2, spacing=10, padding=10, size_hint_y=None)
        self.layout.bind(minimum_height=self.layout.setter('height'))
        scroll_view.add_widget(self.layout)
        self.add_widget(scroll_view)

        menu_button = Button(text='Menu', size_hint=(None, None), size=(
            100, 50), pos_hint={'center_x': 0.5, 'y': 0})
        menu_button.bind(on_release=self.open_menu)
        self.add_widget(menu_button)

        menu_button = Button(
            text='Menu',
            size_hint=(None, None),
            size=(100, 50),
            pos_hint={'center_x': 0.5, 'y': 0}
        )
        menu_button.bind(on_release=self.open_menu)
        self.add_widget(menu_button)

    def go_to_first_screen(self):
        self.manager.current = 'first'

    def open_menu(self, button):
        menu_items = [
            {
                'text': 'Main',
                'viewclass': 'OneLineIconListItem',
                'icon': 'home',
                'on_release': lambda x='Main': self.menu_callback(x)
            },
            {
                'text': 'Families',
                'viewclass': 'OneLineIconListItem',
                'icon': 'page-next-outline',  
                'on_release': lambda x='Second': self.menu_callback(x)
            },
        ]

        self.menu = MDDropdownMenu(
            caller=button,
            items=menu_items,
            position="auto",
            width_mult=4,
        )

        self.menu.open()

    def close_dropdown_and_navigate(self, dropdown, navigation_action):
        """Close dropdown and perform the specified navigation action."""
        dropdown.dismiss()
        navigation_action()

    def menu_callback(self, text_item):
        if text_item == 'Main':
            self.go_to_main_screen()
        elif text_item == 'Second':
            self.go_to_second_screen()
        self.menu.dismiss()

    def go_to_main_screen(self):
        self.manager.current = 'first'

    def go_to_second_screen(self):
        self.manager.current = 'second'

    def add_completed_set(self, completed_set):
        framed_layout = FloatLayout(size_hint=(None, None), size=(240, 240))
        self.add_black_frame(framed_layout)

        completed_image = AsyncImage(source=completed_set['Image'], size_hint=(
            None, None), size=(200, 200), pos_hint={'center_x': 0.5, 'center_y': 0.65})
        completed_label = Label(
            text=f"Raised: {completed_set['Amount']}",
            size_hint_y=None, height=40, pos_hint={'center_x': 0.5, 'center_y': 0.3})

        framed_layout.add_widget(completed_image)
        framed_layout.add_widget(completed_label)

        self.layout.add_widget(framed_layout)
        self.layout.height = self.layout.minimum_height

    def add_black_frame(self, widget):
        with widget.canvas.before:
            Color(0, 0, 0, 1)  
            widget.frame = Rectangle(pos=widget.pos, size=widget.size)
        widget.bind(pos=self.update_frame, size=self.update_frame)

    def update_frame(self, instance, value):
        instance.frame.pos = (instance.pos[0] - 10, instance.pos[1] - 10)
        instance.frame.size = (instance.size[0] + 20, instance.size[1] + 20)


class SignUpScreen(Screen):
    def __init__(self, **kwargs):
        super(SignUpScreen, self).__init__(**kwargs)

        bg = AsyncImage(source='https://cdn.glitch.global/53883c99-cc30-4656-9386-14bc8357b85c/fundd.png?v=1706210860343',
                allow_stretch=True,
                keep_ratio=False)
        self.add_widget(bg)

        layout = BoxLayout(orientation='vertical', spacing=10, padding=10)

        back_button = MDIconButton(icon='arrow-left', pos_hint={'x': 0, 'top': 1})
        back_button.bind(on_press=self.go_to_first_screen)

        self.username_input = CustomMDTextField(hint_text='Username', multiline=False)
        layout.add_widget(self.username_input)

        self.number_input = CustomMDTextField(hint_text='phone number', multiline=False)
        layout.add_widget(self.number_input)

        self.password_input = CustomMDTextField(hint_text='Password', password=True, multiline=False)
        layout.add_widget(self.password_input)

        self.confirm_password_input = CustomMDTextField(hint_text='Confirm Password', password=True, multiline=False)
        layout.add_widget(self.confirm_password_input)

        signup_button = MDRaisedButton(text='Sign Up', size_hint=(None, None), size=(150, 48))
        signup_button.bind(on_press=self.register_user)
        layout.add_widget(signup_button)
        layout.add_widget(back_button)

        self.add_widget(layout)

    def go_to_first_screen(self, instance):
        self.manager.current = 'first'

    def register_user(self, instance):
        username = self.username_input.text
        number = self.number_input.text
        password = self.password_input.text
        confirm_password = self.confirm_password_input.text

        if password != confirm_password:
            self.show_error_popup("Passwords do not match.")
            return

        signup_data = {'username': username, 'number': number, 'password': password}
        signup_url = 'https://fund-flask.onrender.com/register'
        UrlRequest(signup_url, req_body=json.dumps(signup_data),
                   on_success=self.on_signup_success, on_failure=self.on_signup_failure,
                   method='POST', req_headers={'Content-type': 'application/json'})

    def on_signup_success(self, request, result):
        print("Signup successful:", result)
        self.manager.current = 'second'  

    def on_signup_failure(self, request, result):
        print("Signup failed:", result)

    def show_error_popup(self, message):
        popup_content = Label(text=message)
        popup = Popup(title="Error",
                      content=popup_content,
                      size_hint=(None, None), size=(300, 150))
        popup.open()

class LoginScreen(Screen):
    def __init__(self, **kwargs):
        super(LoginScreen, self).__init__(**kwargs)
        self.user_data = {}  # Initialize user_data as an empty dictionary


        bg = AsyncImage(source='https://cdn.glitch.global/53883c99-cc30-4656-9386-14bc8357b85c/fundd.png?v=1706210860343',
                allow_stretch=True,
                keep_ratio=False)
        self.add_widget(bg)

        login_layout = FloatLayout()

        grid_layout = GridLayout(cols=1, spacing=10, padding=10, size_hint=(None, None), size=(300, 200))
        grid_layout.pos_hint = {'center_x': 0.5, 'center_y': 0.5}

        back_button = MDIconButton(icon='arrow-left', pos_hint={'x': 0, 'top': 1})
        back_button.bind(on_press=self.go_to_first_screen)

        self.username_input = CustomMDTextField(hint_text='Username or Number', multiline=False)
        grid_layout.add_widget(self.username_input)

        self.password_input = CustomMDTextField(hint_text='Password', password=True, multiline=False)
        grid_layout.add_widget(self.password_input)

        login_button = MDRaisedButton(text='Login', size_hint=(None, None), size=(150, 48))
        login_button.bind(on_press=self.login_user)
        
        login_button.pos_hint = {'center_x': 0.5, 'y': 0.1}
        
        login_layout.add_widget(grid_layout)
        login_layout.add_widget(login_button)
        login_layout.add_widget(back_button)

        self.add_widget(login_layout)

    def go_to_first_screen(self, instance):
        self.manager.current = 'first'

    def login_user(self, instance):
        username = self.username_input.text
        password = self.password_input.text
        login_data = {'username': username, 'password': password}
        login_url = 'https://fund-flask.onrender.com/login'
        UrlRequest(login_url, req_body=json.dumps(login_data),
                   on_success=self.on_login_success, on_failure=self.on_login_failure,
                   method='POST', req_headers={'Content-type': 'application/json'})

    def on_login_success(self, request, result):
        print("Login successful:", result)
        user_data = result.get('user', {})

        # Store user data in self.user_data
        self.user_data = user_data
        
        first_initial = user_data.get('username', '')[0].upper() if user_data.get('username') else ''
        self.manager.get_screen('second').update_planet_button(first_initial)
        self.manager.current = 'second'  
        

        # Pass user data to the ProfileScreen and update the UI
        self.update_profile_screen(user_data)

        # Navigate to the ProfileScreen
        # self.manager.current = 'profile'
        self.save_login_state(True)

    def update_profile_screen(self, user_data):
        profile_screen = self.manager.get_screen('profile')
        profile_screen.update_user_profile(user_data)

    def save_login_state(self, logged_in):
        with open('login_state.json', 'w') as file:
            json.dump({'logged_in': logged_in}, file)

    def on_login_failure(self, request, result):
        print("Login failed:", result)

class ProfileScreen(Screen):
    def __init__(self, **kwargs):
        super(ProfileScreen, self).__init__(**kwargs)

        # Set the background image for the profile screen
        bg = AsyncImage(source='https://cdn.glitch.global/53883c99-cc30-4656-9386-14bc8357b85c/fundd.png?v=1706210860343',
                        allow_stretch=True,
                        keep_ratio=False)
        self.add_widget(bg)

        layout = BoxLayout(orientation='vertical')

        self.user_data_label = Label(text="", font_size=20, color=(0, 0, 0, 1))
        layout.add_widget(self.user_data_label)

        back_button = MDIconButton(icon='arrow-left', pos_hint={'x': 0, 'top': 1})
        back_button.bind(on_press=self.go_to_second_screen)

         # Add the back button to the layout
        layout.add_widget(back_button)        

        self.add_widget(layout)

    def on_enter(self):
        # This method will be called when the screen is displayed
        Clock.schedule_once(self.delayed_check_account, 0.1)

    def delayed_check_account(self, dt):
        # This method will be called after a short delay (0.1 seconds)
        self.check_account(None)

            
    def go_to_second_screen(self, instance):
        self.manager.current = 'second'

    def update_user_profile(self, user_data, total_amount=None):
        print("Received user data:", user_data)

        # Extract user information from the 'user' key        
        username = user_data.get('username', '')
        amount = user_data.get('amount', '')
        phone_number = user_data.get('phone_number', '')
        print(f"phone number", phone_number)


        if username and amount and phone_number:
            if total_amount is not None:
                # If total_amount is provided, include it in the profile text
                profile_text = f"Username: {username}\nAmount: {amount}\nPhone Number: {phone_number}\nTotal Amount: {total_amount}"
            else:
                profile_text = f"Username: {username}\nAmount: {amount}\nPhone Number: {phone_number}"

            self.user_data_label.text = profile_text
        else:
            # Handle the case where some information is missing
            self.user_data_label.text = "User data is incomplete"


    def check_account(self, instance):
        login_screen = self.manager.get_screen('login')
        user_data = login_screen.user_data

        phone_number = user_data.get('phone_number', '')  # Assuming 'phone_number' is in user_data
        try:
            # Ensure 'phone_number' is included in the request payload
            if not phone_number:
                print("Phone number is missing in user_data.")
                return

            response = requests.post('https://mock-server-atvi.onrender.com//check_account', json={'phone_number': phone_number})
            if response.ok:
                total_amount = response.json().get('amount', 0)
                self.update_user_profile(user_data, total_amount)

            else:
                print(f'Failed to check account. Status Code: {response.status_code}, Response Content: {response.content}')
        except requests.RequestException as e:
            print(f'Request failed: {e}')



class CustomMDTextField(MDTextField):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        with self.canvas.before:
            self.bg_color = Color(rgba=(1, 1, 1, 0.5))  
            self.bg_rect = RoundedRectangle(size=self.size, pos=self.pos, radius=[(15, 15)])
            self.text_color = Color(0, 0, 0, 1)  

        self.bind(pos=self.update_bg, size=self.update_bg)

    def update_bg(self, *args):
        self.bg_rect.pos = self.pos
        self.bg_rect.size = self.size

class SomeScreen(Screen):

    def log_out(self):
        app = App.get_running_app()
        app.save_login_state(False)
        app.sm.current = 'login'

class MyApp(MDApp):

    def build(self):
        self.sm = ScreenManager()

        self.sm.add_widget(FirstScreen(name='first'))
        self.sm.add_widget(SecondScreen(name='second'))
        self.sm.add_widget(BeneficiaryScreen(name='beneficiary'))
        self.sm.add_widget(LoginScreen(name='login'))
        self.sm.add_widget(SignUpScreen(name='signup'))
        self.sm.add_widget(ProfileScreen(name='profile'))


        if self.is_logged_in():
            self.sm.current = 'second'  
        else:
            self.sm.current = 'first'

        return self.sm

    def is_logged_in(self):
        try:
            with open('login_state.json', 'r') as file:
                state = json.load(file)
                return state.get('logged_in', False)
        except (FileNotFoundError, json.JSONDecodeError):
            return False
        
    def logout_user(self):
        self.save_login_state(False)
        second_screen = self.sm.get_screen('second')
        second_screen.reset_planet_button_label()
        self.sm.current = 'login'

    def save_login_state(self, logged_in):
        with open('login_state.json', 'w') as file:
            json.dump({'logged_in': logged_in}, file)