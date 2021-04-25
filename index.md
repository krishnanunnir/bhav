## Bhavcopy

### Problem Statement

Mandatory Django + Vue + CSV task

Description: BSE publishes a "Bhavcopy" (Equity) ZIP every day here: https://www.bseindia.com/markets/MarketInfo/BhavCopy.aspx

Requirements:
Write a standalone Python Django web app/server that:

- Downloads the equity bhavcopy zip from the above page every day at 18:00 IST for the current date.
- Extracts and parses the CSV file in it.
- Writes the records into Redis with appropriate data structures (Fields: code, name, open, high, low, close).
- Renders a simple VueJS frontend with a search box that allows the stored entries to be searched by name and renders a table of results and optionally downloads the results as CSV. Make this page look nice!
- The search needs to be performed on the backend using Redis.

### Design Decisions
<details>
 <summary>Handling downloading from the website.</summary>

a. The url can be extracted using a parsing library like beautiful soup.  
b. The url has a standard format where the only variable in it is the day, by editing the vlaue of day we can obtain the bhavcopy for that day.  

Both of them suffer from the same problem of being at the mercy of the website, if the structure of the website changes, it will not be possible to parse the url. If the url changes then the donwloads will fail. I went with option b since it is easier to implement and will be easier to correct in case of changes.
</details>  

<details>
 <summary>Scheduling</summary>
I thought of using cron jobs for implementing scheduling.

But I wanted to familiarise myself with Celery and I felt it would be easier to integrate features like Cache and models in Django by using Celery over cron jobs. the learning curve to Celery is a bit steeper.
</details>  


<details>
 <summary>Pagination</summary>
Pagination make sense in this context since we a lot of data without any order and sometimes it is not possible to keep track of it manually, breaking down the data into smaller chunks make it more manageable.  
<br>
Pagination is only one page forward and one page backward, since data is not ordered and we already provide search..
</details>  

