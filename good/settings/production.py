import os

from .base import *  # NOQA

DEBUG = TEMPLATE_DEBUG = False
ALLOWED_HOSTS = ['debt.colinrolfe.com']
PIPELINE_ENABLED = True

TEMPLATE_DIRS = (
    ('/srv/vhosts/debt.colinrolfe.com/get-out-of-debt/templates'),
)

STATIC_ROOT = os.path.abspath(os.path.join(BASE_DIR, '..', '..', 'static'))
