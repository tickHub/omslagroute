from django.views.generic import CreateView, DeleteView, ListView, UpdateView, DetailView, FormView
from .models import *
from django.urls import reverse_lazy, reverse
from .forms import *
from web.users.auth import auth_test
from django.contrib.auth.mixins import UserPassesTestMixin
from django.contrib import messages
from web.users.statics import BEGELEIDER
from web.profiles.models import Profile
from web.forms.statics import URGENTIE_AANVRAAG, FORMS_BY_SLUG
from web.forms.views import GenericUpdateFormView, GenericCreateFormView
import sendgrid
from sendgrid.helpers.mail import Mail
from django.contrib.sites.shortcuts import get_current_site
from django.conf import settings
from django.template.loader import render_to_string
from web.organizations.models import Organization
from django.http import Http404


class UserCaseList(UserPassesTestMixin, ListView):
    model = Case
    template_name_suffix = '_list_page'

    def test_func(self):
        return auth_test(self.request.user, BEGELEIDER) and hasattr(self.request.user, 'profile')

    def get_queryset(self):
        # qs = super().get_queryset()
        # profile = get_object_or_404(Profile, id=self.request.user.profile.id)
        return self.request.user.profile.cases.all()

    def get_context_data(self, *, object_list=None, **kwargs):
        # self.profile = self.request.user.profile
        return super().get_context_data(object_list=object_list, **kwargs)


class CaseDetailView(UserPassesTestMixin, DetailView):
    model = Case
    template_name_suffix = '_page'

    def test_func(self):
        return auth_test(self.request.user, BEGELEIDER) and hasattr(self.request.user, 'profile')


class CaseCreateView(UserPassesTestMixin, CreateView):
    model = Case
    form_class = CaseForm
    template_name_suffix = '_create_form'
    success_url = reverse_lazy('cases_by_profile')

    def test_func(self):
        return auth_test(self.request.user, BEGELEIDER) and hasattr(self.request.user, 'profile')

    def form_valid(self, form):
        case = form.save(commit=True)
        self.request.user.profile.cases.add(case)
        messages.add_message(self.request, messages.INFO, "De cliënt '%s' is aangemaakt." % case.client_name)
        return super().form_valid(form)


class CaseUpdateView(UserPassesTestMixin, UpdateView):
    model = Case
    form_class = CaseForm
    template_name_suffix = '_update_form'
    success_url = reverse_lazy('cases_by_profile')

    def test_func(self):
        return auth_test(self.request.user, BEGELEIDER) and hasattr(self.request.user, 'profile')

    def form_valid(self, form):
        messages.add_message(self.request, messages.INFO, "De cliënt '%s' is aangepast." % self.object.client_name)
        return super().form_valid(form)


class CaseDeleteView(UserPassesTestMixin, DeleteView):
    model = Case
    form_class = CaseForm
    template_name_suffix = '_delete_form'
    success_url = reverse_lazy('cases_by_profile')

    def test_func(self):
        return auth_test(self.request.user, BEGELEIDER) and hasattr(self.request.user, 'profile')

    def delete(self, request, *args, **kwargs):
        response = super().delete(self, request, *args, **kwargs)
        messages.add_message(self.request, messages.INFO, "De cliënt '%s' is verwijderd." % self.object.client_name)
        return response


class GenericCaseUpdateFormView(GenericUpdateFormView):
    model = Case
    template_name = 'forms/generic_form.html'
    success_url = reverse_lazy('cases_by_profile')
    form_class = CaseGenericModelForm

    def get_success_url(self):
        next = self.request.POST.get('next')
        if next:
            return next
        return reverse('update_case', kwargs={'pk': self.object.id, 'slug': self.kwargs.get('slug')})

    def get_discard_url(self):
        return reverse('case', kwargs={'pk': self.object.id})

    def form_invalid(self, form):
        return super().form_invalid(form)

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.add_message(self.request, messages.INFO, "De gegevens zijn aangepast.")
        return response


class GenericCaseCreateFormView(GenericCreateFormView):
    model = Case
    template_name = 'forms/generic_form.html'
    success_url = reverse_lazy('cases_by_profile')
    form_class = CaseGenericModelForm

    def get_success_url(self):
        return reverse('update_case', kwargs={'pk': self.object.id, 'slug': self.kwargs.get('slug')})

    def get_discard_url(self):
        return reverse('cases_by_profile')

    def form_valid(self, form):
        response = super().form_valid(form)
        case = form.save(commit=True)
        self.request.user.profile.cases.add(case)
        messages.add_message(self.request, messages.INFO, "De cliënt '%s' is aangemaakt." % case.client_name)
        return response


class SendCaseView(UpdateView):
    model = Case
    template_name = 'cases/send.html'
    form_class = SendCaseForm

    def get_success_url(self):
        return reverse('case', kwargs={'pk': self.object.id})

    def get_context_data(self, **kwargs):
        kwargs.update(self.kwargs)
        form_context = FORMS_BY_SLUG.get(self.kwargs.get('slug'))
        if not form_context:
            raise Http404
        kwargs.update(form_context)
        kwargs.update({
            'organization_list': Organization.objects.filter(main_email__isnull=False),
            'object': self.object,
        })
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        organization_list = Organization.objects.filter(main_email__isnull=False)
        for organization in organization_list:
            body = render_to_string('cases/mail/case.txt', {
                'case': self.object.to_dict(organization.field_restrictions)
            })
            current_site = get_current_site(self.request)
            sg = sendgrid.SendGridAPIClient(settings.SENDGRID_KEY)
            email = Mail(
                from_email='noreply@%s' % current_site.domain,
                to_emails=organization.main_email,
                subject='Omslagroute - %s' % self.kwargs.get('title'),
                plain_text_content=body
            )
            sg.send(email)
            messages.add_message(
                self.request, messages.INFO, "De cliëntgegevens van '%s', zijn gestuurd naar '%s'." % (
                    self.object.client_name,
                    organization.main_email
                )
            )
        return super().form_valid(form)

    def form_invalid(self, form):

        return super().form_invalid(form)










