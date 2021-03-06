import io
import csv
from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from braces.views import JsonRequestResponseMixin, AjaxResponseMixin
from django.contrib import messages
from django.views.generic import View
from django.views.generic import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import AddressBookList


class ContactList(LoginRequiredMixin, ListView):
    model = AddressBookList

    def get_queryset(self):
        print("====================================")
        if self.request.user.is_authenticated:
            return AddressBookList.objects.filter(author=self.request.user)
        else:
            return None


class ContactCreate(LoginRequiredMixin, JsonRequestResponseMixin, AjaxResponseMixin, CreateView):
    model = AddressBookList
    fields = ['fname', 'lname', 'cnumber', 'address']
    success_url = reverse_lazy('addressbooklist_list')

    def post_ajax(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            form.instance.author = self.request.user
            form.save()
            data_pk = form.instance.pk
            contact = AddressBookList.objects.get(pk=data_pk)
            return self.render_json_response({
                "pk": contact.pk,
                "fname": contact.fname,
                "lname": contact.lname,
                "cnumber": contact.cnumber,
                "address": contact.address,
                "success": True,
                "message": "Contact updated successfully",
                "update_url": "http://127.0.0.1:8000/update_contact/{}".format(data_pk),
                "delete_url": "http://127.0.0.1:8000/delete_contact/{}".format(data_pk),
            })


class ContactUpdate(LoginRequiredMixin, JsonRequestResponseMixin, AjaxResponseMixin, UpdateView):
    model = AddressBookList
    fields = ['fname', 'lname', 'cnumber', 'address']
    success_url = reverse_lazy('addressbooklist_list')

    def post_ajax(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            form.instance.author = self.request.user
            form.save()
            data_pk = form.instance.pk
            contact = AddressBookList.objects.get(pk=data_pk)
            return self.render_json_response({
                "pk": contact.pk,
                "fname": contact.fname,
                "lname": contact.lname,
                "cnumber": contact.cnumber,
                "address": contact.address,
                "success": True,
                "message": "Contact updated successfully",
                "updateurl": "http://127.0.0.1:8000/delete_contact/{}".format(data_pk),
                "delete_url": "http://127.0.0.1:8000/delete_contact/{}".format(data_pk),
            })


class ContactDelete(LoginRequiredMixin, JsonRequestResponseMixin, AjaxResponseMixin, DeleteView):
    model = AddressBookList
    success_url = reverse_lazy('addressbooklist_list')

    def post_ajax(self, request, *args, **kwargs):
        data_pk = self.kwargs['pk']
        if data_pk:
            AddressBookList.objects.filter(pk=data_pk).delete()
            return self.render_json_response({
                "pk": data_pk,
                "success": True,
                "message": "Contact deleted successfully",
            })


class CSVImportView(LoginRequiredMixin, View):
    def get(self, request):
        template = "addressbook/contact_upload.html"

        prompt = {
            'order': 'Order of the CSV should be FirstName, ' +
                     ' LastName, ContactNo, Address'
        }
        return render(request, template, prompt)

    def post(self, request):
        template = "addressbook/contact_upload.html"
        csv_file = request.FILES['file']

        if not csv_file.name.endswith('.csv'):
            messages.error(request, 'Not a csv file', extra_tags='excel')
            return render(request, template)

        data_set = csv_file.read().decode('UTF-8')
        io_string = io.StringIO(data_set)
        next(io_string)
        for column in csv.reader(io_string, quotechar="|"):
            _, created = AddressBookList.objects.update_or_create(
                fname=column[0],
                lname=column[1],
                cnumber=column[2],
                address=column[3],
                author=request.user,
            )

        context = {}
        return render(request, template, context)


class CSVExportView(LoginRequiredMixin, View):
    def get(self, request):
        items = AddressBookList.objects.filter(author=self.request.user)
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="contact.csv"'

        writer = csv.writer(response)
        writer.writerow(['FirstName', 'LastName', 'ContactNo', 'Address'])

        for obj in items:
            writer.writerow([obj.fname, obj.lname, obj.cnumber, obj.address])

        return response
