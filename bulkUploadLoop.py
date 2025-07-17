#  bulk upload loopin 
# this program will upload all files one by one on server
# if file is uploaded it will be moved to processed folder
# if not uploaded it will remain there and transaction will stop
import os
import shutil
import mysql.connector
import re
import configparser
import mysql.connector
from datetime import datetime

# Database connection details
DB_CONFIG = {
    "host": "172.21.163.160",
    "user": "GCSSBI",
    "password": "Engineer@7070",
    "database": "gcssbi_dashboard_adi"
}

def get_db_url(config):
    return f"postgresql://{config['user']}:{config['password']}@{config['host']}/{config['database']}"

def make_dummy_table(original_table):
    today_date = datetime.today().strftime('%d%b%y').lower()
    # todo: before running age change below
    new_table_name = f"aging_{today_date}"
    # new_table_name = f"zong_pakistan_{today_date}"
    conn = mysql.connector.connect(**DB_CONFIG)
    cursor = conn.cursor()
    try:
        # Step 1: Create a replica of the original table with today's date
        cursor.execute(f"CREATE TABLE {new_table_name} LIKE {original_table};")
        conn.commit()
        print(f"Table {new_table_name} successfully created as a replica of {original_table}")
        return new_table_name  # Return the created table name
    except Exception as e:
        conn.rollback()
        print(f"Error during table creation: {e}")
        return None
    finally:
        cursor.close()
        conn.close()

def upload_to_live(table_name):
    # MySQL Connection
    db = mysql.connector.connect(
        host="172.21.163.160",
        user="GCSSBI",
        password="Engineer@7070",
        database="gcssbi_dashboard_adi",
        allow_local_infile=True
    )
    cursor = db.cursor()

    # First truncate the table then upload
    clear_query = f"TRUNCATE TABLE {table_name};"
    cursor.execute(clear_query)
    
    # Folders    
    config = configparser.ConfigParser()
    config.read("config.ini")
    UPLOAD_DIR = config["settings"]["upload_dir"]
    PROCESSED_DIR = config["settings"]["porcessed_dir"]
    
    # Extract numbers from filenames and sort correctly
    def natural_sort(file_list):    
        return sorted(file_list, key=lambda x: int(re.search(r'\d+', x).group()))
                            
    # Get all CSV files in upload folder
    csv_files = [f for f in os.listdir(UPLOAD_DIR) if f.endswith('.csv')]

    # Apply natural sorting
    csv_files = natural_sort(csv_files)

    # Process each file one by one
    for file_name in csv_files:  # Sort to maintain order
        file_path = os.path.join(UPLOAD_DIR, file_name).replace("\\", "/")
   
        # SQL Query for Upload
        # SET AUTO COMMIT 0 FOR SPEED
        query = f"""            
            LOAD DATA LOCAL INFILE '{file_path}'
            INTO TABLE {table_name}
            FIELDS TERMINATED BY ','
            LINES TERMINATED BY '\n'
            IGNORE 1 ROWS;
        """

        try:
            cursor.execute("START TRANSACTION;")  # Start transaction
            cursor.execute(query)  # Upload file
            cursor.execute("COMMIT;")  # Commit if successful            
            # logging.info("✅ Uploaded: {file_name}")            

            print(f"✅ Uploaded: {file_name}")

            # Move file to processed folder
            shutil.move(file_path, os.path.join(PROCESSED_DIR, file_name))
            # logging.info("📂 Moved {file_name} to processed folder.")  
            print(f"📂 Moved {file_name} to processed folder.")

        except Exception as e:
            cursor.execute("ROLLBACK;")  # Rollback if error occurs
            # logging.error("❌ Error uploading {file_name}: {e}")
            print(f"❌ Error uploading {file_name}: {e}")

    # Close connection
    cursor.close()
    db.close()


# def upload_to_live(table_name, max_files=100):
#     # MySQL Connection
#     db = mysql.connector.connect(
#         host="172.21.163.160",
#         user="GCSSBI",
#         password="Engineer@7070",
#         database="gcssbi_dashboard_adi",
#         allow_local_infile=True
#     )
#     cursor = db.cursor()

#     # First truncate the table then upload
#     clear_query = f"TRUNCATE TABLE {table_name};"
#     cursor.execute(clear_query)
    
#     # Folders    
#     config = configparser.ConfigParser()
#     config.read("config.ini")
#     UPLOAD_DIR = config["settings"]["upload_dir"]
#     PROCESSED_DIR = config["settings"]["porcessed_dir"]
    
#     # Extract numbers from filenames and sort correctly
#     def natural_sort(file_list):    
#         return sorted(file_list, key=lambda x: int(re.search(r'\d+', x).group()))
                            
#     # Get all CSV files in upload folder
#     csv_files = [f for f in os.listdir(UPLOAD_DIR) if f.endswith('.csv')]

#     # Apply natural sorting and limit to max_files
#     csv_files = natural_sort(csv_files)[:max_files]

#     # Process each file one by one
#     for file_name in csv_files:
#         file_path = os.path.join(UPLOAD_DIR, file_name).replace("\\", "/")

#         query = f"""            
#             LOAD DATA LOCAL INFILE '{file_path}'
#             INTO TABLE {table_name}
#             FIELDS TERMINATED BY ','
#             LINES TERMINATED BY '\\n'
#             IGNORE 1 ROWS;
#         """

#         try:
#             cursor.execute("START TRANSACTION;")
#             cursor.execute(query)
#             cursor.execute("COMMIT;")
#             print(f"✅ Uploaded: {file_name}")

#             shutil.move(file_path, os.path.join(PROCESSED_DIR, file_name))
#             print(f"📂 Moved {file_name} to processed folder.")

#         except Exception as e:
#             cursor.execute("ROLLBACK;")
#             print(f"❌ Error uploading {file_name}: {e}")

#     cursor.close()
#     db.close()

def read_save_distinct_records(source_table, target_table):
    try:
        # Connect to the database
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor()

        # Step 1: Clear the target table
        clear_query = f"TRUNCATE TABLE {target_table};"
        cursor.execute(clear_query)
        print(f"🗑️ Cleared target table: {target_table}")

        # Query to get distinct records
        query = f"SELECT DISTINCT NTN_ID, NTN_COMPANY FROM {source_table}"
        cursor.execute(query)

        # Fetch all distinct records
        distinct_records = cursor.fetchall()       

        # Step 3: Insert distinct records into target table
        insert_query = f"INSERT INTO aging_report_companies (NTN_ID, NTN_COMPANY) VALUES (%s, %s);"
        cursor.executemany(insert_query, distinct_records)
        conn.commit()
        print(f"📥 Inserted {len(distinct_records)} records into aging_report_companies")        

    except mysql.connector.Error as err:
        print(f"❌ Error: {err}")

    finally:
        cursor.close()
        conn.close()

# create_replica_table
# step 1: make a dummy table "feb13_2025_aging" 
new_table = make_dummy_table("aging_report_17feb22")
# Upload data.
# new_table = "aging_16jun25"
# upload_to_live(new_table, 25)
upload_to_live(new_table)
# read_save_distinct_records
read_save_distinct_records(new_table, "aging_report_companies")

