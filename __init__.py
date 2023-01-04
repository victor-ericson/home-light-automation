import time
import RPi.GPIO as GPIO

from mycroft import MycroftSkill, intent_file_handler

livingroom = 17  # physical pin 11
bedroom = 18  # physical pin 12
kitchen = 19  # physical pin 35


class Homelightautomation(MycroftSkill):
    def __init__(self):
        MycroftSkill.__init__(self)
        global pwm_bedroom
        global pwm_livingroom
        global pwm_kitchen
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(livingroom, GPIO.OUT)
        GPIO.setup(bedroom, GPIO.OUT)
        GPIO.setup(kitchen, GPIO.OUT)
        pwm_bedroom = GPIO.PWM(bedroom, 100)
        pwm_livingroom = GPIO.PWM(livingroom, 100)
        pwm_kitchen = GPIO.PWM(kitchen, 100)
        pwm_bedroom.start(0)
        pwm_livingroom.start(0)
        pwm_kitchen.start(0)
        

    # Called after skill loads
    def initialize(self):
        self.log.info("Skill loaded")

    # called when skill is activated
    @intent_file_handler('turnon.intent')
    def handle_turnon(self, message):

        action = message.data.get('action')

        if action.casefold() == "living room":
            if pwm_livingroom.duty_cycle == 100:
                self.speak_dialog("living room already on")
            else:
                pwm_livingroom.ChangeDutyCycle(100) 
                self.speak_dialog("illuminating living room")
        elif action.casefold() == "bedroom":
            if pwm_bedroom.duty_cycle == 100:
                self.speak_dialog("bedroom already on")
            else:
                pwm_bedroom.ChangeDutyCycle(100)
                self.speak_dialog("illuminating bedroom")
        elif action.casefold() == "kitchen":
            if pwm_kitchen.duty_cycle == 100:
                self.speak_dialog("kitchen already on")
            else:
                pwm_kitchen.ChangeDutyCycle(100)
                self.speak_dialog("illuminating kitchen")
        elif action.casefold() == "all lights":
            if pwm_livingroom.duty_cycle == 100 and pwm_bedroom.duty_cycle == 100 and pwm_kitchen.duty_cycle == 100:
                self.speak_dialog("all lights are already on")
            else:
                pwm_livingroom.ChangeDutyCycle(100)
                pwm_bedroom.ChangeDutyCycle(100)
                pwm_kitchen.ChangeDutyCycle(100)
                self.speak_dialog("illuminating all lights")
        else:
            self.speak_dialog('negative.homelightautomation')

    @intent_file_handler('turnoff.intent')
    def handle_turnoff(self, message):

        action = message.data.get('action')

        if action.casefold() == "living room":
            if pwm_livingroom.duty_cycle > 0:
                pwm_livingroom.ChangeDutyCycle(0)
                self.speak_dialog("turning off living room")
            else:
                self.speak_dialog("living room already off")
        elif action.casefold() == "bedroom":
            if pwm_bedroom.duty_cycle > 0:
                pwm_bedroom.ChangeDutyCycle(0)
                self.speak_dialog("turning off bedroom")
            else:
                self.speak_dialog("bedroom already off")
        elif action.casefold() == "kitchen":
            if pwm_kitchen.duty_cycle > 0:
                pwm_kitchen.ChangeDutyCycle(0)
                self.speak_dialog("turning off kitchen")
            else:
                self.speak_dialog("kitchen already off")
        elif action.casefold() == "all lights":
            if pwm_livingroom.duty_cycle > 0 or pwm_bedroom.duty_cycle > 0 or pwm_kitchen.duty_cycle > 0:
                pwm_livingroom.ChangeDutyCycle(0)
                pwm_bedroom.ChangeDutyCycle(0)
                pwm_kitchen.ChangeDutyCycle(0)
                self.speak_dialog("turning off all lights")
            else:
                self.speak_dialog("all lights are already off")
        else:
            self.speak_dialog('negative.homelightautomation')

    @intent_file_handler('status.intent')
    def check_status(self, message):
        action = message.data.get('action')

        if action.casefold() == "living room":
            if pwm_livingroom.duty_cycle > 0:
                self.speak_dialog("living room is on")
            else:
                self.speak_dialog("living room is off")
        elif action.casefold() == "bedroom":
            if pwm_bedroom.duty_cycle > 0:
                self.speak_dialog("bedroom is on")
            else:
                self.speak_dialog("bedroom is off")
        elif action.casefold() == "kitchen":
            if pwm_kitchen.duty_cycle > 0:
                self.speak_dialog("kitchen is on")
            else:
                self.speak_dialog("kitchen is off")
        elif action.casefold() == "all":
            if pwm_livingroom.duty_cycle > 0:
                self.speak_dialog("living room is on")
            else:
                self.speak_dialog("living room is off")
            if pwm_bedroom.duty_cycle > 0:
                self.speak_dialog("bedroom is on")
            else:
                self.speak_dialog("bedroom is off")
            if pwm_kitchen.duty_cycle > 0:
                self.speak_dialog("kitchen is on")
            else:
                self.speak_dialog("kitchen is off")
        else:
            self.speak_dialog('negative.homelightautomation')

    @intent_file_handler('dimmer.intent')
    def handle_dimming(self, message):
        action = message.data.get('action')
        if action.casefold() == "living room":
            if pwm_livingroom.duty_cycle == 0:
                self.speak_dialog("living room already off")
                return
            pwm_livingroom.ChangeDutyCycle(pwm_livingroom.duty_cycle - 20)
            if(pwm_livingroom.duty_cycle == 0):
                self.speak_dialog("turning off living room")
        elif action.casefold() == "bedroom":
            if pwm_bedroom.duty_cycle == 0:
                self.speak_dialog("bedroom already off")
                return
            pwm_bedroom.ChangeDutyCycle(pwm_bedroom.duty_cycle - 20)
            if(pwm_bedroom.duty_cycle == 0):
                self.speak_dialog("turning off bedroom")
        elif action.casefold() == "kitchen":
            if pwm_kitchen.duty_cycle == 0:
                self.speak_dialog("kitchen already off")
                return             
            pwm_kitchen.ChangeDutyCycle(pwm_kitchen.duty_cycle - 20)
            if(pwm_kitchen.duty_cycle == 0):
                self.speak_dialog("turning off kitchen")
        else:
            self.speak_dialog('negative.homelightautomation')
            return


def create_skill():
    return Homelightautomation()
