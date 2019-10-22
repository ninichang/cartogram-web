import requests

def verify_recaptcha_response(secret_key, response):

    r = requests.post(
          "https://www.google.com/recaptcha/api/siteverify"
        , { "secret": secret_key
          , "response": response
          }
        )
    
    try:
        captcha_response = r.json()

        return captcha_response['success']
    
    except ValueError:

        return False

