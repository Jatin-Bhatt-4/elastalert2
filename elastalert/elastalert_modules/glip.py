#This is the python program which sends elastalert to RingCentral Glip
import copy
import json
import requests
import warnings
import sys
sys.path.append('/etc/elastalert/elastalert_modules')
from elastalert.alerts import Alerter, DateTimeEncoder
from elastalert.util import elastalert_logger, EAException, lookup_es_key
from requests.exceptions import RequestException


class GlipAlerter(Alerter):
    """ Creates a RingCentral Glip message for each alert """
    required_options = frozenset(['glip_webhook_url'])

    def __init__(self, rule):
        super(GlipAlerter, self).__init__(rule)
        self.glip_webhook_url = self.rule.get('glip_webhook_url', None)
        if isinstance(self.glip_webhook_url, str):
            self.glip_webhook_url = [self.glip_webhook_url]
        self.glip_proxy = self.rule.get('glip_proxy', None)
        self.glip_text_string = self.rule.get('glip_text_string', '')
        self.glip_alert_fields = self.rule.get('glip_alert_fields', '')
        self.glip_ignore_ssl_errors = self.rule.get('glip_ignore_ssl_errors', False)
        self.glip_timeout = self.rule.get('glip_timeout', 10)
        self.glip_ca_certs = self.rule.get('glip_ca_certs')

    def format_body(self, body):
        # Format the message body as needed for RingCentral Glip
        return body

    def alert(self, matches):
        body = self.create_alert_body(matches)
        body = self.format_body(body)
        # Post to RingCentral Glip
        headers = {'content-type': 'application/json'}
        # Set https proxy if provided
        proxies = {'https': self.glip_proxy} if self.glip_proxy else None
        payload = {
            'text': self.glip_text_string + '\n' + body,
        }

        # If we have defined fields, populate noteable fields for the alert
        if self.glip_alert_fields != '':
            payload['fields'] = self.populate_fields(matches)

        # Print the payload for debugging
        print("Debug: Glip Payload:", json.dumps(payload, cls=DateTimeEncoder, indent=2))

        for url in self.glip_webhook_url:
            try:
                if self.glip_ca_certs:
                    verify = self.glip_ca_certs
                else:
                    verify = not self.glip_ignore_ssl_errors
                if self.glip_ignore_ssl_errors:
                    requests.packages.urllib3.disable_warnings()
                response = requests.post(
                    url, data=json.dumps(payload, cls=DateTimeEncoder),
                    headers=headers, verify=verify,
                    proxies=proxies,
                    timeout=self.glip_timeout)
                warnings.resetwarnings()
                response.raise_for_status()
            except RequestException as e:
                raise EAException("Error posting to RingCentral Glip: %s" % e)
        elastalert_logger.info("Alert '%s' sent to RingCentral Glip" % self.rule['name'])

    def get_info(self):
        return {'type': 'glip'}

    def populate_fields(self, matches):
        alert_fields = []
        for arg in self.glip_alert_fields:
            arg = copy.copy(arg)
            arg['value'] = lookup_es_key(matches[0], arg['value'])
            alert_fields.append(arg)
        return alert_fields

