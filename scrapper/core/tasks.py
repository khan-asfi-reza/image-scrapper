"""
Note:
    The bottom usage/features is just implemented but due to complexity to setup
    To check the usage of celery, must install Redis
"""
from celery import shared_task

from scrapper.core.models import Address


@shared_task()
def sync_images():
    Address.sync_url_images()
