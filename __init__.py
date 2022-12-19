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
        else:
            self.speak_dialog('negative.homelightautomation')


def create_skill():
    return Homelightautomation()
