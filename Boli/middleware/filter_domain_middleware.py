from django.utils.deprecation import MiddlewareMixin
from mandir.models import MandirDomain


class FilterDomainMiddleware(MiddlewareMixin):
    # Check if client IP is allowed

    def process_request(self, request):
        domain = request.get_host()
        obje = MandirDomain.getMandirByDomain(domain)
        request.mandir = obje.mandir
        return None