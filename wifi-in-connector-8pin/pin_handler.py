class PinHandler:
    def __init__(self, pins, pin_numbers):
        self.pins = pins
        self.pin_numbers = pin_numbers

    def handle_request(self, request):
        for i in range(len(self.pin_numbers)):
            if f"/pin{self.pin_numbers[i]}/on" in request:
                self.pins[i].on()
            elif f"/pin{self.pin_numbers[i]}/off" in request:
                self.pins[i].off()

        if "/allpin/on" in request:
            for i in range(len(self.pin_numbers)):
                self.pins[i].on()

        elif "/allpin/off" in request:
            for i in range(len(self.pin_numbers)):
                self.pins[i].off()