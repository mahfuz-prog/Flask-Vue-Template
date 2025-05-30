import json
import hmac
import random
import hashlib
from flask import current_app

# generate a random 6 digit code
def generate_otp():
	otp = random.randint(0,999999)
	return f"{otp:06}"