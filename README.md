# DevOps-SRE-Daily-Challenge-Day 2
DevOps SRE Daily Challenge!

Sure! Here's a `README.md` file that explains the approach, challenges faced, and key learnings for the provided Python script:

```markdown
# S3 Bucket Analysis and Optimization

## Overview

This Python script analyzes, modifies, and optimizes S3 bucket metadata based on the provided JSON file (`buckets.json`). The script performs the following tasks:
1. Prints a summary of each bucket.
2. Identifies buckets larger than 80 GB and unused for 90+ days.
3. Generates a cost report grouped by region and department, highlighting buckets for cleanup and adding certain buckets to a deletion queue.
4. Provides a final list of buckets to delete and suggests archival candidates for Glacier.

## Requirements

- Python 3.x
- JSON file (`buckets.json`) containing S3 bucket metadata

## Usage

1. Ensure you have Python 3.x installed on your system.
2. Place the `buckets.json` file in the same directory as the script.
3. Run the script using the following command:
   ```bash
   python s3_bucket_analysis.py
   ```

## Approach

1. **Loading JSON Data**: The script starts by loading the JSON data from the `buckets.json` file. It includes error handling to ensure the JSON is correctly formatted.
2. **Data Extraction**: The script extracts the list of buckets from the JSON data and verifies that it is a list.
3. **Bucket Summary**: A function `print_bucket_summary` iterates through the list of buckets and prints a summary of each bucket, including its name, region, size, and versioning status.
4. **Identifying Large Unused Buckets**: The function `identify_large_unused_buckets` identifies buckets larger than 80 GB that have not been accessed for more than 90 days.
5. **Generating Cost Report**: The function `generate_cost_report` generates a cost report grouped by region and department. It also highlights buckets that require cleanup and adds certain buckets to a deletion queue based on their size and last accessed date.
6. **Finalizing Deletion and Archival**: The function `finalize_deletion_and_archival` provides a final list of buckets to delete and suggests archival candidates for Glacier.

## Challenges Faced

1. **JSON Structure**: The initial assumption about the JSON structure was incorrect. The script was updated to handle the nested structure under the `"buckets"` key.
2. **Date Parsing**: Parsing and comparing dates required careful handling to ensure accurate identification of unused buckets.
3. **Data Validation**: Ensuring the JSON data was correctly formatted and contained all necessary fields was crucial to avoid runtime errors.

## Key Learnings

1. **Error Handling**: Implementing robust error handling for JSON parsing and data validation is essential for building reliable scripts.
2. **Data Structure Assumptions**: Always verify the structure of input data before processing to avoid incorrect assumptions.
3. **Modular Functions**: Breaking down the script into modular functions improves readability and maintainability.

## Example Output

```plaintext
Bucket Summary:
Bucket Name: prod-data, Region: us-west-2, Size: 120 GB, Versioning: True
Bucket Name: dev-app-logs, Region: us-east-1, Size: 10 GB, Versioning: False
...

Large Unused Buckets (Size > 80 GB and Unused for 90+ days):
Bucket Name: prod-data, Size: 120 GB, Created On: 2023-10-12
...

Cost Report (Grouped by Region and Department):
Region: us-west-2
  Department: analytics, Total Size: 210 GB
...

Buckets to Delete:
Bucket Name: prod-data, Size: 120 GB, Created On: 2023-10-12
...

Archival Candidates (Suggest moving to Glacier):
Bucket Name: dev-app-logs, Size: 10 GB, Created On: 2024-02-15
...
```

## Conclusion

This script provides a comprehensive analysis and optimization of S3 bucket metadata, helping to identify unused and oversized buckets, generate cost reports, and suggest cleanup and archival actions. By following the outlined approach and addressing the challenges faced, the script ensures efficient management of S3 resources.
```

Feel free to modify this `README.md` file as needed to better fit your project's requirements! If you have any further questions or need additional assistance, let me know.
