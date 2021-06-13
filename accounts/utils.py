import random
import requests
from datetime import datetime, timedelta


def send_verification_code(phone, code):
    print(f'Verification code for "{phone}" is:\t{code}')
    ## This is for Kavenegar service and currently disabled
    # api_key = '324F7475397257796D69595A5874546E6E5442686B646E5830436347724C676878584A6A7552766748436B3D'
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