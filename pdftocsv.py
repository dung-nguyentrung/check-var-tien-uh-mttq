import pdfplumber
import csv
import re

def clean_money_column(column):
    """
    Hàm này làm sạch dữ liệu trong cột số tiền.
    Loại bỏ các dấu phân cách hàng nghìn và sửa dấu phân cách thập phân.
    """
    if column is None:
        return ''
    
    column = column.strip()
    
    # Sử dụng regex để nhận diện và làm sạch số tiền
    # Loại bỏ dấu phân cách hàng nghìn (dấu chấm) và thay dấu phẩy thành dấu chấm nếu cần
    if re.match(r'^\d{1,3}(\.\d{3})*(,\d+)?$', column):  # Dạng "100.000,00" hoặc "1.000,00"
        # Thay dấu chấm phân cách hàng nghìn và dấu phẩy thành dấu chấm thập phân
        column = column.replace('.', '')  # Loại bỏ dấu chấm
        column = column.replace(',', '.')  # Thay dấu phẩy thành dấu chấm
    elif re.match(r'^\d{1,3}(,\d{3})*(\.\d+)?$', column):  # Dạng "100,000.00" hoặc "1,000.00"
        # Thay dấu phẩy phân cách hàng nghìn và giữ dấu chấm cho thập phân
        column = column.replace(',', '')  # Loại bỏ dấu phẩy
    
    return column

def pdf_table_to_csv(pdf_path, csv_path):
    # Mở file PDF
    with pdfplumber.open(pdf_path) as pdf:
        # Tạo file CSV để ghi
        with open(csv_path, mode='w', newline='', encoding='utf-8') as csv_file:
            writer = csv.writer(csv_file)
            
            # Duyệt qua từng trang trong PDF
            for page_num, page in enumerate(pdf.pages):
                # Trích xuất các bảng từ trang với extract_table
                tables = page.extract_tables()
                
                if tables:
                    # Duyệt qua từng bảng trong trang
                    for table in tables:
                        for row in table:
                            # Làm sạch từng cột trong hàng
                            cleaned_row = []
                            for i, col in enumerate(row):
                                col = col.strip() if col else ''
                                # Nếu là cột số tiền (cột 4), ta làm sạch nó
                                if i == 3:  # Cột 4 (index 3)
                                    col = clean_money_column(col)
                                cleaned_row.append(col)
                            writer.writerow(cleaned_row)
    
    print(f'Chuyển đổi các bảng PDF thành CSV thành công! File CSV: {csv_path}')

# Sử dụng hàm
pdf_path = 'original.pdf'  # Đường dẫn tới file PDF
csv_path = 'output.csv'  # Đường dẫn tới file CSV kết quả

pdf_table_to_csv(pdf_path, csv_path)
