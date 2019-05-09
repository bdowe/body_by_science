class EmailSubscriptionError(Exception):
    def __init__(self, message):
        self.message = message

class UserNotExistsError(EmailSubscriptionError):
    pass

class IncorrectPasswordError(EmailSubscriptionError):
    pass

class EmailAlreadyRegisteredError(EmailSubscriptionError):
    def __init__(self):
        message = "Error: Email already registered"
        EmailSubscriptionError.__init__(self, message=message)

class InvalidEmailError(EmailSubscriptionError):
    def __init__(self):
        message = "Error: Invalid email"
        EmailSubscriptionError.__init__(self, message=message)