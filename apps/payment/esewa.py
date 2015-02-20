from datetime import datetime
import urllib

from django.conf import settings
from django.db import models
import requests
from jsonfield import JSONField


class EsewaTransaction(models.Model):
    amount = models.FloatField()
    pid = models.CharField(max_length=255)
    tax_amount = models.FloatField(default=0)
    service_charge = models.FloatField(default=0)
    delivery_charge = models.FloatField(default=0)
    datetime = models.DateTimeField(default=datetime.now)
    details = JSONField()

    def __init__(self, *args, **kwargs):
        self.debug = getattr(settings, 'ESEWA_DEBUG', False)
        self.scd = getattr(settings, 'ESEWA_SCD')
        if self.debug:
            self.url = 'http://dev.esewa.com.np/epay/main'
            self.verification_url = 'http://dev.esewa.com.np/epay/transrec'
            self.transaction_url = 'http://dev.esewa.com.np/epay/transdetails'
        else:
            self.url = 'https://esewa.com.np/epay/main'
            self.verification_url = 'https://esewa.com.np/epay/transrec'
            self.transaction_url = 'https://esewa.com.np/epay/transdetails'
        super(EsewaTransaction, self).__init__(*args, **kwargs)

    def clear_details(self):
        self.details = {}

    def get_details(self):
        if self.details:
            return self.details
        kwargs = {'amt': self.amount, 'pid': self.pid, 'scd': self.scd}
        url = self.transaction_url+'?' + urllib.urlencode(kwargs)
        response = requests.get(url)
        self.details = response.json()
        return self.details

    def refresh_details(self):
        self.clear_details()
        return self.get_details()

    def verify(self):
        details = self.get_details()
        if details['code'] == '00' and float(details['txnDetail']['amt']) == self.amount:
            return True
        return False

    class Meta:
        abstract = True