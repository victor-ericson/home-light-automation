import time
import RPi.GPIO as GPIO

from mycroft import MycroftSkill, intent_file_handler

livingroom = 17  # physical pin 11
bedroom = 18  # physical pin ...
kitchen = 19  # physical pin ...


class Homelightautomation(MycroftSkill):
    def __init__(self):
        MycroftSkill.__init__(self)

        self.brightness = {livingroom: 100,
                           bedroom: 100,
                           kitchen: 100}  # Dictionary to store the current brightness level for each light

        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(livingroom, GPIO.OUT)
        GPIO.setup(bedroom, GPIO.OUT)
        GPIO.setup(kitchen, GPIO.OUT)

    # Called after skill loads
    def initialize(self):
        self.log.info("Skill loaded")

    @intent_file_handler('turnon.intent')
    def handle_turnon(self, message):
        # Parse the action from the utterance
        action = message.data.get('action')

        if action.casefold() == "living room":
            if GPIO.input(livingroom):
                self.speak_dialog("living room already on")
            else:
                # Set the duty cycle for the living room light to the saved brightness level
                livingroom_light = GPIO.PWM(livingroom, 100)
                livingroom_light.start(self.brightness[livingroom])
                self.speak_dialog("illuminating living room")
        elif action.casefold() == "bedroom":
            if GPIO.input(bedroom):
                self.speak_dialog("bedroom already on")
            else:
                # Set the duty cycle for the bedroom light to the saved brightness level
                bedroom_light = GPIO.PWM(bedroom, 100)
                bedroom_light.start(self.brightness[bedroom])
                self.speak_dialog("illuminating bedroom")
        elif action.casefold() == "kitchen":
            if GPIO.input(kitchen):
                self.speak_dialog("kitchen already on")
            else:
                # Set the duty cycle for the kitchen light to the saved brightness level
                kitchen_light = GPIO.PWM(kitchen, 100)
                kitchen_light.start(self.brightness[kitchen])
                self.speak_dialog("illuminating kitchen")
        elif action.casefold() == "all lights":
            if GPIO.input(livingroom) and GPIO.input(bedroom) and GPIO.input(kitchen):
                self.speak_dialog("all lights are already on")
            else:
                # Set the duty cycles for all lights to the saved brightness levels
                livingroom_light = GPIO.PWM(livingroom, 100)
                livingroom_light.start(self.brightness[livingroom])
                bedroom_light = GPIO.PWM(bedroom, 100)
                bedroom_light.start(self.brightness[bedroom])
                kitchen_light = GPIO.PWM(kitchen, 100)
                kitchen_light.start(self.brightness[kitchen])
                self.speak_dialog("illuminating all lights")
        else:
            self.speak_dialog('negative.homelightautomation')

    @intent_file_handler('turnoff.intent')
    def handle_turnoff(self, message):
        # Parse the action from the utterance
        action = message.data.get('action')

        if action.casefold() == "living room":
            if GPIO.input(livingroom):
                # Stop the PWM signal for the living room light
                livingroom_light = GPIO.PWM(livingroom, 100)
                livingroom_light.stop()
                self.speak_dialog("turning off living room")
            else:
                self.speak_dialog("living room already off")
        elif action.casefold() == "bedroom":
            if GPIO.input(bedroom):
                # Stop the PWM signal for the bedroom light
                bedroom_light = GPIO.PWM(bedroom, 100)
                bedroom_light.stop()
                self.speak_dialog("turning off bedroom")
            else:
                self.speak_dialog("bedroom already off")
        elif action.casefold() == "kitchen":
            if GPIO.input(kitchen):
                # Stop the PWM signal for the kitchen light
                kitchen_light = GPIO.PWM(kitchen, 100)
                kitchen_light.stop()
                self.speak_dialog("turning off kitchen")
            else:
                self.speak_dialog("kitchen already off")
        elif action.casefold() == "all lights":
            if GPIO.input(livingroom) or GPIO.input(bedroom) or GPIO.input(kitchen):
                # Stop the PWM signals for all lights
                livingroom_light = GPIO.PWM(livingroom, 100)
                livingroom_light.stop()
                bedroom_light = GPIO.PWM(bedroom, 100)
                bedroom_light.stop()
                kitchen_light = GPIO.PWM(kitchen, 100)
                kitchen_light.stop()
                self.speak_dialog("turning off all lights")
            else:
                self.speak_dialog("all lights are already off")
        else:
            self.speak_dialog('negative.homelightautomation')

    @intent_file_handler('status.intent')
    def check_status(self, message):
        # Parse the action from the utterance
        action = message.data.get('action')

        if action.casefold() == "living room":
            if GPIO.input(livingroom):
                self.speak_dialog("living room is on, brightness is {}%".format(self.brightness[livingroom]))
            else:
                self.speak_dialog("living room is off")
        elif action.casefold() == "bedroom":
            if GPIO.input(bedroom):
                self.speak_dialog("bedroom is on, brightness is {}%".format(self.brightness[bedroom]))
            else:
                self.speak_dialog("bedroom is off")
        elif action.casefold() == "kitchen":
            if GPIO.input(kitchen):
                self.speak_dialog("kitchen is on, brightness is {}%".format(self.brightness[kitchen]))
            else:
                self.speak_dialog("kitchen is off")
        elif action.casefold() == "all lights":
            if GPIO.input(livingroom) or GPIO.input(bedroom) or GPIO.input(kitchen):
                self.speak_dialog("at least one light is on")
            else:
                self.speak_dialog("all lights are off")
        else:
            self.speak_dialog('negative.homelightautomation')

    @intent_file_handler('dimmer.intent')
    def dimmer(self, message):
        # Parse the action from the utterance
        action = message.data.get('action')

        if action.casefold() == "living room":
            # Check if the living room light is already dimmed
            if self.brightness[livingroom] == 50:
                self.speak_dialog("living room already dimmed")
            elif self.brightness[livingroom] == 100:
                # Set the duty cycle for the living room light to 50%
                livingroom_light = GPIO.PWM(livingroom, 100)
                livingroom_light.start(50)
                self.speak_dialog("dimming living room")
            else:
                # Update the brightness for the living room
                self.brightness[livingroom] = 50
                # Set the duty cycle for the living room light to 50%
                livingroom_light = GPIO.PWM(livingroom, 100)
                livingroom_light.start(50)
                self.speak_dialog("dimming living room")
        elif action.casefold() == "bedroom":
            # Check if the bedroom light is already dimmed
            if self.brightness[bedroom] == 50:
                self.speak_dialog("bedroom already dimmed")
            elif self.brightness[bedroom] == 100:
                # Set the duty cycle for the bedroom light to 50%
                bedroom_light = GPIO.PWM(bedroom, 100)
                bedroom_light.start(50)
                self.speak_dialog("dimming bedroom")
            else:
                # Update the brightness for the bedroom
                self.brightness[bedroom] = 50
                # Set the duty cycle for the bedroom light to 50%
                bedroom_light = GPIO.PWM(bedroom, 100)
                bedroom_light.start(50)
                self.speak_dialog("dimming bedroom")
        elif action.casefold() == "kitchen":
            # Check if the kitchen light is already dimmed
            if self.brightness[kitchen] == 50:
                self.speak_dialog("kitchen already dimmed")
            elif self.brightness[kitchen] == 100:
                # Set the duty cycle for the kitchen light to 50%
                kitchen_light = GPIO.PWM(kitchen, 100)
                kitchen_light.start(50)
                self.speak_dialog("dimming kitchen")
            else:
                # Update the brightness for the kitchen
                self.brightness[kitchen] = 50
                # Set the duty cycle for the kitchen light to 50%
                kitchen_light = GPIO.PWM(kitchen, 100)
                kitchen_light.start(50)
                self.speak_dialog("dimming kitchen")
        else:
            self.speak_dialog('negative.homelightautomation')


def create_skill():
    return Homelightautomation()
