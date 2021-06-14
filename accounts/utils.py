import random
import requests
from datetime import datetime, timedelta


def send_verification_code(phone, code):
    ## This is for Kavenegar service and currently disabled
    #  You can use Kavenagar python module too, but i prefferd to
    #  not use any external modules, so I used basic web request
    #  Also verification code print in django console for debugging
    print(f'Verification code at {datetime.now()} for "{phone}" is:\t{code}')

    # api_key = 'PASTE_YOUR_API_KEY_HERE'
    # url = f'https://api.kavenegar.com/v1/{api_key}/sms/send.json?receptor={phone}&sender=10004346&message={code}'
    # try:
    #     x = requests.get(url)
    #     if x.status_code != 200:
    #         # send one more time
    #         requests.get(url)
    # except:
    #     pass

        
        
def generate_code():
    code = random.randint(100000,999999)
    code_expire_datetime = datetime.now() + timedelta(minutes=2)
    return code, code_expire_datetime