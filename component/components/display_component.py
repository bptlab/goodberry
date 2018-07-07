from component import ActionComponent
from .lib.lcddriver import lcd as LCD
import math
from utils import get_logger


class DisplayComponent(ActionComponent):
    def __init__(self, device_id):
        self.logger = get_logger(__name__)
        ActionComponent.__init__(self, device_id)

    def trigger_action(self, value, **kwargs):
        lcd = LCD()
        lcd.lcd_clear()
        lines = value.split("\n")
        short_lines = []
        for i in range(0, len(lines)):
            for ii in range(0, int(math.ceil(len(lines[i])/16))):
                short_lines.append(lines[i][ii*16:(ii+1)*16])
        self.logger.info("Displaying:" + str(short_lines))
        for line_number, line_content in enumerate(short_lines):
            lcd.lcd_display_string(line_content, line_number + 1)

    @staticmethod
    def configure_action():
        print("The Display Action doesn't need to be configured.")
        return {}
