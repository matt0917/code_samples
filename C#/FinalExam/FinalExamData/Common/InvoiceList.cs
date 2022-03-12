using FinalExamData.Data;
using System;
using System.Collections.Generic;
using System.Collections.ObjectModel;
using System.ComponentModel;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace FinalExamData.Common
{
    public class InvoiceList : BindingList<Invoice>
    {
        private readonly TaxList taxList = InvoiceRepository.GetSalesTaxRate();

        public decimal GstRate 
        {
            get {
                decimal rate = 0.0m;
                foreach (Tax tax in taxList)
                {
                    if (tax.TaxCode == "GST") {
                        rate = tax.TaxRate * 0.01m;
                    }
                }
                return rate;
            }
        }

        public decimal PstRate
        {
            get
            {
                //foreach (Tax tax in taxList)
                //{
                //    if (tax.TaxCode == "BCPST")
                //    {
                //        rate = tax.TaxRate * 0.01m;
                //    }
                //}
                //return rate;

                // LINQ
                List<decimal> rate = (taxList.Where(x => x.TaxCode == "BCPST")
                                    .Select(x => x.TaxRate)).ToList<decimal>();
                return rate.FirstOrDefault() * 0.01m;
            }
        }

        public decimal SubTotal => this.Sum<Invoice>(x => x.Extended);
        public decimal GstTotal => this.Sum<Invoice>(x => (x.Extended * GstRate));
        public decimal PstTotal => this.Sum<Invoice>(x => (x.Extended * PstRate));
        public decimal GrandTtoal => (SubTotal + GstTotal + PstTotal);
    
        public decimal AveragePrice => this.Average<Invoice>(x => x.Price);
        public decimal MaximumPrice => this.Max<Invoice>(x => x.Price);
        public decimal MinimumPrice => this.Min<Invoice>(x => x.Price);

        public int ItemCount => this.Count;

        public int TaxableCount => this.Count<Invoice>(x => x.Taxable == true);
    }
}
