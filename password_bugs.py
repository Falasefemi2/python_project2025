class PasswordValidator:
    def __init__(self):
        self.min_length = 8
        self.password_history = []

    def validate_password(self, password):
        # Bug 1: Doesn't check for uppercase
        # Bug 2: Doesn't check for numbers
        # Bug 3: Allows common passwords
        if len(password) < self.min_length:
            return False
        if ' ' in password:
            return False
        return True

    def add_to_history(self, password):
        self.password_history.append(password)
        if len(self.password_history) > 5:
            self.password_history.pop(0)

    def check_history(self, password):
        return password not in self.password_history

def test_password():
    validator = PasswordValidator()
    test_cases = [
        "password123",  # Should fail (common password)
        "abcdefgh",    # Should fail (no uppercase/numbers)
        "Pass word1",  # Should fail (contains space)
        "Short1",      # Should fail (too short)
    ]
    
    for password in test_cases:
        result = validator.validate_password(password)
        print(f"Password {password}: {'Valid' if result else 'Invalid'}")

if __name__ == "__main__":
    test_password()