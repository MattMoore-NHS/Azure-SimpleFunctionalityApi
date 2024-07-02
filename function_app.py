import azure.functions as func
import logging

import re

app = func.FunctionApp(http_auth_level=func.AuthLevel.ANONYMOUS)

@app.route(route="email_validation")
def email_validation(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    headers = {"Content-Type":"application/json"}

    try:
        req_body = req.get_json()
    except ValueError:
        pass
    else:
        email = req_body.get('email')

    if not email:
        return func.HttpResponse(
            "bad request",
            status_code=400,
            headers=headers
        )

    valid = validate_email_syntax(email)

    return func.HttpResponse(
            f"{valid}",
            status_code=200,
            headers=headers
        )


def validate_email_syntax(email: str) -> bool:

    # make sure email is a string
    if type(email) != str:
        return False
    
    # disallow double '.' - couldn't figure out how to do it in regex
    if '..' in email:
        return False
        
    # regular expression syntax for further string validation
    # if re.match(re.compile(r"^(?!\.)[a-zA-Z0-9_.+-]+(?<!\.)@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]*[a-zA-Z0-9]$"), email) is None:
    #     return False
    
    # Modified RFC 5322 Standard. Removes special characters from local and domain (!#$%&\*+/=?^_`{|}~), stopping strings from starting and finishing with special characters, and stopping double special characters
    # Original: r"^(?=.{1,256})(?=.{1,64}@.{1,255})((?=[a-zA-Z0-9!#$%&\'*+/=?^_`{|}~.-]{1,64}@)(?!.*[.]{2})[^.@][a-zA-Z0-9!#$%&\'*+/=?^_`{|}~.-]{0,63}(?<![.])@((?!-)[a-zA-Z0-9-]{1,63}(?<!-)\.){1,8}[a-zA-Z]{2,63})$"
    if re.match(re.compile(r"^(?=.{1,256})(?=.{1,64}@.{1,255})((?=[a-zA-Z0-9'.-]{1,64}@)(?!.*[.]{2})(?!.*[']{2})(?!.*[-]{2})(?!.*[@]{2})[^.@'-][a-zA-Z0-9'.-]{0,62}(?<![.'-])@((?!-)[a-zA-Z0-9-]{1,63}(?<!-)\.){1,8}[a-zA-Z]{2,63})$"), email) is None:
        return False

    return True
