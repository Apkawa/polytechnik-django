# -*- coding: utf-8 -*-
import os, sys
sys.path.append('/home/apkawa/Code/work')
os.environ['DJANGO_SETTINGS_MODULE'] = 'polytechnik.settings_remote'
from django.core.management import setup_environ
from polytechnik import settings_remote

setup_environ(settings_remote)
