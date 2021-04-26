## Bhav

Bhav  website- A searchable interface for the bhavcopy data generated daily.

Bhavcopy zip is generated everyday at [BSE INDIA](https://www.bseindia.com/markets/MarketInfo/BhavCopy.aspx) website, Bhav parses the data  automatically and provides an interface for a user to search different equities by name. A user can also export the search data for furture usage.

Implemented with   Django/VUE/Redis/Celery

### Development Setup

1. Clone the Github repo and move to the repo directory.
 ```$ git clone https://github.com/krishnanunnir/bhavcopy.git```

2. Install all the dependencies required for your local installation like python3 and redis server.
```$ sudo apt install redis-server python3-pip python3-dev``` 
```$ sudo pip3 install virtualenv ```
3. Create a virtual environment to isolate dependancies for the project.
```cd bhavcopy && python3 -m venv .envs/bhavcopyenv```
4. Activate the virtual environment and install the all the required dependancies listed in the requirements file.
```$ source .envs/bhavcopy/bin/activate```
```$ pip install -r requirements.txt```
5. Create a file with your environment settings in the nested bhavcopy folder based of the .ex-env file.
```$ cd bhavcopy && cp .ex-env .env```
6. Run the redis-server
```$ redis-server```
7. Start the celery beat service for the scheduling
```$ celery -A proj beat```
8. Run python migration for handling db migrations of dependancies.
```$ python manage.py migrate``` 
9. Start the python server.
```$ python manage.py runserver```  

For production, use a fully fledged server like gunicorn and daemonize celery beat using tools like supervisor. 

### Features
[x] Schedule data retrieval from BSE INDIA website and update to Redis.
[x] Create apis for retrieval of entire dataset and searched dataset.
[x] Create a front end based of VUE to display the data from API.
[x] Provide a input field for user to search for equity by name.
[x] Export the dataset as CSV.
[x] Add pagination to show only a chunk of data in each page.