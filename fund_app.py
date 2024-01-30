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

# Reshape the Arabic text
reshaped_text = reshape('تسجيل')

# Get the display text with correct RTL rendering
bidi_text = get_display(reshaped_text)

class PlanetButton(ButtonBehavior, Image):
    border_width = 3.5  # Width of the border

    def __init__(self, **kwargs):
        self.text_label = Label(text=bidi_text, font_name='DejaVuSans', font_size='15sp')
        super(PlanetButton, self).__init__(**kwargs)
        self.always_release = True
        self.keep_ratio = True
        self.allow_stretch = True
        self.source = './res/fdr.png'  # Correct path for your image

        
        self.add_widget(self.text_label)
        
        Clock.schedule_once(self.init_graphics, 0)

    def init_graphics(self, *args):
    # Safely access the canvas.before attribute
        if getattr(self.canvas, 'before', None):
            self.canvas.before.clear()
            with self.canvas.before:
                # Set the color for the border here. (r, g, b, a)
                Color(0, 0, 0, 1)  # Black color for the border
                # Drawing the border
                self.border = Line(ellipse=(self.x, self.y, self.width, self.height), width=self.border_width)
        self.update_text_label()

    def update_text_label(self):
        self.text_label.size = self.size
        self.text_label.pos = self.pos

    def on_size(self, *args):
        self.init_graphics()
        self.update_text_label()


    def on_pos(self, *args):
        self.init_graphics()
        self.update_text_label()

    def on_press(self):
        # You can add visual effects on button press, like changing color or making it look pressed down
        pass

    def on_release(self):
        # Reset visual effects when the button is released
        pass


class LabelB(Label):
    def __init__(self, **kwargs):
        self.bg_color = kwargs.pop(
            'bg_color', (1, 1, 1, 1))  # Default to white
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

        # Using FloatLayout for flexibility in positioning
        layout = FloatLayout()
        self.add_widget(layout)

     # Stylish Donate button
        donate_button = Button(
            text="Donate",
            font_size="20sp",
            background_color=(0.2, 0.5, 0.8, 1),  # Deep blue color
            color=(1, 1, 1, 1),  # White text color
            size_hint=(None, None),
            size=(200, 60),
            pos_hint={'center_x': 0.5, 'center_y': 0.2}
        )

        # Adjustments for donate_button in the FirstScreen class
        donate_button.size_hint = (0.5, None)
        donate_button.height = '48dp'
        donate_button.pos_hint = {'center_x': 0.5, 'y': 0.1}

        donate_button.bind(on_press=self.go_to_second_screen)
        layout.add_widget(donate_button)

        login_signup_button = PlanetButton(
            size_hint=(None, None),
            size=(dp(56), dp(56)),  # Button size
            pos_hint={'center_x': 0.1, 'center_y': 0.06}
        )
        login_signup_button.bind(on_press=self.show_login_signup_options)
        layout.add_widget(login_signup_button)

    def show_login_signup_options(self, instance):
        content = BoxLayout(orientation='vertical', padding=10, spacing=10, size_hint_y=None)
        # Set the height of the BoxLayout to the combined height of the buttons and spacing
        content.height = dp(100)  # Adjust the height based on your needs

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
        self.manager.current = 'second'


class SecondScreen(Screen):
    def __init__(self, **kwargs):
        super(SecondScreen, self).__init__(**kwargs)

        self.widget_dict = {}  # Initialize the dictionary
        self.counters = {}  # Dictionary to store counters for each set of buttons
        self.widget_ids = {}  # Dictionary to store widget references

        self.fetch_data()
        self.available_frames = []
        self.processed_sets = []  # List to keep track of processed sets

        self.next_index = 1
        self.last_fetched_family_id = 4  # assuming you start with 1-4
        # Maps frame to family ID
        self.frame_data_map = {i: i for i in range(1, 5)}

        bg = AsyncImage(source='https://cdn.glitch.global/53883c99-cc30-4656-9386-14bc8357b85c/fundd.png?v=1706210860343',
                allow_stretch=True,
                keep_ratio=False)
        self.add_widget(bg)

        self.cols = 2  # Number of columns in the grid
        self.rows = 2  # Number of rows in the grid
        
        # Assuming you have 2 columns and 2 rows, adjust as needed
        screen_width, screen_height = Window.size
        column_width = screen_width / self.cols
        row_height = screen_height / self.rows
        

        layout = GridLayout(cols=self.cols, spacing=dp(10), padding=dp(10), size_hint=(1, None))
        layout.bind(minimum_height=layout.setter('height'))
        self.add_widget(layout)

        # Adjust the spacing and padding in the GridLayout
        layout.spacing = dp(2)
        layout.padding = dp(2)


        # Loop to create the image and button pairs
        for i in range(1, 5):
            self.counters[f'counter_{i}'] = 0  # Initialize the counter

            framed_layout = FloatLayout(size_hint=(None, None), size=(
                column_width, row_height))  # Slightly larger to accommodate the frame
            # Add a black frame to the layout
            self.add_black_frame(framed_layout)

            image_layout = FloatLayout(size_hint=(1, 1), pos_hint={
                                       'center_x': 0.5, 'center_y': 0.5})

            top_text = LabelB(
                text='',
                bg_color=(0.2, 0.5, 0.8, 1),  # Deep blue background
                color=(1, 1, 1, 1),  # White text color
                font_size='20sp',  # Set font size
                bold=True,  # Make the text bold
                size_hint=(None, None),
                size=(200, 50),
                pos_hint={'center_x': 0.5, 'top': 1},
                halign="center",  # Center-align text horizontally
                valign="middle"  # Center-align text vertically
            )

            # Adjustments for top_text in the SecondScreen class
            top_text.size_hint = (0.8, None)  # Take 90% of the width and automatic height
            top_text.height = dp(30)  # Assign a height that scales properly
            top_text.pos_hint = {'center_x': 0.5, 'top': 0.99}  # Position at the top

            # Ensure text alignment
            top_text.bind(size=top_text.setter('text_size'))
            self.widget_ids[f'top_text_{i}'] = top_text  # Assign ID
            image_layout.add_widget(top_text)

            # Image between the buttons
            image = AsyncImage(source='', size_hint=(0.8, 0.3), allow_stretch=True)
            image.pos_hint = {'center_x': 0.5, 'center_y': 0.5}
            self.widget_ids[f'image_{i}'] = image  # Assign ID
            image_layout.add_widget(image)

            # Adjustments for image in the SecondScreen class
            image.size_hint = (0.8, 0.3)  # Adjust the width and height percentages as necessary
            image.allow_stretch = True  # Allow image to stretch to fill the space
            image.pos_hint = {'center_x': 0.5, 'center_y': 0.7}  # Center in the middle of the FloatLayout

            # Container for small buttons
            button_container = GridLayout(rows=1, size_hint=(None, None),size=(200, 50),  # same size as bottom_text
                pos_hint={'center_x': 0.5, 'y': 0.27}
            )
            # Adjustments for button_container in the SecondScreen class
            button_container.size_hint = (0.8, None)
            button_container.height = dp(40)
            button_container.padding = [dp(2)] * 4  # Padding on all sides

            custom_amount_input = TextInput(
                hint_text='Enter Num',
                # Grey color for the placeholder
                hint_text_color=[0.5, 0.5, 0.5, 1],
                multiline=False,
                size_hint=(None, None),
                size=(140, 50),
                pos_hint={'center_x': 0.4, 'y': 0.2}
            )

            for amount in ["1", "5", "50", "100"]:
                button = Button(text=amount, size_hint=(None, 1), width=dp(48))  # Set button width using dp
                button.bind(on_press=self.create_button_callback(amount, f'counter_{i}', custom_amount_input))
                button_container.add_widget(button)

            # Be sure to adjust the size_hint of the buttons after adding them to the container:
            for button in button_container.children:
                button.size_hint_x = 1 / len(button_container.children)
                
            # For buttons within button_container
            button.size_hint = (1 / len(button_container.children), 1)  # Equal width for all buttons

            # Add TextInput for custom donation amount
          
            # Adjustments for custom_amount_input in the SecondScreen class
            custom_amount_input.size_hint = (0.6, None)
            custom_amount_input.height = dp(40)  # Adjust the height as necessary
            custom_amount_input.pos_hint = {'center_x': 0.4, 'y': 0.4}

            self.widget_dict[f'custom_amount_{i}'] = custom_amount_input
            image_layout.add_widget(custom_amount_input)

            # Submit button for the custom amount input
            submit_button = Button(
                text="Sub",
                size_hint=(None, None),
                # Adjusted 'x' position
                size=(60, 50), pos_hint={'x': custom_amount_input.pos_hint['center_x'] + 0.35, 'y': 0.2}

            )
            # Adjustments for submit_button in the SecondScreen class
            submit_button.size_hint = (0.2, None)
            submit_button.height = dp(40)  # Adjust the height as necessary
            submit_button.pos_hint = {'right': custom_amount_input.pos_hint['center_x'] + 0.5, 'y': 0.4}
            
            submit_button.bind(on_press=lambda instance, x=custom_amount_input, counter_key=f'counter_{i}':
                               self.show_confirmation_from_input(x, counter_key))

            image_layout.add_widget(submit_button)

            # Create and add the small buttons
            # Inside the loop where you bind buttons to callbacks
            

            image_layout.add_widget(button_container)
            # Bottom Button
            bottom_text = Label(
                text=f'Bottom {i}',
                size_hint=(None, None),
                size=(200, 50),
                pos_hint={'center_x': 0.5, 'y': 0}
            )
            
            # For bottom_text, make it responsive
            bottom_text.size_hint = (0.8, None)
            bottom_text.height = dp(30)  # Adjust the height as necessary
            bottom_text.pos_hint = {'center_x': 0.5, 'y': 0.17}

            self.add_frame(bottom_text)
            image_layout.add_widget(bottom_text)
            self.widget_dict[f'bottom_text_{i}'] = bottom_text

            framed_layout.add_widget(image_layout)
            layout.add_widget(framed_layout)

        

        # Menu button at the bottom
        menu_button = Button(
            text='Menu',
            size_hint=(None, None),
            size=(100, 50),
            pos_hint={'center_x': 0.5, 'y': 0}
        )

        # For menu_button, make it responsive
        menu_button.size_hint = (0.5, None)
        menu_button.height = dp(40)  # Adjust the height as necessary
        menu_button.pos_hint = {'center_x': 0.5, 'bottom': 1}

        menu_button.bind(on_release=self.open_menu)
        self.add_widget(menu_button)
        # Don't forget to add the main layout to the screen
        
        self.planet_button = PlanetButton(
            size_hint=(None, None),
            size=(dp(40), dp(40)),  # Button size
            pos_hint={'center_x': 0.1, 'center_y': 0.04}
        )
        self.add_widget(self.planet_button)

    def go_to_first_screen(self):
        # Method to switch to FirstScreen
        self.manager.current = 'first'

    def create_button_callback(self, amt, key, input_field):
        def button_callback(instance):
            self.show_confirmation(amt, key, input_field)
        return button_callback

    def fetch_data(self):
        url = 'https://fundraising-flask.onrender.com/get_data'
        UrlRequest(url, on_success=self.on_request_success, on_failure=self.on_request_failure, on_error=self.on_request_error, on_redirect=self.on_request_redirect)


    def on_request_failure(self, request, result):
        logging.error("Request failed with result: %s" % result)


    def on_request_redirect(self, request, result):
        logging.info("Request was redirected, final result: %s" % result)


    def on_request_success(self, request, result):
        Clock.schedule_once(lambda dt: self.update_ui_with_data(result))

        logging.info("Request to Flask server successful.")
        logging.info(f"Data received: {result}")

        # Ensure result is a list and has at least one item.
        if isinstance(result, list) and len(result) > 0:
            # Update your widgets here.
            self.update_ui_with_data(result)
        else:
            logging.error("Data received is not in the expected format or is empty.")

    def update_ui_with_data(self, data):
    # Ensure 'data' is a list of dictionaries and has items.
        if isinstance(data, list) and len(data) > 0:
            for i, data_item in enumerate(data):
                logging.info(f"Updating UI for frame {i+1}")
                # Limit the number of items to process based on the UI's capacity.
                if i < 4:  # Assuming there are 4 slots to display the data.
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
        # Create a new DropDown each time the menu is opened
        dropdown = DropDown()

        # Beneficiary button
        beneficiary_btn = Button(
            text='Beneficiary', size_hint_y=None, height=44)
        beneficiary_btn.bind(on_release=lambda btn: self.close_dropdown_and_navigate(
            dropdown, self.go_to_beneficiary))

        dropdown.add_widget(beneficiary_btn)

        # Open button (previously Option 2)
        open_btn = Button(text='Open', size_hint_y=None, height=44)
        open_btn.bind(on_release=lambda btn: self.close_dropdown_and_navigate(
            dropdown, self.go_to_first_screen))

        dropdown.add_widget(open_btn)

        # Other options
        for option in []:
            btn = Button(text=option, size_hint_y=None, height=44)
            btn.bind(on_release=lambda btn: self.close_dropdown_and_navigate(
                dropdown, lambda: dropdown.select(btn.text)))
            dropdown.add_widget(btn)

        # Open the dropdown
        dropdown.open(button)

    def close_dropdown_and_navigate(self, dropdown, navigation_action):
        """Close dropdown and perform the specified navigation action."""
        dropdown.dismiss()
        navigation_action()

    def go_to_beneficiary(self):
        # Method to switch to BeneficiaryScreen
        self.manager.current = 'beneficiary'

    def show_confirmation_from_input(self, custom_input, counter_key):
        try:
            amount = float(custom_input.text)
            self.show_confirmation(amount, counter_key, custom_input)

        except ValueError:
            self.show_error_popup("Please enter a valid number.")

    def show_error_popup(self, message):
        content = Label(text=message)
        popup = Popup(title="Error",
                      content=content,
                      size_hint=(None, None), size=(400, 200))
        popup.open()

    def add_black_frame(self, widget):
        with widget.canvas.before:
            Color(0, 0, 0, 1)  # Black color for the frame
            widget.frame = Rectangle(pos=widget.pos, size=widget.size)
        widget.bind(pos=self.update_frame, size=self.update_frame)

    def update_frame(self, instance, value):
        # Adjust the position to be slightly outside the widget
        instance.frame.pos = (instance.pos[0] - 10, instance.pos[1] - 10)
        # Make the frame slightly larger than the widget
        instance.frame.size = (instance.size[0] + 20, instance.size[1] + 20)

    def add_frame(self, widget):
        # Draw a frame around the widget
        with widget.canvas.before:
            Color(0.2, 0.5, 0.8, 1)  # Frame color
            widget.frame = Rectangle(pos=widget.pos, size=widget.size)

        # Update frame position and size when widget position or size change
        widget.bind(pos=self.update_frame, size=self.update_frame)

    def update_frame(self, instance, value):
        instance.frame.pos = instance.pos
        instance.frame.size = instance.size

    def show_confirmation(self, amount, counter_key, custom_input):
        try:
            # Convert the string to a float
            amount = float(amount)
        except ValueError:
            # If conversion fails, show an error and return
            self.show_error_popup(f"Invalid amount: {amount}")
            return

        print(f"Showing confirmation for {amount}")  # Debug print
        content = GridLayout(cols=1, spacing=10, size_hint_y=None)
        content.add_widget(
            Label(text=f"Are you sure you want to donate {amount}?"))


        # Buttons for confirmation
        btn_layout = GridLayout(cols=2, spacing=10, size_hint_y=None)
        yes_btn = Button(text="Yes")
        no_btn = Button(text="No")
        btn_layout.add_widget(yes_btn)
        btn_layout.add_widget(no_btn)
        content.add_widget(btn_layout)

        # Popup instance
        popup = Popup(title="Confirm Donation",
                      content=content,
                      size_hint=(None, None), size=(400, 200))

        # Binding buttons to actions
        yes_btn.bind(
            on_press=lambda *args: self.confirm_donation(amount, counter_key, popup))
        no_btn.bind(on_press=popup.dismiss)
        popup.open()

    def confirm_donation(self, amount, counter_key, popup):
        # Convert amount to float for consistency
        amount = float(amount)

        # Extract the goal amount from the top_text widget
        top_text_widget = self.widget_ids.get(f'top_text_{counter_key[-1]}')
        if top_text_widget:
            goal_text = top_text_widget.text
            # Assuming the goal text is in the format "Goal: <amount>"
            try:
                completion_goal = float(goal_text.split(" ")[1])
            except (IndexError, ValueError):
                print("Error extracting goal amount from top_text")
                completion_goal = 0  # default or error value
        else:
            completion_goal = 0  # default or error value if widget not found

        # Debug print
        print(
            f"Confirming donation: {amount} for {counter_key} with goal {completion_goal}")

        self.update_counter(amount, counter_key)

        if self.counters[counter_key] >= completion_goal:
            print(f"Amount completed for {counter_key}")  # Debug print
            completed_image_path = self.widget_ids[f'image_{counter_key[-1]}'].source

            completed_set = {
                'Image': completed_image_path,
                # Use the collected amount
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

        # Reset the custom amount input for the specific frame
        custom_amount_input = self.widget_dict.get(
            f'custom_amount_{counter_key[-1]}')
        if custom_amount_input:
            custom_amount_input.text = ''  # Reset to empty

        popup.dismiss()

    def mark_frame_as_available(self, counter_key):
        # Mark the frame associated with counter_key as available
        # You can maintain a list or dictionary to track available frames
        self.available_frames.append(counter_key[-1])  # Assuming it's a list

    def reset_frame(self, counter_key):
        # Resetting the image, text, and counter for the specified frame
        image_widget = self.widget_ids.get(f'image_{counter_key[-1]}')
        text_widget = self.widget_ids.get(f'top_text_{counter_key[-1]}')
        bottom_text_widget = self.widget_dict.get(
            counter_key.replace('counter', 'bottom_text'))
        custom_amount_input = self.widget_dict.get(
            f'custom_amount_{counter_key[-1]}')

        if image_widget:
            image_widget.source = ''  # Set to default or empty image
        if text_widget:
            text_widget.text = 'Default Text'  # Reset text
        if bottom_text_widget:
            bottom_text_widget.text = 'Total: 0.00'  # Reset amount
        if custom_amount_input:
            custom_amount_input.text = ''  # Reset custom_amount_input text

        # Reset the counter for the frame
        self.counters[counter_key] = 0

    def update_frame_with_new_data(self, counter_key, data):
        # Assuming data is a dictionary with keys 'ID', 'Image', 'Amount', 'Details'

        # Fetch the widgets associated with the given counter_key
        image_widget = self.widget_ids.get(f'image_{counter_key[-1]}')
        top_text_widget = self.widget_ids.get(f'top_text_{counter_key[-1]}')
        bottom_text_widget = self.widget_dict.get(
            counter_key.replace('counter', 'bottom_text'))
        custom_amount_input = self.widget_dict.get(
            f'custom_amount_{counter_key[-1]}')

        # Update the image source
        if image_widget:
            image_widget.source = data['Image']

        # Update the top text with the new goal amount
        if top_text_widget:
            top_text_widget.text = f"Goal: {data['Amount']}"

        # Reset the bottom text to show the new goal starting at 0
        if bottom_text_widget:
            bottom_text_widget.text = 'Total: 0.00'

        # Clear any previous custom input
        if custom_amount_input:
            custom_amount_input.text = ''

        # Reset the counter for the new family set
        self.counters[counter_key] = 0

        print(f"New family set fetched for frame {counter_key}: {data}")

    def on_request_error(self, request, error):
        logging.error(f"Request to Flask server error: {error}")
        traceback.print_exc()
        print("Error fetching total sets:", error)
        # Handle the error as needed, e.g., set a default value or show a message

    def update_counter(self, value, counter_key):
        self.counters[counter_key] += value
        updated_count = self.counters[counter_key]
        bottom_text_widget = self.widget_dict.get(
            counter_key.replace('counter', 'bottom_text'))
        if bottom_text_widget:
            # Format to two decimal places
            bottom_text_widget.text = f"Total: {updated_count:.2f}"

    def get_numeric_value(self, text):
        # Extracts numeric value from the text
        try:
            return int(''.join(filter(str.isdigit, text)))
        except ValueError:
            return 0

    def show_thank_you_popup(self):
        content = Label(text="Thank you, the amount is completed")
        popup = Popup(title="Thank You",
                      content=content,
                      size_hint=(None, None), size=(400, 200))
        popup.open()

    def go_to_beneficiary(self):
        # Method to switch to BeneficiaryScreen
        self.manager.current = 'beneficiary'

    def fetch_next_family_set(self, frame_number):
        self.last_fetched_family_id += 1  # Increment to fetch the next family
        next_family_id = self.last_fetched_family_id

        base_url = 'https://fundraising-flask.onrender.com'  # Update the URL here


        # Use the base URL in the UrlRequest
        UrlRequest(f'{base_url}/get_family_data/{next_family_id}', on_success=lambda req, res: self.update_frame_with_new_data(f'counter_{self.available_frames.pop(0)}', res), on_error=self.on_request_error, on_failure=self.on_request_error)
    
    def update_planet_button(self, initial):
    # Update the text label inside the planet button with the user's first initial
        self.planet_button.text_label.text = initial

class BeneficiaryScreen(Screen):
    def __init__(self, **kwargs):
        super(BeneficiaryScreen, self).__init__(**kwargs)

        bg = AsyncImage(source='https://cdn.glitch.global/53883c99-cc30-4656-9386-14bc8357b85c/fundd.png?v=1706210860343',
                allow_stretch=True,
                keep_ratio=False)
        self.add_widget(bg)

        # Initialize ScrollView and GridLayout
        scroll_view = ScrollView(size_hint=(
            1, None), size=(Window.width, Window.height))
        self.layout = GridLayout(
            cols=2, spacing=10, padding=10, size_hint_y=None)
        self.layout.bind(minimum_height=self.layout.setter('height'))
        scroll_view.add_widget(self.layout)
        self.add_widget(scroll_view)

        # Add a menu button at the bottom
        menu_button = Button(text='Menu', size_hint=(None, None), size=(
            100, 50), pos_hint={'center_x': 0.5, 'y': 0})
        menu_button.bind(on_release=self.open_menu)
        self.add_widget(menu_button)

        # Create a menu button at the bottom
        menu_button = Button(
            text='Menu',
            size_hint=(None, None),
            size=(100, 50),
            pos_hint={'center_x': 0.5, 'y': 0}
        )
        menu_button.bind(on_release=self.open_menu)
        self.add_widget(menu_button)

    def go_to_first_screen(self):
        # This method will switch the current screen to the FirstScreen
        self.manager.current = 'first'

    def open_menu(self, button):
        # Create a new DropDown each time the menu is opened
        dropdown = DropDown()

        # Option 1: Main
        main_btn = Button(
            text='Main',
            size_hint_y=None,
            height=44
        )
        main_btn.bind(on_release=lambda btn: self.close_dropdown_and_navigate(
            dropdown, lambda: self.go_to_main_screen(btn)))

        dropdown.add_widget(main_btn)

        # Open button (previously Option 2)
        open_btn = Button(text='Open', size_hint_y=None, height=44)
        open_btn.bind(on_release=lambda btn: self.close_dropdown_and_navigate(
            dropdown, self.go_to_first_screen))

        dropdown.add_widget(open_btn)

        # Other options
        for option in ['Option 2', 'Option 3']:
            btn = Button(text=option, size_hint_y=None, height=44)
            btn.bind(on_release=lambda btn: self.close_dropdown_and_navigate(
                dropdown, lambda: dropdown.select(btn.text)))

            dropdown.add_widget(btn)

        # Open the dropdown
        dropdown.open(button)

    def close_dropdown_and_navigate(self, dropdown, navigation_action):
        """Close dropdown and perform the specified navigation action."""
        dropdown.dismiss()
        navigation_action()

    def go_to_main_screen(self, button):
        # Method to switch to SecondScreen
        self.manager.current = 'second'

    def add_completed_set(self, completed_set):
        # Create a black frame for the completed set
        framed_layout = FloatLayout(size_hint=(None, None), size=(240, 240))
        self.add_black_frame(framed_layout)

        # Create widgets to display the completed set
        completed_image = AsyncImage(source=completed_set['Image'], size_hint=(
            None, None), size=(200, 200), pos_hint={'center_x': 0.5, 'center_y': 0.65})
        completed_label = Label(
            text=f"Raised: {completed_set['Amount']}",
            size_hint_y=None, height=40, pos_hint={'center_x': 0.5, 'center_y': 0.3})

        # Add these widgets to the framed layout
        framed_layout.add_widget(completed_image)
        framed_layout.add_widget(completed_label)

        # Add the framed layout to your main layout
        self.layout.add_widget(framed_layout)
        self.layout.height = self.layout.minimum_height

    def add_black_frame(self, widget):
        with widget.canvas.before:
            Color(0, 0, 0, 1)  # Black color for the frame
            widget.frame = Rectangle(pos=widget.pos, size=widget.size)
        widget.bind(pos=self.update_frame, size=self.update_frame)

    def update_frame(self, instance, value):
        instance.frame.pos = (instance.pos[0] - 10, instance.pos[1] - 10)
        instance.frame.size = (instance.size[0] + 20, instance.size[1] + 20)

class LoginScreen(Screen):
    def __init__(self, **kwargs):
        super(LoginScreen, self).__init__(**kwargs)

        bg = AsyncImage(source='https://cdn.glitch.global/53883c99-cc30-4656-9386-14bc8357b85c/fundd.png?v=1706210860343',
                allow_stretch=True,
                keep_ratio=False)
        self.add_widget(bg)

        login_layout = FloatLayout()

        # GridLayout for login content
        grid_layout = GridLayout(cols=1, spacing=10, padding=10, size_hint=(None, None), size=(300, 200))
        grid_layout.pos_hint = {'center_x': 0.5, 'center_y': 0.5}

        # Back arrow button
        back_button = MDIconButton(icon='arrow-left', pos_hint={'x': 0, 'top': 1})
        back_button.bind(on_press=self.go_to_first_screen)

        # Username/Number input
        self.username_input = CustomMDTextField(hint_text='Username or Number', multiline=False)
        grid_layout.add_widget(self.username_input)

        # Password input
        self.password_input = CustomMDTextField(hint_text='Password', password=True, multiline=False)
        grid_layout.add_widget(self.password_input)

        # Login button
        login_button = MDRaisedButton(text='Login', size_hint=(None, None), size=(150, 48))
        login_button.bind(on_press=self.login_user)
        
        # Center the login button within the FloatLayout
        login_button.pos_hint = {'center_x': 0.5, 'y': 0.1}
        
        # Add the GridLayout and the login button to the FloatLayout
        login_layout.add_widget(grid_layout)
        login_layout.add_widget(login_button)
        login_layout.add_widget(back_button)


        # Add the layout to the screen
        self.add_widget(login_layout)

    def go_to_first_screen(self, instance):
        self.manager.current = 'first'

    def login_user(self, instance):
        username = self.username_input.text
        password = self.password_input.text
        login_data = {'username': username, 'password': password}
        login_url = 'https://fundraising-flask.onrender.com/login'
        UrlRequest(login_url, req_body=json.dumps(login_data),
                   on_success=self.on_login_success, on_failure=self.on_login_failure,
                   method='POST', req_headers={'Content-type': 'application/json'})

    def on_login_success(self, request, result):
        # Handle successful login
        # For example, navigate to a different screen or display a success message
        print("Login successful:", result)
        first_initial = self.username_input.text[0].upper() if self.username_input.text else ''
        # Update the planet button on the SecondScreen
        self.manager.get_screen('second').update_planet_button(first_initial)
        self.manager.current = 'second'  # Navigate to SecondScreen


    def on_login_failure(self, request, result):
        # Handle login failure
        # Display an error message to the user
        print("Login failed:", result)
        # You can use Popup or another widget to show the error


class SignUpScreen(Screen):
    def __init__(self, **kwargs):
        super(SignUpScreen, self).__init__(**kwargs)

        bg = AsyncImage(source='https://cdn.glitch.global/53883c99-cc30-4656-9386-14bc8357b85c/fundd.png?v=1706210860343',
                allow_stretch=True,
                keep_ratio=False)
        self.add_widget(bg)

        layout = BoxLayout(orientation='vertical', spacing=10, padding=10)

        # Back arrow button
        back_button = MDIconButton(icon='arrow-left', pos_hint={'x': 0, 'top': 1})
        back_button.bind(on_press=self.go_to_first_screen)

        # Username input
        self.username_input = CustomMDTextField(hint_text='Username', multiline=False)
        layout.add_widget(self.username_input)

        # Number input
        self.number_input = CustomMDTextField(hint_text='phone number', multiline=False)
        layout.add_widget(self.number_input)

        # Password input
        self.password_input = CustomMDTextField(hint_text='Password', password=True, multiline=False)
        layout.add_widget(self.password_input)

        # Confirm Password input
        self.confirm_password_input = CustomMDTextField(hint_text='Confirm Password', password=True, multiline=False)
        layout.add_widget(self.confirm_password_input)

        # Signup button
        signup_button = MDRaisedButton(text='Sign Up', size_hint=(None, None), size=(150, 48))
        signup_button.bind(on_press=self.register_user)
        layout.add_widget(signup_button)
        layout.add_widget(back_button)


        # Add the layout to the screen
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
        signup_url = 'https://fundraising-flask.onrender.com/register'
        UrlRequest(signup_url, req_body=json.dumps(signup_data),
                   on_success=self.on_signup_success, on_failure=self.on_signup_failure,
                   method='POST', req_headers={'Content-type': 'application/json'})

    def on_signup_success(self, request, result):
        # Handle successful signup
        # For example, navigate to the login screen or display a success message
        print("Signup successful:", result)
        self.manager.current = 'second'  # Navigate to SecondScreen


    def on_signup_failure(self, request, result):
        # Handle signup failure
        # Display an error message to the user
        print("Signup failed:", result)
        # You can use Popup or another widget to show the error

    def show_error_popup(self, message):
        popup_content = Label(text=message)
        popup = Popup(title="Error",
                      content=popup_content,
                      size_hint=(None, None), size=(300, 150))
        popup.open()

class CustomMDTextField(MDTextField):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        with self.canvas.before:
            self.bg_color = Color(rgba=(1, 1, 1, 0.5))  # Semi-transparent white
            self.bg_rect = RoundedRectangle(size=self.size, pos=self.pos, radius=[(15, 15)])
            self.text_color = Color(0, 0, 0, 1)  # Black text color

        self.bind(pos=self.update_bg, size=self.update_bg)

    def update_bg(self, *args):
        self.bg_rect.pos = self.pos
        self.bg_rect.size = self.size


class MyApp(MDApp):

    def build(self):
        sm = ScreenManager()
        sm.add_widget(FirstScreen(name='first'))
        sm.add_widget(SecondScreen(name='second'))
        sm.add_widget(BeneficiaryScreen(name='beneficiary'))
        sm.add_widget(LoginScreen(name='login'))
        sm.add_widget(SignUpScreen(name='signup'))
        
        return sm
    