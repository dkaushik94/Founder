# -*- coding: utf-8 -*-
from __future__ import absolute_import


from boto.s3.connection import S3Connection, Key
from boto import ses
import sys
import boto
import traceback
import logging

#from .constants import CONST_EMAIL_FROM

from portal.settings import S3_ACCESS_KEY, S3_BUCKET_NAME, S3_SECRET_ACCESS_KEY


win_botohelper_logger = logging.getLogger(__name__)


def upload_image(file_path, file_name):
    '''Get a upload url
    Return key_name, url
    '''
    conn = S3Connection(S3_ACCESS_KEY, S3_SECRET_ACCESS_KEY)
    bucket = conn.get_bucket(S3_BUCKET_NAME)

    def percent_cb(complete, total):
        sys.stdout.write('.')
        sys.stdout.flush()

    k = Key(bucket)
    k.key = file_name
    if file_path:
        file_path = file_path + file_name
    else:
        file_path = "/home/saksham/startupportal/portal/media/" + (str(file_name))
    
    k.set_contents_from_filename(file_path, cb=percent_cb, num_cb=10)
    k.set_acl('public-read')
    win_botohelper_logger.debug("upload_image doc upload with %s name" % str(file_name) )
    return file_name
