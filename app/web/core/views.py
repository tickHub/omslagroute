from django.views.generic import TemplateView, RedirectView
import os
import sys
from django.contrib.auth.mixins import UserPassesTestMixin
from django.core.files.storage import default_storage
from web.timeline.models import *
from web.documents.models import *
from web.organizations.models import *
from django.urls import reverse_lazy
import sendgrid
from sendgrid.helpers.mail import *
from django.conf import settings
from django.contrib.sites.shortcuts import get_current_site
from .utils import *
from django.contrib.auth.decorators import user_passes_test
from django.core.management import call_command
from django.http import HttpResponse


class HomePageView(TemplateView):
    template_name = "home.html"

    def get_context_data(self, **kwargs):
        document_list = Document.objects.all()
        floating_document_list = Document.objects.filter(moment__documents__isnull=True)
        moment_list = Moment.objects.all()
        organization_list = Organization.objects.all()

        kwargs.update({
            'document_list': document_list,
            'floating_document_list': floating_document_list,
            'moment_list': moment_list,
            'organization_list': organization_list,
        })
        return super().get_context_data(**kwargs)


class VariablesView(UserPassesTestMixin, TemplateView):
    template_name = "variables.html"

    def test_func(self):
        return self.request.user.is_superuser

    def get_context_data(self, **kwargs):
        l = [[k, v] for k, v in os.environ.items()]
        l = sorted(l)

        kwargs.update({
            'var_list': dict(l),
        })
        return super().get_context_data(**kwargs)


class ObjectStoreView(UserPassesTestMixin, TemplateView):
    template_name = "objectstore.html"

    def test_func(self):
        return self.request.user.is_superuser

    def get_context_data(self, **kwargs):

        documentversion_list = [{
            'name': d.uploaded_file.name,
            'generate_filename': default_storage.generate_filename(d.uploaded_file.name),
            'url': default_storage.url(default_storage.generate_filename(d.uploaded_file.name)),
            'exists': default_storage.exists(default_storage.generate_filename(d.uploaded_file.name)),
            'id': d.id
        } for d in DocumentVersion.objects.all()]

        kwargs.update({
            'objectstore_container_list': ['uploads/%s' % default_storage.get_valid_name(o) for o in default_storage.listdir('uploads')[1]],
            'documentversion_list': documentversion_list,
        })
        return super().get_context_data(**kwargs)


class SendMailView(UserPassesTestMixin, RedirectView):
    url = reverse_lazy('home')

    def test_func(self):
        return self.request.user.is_superuser

    def get(self, request, *args, **kwargs):
        mailadres = request.GET.get('mailadres')
        if mailadres:
            current_site = get_current_site(self.request)
            sg = sendgrid.SendGridAPIClient(settings.SENDGRID_KEY)
            email = Mail(
                from_email='noreply@%s' % current_site.domain,
                to_emails=mailadres,
                subject='Omslagroute - mail',
                plain_text_content='Het werkt!'
            )

            sg.send(email)

        return super().get(request, *args, **kwargs)


@user_passes_test(lambda u: u.is_superuser)
def dumpdata(request):
    sysout = sys.stdout
    fname = "%s-%s.json" % ('omslagroute', settings.SOURCE_COMMIT.strip())
    response = HttpResponse(content_type='application/json')
    response['Content-Disposition'] = 'attachment; filename=%s' % fname

    sys.stdout = response
    call_command('dumpdata', 'organizations', 'documents', 'timeline', '--indent=4')
    sys.stdout = sysout

    return response
