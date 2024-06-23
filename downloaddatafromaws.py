from urllib.parse import urlparse
import os
import boto3
from botocore.exceptions import NoCredentialsError



# os.environ['AWS_ACCESS_KEY_ID'] = 'your_access_key_id'
# os.environ['AWS_SECRET_ACCESS_KEY'] = 'your_secret_access_key'


from urllib.parse import urlparse
# Read the file content
file_path = '/Users/amarnathgowda/Desktop/Videodata/s3ieee-dataportcompetition125348713 data.txt'

with open(file_path, 'r') as file:
    lines = file.readlines()

# Initialize a list to store the URLs
urls = []
local_dir = '/Users/amarnathgowda/Desktop/Videodata/data'
if not os.path.exists(local_dir):
        os.makedirs(local_dir)


def get_folder_path(s3_url):
    # Parse the S3 URL
    parsed_url = urlparse(s3_url)
    
    # Extract the file key (path) from the parsed URL
    file_key = parsed_url.path.lstrip('/')
    
    # Get the directory (folder) path excluding the file name
    folder_path = os.path.dirname(file_key)
    
    return folder_path

def download_from_s3(s3_url, local_dir):
    # Parse the S3 URL
    parsed_url = urlparse(s3_url)
    bucket_name = parsed_url.netloc
    file_key = parsed_url.path.lstrip('/')
    
    # Get the folder path from the file key
    folder_path = get_folder_path(s3_url)
    
    # Create the local directory structure if it does not exist
    local_folder_path = os.path.join(local_dir, folder_path)
    if not os.path.exists(local_folder_path):
        os.makedirs(local_folder_path)
    
    # Define the local file path
    local_file_path = os.path.join(local_dir, file_key)
    
    # Initialize the S3 client
    s3 = boto3.client('s3')
    
    try:
        # Download the file from S3
        s3.download_file(bucket_name, file_key, local_file_path)
        print(f"File downloaded successfully to {local_file_path}")
    except NoCredentialsError:
        print("Credentials not available")
    except Exception as e:
        print(f"Error occurred: {e}")
    
    

# Iterate over each line in the file and add to the list if it starts with "s3://"
for line in lines:
    if line.startswith('s3://'):
        urls.append(line.strip())
        s3_url = line.strip()
        # Call the function to download the file
        download_from_s3(s3_url, local_dir)
        # Parse the URL
#         parsed_url = urlparse(s3_url)

# # Extract the bucket name and file key
#         bucket_name = parsed_url.netloc
#         file_key = parsed_url.path.lstrip('/')
        
#         # Define the local file path
#         local_file_path = os.path.join(local_dir, os.path.dirname(file_key))

# # Print the bucket name and file key
#         # print(f"Bucket Name: {bucket_name}")
#         # print(f"File Key: {file_key}")


#         # Initialize a session using Amazon S3
#         s3 = boto3.client('s3')

#         # Define the bucket name and the file path
#         bucket_name = 'ieee-dataport'
#         # file_key = 'competition/1253487/13083/Camera Views/(CENTRAL-478) STATION JUNCTION (PS-SADASHIVANAGARA).pdf'
#         # local_file_path = '(CENTRAL-478) STATION JUNCTION (PS-SADASHIVANAGARA).pdf'

#         try:
#             # Download the file
#             print(local_file_path)
#             if not os.path.exists(local_file_path):
#                 os.makedirs(local_file_path)
#             s3.download_file(bucket_name, file_key, local_file_path)
#             print(f"File downloaded successfully to {file_key}")
#         except NoCredentialsError:
#             print("Credentials not available")
#         except Exception as e:
#             print(f"Error occurred: {e}")
