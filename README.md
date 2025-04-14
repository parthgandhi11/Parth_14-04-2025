This is Parth Gandhi and this repository contains my code for the task assigned.
I have used Django Rest framework. I have created 3 models, one for each csv - StoreStatus, MenuHours and Timezones - as well as a new model called Reports for storing the data related to CSV report that is being generated.
The ```views.py``` file of ```trigger_report``` has a function that initiates report generation and also returns a report_id.
The ```views.py``` file of ```get_report``` has all the logic and code for report generation.

```generate_report``` is the main function that automatically get triggered in a separate thread when ```trigger_report``` API is called.
```get_store_working_hours``` is a function that returns the start and end times of a store in UTC as an array. This is a resusable function that gets called to return working hours for last hour, last day and last week. It returns a list of working hours for each day, with one day having multiple working hours.
```calculate_uptime_downtime``` function has the logic of calculating the uptime and downtime which has been explained more in the video.
The CSV report generated is stored in a file as ```{report_id}.csv``` as the filename in a folder called ```csv_reports``` inside the backend folder.
This file can also be downloaded when url ```get_report/{report_id}/download``` is called.

## Ways to improve the solution:
1. If the user is authenticated or provides an email, we can send them an email with the download link when the report is ready.
2. Instead of just "Running" or "Complete" as status, we can show actual progress like x% completed.
3. Add an expiration date tag with each report to avoid unnecessary CSVs from piling up.

## Sample output CSV
https://drive.google.com/file/d/1IrQse0ULYScjVRC82moDRQJ8svgwdWU6/view?usp=sharing

## Screen recording of demo
https://drive.google.com/file/d/1SMQKV4po6qk_XJjatsK0FD60G7YB4EOy/view?usp=sharing
