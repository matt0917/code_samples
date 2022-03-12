using FinalExamData.Common;
using FinalExamData.Data;
using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Data.SqlClient;
using System.Diagnostics;
using System.Drawing;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;

namespace FinalExam
{
    public partial class MainForm : Form
    {
        private InvoiceViewModel invoiceVM;

        public MainForm()
        {
            InitializeComponent();
        }

        private void MainForm_Load(object sender, EventArgs e)
        {
           clearTempBoxes();
            try
            {
                invoiceVM = new InvoiceViewModel();
                setBindings();
            }

            catch (SqlException ex)
            {
                MessageBox.Show(ex.Message, "DB Error", MessageBoxButtons.OK, MessageBoxIcon.Error);
            }

            catch (Exception ex)
            {
                MessageBox.Show(ex.Message, "Processing Error", MessageBoxButtons.OK, MessageBoxIcon.Error);
            }
        }

        private void clearTempBoxes()
        {
            var allTextBoxes = this.Controls.OfType<TextBox>();
            foreach (TextBox textBox in allTextBoxes)
            {
                textBox.Text = String.Empty;
            }
            var allMaskedTextBoxes = this.Controls.OfType<MaskedTextBox>();
            foreach (MaskedTextBox maskedTextBox in allMaskedTextBoxes)
            {
                maskedTextBox.Text = String.Empty;
            }
            labelInvoiceData.Text = String.Empty;
        }

        private void setBindings()
        {
            textBoxQuantity.DataBindings.Add("Text", invoiceVM, "Invoice.Quantity", true, DataSourceUpdateMode.OnValidation, "0", "#,##0;(#,##0);0");
            maskedTextBoxSku.DataBindings.Add("Text", invoiceVM, "Invoice.Sku", false, DataSourceUpdateMode.OnValidation, "");
            textBoxDescription.DataBindings.Add("Text", invoiceVM, "Invoice.Description");
            textBoxPrice.DataBindings.Add("Text", invoiceVM, "Invoice.Price", true, DataSourceUpdateMode.OnValidation, "0.00", "#,##0.00;(#,##0.00);0.00");
            textBoxExtended.DataBindings.Add("Text", invoiceVM, "Invoice.Extended", true, DataSourceUpdateMode.OnValidation, "0.00", "#,##0.00;(#,##0.00);0.00");
            checkBoxTaxable.DataBindings.Add("Checked", invoiceVM, "Invoice.Taxable");

            listBoxInvoice.DataSource = invoiceVM.Invoices;
            listBoxInvoice.DisplayMember = "Sku";

        }

        private void listBoxProducts_SelectedIndexChanged(object sender, EventArgs e)
        {
            int selectedIndex = Math.Max(0, listBoxInvoice.SelectedIndex);
            Invoice invoice = invoiceVM.Invoices[selectedIndex];
            invoiceVM.SetDisplayProduct(invoice);
        }

        private void buttonSave_Click(object sender, EventArgs e)
        {
            try
            {
                int index = listBoxInvoice.SelectedIndex;

                Invoice invoice = invoiceVM.GetDisplayProduct();
                invoiceVM.Invoices[index] = invoice;

                string outputData = string.Format("{0:N2}\r\n{1:N2}\r\n{2:N2}\r\n{3:N2}\r\n{4}\r\n{5:N2}\r\n{6:N2}\r\n{7:N2}\r\n{8}\r\n{9:N0}\r\n{10:N0}\r\n",
                                               invoiceVM.Invoices.SubTotal,
                                               invoiceVM.Invoices.GstTotal,
                                               invoiceVM.Invoices.PstTotal,
                                               invoiceVM.Invoices.GrandTtoal,
                                               "",
                                               invoiceVM.Invoices.AveragePrice,
                                               invoiceVM.Invoices.MaximumPrice,
                                               invoiceVM.Invoices.MinimumPrice,
                                               "",
                                               invoiceVM.Invoices.ItemCount,
                                               invoiceVM.Invoices.TaxableCount);

                labelInvoiceData.Text = outputData;
            }
            catch (Exception ex)
            {
                MessageBox.Show(ex.Message, "Processing Error", MessageBoxButtons.OK, MessageBoxIcon.Error);
            }
        }


        private void buttonNewProduct_Click(object sender, EventArgs e)
        {
            invoiceVM.SetDisplayProduct(new Invoice());
            textBoxQuantity.Select();
            textBoxQuantity.SelectAll();
        }

        
        
        private void refreshListBox()
        {
            invoiceVM.Invoices = InvoiceRepository.GetInvoices();
            listBoxInvoice.DataSource = invoiceVM.Invoices;
            listBoxInvoice.DisplayMember = "Sku";
        }

        private bool confirmUserEntry(string message)
        {
            bool status = false;
            DialogResult result = MessageBox.Show(message, "Confirmation", MessageBoxButtons.YesNo, MessageBoxIcon.Information);
            if (result == DialogResult.Yes) { 
                status = true;
            }
            return status;
        }

        private void selectAllText(TextBox textBox)
        {
            textBox.Select();
            textBox.SelectAll();
        }
        private void selectAllText(MaskedTextBox maskedTextBox)
        {
            maskedTextBox.Select();
            maskedTextBox.SelectAll();
        }

        private void textBoxQuantity_MouseEnter(object sender, EventArgs e)
        {
            selectAllText((TextBox)sender);
        }

        private void maskedTextBoxSku_MouseEnter(object sender, EventArgs e)
        {
            selectAllText((MaskedTextBox)sender);
        }

        private void textBoxDescription_MouseEnter(object sender, EventArgs e)
        {
            selectAllText((TextBox)sender);
        }

        private void textBoxPrice_MouseEnter(object sender, EventArgs e)
        {
            selectAllText((TextBox)sender);
        }

        private void textBoxExtended_MouseEnter(object sender, EventArgs e)
        {
            selectAllText((TextBox)sender);
        }
    }
}
