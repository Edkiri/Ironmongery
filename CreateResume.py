from utils import string_to_float
import xlsxwriter
from functools import reduce
from datetime import date
# Tkinter
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
# Models
from models import Order, Sale


class CreateResume():
  
  def __init__(self, parent, sale_id, rate):
    try:
      self.sale_id = sale_id
      self.parent = parent
      self.rate = rate
      self.orders = Order.select().where(Order.sale_id == sale_id)
      self.sale = Sale.get(Sale.id == self.sale_id)
      if not self.sale.client:
        raise Exception('No se encontró el cliente')
      self.resume_window = tk.Toplevel(padx=30, pady=50)
      # Title.
      title = 'Crear nota de entrega'
      self.resume_window.title(title)
      title_label = tk.Label(
          self.resume_window,
          text=title,
          font=('calibri', 18, 'bold'))
      title_label.grid(row=0, column=0, pady=(0,20), columnspan=2)
      
      # Currency.
      curr_label = tk.Label(
          self.resume_window,
          text="Moneda",
          font=('calibri', 15))
      curr_label.grid(row=1, column=0, sticky=tk.W)
      self.currency = tk.StringVar()
      currency_choices = ('', 'Bolívares', 'Dólares')
      self.currency.set(currency_choices[1])
      curr_option = ttk.OptionMenu(
          self.resume_window,
          self.currency,
          *currency_choices)
      curr_option.grid(row=1, column=1, sticky=tk.E)
      
      # Sale Option.
      option_label = tk.Label(
          self.resume_window,
          text="Condición",
          font=('calibri', 15))
      option_label.grid(row=2, column=0, pady=(10,0), sticky=tk.W)
      self.option = tk.StringVar()
      option_choices = ('', 'DE CONTADO', 'CRÉDITO')
      self.option.set(option_choices[1])
      curr_option = ttk.OptionMenu(
          self.resume_window,
          self.option,
          *option_choices)
      curr_option.grid(row=2, column=1, pady=(10,0), sticky=tk.E)
      
      # IVA.
      iva_label = tk.Label(
          self.resume_window,
          text="IVA",
          font=('calibri', 15))
      iva_label.grid(row=3, column=0, pady=(10,0), sticky=tk.W)
      self.iva = tk.StringVar()
      iva_choices = ('', 'No', 'Sí')
      self.iva.set(iva_choices[1])
      iva_options = ttk.OptionMenu(
          self.resume_window,
          self.iva,
          *iva_choices)
      iva_options.grid(row=3, column=1, pady=(10,0), sticky=tk.E)
      
      # Rate
      # Amount
      rate_label = tk.Label(
          self.resume_window,
          text="Tasa",
          font=('calibri', 15))
      rate_label.grid(row=4, pady=(10,0), sticky=tk.W)
      self.rate_entry = ttk.Entry(
          self.resume_window, 
          width=13, 
          font=('calibri', 15),
          justify='right')
      self.rate_entry.insert(0, self.rate)
      self.rate_entry.grid(row=4, column=1, pady=(10,0), sticky=tk.E)
      
      
      create_button = tk.Button(
        self.resume_window,
        text="Crear",
        font=('calibri', 18, 'bold'),
        bd=1,
        relief=tk.RIDGE,
        bg='#54bf54',
        command=self.create_xlsx
      )
      create_button.grid(row=7, pady=(20,0), sticky=tk.W+tk.E, columnspan=2)
      
    except Exception as err:
      messagebox.showerror("Error!", err, parent=self.parent)
      


  def create_xlsx(self):
    if self.currency.get() == 'Bolívares' and string_to_float(self.rate_entry.get()) == 0:
      messagebox.showerror("Error!", 'No se pudo leer la tasa', parent=self.resume_window)
    else:
      workbook  = xlsxwriter.Workbook(f'./resumes/NOTA_DE_ENTREGA_{self.sale_id}.xlsx')
      worksheet = workbook.add_worksheet("NOTA_DE_ENTREGA")


      worksheet.set_column('C:C', 65)
      worksheet.set_column('D:D', 25)
      worksheet.set_column('E:E', 25)


      # TITLE
      ENTERPRISE_NAME = 'COMERCIAL GUERRA C.A.'
      SUBTITLE = 'FERRETERÍA EN GENERAL'
      ADDRESS = 'CALLE SANTA ROSA  TEL: 0293-4310577  CUMANA RIF.J-08013970-4 '

      title_format = workbook.add_format({
        'font_size': 24,
        'align': 'center',
        'bold': True,
      })
      subtitle_format = workbook.add_format({
        'font_size': 20,
        'align': 'center',
      })
      address_format = workbook.add_format({
        'font_size': 12,
        'align': 'center',
      })
      worksheet.merge_range(2, 1, 2, 4, ENTERPRISE_NAME, title_format)
      worksheet.merge_range(3, 1, 3, 4, SUBTITLE, subtitle_format)
      worksheet.merge_range(4, 1, 4, 4, ADDRESS, address_format)


      # HEADER_1

      header_top_format = workbook.add_format({
        'font_size': 12,
        'top': 2,
        'left': 2,
        'right': 2,
        'bold': True,
        'align': 'center',
      })
      header_bottom_format = workbook.add_format({
        'font_size': 12,
        'bottom': 2,
        'left': 2,
        'right': 2,
        'align': 'center',
      })


      CLIENT_NAME_HEADER = 'NOMBRE O RAZÓN SOCIAL'
      worksheet.merge_range(6, 1, 6, 2, CLIENT_NAME_HEADER, header_top_format)
      worksheet.merge_range(7, 1, 7, 2, self.sale.client.name, header_bottom_format)

      CLIENT_RIF_HEADER = 'RIF'
      worksheet.write('D7', CLIENT_RIF_HEADER, header_top_format)
      worksheet.write('D8', self.sale.client.identity_card, header_bottom_format)

      CLIENT_PAYMENT_CONDITION = 'CONDICIÓN DE PAGO'
      worksheet.write('E7', CLIENT_PAYMENT_CONDITION, header_top_format)
      worksheet.write('E8', self.option.get(), header_bottom_format)

      # HEADER 2

      CLIENT_ADDRESS_HEADER = 'DIRECCIÓN'
      worksheet.merge_range(8, 1, 8, 2, CLIENT_ADDRESS_HEADER, header_top_format)
      worksheet.merge_range(9, 1, 9, 2, 'CUMANÁ', header_bottom_format)

      SALE_DATE_HEADER = 'FECHA'
      TODAY = date.today().strftime('%d/%m/%y')
      worksheet.write('D9', SALE_DATE_HEADER, header_top_format)
      worksheet.write('D10', TODAY, header_bottom_format)

      CLIENT_PHONE_HEADER = 'TELÉFONO'
      worksheet.write('E9', CLIENT_PHONE_HEADER, header_top_format)
      worksheet.write('E10', self.sale.client.phone_number, header_bottom_format)


      # ORDER LIST

      # Header
      header_format = workbook.add_format({
        'font_size': 12,
        'border': 2,
        'align': 'center',
        'bold': True,
      })
      price_u_header_title = 'PRECIO U. $'
      order_price_header_title = 'MONTO $'
      if self.currency.get() == 'Bolívares':
        price_u_header_title = price_u_header_title.rstrip('$')
        order_price_header_title = order_price_header_title.rstrip('$')
        price_u_header_title += 'BsS'
        order_price_header_title += 'BsS'
      worksheet.write('B11', 'CAN.', header_format)
      worksheet.write('C11', 'DESCRIPCIÓN', header_format)
      worksheet.write('D11', price_u_header_title, header_format)
      worksheet.write('E11', order_price_header_title, header_format)

      def write_order_row(index, order=None):
        row_format_center = workbook.add_format({
          'font_size': 12,
          'left': 2,
          'right': 2,
          'bottom': 1,
          'align': 'center',
        })
        row_format_right = workbook.add_format({
          'font_size': 12,
          'left': 2,
          'right': 2,
          'bottom': 1,
          'align': 'right',
        })
        name, quantity, unit_price = None, 0, 0
        if order:
          name = order.product.name
          quantity = order.amount
          unit_price = order.product.price
        
        total_order = unit_price * quantity
        if self.currency.get() == 'Bolívares':
          total_order *= string_to_float(self.rate_entry.get())
          unit_price *= string_to_float(self.rate_entry.get())
        if total_order == 0:
          total_order = '-'
          unit_price = '-'
        worksheet.write(f'B{index}', quantity, row_format_center)
        worksheet.write(f'C{index}', name, row_format_center)
        worksheet.write(f'D{index}', unit_price, row_format_right)
        worksheet.write(f'E{index}', total_order, row_format_right)
          
      DEFAULT_ROWS = 8
      order_row_index = 12
      for order in self.orders:
        write_order_row(order_row_index, order)
        order_row_index += 1
        
      if len(self.orders) < DEFAULT_ROWS:
        rows_for_fill = DEFAULT_ROWS - len(self.orders)
        for row in range(rows_for_fill):
          write_order_row(order_row_index)
          order_row_index += 1


      # FOOTER

      # RESUME ID 
      RESUME_ID = f'NOTA DE ENTREGA \n NÚMERO {self.sale_id}'
      resume_format = workbook.add_format({
        'font_size': 12,
        'border': 2,
        'align': 'center',
        'valign': 'top',
      })
      worksheet.merge_range(
        order_row_index - 1, 
        1, 
        order_row_index + 1, 
        2, 
        RESUME_ID, 
        resume_format
      )

      # ORDERS TOTAL
      top_title_format = workbook.add_format({
        'font_size': 12,
        'align': 'center',
        'top': 2,
        'right': 2,
        
      })
      middle_title_format = workbook.add_format({
        'font_size': 12,
        'align': 'center',
        'top': 1,
        'right': 2,
      })
      bottom_title_format = workbook.add_format({
        'font_size': 12,
        'align': 'center',
        'top': 2,
        'right': 2,
        'bottom': 2,
        'bold': True,
        
      })

      iva_title = None
      sub_total_title = 'SUB. TOTAL $'
      total_title = 'TOTAL $'
      if (self.currency.get() == 'Bolívares') and (self.iva.get() == 'Sí'):
        iva_title = 'IVA 16%'
      if (self.currency.get() == 'Bolívares'):
        sub_total_title = sub_total_title.rstrip('$')
        sub_total_title += 'BsS'
        total_title = total_title.rstrip('$')
        total_title += 'BsS'
      worksheet.write(f'D{order_row_index}', sub_total_title, top_title_format)
      worksheet.write(f'D{order_row_index + 1}', iva_title, middle_title_format)
      worksheet.write(f'D{order_row_index + 2}', total_title, bottom_title_format)

      top_amount_format = workbook.add_format({
      'font_size': 12,
        'align': 'right',
        'top': 2,
        'right': 2,
      })
      middle_amount_format = workbook.add_format({
      'font_size': 12,
        'align': 'right',
        'top': 1,
        'right': 2,
      })
      bottom_amount_format = workbook.add_format({
      'font_size': 12,
        'align': 'right',
        'top': 2,
        'right': 2,
        'bottom': 2,
        'bold': True,
      })
      
      iva = 0.16
      total = reduce(
          lambda acc, cur: acc + cur.product.price, 
          self.orders,
          0
        )
      sub_total, total_iva = total, None
      if (self.currency.get() == 'Bolívares'):
        total = total * string_to_float(self.rate_entry.get())
        if (self.iva.get() == 'Sí'):
          sub_total = "%.2f" % (total * (1 - iva))
          total_iva = "%.2f" % (total * iva)
      
      worksheet.write(f'E{order_row_index}', sub_total, top_amount_format)
      worksheet.write(f'E{order_row_index + 1}', total_iva, middle_amount_format)
      worksheet.write(f'E{order_row_index + 2}', total, bottom_amount_format)

      workbook.close()
      messagebox.showinfo('Nota de entrega', 'La nota de entrega se creó exitosamente', parent=self.parent)
      self.resume_window.destroy()