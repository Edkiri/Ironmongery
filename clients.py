# Tkinter.
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

# Models.
from models import Client

# Peewee.
from peewee import IntegrityError

class SearchClient:

    def __init__(self, callback):

        self.callback = callback

        # Window.
        self.search_window = tk.Toplevel(
            width=350, 
            height=350,
            padx=30, 
            pady=30
        )
        # Title
        search_label = tk.Label(
            self.search_window,
            text="Buscar cliente",
            font=('calibri', 18, 'bold'))
        search_label.grid(row=0, column=0, columnspan=2, pady=(0,15))
        # Name Entry
        self.name_entry = ttk.Entry(
            self.search_window, 
            width=18, 
            font=('calibri', 15))
        self.name_entry.focus()
        self.name_entry.grid(row=1, column=0, sticky=tk.W, pady=(0,20))
        def search(event):
            self._search_in_database()
        self.name_entry.bind("<Return>", search)
        # Tree
        columns = ('id', 'name', 'id_card')
        self.clients_tree = ttk.Treeview(
            self.search_window, 
            height=5, 
            selectmode ='browse',
            columns=columns,
            style="mystyle.Treeview")
        # HEADING
        self.clients_tree.column("#0", width=0, stretch=tk.NO)
        # Client Id.
        self.clients_tree.column('id', width=0, stretch=tk.NO)
        # Name.
        self.clients_tree.column('name', width=150, minwidth=25)
        self.clients_tree.heading('name', text='Nombre', anchor=tk.W)
        # Identity card.
        self.clients_tree.column('id_card', width=150, minwidth=25)
        self.clients_tree.heading('id_card', text='Cédula', anchor=tk.W)
        # Grid tree.
        self.clients_tree.grid(row=1, column=1)

        # Select button.
        select_client_button = tk.Button(
                self.search_window, 
                text="Verificar", 
                font=('calibri', 12),
                bd=1,
                relief=tk.RIDGE,
                bg='#54bf54',
                command=self._get_client
        )
        select_client_button.grid(row=2, column=0, columnspan=2, pady=(15,0))

    
    def _search_in_database(self):
        name = self.name_entry.get()
        clients = Client.select().where(Client.name.contains(name))

        for client in clients:
            self.clients_tree.insert(
                "",
                index='end',
                values=(
                    client.id,
                    client.name,
                    client.identity_card
                )
            )

    
    def _get_client(self):
        if self.clients_tree.focus():
            index = self.clients_tree.focus()
            client_id = self.clients_tree.item(index)['values'][0]
            if client_id:
                client = Client.get(id=client_id)
                self.callback(client)
                self.search_window.destroy()



class ClientHandler():

    def __init__(self, frame, client=None):
        self.frame = frame
        self.client = client


        
    def display_client_checker(self):
        
        # Client Label.
        self.client_label = tk.Label(
            self.frame,
            text="Cliente: ",
            font=('calibri', 15, 'bold'))
        
        # Pre-Id
        self.pre_id = tk.StringVar()
        self.pre_id_choices = ('', 'V', 'J')
        self.pre_id.set(self.pre_id_choices[1])
        self.curr_option = ttk.OptionMenu(
            self.frame,
            self.pre_id,
            *self.pre_id_choices)

        # Id Entry
        self.id_entry = ttk.Entry(
            self.frame, 
            width=12, 
            font=('calibri', 14))

        def client_callback(event):
            self.client_checker()
        self.id_entry.bind("<Return>", client_callback)

        # Verify Button
        self.verify_client_button = tk.Button(
                self.frame, 
                text="Verificar", 
                font=('calibri', 12),
                bd=1,
                relief=tk.RIDGE,
                bg='#54bf54',
                command=self.client_checker)
        # Search client.
        def display_client_searching():
            search_client = SearchClient(self.update_client_frame)
        self.search_button = tk.Button(
            self.frame, 
            text="Buscar",
            font=('calibri', 12),
            bd=1,
            relief=tk.RIDGE,
            bg='#54bf54',
            command=display_client_searching)
        
        # Grid
        self.client_label.grid(row=0, column=0)
        self.id_entry.grid(row=0, column=2)
        self.curr_option.grid(row=0, column=1)
        self.verify_client_button.grid(row=0, column=3, padx=4)
        self.search_button.grid(row=0, column=4, padx=(20,0))
   
   
   
    def client_checker(self):
        try:
            pre_id = self.pre_id.get()
            id_card = self.id_entry.get()
            client = Client.get(identity_card=pre_id + "-" + id_card)
            self.update_client_frame(client)
        except Exception as err:
            self.create_or_update_client()
    
    
    
    def display_client_detail(self, client):
        
        self.client = client

        # Client Label.
        self.client_label = tk.Label(
            self.frame,
            text="Cliente: ",
            font=('calibri', 15, 'bold'))

        # Client name.
        self.client_name_label = tk.Label(
                self.frame,
                text="",
                font=('calibri', 15))
        
        # Client Id.
        self.id_client_label = tk.Label(
            self.frame,
            text=self.client.identity_card,
            font=('calibri', 15))
        

        # Detail button
        self.update_button = tk.Button(
            self.frame, 
            text="Detalle",
            font=('calibri', 12),
            bd=1,
            relief=tk.RIDGE,
            bg='#54bf54',
            command=lambda: self.create_or_update_client(self.client.id))

        # Calcel button.
        def change_client():
            self.cancel_client()
            self.display_client_checker()
        self.cancel_button = tk.Button(
            self.frame, 
            text="Cambiar",
            font=('calibri', 12),
            bd=1,
            relief=tk.RIDGE,
            bg='#e85d5d',
            command=change_client)
        self.client_name_label['text'] = self.client.name
        
        # Grid
        self.client_label.grid(row=0, column=0)
        self.client_name_label.grid(row=0, column=1)
        self.id_client_label.grid(row=0, column=2, padx=(15,30))
        self.update_button.grid(row=0, column=3)
        self.cancel_button.grid(row=0, column=4, padx=(20,0))
    
    
    
    def cancel_client(self):
        self.client = None
        self.cancel_button.grid_forget()
        self.client_name_label.grid_forget()
        self.id_client_label.grid_forget()
        self.update_button.grid_forget()    


    def update_client_frame(self, client):
        self.verify_client_button.grid_forget()
        self.id_entry.grid_forget()
        self.curr_option.grid_forget()
        self.search_button.grid_forget()
        self.display_client_detail(client)


    def create_or_update_client(self, client_id=None):
        # Functions.
        def create_client():
            try:
                client = Client.create(
                    name=name_entry.get(), 
                    identity_card=pre_id.get() + "-" + identity_entry.get(),
                    phone_number=phone_entry.get())
                new_client_window.destroy()
                self.update_client_frame(client)

            except IntegrityError:
                error_message = "Ya existe un cliente con esta cédula o rif."
                messagebox.showerror("Error", error_message, parent=new_client_window)
        
        def update_client():
            client = Client.get(Client.id == client_id)
            
            ident = pre_id.get() + "-" + identity_entry.get()
            if client.identity_card != ident:
                client.identity_card = ident

            if client.name != name_entry.get():
                client.name = name_entry.get()
            
            if client.phone_number != phone_entry.get():
                client.phone_number = phone_entry.get()
            
            client.save()
            new_client_window.destroy()
            self.cancel_client()
            self.client = client
            self.display_client_detail(client)

        # New Window.
        new_client_window = tk.Toplevel(
            width=350, 
            height=350,
            padx=30, 
            pady=30)
        title = "Nuevo Cliente"
        if client_id:
            title = "Cliente"
        # Title.
        client_label = tk.Label(
            new_client_window,
            text=title,
            font=('calibri', 18, 'bold'))
        client_label.grid(row=0, column=0, columnspan=3, pady=(0,15))

        # Frame.
        new_client_frame = tk.Frame(new_client_window)
        new_client_frame.grid(row=1,column=0,padx=20,pady=20)

        # Name.
        name_label = tk.Label(
            new_client_frame,
            text="Nombre",
            font=('calibri', 15))
        name_label.grid(row=0, column=0, sticky= tk.W, pady=(0,20))
        name_entry = ttk.Entry(
            new_client_frame, 
            width=18, 
            font=('calibri', 15))
        name_entry.focus()
        name_entry.grid(row=0, column=2, sticky=tk.W, pady=(0,20))

        # Pre-Identity-card.
        pre_id = tk.StringVar()
        pre_id_choices = ('', 'V', 'J')
        curr_option = ttk.OptionMenu(
            new_client_frame,
            pre_id,
            *pre_id_choices)
        curr_option.grid(row=1, column=1, pady=(0,20))

        # Identity-card.
        identity_label = tk.Label(
            new_client_frame,
            text="Cédula",
            font=('calibri', 15))
        identity_label.grid(row=1, column=0, sticky= tk.W, pady=(0,20))
        identity_entry = ttk.Entry(
            new_client_frame, 
            width=18, 
            font=('calibri', 15))
        identity_entry.grid(row=1, column=2, sticky=tk.W, pady=(0,20))


        # Phone number.
        phone_label = tk.Label(
            new_client_frame,
            text="Teléfono",
            font=('calibri', 15))
        phone_label.grid(row=2, column=0, sticky= tk.W, pady=(0,20))
        phone_entry = ttk.Entry(
            new_client_frame, 
            width=18, 
            font=('calibri', 15))
        phone_entry.grid(row=2, column=2, sticky=tk.W, pady=(0,20))

        # Buttons.
        cancel_button = tk.Button(
            new_client_frame, 
            text="Cancelar", 
            font=('calibri', 12),
            bd=1,
            relief=tk.RIDGE,
            bg='#e85d5d',
            command=new_client_window.destroy)
        cancel_button.grid(row=3, column=2, sticky=tk.E, pady=(15,0))
       
        if not client_id:
            add_client_button = tk.Button(
                new_client_frame, 
                text="Agregar", 
                font=('calibri', 12),
                bd=1,
                padx=15,
                relief=tk.RIDGE,
                bg='#54bf54',
                command=create_client)
            add_client_button.grid(row=3, column=0,  columnspan=2, sticky=tk.W, pady=(15,0))
            pre_id.set(self.pre_id.get())
            identity_entry.insert(0, self.id_entry.get())
        else:
            client = Client.get(Client.id == client_id)
            name_entry.insert(0, client.name)
            pre_id.set(client.identity_card.split("-")[0])
            identity_entry.delete(0, 'end')
            identity_entry.insert(0, client.identity_card.split("-")[1])
            phone_entry.insert(0, client.phone_number)
            update_client_button = tk.Button(
                new_client_frame, 
                text="Modificar", 
                font=('calibri', 12),
                bd=1,
                padx=15,
                relief=tk.RIDGE,
                bg='#54bf54',
                command=update_client)
            update_client_button.grid(row=3, column=0,  columnspan=2, sticky=tk.W, pady=(15,0))

