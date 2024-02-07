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

        app = MDApp.get_running_app()
        self.phone_number = app.phone_number

        
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

    def on_pre_enter(self):
        super().on_pre_enter()
        app = MDApp.get_running_app()
        phone_number = app.phone_number  # Access phone_number attribute from MyApp class
        if phone_number:
            self.check_account(phone_number)

    def check_account(self, phone_number):
        try:            
            response = requests.post('https://mock-server-atvi.onrender.com//check_account', json={'phone_number': phone_number})
            if response.ok:
                total_amount = response.json().get('amount', 0)
                print(f'total amount is', total_amount)
            else:
                print('Failed to check account')
        except requests.RequestException as e:
            print(f'Request failed: {e}')

    

    def update_phone_number(self, phone_number):
        self.phone_number = phone_number
    

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

        total_amount = self.check_account_result


        print(f"Current total amount before donation: {total_amount}")

        
        if amount > total_amount:
            self.show_error_popup("Insufficient funds for donation.")
            dialog.dismiss()
            return

        new_total_amount = total_amount - amount

        # Update the user's total amount in the UI and user data
        self.manager.get_screen('login').update_total_amount(new_total_amount)
        self.update_user_profile(user_data, new_total_amount)

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
    
