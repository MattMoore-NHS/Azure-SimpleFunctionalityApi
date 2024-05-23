import azure.functions as func
import logging

import re

app = func.FunctionApp(http_auth_level=func.AuthLevel.FUNCTION)

@app.route(route="email_validation", methods=["POST"])
def email_validation(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

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
        )

    valid = validate_email_syntax(email)

    return func.HttpResponse(
            f"{valid}",
            status_code=200,
        )


def validate_email_syntax(email: str) -> bool:

    if type(email) != str:
        return False
        
    # regular expression syntax for email address validation
    email_regex = re.compile(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)")
    return re.match(email_regex, email) is not None
