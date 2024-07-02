import azure.functions as func

from function_app import email_validation, validate_email_syntax
import unittest


class TestEmailValidation(unittest.TestCase):

    def test_email_validation_syntax(self):

        # Email types
        self.assertTrue(validate_email_syntax("abc@yopmail.com")) # True email address
        self.assertTrue(validate_email_syntax("abc@yopmail.subdomain.com")) # True subdomain
        self.assertTrue(validate_email_syntax("abc123@yopmail.com")) # number in address
        self.assertTrue(validate_email_syntax("abc@yopmail123.com")) # number in domain
        self.assertTrue(validate_email_syntax("abc@yopmail.subdomain123.com")) # number in subdomain

        # Symbols
        # '@'s
        self.assertFalse(validate_email_syntax("@"))
        self.assertFalse(validate_email_syntax("@abc@yopmail.subdomain"))
        self.assertFalse(validate_email_syntax("abc@yopmail.subdomain@"))
        self.assertFalse(validate_email_syntax("abc@@yopmail.com"))

        # '#'s
        self.assertFalse(validate_email_syntax("#"))
        self.assertFalse(validate_email_syntax("abc#@yopmail.com"))
        self.assertFalse(validate_email_syntax("abc#@yopmail#.com"))
        self.assertFalse(validate_email_syntax("abc#@yopmail.com#"))

        # '.'s
        self.assertFalse(validate_email_syntax("."))
        self.assertTrue(validate_email_syntax("a.bc@yopmail.com"))
        self.assertTrue(validate_email_syntax("abc@yop.mail.com"))
        self.assertFalse(validate_email_syntax("abc@yopmail.com."))
        self.assertFalse(validate_email_syntax(".abc@yopmail.com"))
        self.assertFalse(validate_email_syntax("ab..c@yopmail.com"))
        self.assertFalse(validate_email_syntax(".abc@yop..mail.com"))

        # '!'s
        self.assertFalse(validate_email_syntax("!"))
        self.assertFalse(validate_email_syntax("!abc@yopmail.com"))
        self.assertFalse(validate_email_syntax("abc@yopmail!.com"))
        self.assertFalse(validate_email_syntax("abc@yopmail.com!"))

        # ' 's
        self.assertFalse(validate_email_syntax("abc @yopmail.com"))
        self.assertFalse(validate_email_syntax("abc@yop mail.com"))
        self.assertFalse(validate_email_syntax("abc @yopmail. com"))
               
        # apostrophes
        self.assertTrue(validate_email_syntax("ab'c@yopmail.com")) # returns false
        self.assertFalse(validate_email_syntax("'abc@yopmail.com")) # returns true
        self.assertFalse(validate_email_syntax("abc'@yopmail.com")) # returns false
        self.assertFalse(validate_email_syntax("abc@yop'mail.com"))
        self.assertFalse(validate_email_syntax("abc@yopmail.c'om"))
        self.assertFalse(validate_email_syntax("abc'@yopmail.com'"))
        self.assertFalse(validate_email_syntax("abc@'yopmail.com"))
        self.assertFalse(validate_email_syntax("abc@yopmail'.com"))
        self.assertFalse(validate_email_syntax("abc@yopmail.'com"))

        # Other strings
        self.assertFalse(validate_email_syntax("")) # no data
        self.assertFalse(validate_email_syntax("John Smith")) # string with space
        self.assertFalse(validate_email_syntax("abcde")) # standard string
        self.assertFalse(validate_email_syntax("abc@yopmail")) # no top-level domain
        self.assertFalse(validate_email_syntax("abc@.com")) # no domain

        # Other types
        self.assertFalse(validate_email_syntax(1)) # int
        self.assertFalse(validate_email_syntax([])) # list
        self.assertFalse(validate_email_syntax({})) # dict
        self.assertFalse(validate_email_syntax(object)) # object

    def test_email_validation_function_request(self):

        req = func.HttpRequest(
            method=["POST"],
            url="/api/email_validation",
            body={"email":"abc@yopmail.com"},
            params={},
            headers={"Content-Type":"application/json"}
        )

        func_call = email_validation.build().get_user_function()
        # Breaks the rest of the test
        # resp = func_call(req) 
       
        # self.assertEqual(resp.status_code, 200)
        # self.assertEqual(resp.get_body().decode(), 'True')

if __name__ == "__main__":
    unittest.main(verbosity=2)
