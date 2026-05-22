
from flask import Flask, render_template
import pandas as pd

app = Flask(__name__)

df = pd.read_csv('data/supermarket.csv')

@app.route('/')
@app.route('/dashboard')
def dashboard():
    total_sales = round(df['Sales'].sum(),2)
    total_orders = len(df)
    total_categories = df['Category'].nunique()

    category_sales = df.groupby('Category')['Sales'].sum().to_dict()

    return render_template(
        'dashboard.html',
        total_sales=total_sales,
        total_orders=total_orders,
        total_categories=total_categories,
        labels=list(category_sales.keys()),
        values=list(category_sales.values())
    )

@app.route('/analytics')
def analytics():
    data = df[['Order ID','Category','Sales']].head(15).to_dict(orient='records')
    return render_template('analytics.html', data=data)

@app.route('/customers')
def customers():
    customers = df.groupby('Customer Name')['Sales'].sum().reset_index().sort_values(by='Sales', ascending=False).head(10)
    data = customers.to_dict(orient='records')
    return render_template('customers.html', data=data)

@app.route('/products')
def products():
    products = df.groupby('Product Name')['Sales'].sum().reset_index().sort_values(by='Sales', ascending=False).head(10)
    data = products.to_dict(orient='records')
    return render_template('products.html', data=data)

@app.route('/regions')
def regions():
    regions = df.groupby('Region')['Sales'].sum().reset_index()
    data = regions.to_dict(orient='records')
    return render_template('regions.html', data=data)

if __name__ == '__main__':
    app.run(debug=True)
