import time
import RPi.GPIO as GPIO

from mycroft import MycroftSkill, intent_file_handler

livingroom = 17  # physical pin 11
bedroom = 18  # physical pin ...
kitchen = 19  # physical pin ...


class Homelightautomation(MycroftSkill):
    def __init__(self):
        MycroftSkill.__init__(self)

        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(livingroom, GPIO.OUT)
        GPIO.setup(bedroom, GPIO.OUT)
        GPIO.setup(kitchen, GPIO.OUT)

    # Called after skill loads
    def initialize(self):
        self.log.info("Skill loaded")

    # called when skill is activated
    @intent_file_handler('turnon.intent')
    def handle_turnon(self, message):

        action = message.data.get('action')

        if action.casefold() == "living room":
            if GPIO.input(livingroom):
                self.speak_dialog("living room already on")
            else:
                GPIO.output(livingroom, GPIO.HIGH)
                self.speak_dialog("illuminating living room")
        elif action.casefold() == "bedroom":
            if GPIO.input(bedroom):
                self.speak_dialog("bedroom already on")
            else:
                GPIO.output(bedroom, GPIO.HIGH)
                self.speak_dialog("illuminating bedroom")
        elif action.casefold() == "kitchen":
            if GPIO.input(kitchen):
                self.speak_dialog("kitchen already on")
            else:
                GPIO.output(kitchen, GPIO.HIGH)
                self.speak_dialog("illuminating kitchen")
        elif action.casefold() == "all lights":
            if GPIO.input(livingroom) and GPIO.input(bedroom) and GPIO.input(kitchen):
                self.speak_dialog("all lights are already on")
            else:
                GPIO.output(livingroom, GPIO.HIGH)
                GPIO.output(bedroom, GPIO.HIGH)
                GPIO.output(kitchen, GPIO.HIGH)
                self.speak_dialog("illuminating all lights")
        else:
            self.speak_dialog('negative.homelightautomation')

    @intent_file_handler('turnoff.intent')
    def handle_turnoff(self, message):

        action = message.data.get('action')

        if action.casefold() == "living room":
            if GPIO.input(livingroom):
                GPIO.output(livingroom, GPIO.LOW)
                self.speak_dialog("turning off living room")
            else:
                self.speak_dialog("living room already off")
        elif action.casefold() == "bedroom":
            if GPIO.input(bedroom):
                GPIO.output(bedroom, GPIO.LOW)
                self.speak_dialog("turning off bedroom")
            else:
                self.speak_dialog("bedroom already off")
        elif action.casefold() == "kitchen":
            if GPIO.input(kitchen):
                GPIO.output(kitchen, GPIO.LOW)
                self.speak_dialog("turning off kitchen")
            else:
                self.speak_dialog("kitchen already off")
        elif action.casefold() == "all lights":
            if GPIO.input(livingroom) or GPIO.input(bedroom) or GPIO.input(kitchen):
                GPIO.output(livingroom, GPIO.LOW)
                GPIO.output(bedroom, GPIO.LOW)
                GPIO.output(kitchen, GPIO.LOW)
                self.speak_dialog("turning off all lights")
            else:
                self.speak_dialog("all lights are already off")
        else:
            self.speak_dialog('negative.homelightautomation')

    @intent_file_handler('status.intent')
    def check_status(self, message):
        action = message.data.get('action')

        if action.casefold() == "living room":
            if GPIO.input(livingroom):
                self.speak_dialog("living room is on")
            else:
                self.speak_dialog("living room is off")
        elif action.casefold() == "bedroom":
            if GPIO.input(bedroom):
                self.speak_dialog("bedroom is on")
            else:
                self.speak_dialog("bedroom is off")
        elif action.casefold() == "kitchen":
            if GPIO.input(kitchen):
                self.speak_dialog("kitchen is on")
            else:
                self.speak_dialog("kitchen is off")
        elif action.casefold() == "all":
            if GPIO.input(livingroom):
                self.speak_dialog("living room is on")
            else:
                self.speak_dialog("living room is off")
            if GPIO.input(bedroom):
                self.speak_dialog("bedroom is on")
            else:
                self.speak_dialog("bedroom is off")
            if GPIO.input(kitchen):
                self.speak_dialog("kitchen is on")
            else:
                self.speak_dialog("kitchen is off")
        else:
            self.speak_dialog('negative.homelightautomation')

    @intent_file_handler('dimmer.intent')
    def handle_dimming(self, message):
        room = message.data.get('room')
        dimming = message.data.get('dimming')
        if room.casefold() == "living room":
            pin = livingroom
        elif room.casefold() == "bedroom":
            pin = bedroom
        elif room.casefold() == "kitchen":
            pin = kitchen
        else:
            self.speak_dialog('negative.homelightautomation')
            return

        # Set the pin to PWM mode and set the frequency to 100 Hz
        pwm = GPIO.PWM(pin, 100)
        # Start PWM with a duty cycle of 0%
        pwm.start(0)
        pwm.ChangeDutyCycle(dimming)


def create_skill():
    return Homelightautomation()
