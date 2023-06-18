import pandas as pd
import matplotlib.pyplot as plt

# Case 0
print("Case 0:")
data = pd.read_csv("retail_raw_reduced.csv")
data['order_date'] = pd.to_datetime(data['order_date'])
data_desember = data[(data['order_date'].dt.month == 12)]
jumlah_customers = data_desember.groupby('order_date')['customer_id'].nunique()

plt.figure(figsize=(10, 5))
plt.plot(jumlah_customers.index, jumlah_customers.values, marker='o', linestyle='-', color='g')
plt.title('Jumlah Pembeli Harian di Bulan Desember 2019', fontsize="15")
plt.xlabel('Tanggal')
plt.ylabel('Jumlah Unique Customers')
plt.grid(True)
plt.show()
print()

# Case 1
print("Case 1:")
data_desember = data[(data['order_date'].dt.month == 12)]
brand_quantity = data_desember.groupby('brand')['quantity'].sum()
top5_brands = brand_quantity.nlargest(5)
dataset_top5brand_dec = data_desember[data_desember['brand'].isin(top5_brands.index)]
print("Top 5 brands dengan jumlah penjualan terbanyak pada Desember 2019:")
print(top5_brands.index.tolist())
print()

# Case 2
print("Case 2:")
plt.figure(figsize=(10, 5))
for brand in dataset_top5brand_dec['brand'].unique():
    brand_data = dataset_top5brand_dec[dataset_top5brand_dec['brand'] == brand]
    quantity_per_date = brand_data.groupby('order_date')['quantity'].sum()
    plt.plot(quantity_per_date.index, quantity_per_date.values, marker='o', linestyle='-', label=brand)
    max_quantity_date = quantity_per_date.idxmax()
    max_quantity = quantity_per_date.max()
    plt.annotate(f'{max_quantity}', xy=(max_quantity_date, max_quantity), xytext=(10, -20), textcoords='offset points',
                 arrowprops=dict(arrowstyle='->', connectionstyle='arc3,rad=.5'))
plt.title('Daily Quantity Terjual per Brand (Top 5)')
plt.xlabel('Tanggal')
plt.ylabel('Quantity Terjual')
plt.legend()
plt.grid(True)
plt.show()
print()

# Case 3
print("Case 3:")
product_count = dataset_top5brand_dec.groupby('brand')['product_id'].count()
sorted_brands = product_count.sort_values(ascending=False)

plt.figure(figsize=(10, 5))
plt.bar(sorted_brands.index, sorted_brands.values)
plt.title('Jumlah Product Terjual per Brand (Top 5)')
plt.xlabel('Brand')
plt.ylabel('Jumlah Product Terjual')
for i, value in enumerate(sorted_brands.values):
    plt.text(i, value, str(value), ha='center', va='bottom')
plt.grid(True)
plt.show()
print()

# Case 4
print("Case 4:")
above_100 = dataset_top5brand_dec[dataset_top5brand_dec['quantity'] >= 100]
below_100 = dataset_top5brand_dec[dataset_top5brand_dec['quantity'] < 100]
above_100_count = above_100.groupby('brand')['quantity'].count()
below_100_count = below_100.groupby('brand')['quantity'].count()
sorted_brands = above_100_count.sort_values(ascending=False)

plt.figure(figsize=(10, 5))
plt.bar(sorted_brands.index, above_100_count, label='>= 100', color="r")
plt.bar(sorted_brands.index, below_100_count.reindex(sorted_brands.index, fill_value=0), bottom=above_100_count, label='< 100', color='b')
plt.title('Breakdown Jumlah Product Terjual per Brand (Top 5)')
plt.xlabel('Brand')
plt.ylabel('Jumlah Product Terjual')
plt.legend()
plt.grid(True)
plt.show()
print()

# Case 5
print("Case 5:")
top5_brands = dataset_top5brand_dec['brand'].value_counts().nlargest(5).index
filtered_data = dataset_top5brand_dec[dataset_top5brand_dec['brand'].isin(top5_brands)]
median_prices = filtered_data.groupby('product_id')['item_price'].median()

plt.figure(figsize=(10, 5))
plt.hist(median_prices, bins=20, color='purple')
plt.title('Distribusi Harga Produk (Brand Top 5)')
plt.xlabel('Harga Produk (Median)')
plt.ylabel('Jumlah Produk')
plt.grid(True)
plt.show()
print()

# Case 6
print("Case 6:")
data = dataset_top5brand_dec[['product_id', 'quantity', 'item_price']].drop_duplicates()
data['GMV'] = data['item_price'] * data['quantity']

plt.figure(figsize=(10, 5))
plt.subplot(1, 2, 1)
plt.scatter(data['quantity'], data['GMV'], color='blue', alpha=0.5)
plt.title('Scatter Plot: Quantity vs GMV')
plt.xlabel('Quantity')
plt.ylabel('GMV')
plt.grid(True)

plt.subplot(1, 2, 2)
plt.scatter(data['item_price'], data['quantity'], color='red', alpha=0.5)
plt.title('Scatter Plot: Median Harga vs Quantity')
plt.xlabel('Median Harga')
plt.ylabel('Quantity')
plt.grid(True)

plt.tight_layout()
plt.show()
