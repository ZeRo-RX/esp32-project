class HtmlGenerator:
    def __init__(self, pins: list):
        self.html_start = """<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>ESP32 Web Server</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css" rel="stylesheet"
        integrity="sha384-T3c6CoIi6uLrA9TneNEoa7RxnatzjcDSCmG1MXxSR1GAsXEV/Dwwykc2MPK8M2HN" crossorigin="anonymous" />
</head>

<body data-bs-theme="dark" class="text-center">
    <nav class="navbar bg-body-tertiary">
        <div class="container-fluid">
            <a class="navbar-brand" href="#">ESP32 Web Server</a>
        </div>
    </nav>
    <br />
        """
        self.html_end = """
            <button class="btn btn-primary" onclick="window.location.href='/allpin/on'">
                All Pins On
            </button>
            <button class="btn btn-danger" onclick="window.location.href='/allpin/off'">
                All Pins Off
            </button>
            <hr />
        <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/js/bootstrap.bundle.min.js"
        integrity="sha384-C6RzsynM9kWDrMNeT87bh95OGNyZPhcTNXj1NW7RuBCsyN/o0jlpcV8Qyq46cDfL"
        crossorigin="anonymous"></script>
</body>

</html>
        """
        self.pins = pins

    def single_button_generator(self, pin_num) -> str:
        button = f"""
            <button class="btn btn-primary" onclick="window.location.href='/pin{pin_num}/on'">
                Pin{pin_num}
            </button>
            <button class="btn btn-danger" onclick="window.location.href='/pin{pin_num}/off'">
                Pin{pin_num}
            </button>
            <hr />"""
        return button

    def button_generator(self, pins: list) -> str:
        buttons = ""
        for pin in pins:
            buttons += self.single_button_generator(pin)
        return buttons

    def create_html(self):
        return self.html_start + self.button_generator(self.pins) + self.html_end

    def print_buttons(self):
        print(self.create_html())


if __name__ == "__main__":
    htmlGenerator = HtmlGenerator([1, 3, 4, 6, 188])
    htmlGenerator.print_buttons()

