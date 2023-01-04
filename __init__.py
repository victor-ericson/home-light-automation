import time
import RPi.GPIO as GPIO

from mycroft import MycroftSkill, intent_file_handler

livingroom = 17  # physical pin 11
bedroom = 18  # physical pin 12
kitchen = 19  # physical pin 35


class Homelightautomation(MycroftSkill):
    def __init__(self):
        # self.pwm_bedroom_get_duty_cycle = 0
        # self.pwm_livingroom_get_duty_cycle = 0
        # self.pwm_kitchen_get_duty_cycle = 0

        MycroftSkill.__init__(self)
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(livingroom, GPIO.OUT)
        GPIO.setup(bedroom, GPIO.OUT)
        GPIO.setup(kitchen, GPIO.OUT)
        self.pwm_bedroom = GPIO.PWM(bedroom, 100)
        self.pwm_livingroom = GPIO.PWM(livingroom, 100)
        self.pwm_kitchen = GPIO.PWM(kitchen, 100)
        self.pwm_bedroom.start(0)
        self.pwm_livingroom.start(0)
        self.pwm_kitchen.start(0)
        self.pwm_bedroom_get_duty_cycle = 0
        self.pwm_livingroom_get_duty_cycle = 0
        self.pwm_kitchen_get_duty_cycle = 0




    # Called after skill loads
    def initialize(self):
        self.log.info("Skill loaded")

    # called when skill is activated
    @intent_file_handler('turnon.intent')
    def handle_turnon(self, message):

        action = message.data.get('action')

        if action.casefold() == "living room":
            if self.pwm_livingroom_get_duty_cycle == 100:
                self.speak_dialog("living room already on")
            else:
                self.pwm_livingroom.ChangeDutyCycle(100)
                self.pwm_livingroom_get_duty_cycle = 100
                self.speak_dialog("illuminating living room")
        elif action.casefold() == "bedroom":
            if self.pwm_bedroom_get_duty_cycle == 100:
                self.speak_dialog("bedroom already on")
            else:
                self.pwm_bedroom.ChangeDutyCycle(100)
                self.pwm_bedroom_get_duty_cycle = 100
                self.speak_dialog("illuminating bedroom")
        elif action.casefold() == "kitchen":
            if self.pwm_kitchen_get_duty_cycle == 100:
                self.speak_dialog("kitchen already on")
            else:
                self.pwm_kitchen.ChangeDutyCycle(100)
                self.pwm_kitchen_get_duty_cycle = 100
                self.speak_dialog("illuminating kitchen")
        elif action.casefold() == "all lights":
            if self.pwm_livingroom_get_duty_cycle == 100 and self.pwm_bedroom_get_duty_cycle == 100 and self.pwm_kitchen_get_duty_cycle == 100:
                self.speak_dialog("all lights are already on")
            else:
                self.pwm_livingroom.ChangeDutyCycle(100)
                self.pwm_bedroom.ChangeDutyCycle(100)
                self.pwm_kitchen.ChangeDutyCycle(100)
                self.pwm_livingroom_get_duty_cycle = 100
                self.pwm_bedroom_get_duty_cycle = 100
                self.pwm_kitchen_get_duty_cycle = 100
                self.speak_dialog("illuminating all lights")
        else:
            self.speak_dialog('negative.homelightautomation')

    @intent_file_handler('turnoff.intent')
    def handle_turnoff(self, message):

        action = message.data.get('action')

        if action.casefold() == "living room":
            if self.pwm_livingroom_get_duty_cycle > 0:
                self.pwm_livingroom.ChangeDutyCycle(0)
                self.pwm_livingroom_get_duty_cycle = 0
                self.speak_dialog("turning off living room")
            else:
                self.speak_dialog("living room already off")
        elif action.casefold() == "bedroom":
            if self.pwm_bedroom_get_duty_cycle > 0:
                self.pwm_bedroom.ChangeDutyCycle(0)
                self.pwm_bedroom_get_duty_cycle = 0
                self.speak_dialog("turning off bedroom")
            else:
                self.speak_dialog("bedroom already off")
        elif action.casefold() == "kitchen":
            if self.pwm_kitchen_get_duty_cycle > 0:
                self.pwm_kitchen.ChangeDutyCycle(0)
                self.pwm_kitchen_get_duty_cycle = 0
                self.speak_dialog("turning off kitchen")
            else:
                self.speak_dialog("kitchen already off")
        elif action.casefold() == "all lights":
            if self.pwm_livingroom_get_duty_cycle > 0 or self.pwm_bedroom_get_duty_cycle > 0 or self.pwm_kitchen_get_duty_cycle > 0:
                self.pwm_livingroom.ChangeDutyCycle(0)
                self.pwm_bedroom.ChangeDutyCycle(0)
                self.pwm_kitchen.ChangeDutyCycle(0)
                self.pwm_livingroom_get_duty_cycle = 0
                self.pwm_bedroom_get_duty_cycle = 0
                self.pwm_kitchen_get_duty_cycle = 0
                self.speak_dialog("turning off all lights")
            else:
                self.speak_dialog("all lights are already off")
        else:
            self.speak_dialog('negative.homelightautomation')

    @intent_file_handler('status.intent')
    def check_status(self, message):
        action = message.data.get('action')

        if action.casefold() == "living room":
            if self.pwm_livingroom_get_duty_cycle > 0:
                self.speak_dialog("living room is on")
            else:
                self.speak_dialog("living room is off")
        elif action.casefold() == "bedroom":
            if self.pwm_bedroom_get_duty_cycle > 0:
                self.speak_dialog("bedroom is on")
            else:
                self.speak_dialog("bedroom is off")
        elif action.casefold() == "kitchen":
            if self.pwm_kitchen_get_duty_cycle > 0:
                self.speak_dialog("kitchen is on")
            else:
                self.speak_dialog("kitchen is off")
        elif action.casefold() == "all":
            if self.pwm_livingroom_get_duty_cycle > 0:
                self.speak_dialog("living room is on")
            else:
                self.speak_dialog("living room is off")
            if self.pwm_bedroom_get_duty_cycle > 0:
                self.speak_dialog("bedroom is on")
            else:
                self.speak_dialog("bedroom is off")
            if self.pwm_kitchen_get_duty_cycle > 0:
                self.speak_dialog("kitchen is on")
            else:
                self.speak_dialog("kitchen is off")
        else:
            self.speak_dialog('negative.homelightautomation')

    @intent_file_handler('dimmer.intent')
    def handle_dimming(self, message):
        action = message.data.get('action')
        if action.casefold() == "living room":
            if self.pwm_livingroom_get_duty_cycle == 0:
                self.speak_dialog("living room already off")
                return
            self.pwm_livingroom.ChangeDutyCycle(self.pwm_livingroom_get_duty_cycle - 20)
            if(self.pwm_livingroom_get_duty_cycle == 0):
                self.speak_dialog("turning off living room")
        elif action.casefold() == "bedroom":
            if self.pwm_bedroom_get_duty_cycle == 0:
                self.speak_dialog("bedroom already off")
                return
            self.pwm_bedroom.ChangeDutyCycle(self.pwm_bedroom_get_duty_cycle - 20)
            if(self.pwm_bedroom_get_duty_cycle == 0):
                self.speak_dialog("turning off bedroom")
        elif action.casefold() == "kitchen":
            if self.pwm_kitchen_get_duty_cycle == 0:
                self.speak_dialog("kitchen already off")
                return             
            self.pwm_kitchen.ChangeDutyCycle(self.pwm_kitchen_get_duty_cycle - 20)
            if(self.pwm_kitchen_get_duty_cycle == 0):
                self.speak_dialog("turning off kitchen")
        else:
            self.speak_dialog('negative.homelightautomation')
            return


def create_skill():
    return Homelightautomation()
