"""Staging Settings"""
from .base import *

DEBUG = True
ALLOWED_HOSTS = ['api.dev.officersurvey.com', 'officersurvey-dev.eba-9eag3efh.us-west-2.elasticbeanstalk.com',
                 '127.0.0.1', 'http://os-stag.eba-y23myxvy.us-west-2.elasticbeanstalk.com']

# ALLOWED_HOSTS = ["*"]
CORS_ORIGIN_WHITELIST = [
    "https://dev.officersurvey.com",
    "https://www.dev.officersurvey.com"
]
