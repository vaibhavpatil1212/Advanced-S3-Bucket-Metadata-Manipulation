import json
from datetime import datetime, timedelta

# Load the JSON data from the file
with open('buckets.json', 'r') as f:
    try:
        data = json.load(f)
    except json.JSONDecodeError as e:
        print(f"Error loading JSON: {e}")
        exit(1)

# Extract the list of buckets
buckets_data = data.get('buckets', [])

# Ensure the data is a list
if not isinstance(buckets_data, list):
    print("Error: JSON data is not a list.")
    exit(1)

# Function to print a summary of each bucket
def print_bucket_summary(buckets):
    for bucket in buckets:
        name = bucket.get('name')
        region = bucket.get('region')
        size_gb = bucket.get('sizeGB')
        versioning = bucket.get('versioning')
        print(f"Bucket Name: {name}, Region: {region}, Size: {size_gb} GB, Versioning: {versioning}")

# Function to identify buckets larger than 80 GB and unused for 90+ days
def identify_large_unused_buckets(buckets):
    large_unused_buckets = []
    for bucket in buckets:
        size_gb = bucket.get('sizeGB')
        created_on = datetime.strptime(bucket.get('createdOn'), '%Y-%m-%d')
        if size_gb > 80 and (datetime.now() - created_on).days > 90:
            large_unused_buckets.append(bucket)
    return large_unused_buckets

# Function to generate a cost report
def generate_cost_report(buckets):
    cost_report = {}
    deletion_queue = []
    for bucket in buckets:
        region = bucket.get('region')
        department = bucket['tags'].get('team')
        size_gb = bucket.get('sizeGB')
        created_on = datetime.strptime(bucket.get('createdOn'), '%Y-%m-%d')
       
        # Initialize region and department in cost report if not already present
        if region not in cost_report:
            cost_report[region] = {}
        if department not in cost_report[region]:
            cost_report[region][department] = 0
       
        # Add the size to the cost report
        cost_report[region][department] += size_gb
       
        # Check for cleanup recommendation
        if size_gb > 50:
            print(f"Bucket {bucket['name']} (Size: {size_gb} GB) - Recommend cleanup operations.")
       
        # Check for deletion queue
        if size_gb > 100 and (datetime.now() - created_on).days > 20:
            deletion_queue.append(bucket)
   
    return cost_report, deletion_queue

# Function to provide final list of buckets to delete and suggest archival candidates
def finalize_deletion_and_archival(deletion_queue):
    buckets_to_delete = []
    archival_candidates = []
    for bucket in deletion_queue:
        created_on = datetime.strptime(bucket.get('createdOn'), '%Y-%m-%d')
        if (datetime.now() - created_on).days > 20:
            buckets_to_delete.append(bucket)
        else:
            archival_candidates.append(bucket)
   
    return buckets_to_delete, archival_candidates

# Print the summary of each bucket
print("Bucket Summary:")
print_bucket_summary(buckets_data)

# Identify large unused buckets
large_unused_buckets = identify_large_unused_buckets(buckets_data)
print("\nLarge Unused Buckets (Size > 80 GB and Unused for 90+ days):")
for bucket in large_unused_buckets:
    print(f"Bucket Name: {bucket['name']}, Size: {bucket['sizeGB']} GB, Created On: {bucket['createdOn']}")

# Generate the cost report
cost_report, deletion_queue = generate_cost_report(buckets_data)
print("\nCost Report (Grouped by Region and Department):")
for region, departments in cost_report.items():
    print(f"Region: {region}")
    for department, total_size in departments.items():
        print(f"  Department: {department}, Total Size: {total_size} GB")

# Provide final list of buckets to delete and suggest archival candidates
buckets_to_delete, archival_candidates = finalize_deletion_and_archival(deletion_queue)
print("\nBuckets to Delete:")
for bucket in buckets_to_delete:
    print(f"Bucket Name: {bucket['name']}, Size: {bucket['sizeGB']} GB, Created On: {bucket['createdOn']}")

print("\nArchival Candidates (Suggest moving to Glacier):")
for bucket in archival_candidates:
    print(f"Bucket Name: {bucket['name']}, Size: {bucket['sizeGB']} GB, Created On: {bucket['createdOn']}")