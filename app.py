from flask import Flask, render_template, request, redirect, url_for
from datetime import datetime
import os

app = Flask(__name__)

# Ensure the bill directory exists
if not os.path.exists('static/bill'):
    os.makedirs('static/bill')

bills = []  # This will store bill data in memory for simplicity
customer_id = 0  # Initialize customer ID

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/dashboard')
def dashboard():
    # Read bills from the file directory for demonstration
    bill_files = os.listdir('static/bill')
    bills = [(datetime.fromtimestamp(os.path.getmtime(f'static/bill/{file}')), file) for file in bill_files]
    return render_template('Dashboard.html', bills=bills)

@app.route('/generate_bill', methods=['GET', 'POST'])
def generate_bill():
    global customer_id
    if request.method == 'POST':
        name = request.form['name']
        address = request.form['address']
        gst_percent = request.form['gst_percent']
        total_items = int(request.form['total_items'])
        
        items = []
        for i in range(1, total_items + 1):
            item_name = request.form[f'item_name_{i}']
            item_price = request.form[f'item_price_{i}']
            items.append((item_name, item_price))
        
        customer_id += 1  # Increment customer ID
        bill_filename = f'bill_{name}_{customer_id}.txt'
        bill_path = os.path.join('static/bill', bill_filename)
        
        with open(bill_path, 'w') as bill_file:
            bill_file.write('Sudeep-Develops\n'.center(0, ' '))
            bill_file.write('\n')
            bill_file.write(f'Customer ID: {customer_id}\n'.center(0, ' '))
            bill_file.write(f'Name: {name}\n'.center(0, ' '))
            bill_file.write(f'Address: {address}\n'.center(0, ' '))
            bill_file.write(f'GST Percentage: {gst_percent}\n'.center(0, ' '))
            bill_file.write('Items:\n'.center(0, ' '))
            for item in items:
                bill_file.write(f'  - {item[0]}: {item[1]}\n'.center(0, ' '))

        return redirect(url_for('dashboard'))

    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
