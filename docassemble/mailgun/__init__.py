from typing import List, Optional

import requests
from bs4 import BeautifulSoup
from docassemble.base.core import DAFile
from docassemble.base.util import email_stringer, get_config, \
    mark_task_as_performed, send_email, value
from flask_mail import sanitize_addresses
from requests.auth import HTTPBasicAuth


class Mailgun:
    def __init__(self,
                 config_key: str = "mail",
                 url_key: str = "mailgun send url",
                 domain_key: str = "mailgun domain",
                 api_key_key: str = "mailgun api key",
                 default_sender_key: str = "default sender",
                 url: Optional[str] = None,
                 domain: Optional[str] = None,
                 api_key: Optional[str] = None,
                 default_sender: Optional[str] = None):
        config = get_config(config_key)
        self.url = url or config.get(url_key)
        self.domain = domain or config.get(domain_key)
        self.api_key = api_key or config.get(api_key_key)
        self.default_sender = default_sender or config.get(default_sender_key)
        self.template = None

    @staticmethod
    def _join_email(email):
        return ", ".join(sanitize_addresses(email_stringer(email,
                                                           include_name=True)))

    def send_lmr_email(
            self,
            to=None,
            sender=None,
            cc=None,
            bcc=None,
            body=None,
            html=None,
            subject="",
            template=None,
            task=None,
            attachments: List[DAFile] = None,
            mailgun_variables=None
    ):
        """
        Sends an email. This method is a drop-in replacement for docassemble's
        send_mail function. However this method will send the email using a
        pre-configured Mailgun template if possible. If not it falls back to the
        send_mail function.
        """
        if not all([self.url, self.domain, self.api_key, self.template]):
            return send_email(
                to=to,
                sender=sender,
                cc=cc,
                bcc=bcc,
                body=body,
                html=html,
                subject=subject,
                template=template,
                task=task,
                attachments=attachments,
                mailgun_variables=mailgun_variables
            )

        html = html or template.content_as_html()
        text = body or BeautifulSoup(html, "html.parser").get_text('\n')
        data = {
            "from": sender or self.default_sender,
            "to": Mailgun._join_email(to),
            "subject": subject or template.subject,
            "template": self.template,
            "text": text,
            "v:content": html
        }
        if cc:
            data["cc"] = Mailgun._join_email(cc)
        if bcc:
            data["bcc"] = Mailgun._join_email(bcc)
        if attachments:
            files = tuple(("attachment", (attachment.filename,
                                          attachment.slurp(auto_decode=False),
                                          attachment.mimetype))
                          for attachment in attachments)
        else:
            files = ()
        requests.post(self.url % self.domain,
                      auth=HTTPBasicAuth('api', self.api_key),
                      data=data,
                      files=files).raise_for_status()
        if task is not None:
            mark_task_as_performed(task)
        return True
