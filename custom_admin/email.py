import mimetypes
import os

from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template

from custom_admin.helpers import CustomSite
from custom_admin.utility_functions import log_message, make_list


def base_email_context(request):
    context = dict()

    the_site = CustomSite(request)
    current_site = the_site.site
    site_url = the_site.site_url
    if not isinstance(the_site.site.name, str):
        site_name = ""
    else:
        site_name = current_site.name

    context["site_url"] = site_url
    context["site_name"] = site_name

    return context


def send_multipart_email(subject_str, to_list, from_str, template_path, context_dict, **kwargs):
    """Send a single html email message (which can be sent to multiple recipients).

        subject_str = String to use as email subject
        to_list = list of recipient email address strings
        from_str = string to use as the from email address
        template_path = path, from webroot to the email template to use, .html type
        context_dict = dictionary defining any variables that are required to fully render the template."""

    debug = kwargs.get("debug", False)
    kwargs.get("fail_silently", False)
    attachments = kwargs.get("attachments", False)
    is_html = kwargs.get("html", True)

    if debug:
        log_message("Send multipart email to: {}.".format(to_list))

    if kwargs.get("request") is not None:
        if isinstance(context_dict, dict):
            context_dict.update(base_email_context(kwargs.get("request")))
    else:
        if not isinstance(context_dict, dict):
            context_dict = {}

    if not isinstance(from_str, str):
        if debug:
            log_message("Sending from default sender.")
        from_str = settings.DEFAULT_FROM_EMAIL

    text_template_path = f"{template_path}.txt"
    text_message = get_template(text_template_path).render(context_dict)

    msg = EmailMultiAlternatives(subject_str, text_message, from_str, to_list)

    if is_html:
        html_template_path = f"{template_path}.html"
        html_message = get_template(html_template_path).render(context_dict)
        msg.attach_alternative(html_message, "text/html")

    if attachments:
        mimetypes.init()

        for attachment in make_list(attachments):
            msg.attach(os.path.basename(attachment), open(attachment, "rb").read(), mimetypes.guess_type(attachment)[0])

    result = msg.send(fail_silently)

    return result
