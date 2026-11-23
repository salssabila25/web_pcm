from django import template

register = template.Library()


@register.simple_tag
def pcm_stat(model_name):
    """Return count for dashboard stats. Fails silently."""
    try:
        if model_name == "management":
            from core.models import Management
            return Management.objects.filter(aktif=True).count()
        elif model_name == "news":
            from news.models import News
            return News.objects.count()
        elif model_name == "agenda":
            from agenda.models import Agenda
            return Agenda.objects.count()
        elif model_name == "contact":
            from core.models import ContactMessage
            return ContactMessage.objects.filter(status="baru").count()
    except Exception:
        return 0
    return 0
