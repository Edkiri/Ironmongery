# TKinter.
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
# Database.
import sqlite3
# Utilities.
from datetime import datetime, date, timedelta
# Dates.
# All dates are in "day-month-year" format.
DATE_FORMAT = "%d-%m-%Y"
TODAY = date.today().strftime(DATE_FORMAT)
def get_weekday(day_str):
    weekDays = ("Lunes","Martes","Miércoles","Jueves","Viernes","Sábado","Domingo")
    day = datetime.strptime(day_str, DATE_FORMAT)
    return weekDays[day.weekday()]

class Sales():
    """Sale Object."""
    db_name = "comercial_guerra.db"
    columns = [
        "fecha","tasa","punto_de_venta","pago_movil",   
        "bolivares_efectivo", "dolares_efectivo", 
        "zelle", "vuelto_bolivares", "vuelto_dolares", 
        "total_dolares"]
    column_names = [
        "Fecha", "Tasa", "Punto", "Pago Móvil",
        "Bs ft",  "$ ft",  "Zelle",
        "Vuelto Bs", "Vuelto $",
        "Total $"]

    def __init__(self, root):
        """Init Func."""
        self.root = root
        self.root.title("Comercial Guerra - Ventas")
        # Action buttons Frame
        self.buttons_frame = LabelFrame(self.root)
        self.buttons_frame.grid(row=0, column=0, pady=5, padx=5, sticky=N)
        # Action buttons
        add_sale_button = Button(self.buttons_frame, text="Agregar", command=self.add_sale)
        edit_sale_button = Button(self.buttons_frame, text="Editar", command=self.update_sale)
        delete_sale_button = Button(self.buttons_frame, text="Eliminar", command=self.delete_sale)
        # Display cutton
        add_sale_button.grid(row=0, column=1, pady=(10,0), padx=10, ipadx=1)
        edit_sale_button.grid(row=1, column=1, pady=(10,0), padx=10, ipadx=7)
        delete_sale_button.grid(row=2, column=1, pady=(10,10), padx=10)
        # Rate
        rate_label = Label(self.buttons_frame, text="Tasa del día")
        rate_label.grid(row=6, column=1, padx=5)
        self.rate = Entry(self.buttons_frame, width=10, borderwidth=4)
        self.rate.grid(row=7, column=1, padx=5, pady=5)
        self.rate.insert(0,0)
        # Current date
        self.query_date = Entry(self.buttons_frame, width=12, borderwidth=4)
        self.query_date.insert(0, TODAY)
        self.query_date.grid(row=9, column=1, padx=10)
        today_button = Button(self.buttons_frame, text="Hoy", command=self.today)
        today_button.grid(row=8, column=1, pady=(15,5))
        day_up_button = Button(self.buttons_frame, text=">", command=lambda: self.change_day(">"))
        day_down_button = Button(self.buttons_frame, text="<", command=lambda: self.change_day("<"))
        day_up_button.grid(row=8, column=1, pady=(15,5), padx=10, sticky=E)
        day_down_button.grid(row=8, column=1, pady=(15,5), padx=10, sticky=W)
        display_tree_button = Button(self.buttons_frame, text="Mostrar ventas", command=self.display_tree_day)
        display_tree_button.grid(row=10, column=1, pady=12)
        # Table
        self.display_tree_day()

    def add_sale(self):
        win = Toplevel()
        win.title("Agregar venta")
        # Calculte total $
        def calculate_total(values):
            total = 0
            values = [float(x) for x in values[1:]]
            bs = values[1] + values[2] + values[3] - values[6]
            usd = values[4] + values[5] - values[7]
            rate = values[0]
            if bs != 0:
                total = (bs / rate) + usd
            else:
                total = usd
            return total
        # Save sale
        def save():
            insert_query = """INSERT INTO 'ventas' (
                        '{}', '{}', '{}', '{}', '{}','{}', '{}','{}', '{}', '{}')
                        VALUES (?,?,?,?,?,?,?,?,?,?);""".format(*self.columns)
            values = [value.get() for value in data.values()]
            try:
                values.append(calculate_total(values))
                self.run_query(insert_query, values)
                self.query_date.delete(0, END)
                self.query_date.insert(0, values[0])
                self.display_tree_day()
                win.destroy()
            except ZeroDivisionError:
                messagebox.showerror("Error", "Debes especificar una tasa al agregar una venta en bolívares.")

        # Display entrys and set defaults
        data = {}
        for i, column in enumerate(self.columns[:-1]):
            frame = LabelFrame(win, padx=10, pady=10, width=500)
            frame.grid(row=i, column=0)
            data[column] = Entry(frame, width=20, borderwidth=3)
            data[column].grid(row=1, column=1)
            if column == 'fecha':
                data[column].insert(0, self.query_date.get())
            elif column == 'tasa':
                data[column].insert(0, self.rate.get())
            else:
                data[column].insert(0, 0)
            Label(frame, text=self.column_names[i], width=8, padx=3).grid(row=1, column=0)
        
        save_button = Button(win, text="Guardar", command=save).grid(row=10, column=0, pady=10)

    def format_tuple_numbers(self, sale_tuple):
        try:
            format_sale = ["{:,.2f}".format(x) for x in sale_tuple]
            return tuple(format_sale)
        except ValueError:
            return sale_tuple

    def run_query(self, query, params = ()):
        with sqlite3.connect(self.db_name) as conn:
            c = conn.cursor()
            result = c.execute(query, params)
            conn.commit()
        return result

    def today(self):
        self.query_date.delete(0, END)
        self.query_date.insert(0, TODAY)

    def get_sales(self):
        select_query = """SELECT 
                                tasa, punto_de_venta, pago_movil, bolivares_efectivo,
                                dolares_efectivo, zelle, vuelto_bolivares, vuelto_dolares,
                                total_dolares, oid FROM ventas WHERE fecha = '{}'""".format(self.query_date.get())
        sales = self.run_query(select_query).fetchall()
        return sales

    def change_day(self, sign):
        current_date = datetime.strptime(self.query_date.get(), DATE_FORMAT)
        if sign == ">":
            new_date = current_date + timedelta(days=1)
        else:
            new_date = current_date + timedelta(days=-1)
        self.query_date.delete(0, END)
        self.query_date.insert(0, new_date.strftime(DATE_FORMAT))
        
    def display_tree_day(self):
        date = self.query_date.get()
        tree_frame = LabelFrame(self.root)
        tree_frame.grid(row=0, column=1, rowspan=2)
        tree_label = Label(tree_frame, text="Ventas del {} {}".format(get_weekday(date), date))
        tree_label.grid(row=0, column=0, pady=(10,0))
        self.tree = ttk.Treeview(tree_frame, height=25)
        self.tree.column("#0", width=0, stretch=NO)
        self.tree['columns'] = tuple(self.column_names[1:])
        for i, col in enumerate(self.tree['columns']):
            if i in (4,5,7,8):
                self.tree.column(col, width=60, minwidth=25)
            else:
                self.tree.column(col, width=100, minwidth=25)
            self.tree.heading(col, text=col, anchor=W)
        self.tree.grid(row=1, column=0, padx=15, pady=10)
        self.sales = self.get_sales()
        for sale in self.sales:
            self.tree.insert(parent="",index='end', iid=sale[-1], text="", values=self.format_tuple_numbers(sale))
        self.day_summary()

    def update_sale(self):
        if self.tree.focus():
            update_win = Toplevel()
            update_win.title("Editor de ventas")
            iid = self.tree.focus()
            sale = self.run_query("SELECT * FROM ventas WHERE oid = {}".format(iid)).fetchone()

            def update():
                update_query = """UPDATE ventas SET 
                                        fecha=?, tasa=?, punto_de_venta=?,
                                        pago_movil=?, bolivares_efectivo=?,
                                        dolares_efectivo=?, zelle=?,
                                        vuelto_bolivares=?, vuelto_dolares=?,
                                        total_dolares=? WHERE oid = {}""".format(iid)
                new_sale = []
                for value in data.values():
                    new_sale.append(value.get())
                self.run_query(update_query, new_sale)
                self.display_tree_day()
                update_win.destroy()

            data = {}
            for i, column in enumerate(self.columns):
                frame = LabelFrame(update_win, padx=10, pady=10, width=500)
                frame.grid(row=i, column=0)
                data[column] = Entry(frame, width=20, borderwidth=3)
                data[column].grid(row=1, column=1)
                data[column].insert(0, sale[i])
                Label(frame, text=self.column_names[i], width=8, padx=3).grid(row=1, column=0)

            save_button = Button(update_win, text="Guardar", command=update).grid(row=10, column=0, pady=10)

        else:
            print("Error! Debes seleccionar una venta.")

    def delete_sale(self):
        if self.tree.focus():
            iid = self.tree.focus()
            response = messagebox.askyesno("Atención, atención!", "¿Quieres borrar esta venta?")
            if response:
                delete_query = """DELETE FROM ventas 
                                WHERE oid = {}""".format(iid)
                self.run_query(delete_query)
                self.display_tree_day()
        else:
            print("Error! Debes seleccionar una venta.")

    def day_summary(self):
        summary_frame = LabelFrame(self.root)
        summary_frame.place(x=10, y=320)
        frame_title = Label(summary_frame, text="Resumen del día")
        frame_title.grid(row=0, column=0, sticky=N)
        bs = 0
        dollars = 0
        if self.sales:
            for sale in self.sales:
                bs += (sale[1] + sale[2] + sale[3] - sale[6])
                dollars += (sale[4] + sale[5] - sale[7])
        bs_label = Label(summary_frame, text=str("{:,}".format(bs))+" bsf")
        bs_label.grid(row=1, column=0)
        dollar_label = Label(summary_frame, text=str("{:,}".format(dollars))+" $")
        dollar_label.grid(row=2, column=0)
            
if __name__ == '__main__':
    root = Tk()
    app = Sales(root)
    root.mainloop()