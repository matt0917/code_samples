using FinalExamData.Common;
using FinalExamData.Data;
using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Linq;
using System.Runtime.CompilerServices;
using System.Text;
using System.Threading.Tasks;

namespace FinalExam
{
    class InvoiceViewModel : INotifyPropertyChanged
    {
        private Invoice invoice;

        public event PropertyChangedEventHandler PropertyChanged;

        protected void OnPropertyChanged(string propertyName)
        {
            PropertyChanged?.Invoke(this, new PropertyChangedEventArgs(propertyName));
        }

        
        public InvoiceViewModel()
        {
            this.Invoices = InvoiceRepository.GetInvoices();
            this.TaxRates = InvoiceRepository.GetSalesTaxRate();
            Invoice = new Invoice();
        }

        public Invoice Invoice
        {
            get { return invoice; }
            set
            {
                invoice = value;
                OnPropertyChanged("Invoice");
            }
        }

        public TaxList TaxRates { get; set; }
       
        public InvoiceList Invoices { get; set; }

        public void SetDisplayProduct(Invoice invoice)
        {   // pass by value to prevent changing Invoice instance in collection
            Invoice = new Invoice
            {
                DetailId = invoice.DetailId,
                Quantity = invoice.Quantity,
                Sku = invoice.Sku,
                Description = invoice.Description,
                Price = invoice.Price,
                Taxable = invoice.Taxable,
            };
        }

        public Invoice GetDisplayProduct()
        {
            OnPropertyChanged("Invoice");
            return Invoice;
        }
    }
}
