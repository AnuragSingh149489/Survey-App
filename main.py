from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.lang import Builder
import csv
from kivy.uix.spinner import Spinner
import calendar

# Load all KV definitions
Builder.load_file('Login_Page.kv')
Builder.load_file('Age.kv')
Builder.load_file('DOB.kv')
Builder.load_file('OHTs.kv')
Builder.load_file('55_LPCD.kv')

class LoginScreen(Screen):
    pass

class AgeScreen(Screen):
    pass

class DOBScreen(Screen):
    pass

class OHTsScreen(Screen):
    pass

class LPCDScreen(Screen):
    pass

class MyApp(App):
    def build(self):
        self.data = {}
        self.checks = []  # Initialize checks here
        sm = ScreenManager()
        sm.add_widget(LoginScreen(name='login'))
        sm.add_widget(AgeScreen(name='age'))
        sm.add_widget(DOBScreen(name='dob'))
        sm.add_widget(OHTsScreen(name='ohts'))
        sm.add_widget(LPCDScreen(name='lpcd'))
        return sm

    def back_pressed(self):
        sm = self.root
        if sm.current == 'login':
            return
        elif sm.current == 'age':
            sm.current = 'login'
        elif sm.current == 'dob':
            sm.current = 'age'
        elif sm.current == 'ohts':
            sm.current = 'dob'
        elif sm.current == 'lpcd':
            sm.current = 'ohts'

    def next_pressed(self):
        sm = self.root
        current_screen = sm.current_screen

        if sm.current == 'login':
            username = current_screen.ids.username.text
            password = current_screen.ids.password.text
            if username and password:  # Add proper validation here
                sm.current = 'age'
            else:
                self.show_popup("Error", "Invalid login credentials.")

        elif sm.current == 'age':
            age = current_screen.ids.age.text
            if age.isdigit() and int(age) > 0:
                self.data['age'] = age
                sm.current = 'dob'
            else:
                self.show_popup("Error", "Please enter a valid age.")

        elif sm.current == 'dob':
            dob = current_screen.ids.dob_input.text
            if dob:  # Add proper DOB validation here
                self.data['dob'] = dob
                sm.current = 'ohts'
            else:
                self.show_popup("Error", "Please enter a valid date of birth.")

        elif sm.current == 'ohts':
            ohts = current_screen.ids.ohts_input.text
            if ohts.isdigit() and int(ohts) >= 0:
                self.data['ohts'] = ohts
                sm.current = 'lpcd'
            else:
                self.show_popup("Error", "Please enter a valid number.")

        elif sm.current == 'lpcd':
            lpcd = 'Yes' if current_screen.ids.lpcd_yes.active else 'No' if current_screen.ids.lpcd_no.active else 'Not Applicable'
            self.data['lpcd'] = lpcd
            self.save_to_csv(self.data)

    def show_date_picker(self):
        # Create a popup for date selection
        popup = Popup(title='Select Date', size_hint=(None, None), size=(300, 200))

        # Create spinner widgets for day, month, and year
        day_spinner = Spinner(text='Day', values=[str(i).zfill(2) for i in range(1, 32)])
        month_spinner = Spinner(text='Month', values=[calendar.month_abbr[i] for i in range(1, 13)])
        year_spinner = Spinner(text='Year', values=[str(i) for i in range(1920, 2030)])  # Adjust range as needed

        # Function to update the text input with the selected date
        def update_date(instance):
            selected_date = f"{day_spinner.text}-{month_spinner.text}-{year_spinner.text}"
            current_screen = self.root.current_screen
            current_screen.ids.dob_input.text = selected_date
            popup.dismiss()

        # Create a button to confirm the date selection
        confirm_button = Button(text='Confirm', size_hint_y=None, height=40)
        confirm_button.bind(on_press=update_date)

        # Add widgets to the popup
        popup_content = BoxLayout(orientation='vertical', padding=10, spacing=10)
        popup_content.add_widget(day_spinner)
        popup_content.add_widget(month_spinner)
        popup_content.add_widget(year_spinner)
        popup_content.add_widget(confirm_button)
        popup.content = popup_content

        # Open the popup
        popup.open()

    def checkbox_click(self, instance, value, topping):
        if value:
            self.checks.append(topping)
        else:
            self.checks.remove(topping)

    def show_popup(self, title, message):
        content = BoxLayout(orientation='vertical')
        content.add_widget(Label(text=message))
        close_button = Button(text='Close')
        content.add_widget(close_button)

        popup = Popup(title=title, content=content, size_hint=(0.6, 0.4))
        close_button.bind(on_press=popup.dismiss)
        popup.open()

    def save_to_csv(self, data):
        with open('user_data.csv', mode='a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([data['age'], data['dob'], data['ohts'], data['lpcd']])
        self.show_popup("Success", "Data saved successfully.")

if __name__ == '__main__':
    MyApp().run()
