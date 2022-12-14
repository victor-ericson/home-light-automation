from mycroft import MycroftSkill, intent_file_handler


class Homelightautomation(MycroftSkill):
    def __init__(self):
        MycroftSkill.__init__(self)

    @intent_file_handler('homelightautomation.intent')
    def handle_homelightautomation(self, message):
        self.speak_dialog('homelightautomation')


def create_skill():
    return Homelightautomation()

