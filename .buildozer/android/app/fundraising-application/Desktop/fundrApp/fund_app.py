from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.image import Image
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.graphics import Color, Rectangle
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

        bg = AsyncImage(source='https://cdn.glitch.global/53883c99-cc30-4656-9386-14bc8357b85c/fundr.png?v=1706210211746',
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
        donate_button.bind(on_press=self.go_to_second_screen)
        layout.add_widget(donate_button)

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
        

        layout = GridLayout(cols=self.cols, spacing=10, padding=10,
                            size_hint=(1, 1)) 
        self.add_widget(layout)

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

            # Ensure text alignment
            top_text.bind(size=top_text.setter('text_size'))
            self.widget_ids[f'top_text_{i}'] = top_text  # Assign ID
            image_layout.add_widget(top_text)

            # Image between the buttons
            image = Image(source='',
                          size_hint=(None, None),
                          size=(200, 200),
                          pos_hint={'center_x': 0.5, 'center_y': 0.6}
                          )
            self.widget_ids[f'image_{i}'] = image  # Assign ID
            image_layout.add_widget(image)

            # Container for small buttons
            button_container = GridLayout(
                rows=1,
                size_hint=(None, None),
                size=(200, 50),  # same size as bottom_text
                pos_hint={'center_x': 0.5, 'y': 0.1}
            )

            # Add TextInput for custom donation amount
            custom_amount_input = TextInput(
                hint_text='Enter Num',
                # Grey color for the placeholder
                hint_text_color=[0.5, 0.5, 0.5, 1],

                multiline=False,
                size_hint=(None, None),
                size=(140, 50),
                pos_hint={'center_x': 0.4, 'y': 0.2}
            )
            self.widget_dict[f'custom_amount_{i}'] = custom_amount_input
            image_layout.add_widget(custom_amount_input)

            # Submit button for the custom amount input
            submit_button = Button(
                text="Sub",
                size_hint=(None, None),
                # Adjusted 'x' position
                size=(60, 50), pos_hint={'x': custom_amount_input.pos_hint['center_x'] + 0.35, 'y': 0.2}

            )
            submit_button.bind(on_press=lambda instance, x=custom_amount_input, counter_key=f'counter_{i}':
                               self.show_confirmation_from_input(x, counter_key))

            image_layout.add_widget(submit_button)

            # Create and add the small buttons
            for amount in ["1", "5", "50", "100"]:
                button = Button(
                    text=amount,
                    # Fractional size to fit in the container
                    size_hint=(0.25, 1)
                )
                button.bind(on_press=lambda instance, x=amount, counter_key=f'counter_{i}', custom_input=custom_amount_input:
                            self.show_confirmation(x, counter_key, custom_input))

                button_container.add_widget(button)

            image_layout.add_widget(button_container)
            # Bottom Button
            bottom_text = Label(
                text=f'Bottom {i}',
                size_hint=(None, None),
                size=(200, 50),
                pos_hint={'center_x': 0.5, 'y': 0}
            )

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
        menu_button.bind(on_release=self.open_menu)
        self.add_widget(menu_button)
        # Don't forget to add the main layout to the screen

    def fetch_data(self):
        # Replace 'http://localhost:5000/get_data' with your Glitch app's URL
        url = 'https://fundraising-flask.onrender.com/get_data'
        UrlRequest(url, self.on_request_success)


    def on_request_success(self, request, result):
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
                # Limit the number of items to process based on the UI's capacity.
                if i < 4:  # Assuming there are 4 slots to display the data.
                    image_widget = self.widget_ids.get(f'image_{i+1}')
                    top_text_widget = self.widget_ids.get(f'top_text_{i+1}')

                    if image_widget and 'Image' in data_item:
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

        # Other options
        for option in ['Option 1', 'Option 2', 'Option 3']:
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

        # Replace 'http://localhost:5000' with the base URL of your deployed Flask app
        base_url = 'https://fundraising-flask.onrender.com'

        # Use the base URL in the UrlRequest
        UrlRequest(f'{base_url}/get_family_data/{next_family_id}', on_success=lambda req, res: self.update_frame_with_new_data(f'counter_{self.available_frames.pop(0)}', res), on_error=self.on_request_error, on_failure=self.on_request_error)



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
        completed_image = Image(source=completed_set['Image'], size_hint=(
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


class MyApp(App):

    def build(self):
        sm = ScreenManager()
        sm.add_widget(FirstScreen(name='first'))
        sm.add_widget(SecondScreen(name='second'))
        sm.add_widget(BeneficiaryScreen(name='beneficiary'))
        self.icon = 'https://cdn.glitch.global/53883c99-cc30-4656-9386-14bc8357b85c/fundrr.ico?v=1706210215068'
        return sm