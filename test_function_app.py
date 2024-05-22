from function_app import validate_email_syntax
import unittest
import os
import sys

class TestEmailValidation(unittest.TestCase):

    def test_validate_email_syntax(self):

        # True email address = True
        self.assertTrue(validate_email_syntax("abc@yopmail.com"))

        # Email address with sub domain = True
        self.assertTrue(validate_email_syntax("abc@yopmail.subdomain.com"))

        # string ending in '.'
        self.assertFalse(validate_email_syntax("abc@yopmail.subdomain."))

        # string ending with @ '.'
        self.assertFalse(validate_email_syntax("abc@yopmail.subdomain@"))

        # Multiple @s
        self.assertFalse(validate_email_syntax("abc@@yopmail.com"))

        # Symbols
        self.assertFalse(validate_email_syntax("!"))
        self.assertFalse(validate_email_syntax("#"))

        # No string provided = False
        self.assertFalse(validate_email_syntax(""))

        # Name provided as string = False
        self.assertFalse(validate_email_syntax("John Smith"))

        # Integer provided = False
        self.assertFalse(validate_email_syntax(1))

        # List provided = False
        self.assertFalse(validate_email_syntax([]))

        # Dictionary provided = False
        self.assertFalse(validate_email_syntax({}))

        # Object provided = False
        self.assertFalse(validate_email_syntax(object))


if __name__ == "__main__":
    unittest.main(verbosity=2)
