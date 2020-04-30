from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.forms import widgets
from django.urls import reverse_lazy

from .models import Invoice, InvoiceItem, Receipt
from .forms import InvoiceItemFormset, InvoiceReceiptFormSet

class InvoiceListView(ListView):
  model = Invoice


class InvoiceCreateView(CreateView):
    model = Invoice
    fields = '__all__'
    success_url = '/finance/list'

    def get_context_data(self, **kwargs):
        context = super(InvoiceCreateView, self).get_context_data(**kwargs)
        if self.request.POST:
            context['items'] = InvoiceItemFormset(
                self.request.POST, prefix='invoiceitem_set')
        else:
            context['items'] = InvoiceItemFormset(prefix='invoiceitem_set')
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        formset = context['items']
        self.object = form.save()
        if self.object.id != None:
            if form.is_valid() and formset.is_valid():
                formset.instance = self.object
                formset.save()
        return super().form_valid(form)


class InvoiceDetailView(DetailView):
    model = Invoice
    fields = '__all__'

    def get_context_data(self, **kwargs):
        context = super(InvoiceDetailView, self).get_context_data(**kwargs)
        context['receipts'] = Receipt.objects.filter(invoice=self.object)
        context['items'] = InvoiceItem.objects.filter(invoice=self.object)
        return context


class InvoiceUpdateView(UpdateView):
    model = Invoice
    fields = ['student', 'session', 'term',
              'class_for', 'balance_from_previous_term']

    def get_context_data(self, **kwargs):
        context = super(InvoiceUpdateView, self).get_context_data(**kwargs)
        if self.request.POST:
          context['receipts'] = InvoiceReceiptFormSet(
              self.request.POST, instance=self.object)
          context['items'] = InvoiceItemFormset(
              self.request.POST, instance=self.object)
        else:
          context['receipts'] = InvoiceReceiptFormSet(instance=self.object)
          context['items'] = InvoiceItemFormset(instance=self.object)
        return context

    def form_valid(self, form):
      context = self.get_context_data()
      formset = context['receipts']
      itemsformset = context['items']
      if form.is_valid() and formset.is_valid() and itemsformset.is_valid():
        form.save()
        formset.save()
        itemsformset.save()
      return super().form_valid(form)



class InvoiceDeleteView(DeleteView):
    model = Invoice
    success_url = reverse_lazy('invoice-list')


class ReceiptCreateView(CreateView):
    model = Receipt
    fields = ['amount_paid', 'date_paid', 'comment']
    success_url = reverse_lazy('invoice-list')

    def form_valid(self, form):
        obj = form.save(commit=False)
        invoice = Invoice.objects.get(pk=self.request.GET['invoice'])
        obj.invoice = invoice
        obj.save()
        return redirect('invoice-list')

    def get_context_data(self, **kwargs):
        context = super(ReceiptCreateView, self).get_context_data(**kwargs)
        invoice = Invoice.objects.get(pk=self.request.GET['invoice'])
        context['invoice'] = invoice
        return context


class ReceiptUpdateView(UpdateView):
    model = Receipt
    fields = ['amount_paid', 'date_paid', 'comment']
    success_url = reverse_lazy('invoice-list')


class ReceiptDeleteView(DeleteView):
    model = Receipt
    success_url = reverse_lazy('invoice-list')

