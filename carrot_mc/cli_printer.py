class CliEventPrinter:
    def handle(self, event: str, payload):
        method_name = 'handle_' + event.replace(' ', '_')
        if hasattr(self, method_name):
            method = getattr(self, method_name)
            method(payload)

    def handle_info(self, payload):
        print(payload)