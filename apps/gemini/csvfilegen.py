import pandas as pd
import numpy as np

# Parameters to approximate 2 MB file size
num_rows = 20000  # Adjust based on experimentation
num_columns = 15   # Adjust based on experimentation

# Generate random data
data = np.random.rand(num_rows, num_columns)
columns = [f'Column_{i+1}' for i in range(num_columns)]
df = pd.DataFrame(data, columns=columns)

# Add some text data to increase size
df['Text_Column'] = ['Sample text ' + str(i) for i in range(num_rows)]

# Save to Excel file
output_file = 'output_2mb_excel.xlsx'
df.to_excel(output_file, index=False)

print(f"Excel file '{output_file}' has been generated.")