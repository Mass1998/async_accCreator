import requests
import asyncio
import random
import sys


url = 'https://secure.runescape.com/m=account-creation/create_account'
s = requests.session()
createdAccs = []

async def submitCaptcha():
    from python3_anticaptcha import NoCaptchaTaskProxyless

    ANTICAPTCHA_KEY = 'Captcha Password Key'  # Anticaptcha service key.
    SITE_KEY = '6Lcsv3oUAAAAAGFhlKrkRb029OHio098bbeyi_Hv'  # G-ReCaptcha google key.

    # Get string for solve captcha, and other info.
    user_answer = NoCaptchaTaskProxyless.NoCaptchaTaskProxyless(anticaptcha_key = ANTICAPTCHA_KEY)\
                    .captcha_handler(websiteURL=url, websiteKey=SITE_KEY)

    newKey = user_answer['solution'].get('gRecaptchaResponse')
    print("Key: {}".format(newKey))
    return newKey


def getEmailPrefix():  # Generates email prefix
    prefix = "abcdefghijklmnopqrstuvwxyz123456789"
    return "".join((random.choice(prefix) for i in range(random.randint(6, 11))))


def getEmailSuffix():  # Generates email suffix
    suffix = "gmail.com protonmail.com yahoo.com aol.com hotmail.com outlook.ca outlook.com outlook.com icloud.com mail.com".split()
    return random.choice(suffix)


async def createAccount():
    if requests.get(url).ok == False:
        sys.exit(0)

    email = getEmailPrefix() + '@' + getEmailSuffix()
    passwd = 'YOUR PASSWORD'
    day = random.randint(1, 29)
    month = random.randint(1, 12)
    year = random.randint(1970, 2000)

    accInfo = {
        'email1': email,
        'onlyOneEmail': '1',
        'password1': passwd,
        'onlyOnePassword': '1',
        'day': day,
        'month': month,
        'year': year,
        'create-submit': 'create',
        'g-recaptcha-response': await submitCaptcha(),
    }

    asyncio.sleep(2)

    botAcc = accInfo['email1'] + ':' + accInfo['password1']

    r = s.post(url, data=accInfo)

    if "Account Created - RuneScape" in r.text:
        print('Account Created: {}'.format(botAcc))
        createdAccs.append(botAcc)
    else:
        print("Account creation failed.")

    print(createdAccs)


async def main():
    for i in range(make):
        loop.create_task(createAccount())

if __name__ == '__main__':
    makeString = input('Enter the amount of accounts you want to create: ')
    make = int(makeString)

    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
