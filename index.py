import csv
import pymysql

connection = pymysql.connect(
    host='localhost',  
    user='root',  
    password='', 
    database='laravel'  
)

def import_csv_to_mysql(csv_file, table_name):
    cursor = connection.cursor()

    with open(csv_file, newline='', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        
        columns = next(reader)
        columns_str = ', '.join([f"`{col.strip()}`" for col in columns])  
        sql = f"INSERT INTO {table_name} ({columns_str}) VALUES ({', '.join(['%s'] * len(columns))})"
        
        for data in reader:
            data = [None if val == '' else val for val in data]
            
            try:
                cursor.execute(sql, data)
            except pymysql.err.ProgrammingError as e:
                print(f"Error inserting data: {e}")
        
        connection.commit()

    cursor.close()
    print(f"Imported data from {csv_file} to {table_name}")

# Sử dụng hàm để import CSV
csv_file_path = 'transactions.csv' 
table_name = 'var'        
import_csv_to_mysql(csv_file_path, table_name)

# Đóng kết nối
connection.close()
