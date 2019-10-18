import command

COMMAND_PREFIX = "another_module"
HELP_TEXT = """Dummy module:
================

Pretty useless module at the moment
"""

class Command(command.CommandBase):
    def do_get_iocs(self, line):
        """Dummy method with no real purpose"""
        print("Dummy method")
