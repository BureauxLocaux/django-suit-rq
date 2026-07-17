from django import template
from rq.exceptions import InvalidJobOperation

register = template.Library()


@register.filter
def job_status(job):
    """Get a job's status, tolerating rq's InvalidJobOperation for jobs
    whose Redis hash has no readable 'status' field (e.g. legacy jobs
    scheduled before an rq upgrade)."""
    try:
        return job.get_status().value
    except InvalidJobOperation:
        return 'unknown'
