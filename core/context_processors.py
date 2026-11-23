from .models import OrganizationProfile


def organization(request):
    return {"org": OrganizationProfile.load()}