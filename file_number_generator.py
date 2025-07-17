# File to save the generated SQL script
# output_file = "aging_load_data.sql"
output_file = r"D:\\python projects\\csvSplitter\\aging_load_data_09022025.sql"

# E:\Aging\26012024
# Open the output file in write mode
with open(output_file, 'w') as file:
    for i in range(1, 226):  # Loop from 1 to 225
        sql_command = f"""
LOAD DATA INFILE 'E:/Aging/09022025/part_{i}.csv'
INTO TABLE aging_report_17feb22
FIELDS TERMINATED BY ',' 
LINES TERMINATED BY '\\n' 
IGNORE 1 ROWS;
"""
        file.write(sql_command)  # Write each command to the file

print(f"SQL script generated and saved to {output_file}")
