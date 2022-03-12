namespace FinalExam
{
    partial class MainForm
    {
        /// <summary>
        /// Required designer variable.
        /// </summary>
        private System.ComponentModel.IContainer components = null;

        /// <summary>
        /// Clean up any resources being used.
        /// </summary>
        /// <param name="disposing">true if managed resources should be disposed; otherwise, false.</param>
        protected override void Dispose(bool disposing)
        {
            if (disposing && (components != null))
            {
                components.Dispose();
            }
            base.Dispose(disposing);
        }

        #region Windows Form Designer generated code

        /// <summary>
        /// Required method for Designer support - do not modify
        /// the contents of this method with the code editor.
        /// </summary>
        private void InitializeComponent()
        {
            this.components = new System.ComponentModel.Container();
            System.ComponentModel.ComponentResourceManager resources = new System.ComponentModel.ComponentResourceManager(typeof(MainForm));
            this.listBoxInvoice = new System.Windows.Forms.ListBox();
            this.textBoxQuantity = new System.Windows.Forms.TextBox();
            this.labelQuantity = new System.Windows.Forms.Label();
            this.labelExtended = new System.Windows.Forms.Label();
            this.labelDescription = new System.Windows.Forms.Label();
            this.labelSku = new System.Windows.Forms.Label();
            this.labelList = new System.Windows.Forms.Label();
            this.buttonSave = new System.Windows.Forms.Button();
            this.maskedTextBoxSku = new System.Windows.Forms.MaskedTextBox();
            this.textBoxDescription = new System.Windows.Forms.TextBox();
            this.checkBoxTaxable = new System.Windows.Forms.CheckBox();
            this.textBoxExtended = new System.Windows.Forms.TextBox();
            this.labelPrice = new System.Windows.Forms.Label();
            this.textBoxPrice = new System.Windows.Forms.TextBox();
            this.errorProvider = new System.Windows.Forms.ErrorProvider(this.components);
            this.labelInvoiceLegend = new System.Windows.Forms.Label();
            this.labelInvoiceData = new System.Windows.Forms.Label();
            ((System.ComponentModel.ISupportInitialize)(this.errorProvider)).BeginInit();
            this.SuspendLayout();
            // 
            // listBoxInvoice
            // 
            this.listBoxInvoice.Dock = System.Windows.Forms.DockStyle.Left;
            this.listBoxInvoice.FormattingEnabled = true;
            this.listBoxInvoice.IntegralHeight = false;
            this.listBoxInvoice.Location = new System.Drawing.Point(0, 0);
            this.listBoxInvoice.Name = "listBoxInvoice";
            this.listBoxInvoice.Size = new System.Drawing.Size(128, 241);
            this.listBoxInvoice.TabIndex = 1;
            this.listBoxInvoice.SelectedIndexChanged += new System.EventHandler(this.listBoxProducts_SelectedIndexChanged);
            // 
            // textBoxQuantity
            // 
            this.errorProvider.SetIconPadding(this.textBoxQuantity, 3);
            this.textBoxQuantity.Location = new System.Drawing.Point(234, 17);
            this.textBoxQuantity.Name = "textBoxQuantity";
            this.textBoxQuantity.Size = new System.Drawing.Size(100, 20);
            this.textBoxQuantity.TabIndex = 3;
            this.textBoxQuantity.Text = "<1>";
            this.textBoxQuantity.TextAlign = System.Windows.Forms.HorizontalAlignment.Right;
            this.textBoxQuantity.MouseEnter += new System.EventHandler(this.textBoxQuantity_MouseEnter);
            // 
            // labelQuantity
            // 
            this.labelQuantity.AutoSize = true;
            this.labelQuantity.Location = new System.Drawing.Point(165, 20);
            this.labelQuantity.Name = "labelQuantity";
            this.labelQuantity.Size = new System.Drawing.Size(49, 13);
            this.labelQuantity.TabIndex = 2;
            this.labelQuantity.Text = "&Quantity:";
            // 
            // labelExtended
            // 
            this.labelExtended.AutoSize = true;
            this.labelExtended.ForeColor = System.Drawing.Color.Blue;
            this.labelExtended.Location = new System.Drawing.Point(165, 153);
            this.labelExtended.Name = "labelExtended";
            this.labelExtended.Size = new System.Drawing.Size(55, 13);
            this.labelExtended.TabIndex = 10;
            this.labelExtended.Text = "&Extended:";
            // 
            // labelDescription
            // 
            this.labelDescription.AutoSize = true;
            this.labelDescription.Location = new System.Drawing.Point(165, 85);
            this.labelDescription.Name = "labelDescription";
            this.labelDescription.Size = new System.Drawing.Size(63, 13);
            this.labelDescription.TabIndex = 6;
            this.labelDescription.Text = "&Description:";
            // 
            // labelSku
            // 
            this.labelSku.AutoSize = true;
            this.labelSku.Location = new System.Drawing.Point(165, 51);
            this.labelSku.Name = "labelSku";
            this.labelSku.Size = new System.Drawing.Size(29, 13);
            this.labelSku.TabIndex = 4;
            this.labelSku.Text = "&Sku:";
            // 
            // labelList
            // 
            this.labelList.AutoSize = true;
            this.labelList.Location = new System.Drawing.Point(91, 36);
            this.labelList.Name = "labelList";
            this.labelList.Size = new System.Drawing.Size(23, 13);
            this.labelList.TabIndex = 0;
            this.labelList.Text = "&List";
            // 
            // buttonSave
            // 
            this.buttonSave.Location = new System.Drawing.Point(350, 193);
            this.buttonSave.Name = "buttonSave";
            this.buttonSave.Size = new System.Drawing.Size(85, 23);
            this.buttonSave.TabIndex = 13;
            this.buttonSave.TabStop = false;
            this.buttonSave.Text = "Sa&ve";
            this.buttonSave.UseVisualStyleBackColor = true;
            this.buttonSave.Click += new System.EventHandler(this.buttonSave_Click);
            // 
            // maskedTextBoxSku
            // 
            this.errorProvider.SetIconPadding(this.maskedTextBoxSku, 3);
            this.maskedTextBoxSku.Location = new System.Drawing.Point(234, 48);
            this.maskedTextBoxSku.Mask = ">LLL0000";
            this.maskedTextBoxSku.Name = "maskedTextBoxSku";
            this.maskedTextBoxSku.Size = new System.Drawing.Size(100, 20);
            this.maskedTextBoxSku.TabIndex = 5;
            this.maskedTextBoxSku.Text = "AAA9999";
            this.maskedTextBoxSku.MouseEnter += new System.EventHandler(this.maskedTextBoxSku_MouseEnter);
            // 
            // textBoxDescription
            // 
            this.textBoxDescription.Location = new System.Drawing.Point(234, 82);
            this.textBoxDescription.Name = "textBoxDescription";
            this.textBoxDescription.Size = new System.Drawing.Size(201, 20);
            this.textBoxDescription.TabIndex = 7;
            this.textBoxDescription.Text = "<Nice Widget>";
            this.textBoxDescription.MouseEnter += new System.EventHandler(this.textBoxDescription_MouseEnter);
            // 
            // checkBoxTaxable
            // 
            this.checkBoxTaxable.AutoSize = true;
            this.checkBoxTaxable.Location = new System.Drawing.Point(270, 197);
            this.checkBoxTaxable.Name = "checkBoxTaxable";
            this.checkBoxTaxable.Size = new System.Drawing.Size(64, 17);
            this.checkBoxTaxable.TabIndex = 12;
            this.checkBoxTaxable.Text = "&Taxable";
            this.checkBoxTaxable.UseVisualStyleBackColor = true;
            // 
            // textBoxExtended
            // 
            this.errorProvider.SetIconPadding(this.textBoxExtended, 3);
            this.textBoxExtended.Location = new System.Drawing.Point(234, 150);
            this.textBoxExtended.Name = "textBoxExtended";
            this.textBoxExtended.Size = new System.Drawing.Size(100, 20);
            this.textBoxExtended.TabIndex = 11;
            this.textBoxExtended.Text = "<0.00>";
            this.textBoxExtended.TextAlign = System.Windows.Forms.HorizontalAlignment.Right;
            this.textBoxExtended.MouseEnter += new System.EventHandler(this.textBoxExtended_MouseEnter);
            // 
            // labelPrice
            // 
            this.labelPrice.AutoSize = true;
            this.labelPrice.Location = new System.Drawing.Point(165, 118);
            this.labelPrice.Name = "labelPrice";
            this.labelPrice.Size = new System.Drawing.Size(34, 13);
            this.labelPrice.TabIndex = 8;
            this.labelPrice.Text = "&Price:";
            // 
            // textBoxPrice
            // 
            this.errorProvider.SetIconPadding(this.textBoxPrice, 3);
            this.textBoxPrice.Location = new System.Drawing.Point(234, 115);
            this.textBoxPrice.Name = "textBoxPrice";
            this.textBoxPrice.Size = new System.Drawing.Size(100, 20);
            this.textBoxPrice.TabIndex = 9;
            this.textBoxPrice.Text = "<0.00>";
            this.textBoxPrice.TextAlign = System.Windows.Forms.HorizontalAlignment.Right;
            this.textBoxPrice.MouseEnter += new System.EventHandler(this.textBoxPrice_MouseEnter);
            // 
            // errorProvider
            // 
            this.errorProvider.BlinkStyle = System.Windows.Forms.ErrorBlinkStyle.NeverBlink;
            this.errorProvider.ContainerControl = this;
            // 
            // labelInvoiceLegend
            // 
            this.labelInvoiceLegend.AutoSize = true;
            this.labelInvoiceLegend.Font = new System.Drawing.Font("Microsoft Sans Serif", 11.25F, System.Drawing.FontStyle.Bold, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.labelInvoiceLegend.ForeColor = System.Drawing.Color.Black;
            this.labelInvoiceLegend.Location = new System.Drawing.Point(482, 17);
            this.labelInvoiceLegend.Name = "labelInvoiceLegend";
            this.labelInvoiceLegend.Size = new System.Drawing.Size(129, 198);
            this.labelInvoiceLegend.TabIndex = 14;
            this.labelInvoiceLegend.Text = "Sub Total\r\nGST:\r\nPST:\r\nGrand Total:\r\n\r\nAverage Price:\r\nMaximum Price:\r\nMinimum Pr" +
    "ice:\r\n\r\nItem Count:\r\nTaxable Count:\r\n";
            // 
            // labelInvoiceData
            // 
            this.labelInvoiceData.Font = new System.Drawing.Font("Microsoft Sans Serif", 11.25F, System.Drawing.FontStyle.Bold, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.labelInvoiceData.ForeColor = System.Drawing.Color.Blue;
            this.labelInvoiceData.Location = new System.Drawing.Point(617, 17);
            this.labelInvoiceData.Name = "labelInvoiceData";
            this.labelInvoiceData.Size = new System.Drawing.Size(124, 199);
            this.labelInvoiceData.TabIndex = 15;
            this.labelInvoiceData.Text = "one\r\ntwo\r\nthree\r\nfour\r\nfive\r\nsix\r\nseven\r\neight\r\nnine\r\nten\r\neleven\r\n\r\n\r\n";
            this.labelInvoiceData.TextAlign = System.Drawing.ContentAlignment.MiddleRight;
            // 
            // MainForm
            // 
            this.AcceptButton = this.buttonSave;
            this.AutoScaleDimensions = new System.Drawing.SizeF(6F, 13F);
            this.AutoScaleMode = System.Windows.Forms.AutoScaleMode.Font;
            this.BackColor = System.Drawing.SystemColors.Window;
            this.ClientSize = new System.Drawing.Size(764, 241);
            this.Controls.Add(this.labelInvoiceData);
            this.Controls.Add(this.labelInvoiceLegend);
            this.Controls.Add(this.labelPrice);
            this.Controls.Add(this.textBoxPrice);
            this.Controls.Add(this.listBoxInvoice);
            this.Controls.Add(this.textBoxQuantity);
            this.Controls.Add(this.labelQuantity);
            this.Controls.Add(this.labelExtended);
            this.Controls.Add(this.labelDescription);
            this.Controls.Add(this.labelSku);
            this.Controls.Add(this.labelList);
            this.Controls.Add(this.buttonSave);
            this.Controls.Add(this.maskedTextBoxSku);
            this.Controls.Add(this.textBoxDescription);
            this.Controls.Add(this.checkBoxTaxable);
            this.Controls.Add(this.textBoxExtended);
            this.FormBorderStyle = System.Windows.Forms.FormBorderStyle.FixedSingle;
            this.Icon = ((System.Drawing.Icon)(resources.GetObject("$this.Icon")));
            this.MaximizeBox = false;
            this.Name = "MainForm";
            this.StartPosition = System.Windows.Forms.FormStartPosition.CenterScreen;
            this.Text = "COMP2614 Final Exam";
            this.Load += new System.EventHandler(this.MainForm_Load);
            ((System.ComponentModel.ISupportInitialize)(this.errorProvider)).EndInit();
            this.ResumeLayout(false);
            this.PerformLayout();

        }

        #endregion

        private System.Windows.Forms.ListBox listBoxInvoice;
        private System.Windows.Forms.TextBox textBoxQuantity;
        private System.Windows.Forms.Label labelQuantity;
        private System.Windows.Forms.Label labelExtended;
        private System.Windows.Forms.Label labelDescription;
        private System.Windows.Forms.Label labelSku;
        private System.Windows.Forms.Label labelList;
        private System.Windows.Forms.Button buttonSave;
        private System.Windows.Forms.MaskedTextBox maskedTextBoxSku;
        private System.Windows.Forms.TextBox textBoxDescription;
        private System.Windows.Forms.CheckBox checkBoxTaxable;
        private System.Windows.Forms.TextBox textBoxExtended;
        private System.Windows.Forms.Label labelPrice;
        private System.Windows.Forms.TextBox textBoxPrice;
        private System.Windows.Forms.ErrorProvider errorProvider;
        private System.Windows.Forms.Label labelInvoiceData;
        private System.Windows.Forms.Label labelInvoiceLegend;
    }
}

