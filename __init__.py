import time
import RPi.GPIO as GPIO
from mycroft import MycroftSkill, intent_file_handler

livingroom_led = 17  # physical pin 11


class Homelightautomation(MycroftSkill):
    def __init__(self):
        MycroftSkill.__init__(self)

        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(livingroom_led, GPIO.OUT)

    # Called after skill loads
    def initialize(self):
        self.log.info("Skill loaded")

    # called when skill is activated
    @intent_file_handler('turnon.intent')
    def handle_homelightautomation(self, message):
        self.speak_dialog('homelightautomation')

        action = message.data.get('action')

        if action.casefold() == "livingroom light":
            GPIO.output(livingroom_led, GPIO.HIGH)
        elif action.casefold() == "Bedroom light":
            GPIO.output(bedroom_led, GPIO.HIGH)
        elif action.casefold() == "Kitchen light":
            GPIO.output(kitchen_led, GPIO.HIGH)
        else:
            self.log.info("No can do")
            self.speak_dialog('negative.homelightautomation.dialog')

    @intent_file_handler('turnoff.intent')
    def handle_homelightautomation(self, message):
        self.speak_dialog('homelightautomation')

        action = message.data.get('action')

        if action.casefold() == "livingroom light":
            GPIO.output(livingroom_led, GPIO.LOW)
        elif action.casefold() == "Bedroom light":
            GPIO.output(bedroom_led, GPIO.LOW)
        elif action.casefold() == "Kitchen light":
            GPIO.output(kitchen_led, GPIO.LOW)
        else:
            self.log.info("No can do")
            self.speak_dialog('negative.homelightautomation.dialog')
def create_skill():
    return Homelightautomation()
