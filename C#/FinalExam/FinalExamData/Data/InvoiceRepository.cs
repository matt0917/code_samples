using FinalExamData.Common;
using System;
using System.Collections.Generic;
using System.Data;
using System.Data.SqlClient;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace FinalExamData.Data
{
    public class InvoiceRepository
    {
        //private const string connString = @"Server=tcp:skeena.database.windows.net,1433;
        //                                    Initial Catalog=comp2614;
        //                                    User ID=student;
        //                                    Password=p8SmM5/mKZk=;
        //                                    Encrypt=True;
        //                                    TrustServerCertificate=False;
        //                                    Connection Timeout=30;";

        private const string connString = @"Server=MP-Z800-WIN10\SQLSERVER2019;
                                            Initial Catalog=comp2614;
                                            Integrated Security = True;
                                            Connection Timeout=30;";

        private const string invoiceTableName = "invoiceDetail";
        private const string salesTaxRateTableName = "SalesTaxRate";


        public static InvoiceList GetInvoices()
        {
            InvoiceList invoices;

            using (SqlConnection conn = new SqlConnection(connString))
            {
                string query = $@"SELECT DetailId, Quantity, Sku, Description, Price, Taxable
                                  FROM {invoiceTableName}
                                  ORDER BY Sku";

                using (SqlCommand cmd = new SqlCommand())
                {
                    cmd.CommandType = CommandType.Text;
                    cmd.CommandText = query;
                    cmd.Connection = conn;

                    conn.Open();

                    invoices = new InvoiceList();

                    using (SqlDataReader reader = cmd.ExecuteReader(CommandBehavior.CloseConnection))
                    {
                        int detailId;
                        int quantity;
                        string sku;
                        string description;
                        decimal price;
                        bool taxable;

                        while (reader.Read())
                        {
                            detailId = (int)reader["DetailId"];
                            quantity = (int)reader["Quantity"];
                            sku = reader["Sku"] as string;

                            if (!reader.IsDBNull(3))
                            {
                                description = reader["Description"] as string;
                            }
                            else
                            {
                                description = null;
                            }

                            price = (decimal)reader["Price"];

                            if (!reader.IsDBNull(5))
                            {
                                taxable = (bool)reader["Taxable"];
                            }
                            else 
                            {
                                taxable = false;
                            }


                            invoices.Add(new Invoice
                            {
                                DetailId = detailId,
                                Quantity = quantity,
                                Sku = sku,
                                Description = description,
                                Price = price,
                                Taxable = taxable
                            });
                        }
                    }
                }
            }

            return invoices;
        }


        public static TaxList GetSalesTaxRate()
        {
            TaxList taxes;

            using (SqlConnection conn = new SqlConnection(connString))
            {
                string query = $@"SELECT TaxId, TaxCode, TaxRate
                                  FROM {salesTaxRateTableName}
                                  ORDER BY TaxId";

                using (SqlCommand cmd = new SqlCommand())
                {
                    cmd.CommandType = CommandType.Text;
                    cmd.CommandText = query;
                    cmd.Connection = conn;

                    conn.Open();

                    taxes = new TaxList();

                    using (SqlDataReader reader = cmd.ExecuteReader(CommandBehavior.CloseConnection))
                    {
                        int taxId;
                        string taxCode;
                        decimal taxRate;

                        while (reader.Read())
                        {
                            taxId = (int)reader["TaxId"];
                            taxCode = reader["TaxCode"] as string;
                            taxRate = (decimal)reader["TaxRate"];

                            taxes.Add(new Tax
                            {
                                TaxId = taxId,
                                TaxCode = taxCode,
                                TaxRate = taxRate
                            });
                        }
                    }
                }
            }

            return taxes;
        }

    }
}
