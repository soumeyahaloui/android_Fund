def on_login_success(self, request, result):
        print("Login successful:", result)
        first_initial = self.username_input.text[0].upper() if self.username_input.text else ''
        self.manager.get_screen('second').update_planet_button(first_initial)
        self.manager.current = 'second'  
        # Assuming result is a dictionary containing user information
        user_data = result.get('user', {})

        # Pass user data to the ProfileScreen and update the UI
        self.update_profile_screen(user_data)

        # Navigate to the ProfileScreen
        self.manager.current = 'profile'
        self.save_login_state(True)

    def update_profile_screen(self, user_data):
        profile_screen = self.manager.get_screen('profile')
        profile_screen.update_user_profile(user_data)

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

        # Add the layout to the profile screen
        self.add_widget(layout)
            
    def go_to_second_screen(self, instance):
        self.manager.current = 'second'

    def update_user_profile(self, user_data):
        print("Received user data:", user_data)

        # Extract user information from the 'user' key        
        username = user_data.get('username', '')
        amount = user_data.get('amount', '')
        phone_number = user_data.get('phone_number', '')

        if username and amount and phone_number:
            profile_text = f"Username: {username}\nAmount: {amount}\nPhone Number: {phone_number}"
            self.user_data_label.text = profile_text
        else:
            # Handle the case where some information is missing
            self.user_data_label.text = "User data is incomplete"