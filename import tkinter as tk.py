import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime

class ExpirationTracker:
    def __init__(self, root):
        self.root = root
        self.root.title("Expiration Tracker V1")
        self.root.geometry("600x700")
        
        self.items = []
        
        self.create_widgets()
        self.update_display()
    
    def create_widgets(self):
        # Main frame
        main_frame = ttk.Frame(self.root, pad="10")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Title
        title_label = ttk.Label(main_frame, text="Expiration Tracker", font=('Arial', 14, 'bold'))
        title_label.pack(pady=10)
        
        # Input frame
        input_frame = ttk.Frame(main_frame)
        input_frame.pack(fill=tk.X, pady=10)
        
        # Item name
        ttk.Label(input_frame, text="Item:").grid(row=0, column=0, padx=5)
        self.name_entry = ttk.Entry(input_frame, width=20)
        self.name_entry.grid(row=0, column=1, padx=5)
        
        # Expiration date
        ttk.Label(input_frame, text="Exp Date (YYYY-MM-DD):").grid(row=0, column=2, padx=5)
        self.date_entry = ttk.Entry(input_frame, width=15)
        self.date_entry.grid(row=0, column=3, padx=5)
        
        # Add button
        add_btn = ttk.Button(input_frame, text="Add Item", command=self.add_item)
        add_btn.grid(row=0, column=4, padx=10)
        
        # Today button
        today_btn = ttk.Button(input_frame, text="Today", command=self.set_today)
        today_btn.grid(row=0, column=5, padx=5)
        
        # List frame
        list_frame = ttk.Frame(main_frame)
        list_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        # Treeview
        columns = ('Item', 'Expiration', 'Days Left')
        self.tree = ttk.Treeview(list_frame, columns=columns, show='headings', height=12)
        
        # Set headings
        self.tree.heading('Item', text='Item Name')
        self.tree.heading('Expiration', text='Expiration Date')
        self.tree.heading('Days Left', text='Days Left')
        
        # Set column widths
        self.tree.column('Item', width=200)
        self.tree.column('Expiration', width=150)
        self.tree.column('Days Left', width=100)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Button frame
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(pady=10)
        
        ttk.Button(button_frame, text="Delete Selected", 
                  command=self.delete_item).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Clear All", 
                  command=self.clear_all).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Check Expiring", 
                  command=self.check_expiring).pack(side=tk.LEFT, padx=5)
    
    def set_today(self):
        today = datetime.now().strftime('%Y-%m-%d')
        self.date_entry.delete(0, tk.END)
        self.date_entry.insert(0, today)
    
    def calculate_days_left(self, expiration_date):
        try:
            exp_date = datetime.strptime(expiration_date, '%Y-%m-%d')
            today = datetime.now()
            days_left = (exp_date - today).days
            return days_left
        except ValueError:
            return "Invalid"
    
    def add_item(self):
        name = self.name_entry.get().strip()
        date = self.date_entry.get().strip()
        
        if not name or not date:
            messagebox.showerror("Error", "Please enter both item name and date")
            return
        
        self.items.append({'name': name, 'date': date})
        self.name_entry.delete(0, tk.END)
        self.date_entry.delete(0, tk.END)
        self.update_display()
        messagebox.showinfo("Success", "Item added successfully!")
    
    def update_display(self):
        # Clear existing items
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Sort items by expiration date
        self.items.sort(key=lambda x: x['date'])
        
        # Add items to treeview
        for item in self.items:
            days_left = self.calculate_days_left(item['date'])
            
            # Add color coding based on days left
            tags = ()
            if days_left == "Invalid":
                tags = ('invalid',)
            elif days_left < 0:
                tags = ('expired',)
            elif days_left <= 7:
                tags = ('warning',)
            
            self.tree.insert('', 'end', values=(
                item['name'], item['date'], days_left
            ), tags=tags)
        
        # Configure tag colors
        self.tree.tag_configure('expired', background="red")
        self.tree.tag_configure('warning', background= "yellow")
        self.tree.tag_configure('invalid', background= "gray")
    
    def delete_item(self):
        selected = self.tree.selection()
    
        
        # Get the selected item's values
        item_values = self.tree.item(selected[0])['values']
        item_name = item_values[0]
        
        # Remove from list
        self.items = [item for item in self.items if item['name'] != item_name]
        
        self.update_display()
    
    def clear_all(self):
        if messagebox.askyesno("Confirm", "Are you sure you want to clear all items?"):
            self.items = []
            self.update_display()
    
    def check_expiring(self):
        expiring_items = []
        
        for item in self.items:
            days_left = self.calculate_days_left(item['date'])
            if days_left != "Invalid" and days_left <= 7:
                status = "EXPIRED" if days_left < 0 else f"in {days_left} days"
                expiring_items.append(f"• {item['name']} - {item['date']} ({status})")
        
        if expiring_items:
            message = "Items expiring soon:\n\n" + "\n".join(expiring_items)
            messagebox.showwarning("Expiration Alert", message)
        else:
            messagebox.showinfo("No Alerts", "No items expiring in the next 7 days!")

def main():
    root = tk.Tk()
    app = ExpirationTracker(root)
    root.mainloop()

if __name__ == "__main__":
    main()