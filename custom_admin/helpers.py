from urllib.parse import urlsplit, parse_qs

from django.conf import settings
from django.contrib.sites.models import Site
from django.urls import reverse


class CustomSite(object):
    protocol = "http"
    domain = None
    request_path = None
    fragment = None
    query = None
    params = None

    site = None
    page = None

    site_url = None
    base_url = None
    canonical_url = None

    def __init__(self, request):
        request_uri = request.build_absolute_uri()

        url = urlsplit(request_uri)

        self.protocol = url.scheme
        self.domain = url.hostname
        self.request_path = url.path
        self.fragment = url.fragment
        self.query = url.query
        self.params = parse_qs(self.query)

        self.site_url = "%s://%s" % (self.protocol, self.domain)
        self.base_url = "%s/" % self.site_url
        self.canonical_url = "%s/%s" % (self.site_url, self.request_path)

        try:
            self.site = Site.objects.get_current(request)
        except Site.DoesNotExist:
            if hasattr(settings, "SITE_ID"):
                self.site = Site.objects.get(id=getattr(settings, "SITE_ID"))
            elif hasattr(settings, "SITE_URL") and isinstance(getattr(settings, "SITE_URL"), str):
                default_url = urlsplit(getattr(settings, "SITE_URL"))
                self.site = Site.objects.get(url=default_url.hostname)

        if isinstance(self.domain, str) and "local" in self.domain:
            self.domain = "%s:8000" % self.domain
            self.site_url = "%s://%s" % (self.protocol, self.domain)
            self.base_url = "%s/" % self.site_url
            self.canonical_url = "%s/%s" % (self.site_url, self.request_path)

        setattr(settings, "DOMAIN_NAME", self.domain)

    def external_reverse(self, url_slug, add_slash=False):
        urlbase = self.site_url if not add_slash else self.base_url

        return "%s%s" % (urlbase, reverse(url_slug))
