
# Quotes Scraper Project
This project is a Python-based web scraper that extracts quotes, authors' details, and their associated tags from the website [Quotes to Scrape](https://quotes.toscrape.com/). It collects data across multiple pages and stores the information in a PostgreSQL database. The project serves as a hands-on way to refresh Python knowledge, including web scraping, database interactions, and unit testing.

## Tech Stack
- **Python:** Programming language used for the script.
- **Requests:** For making HTTP requests to fetch web pages.
- **BeautifulSoup:** For parsing HTML and extracting data.
- **Pandas:** For data manipulation and handling.
- **SQLAlchemy:** For database interaction.
- **psycopg2:** PostgreSQL database adapter for Python.
- **Dotenv:** For managing environment variables.
- **pytest:** For running unit tests.
- **unittest.mock:** For mocking during tests.
- **Colorama:** For colored terminal output.


## File Structure

```plaintext
quotes-scraper/
│
├── main.py
├── requirements.txt
├── .env
├── tests/
│   ├── __init__.py
│   └── test_main.py
└── README.md
```

**main.py:** The main script that performs web scraping and interacts with the database.
<br>
**tests/__init__.py:** An empty file that makes the tests directory a package.
tests/test_main.py: Contains unit tests for the main.py script.

## Prerequisites
- **Python 3.x:** Ensure you have Python 3.x installed on your machine.
- **PostgreSQL:** A PostgreSQL database should be set up and accessible.

## Setup
Clone the Repository
```bash
git clone https://github.com/yourusername/quotes-scraper.git
cd quotes-scraper
```
Create a Virtual Environment
<br>
You can use *python* or *python3*, as well as *pip* or *pip3*.

```bash
python -m venv your_venv_name
source venv/bin/activate  # On Windows use: venv\Scripts\activate

deactivate # to stop it
```

Install Dependencies
<br>
This project uses a requirements.txt file to manage dependencies. If the requirements.txt file is included in the project (as shown in the file structure), you can install the required packages with:
```bash
pip install -r requirements.txt
```
If the requirements.txt file is missing or you need to create it yourself, you can generate it using the following command (make sure all your dependencies are installed in your environment first):
```bash
pip freeze > requirements.txt
```



<br>

Additionally, create a **.env** file in the root directory and add your PostgreSQL credentials:
<br> Be careful and DO NOT publish this file. Instead, use a **.gitignore** file to ignore it.

```env
USERNAME = your_username
PASSWORD = your_password
HOST = localhost
PORT = 5432
DATABASE =y our_database
````

## Running the Scripts

To execute the **main.py** script, which performs the scraping and stores data in the database:

```bash
python main.py

# or

python3 main.py
```

To ensure everything is working correctly, run the unit tests:

```bash
pytest tests/

#or 

pytest -v tests/  
# this last one provides more info about your tests
```

## Functions description
- **connect_to_db()**: Establishes a connection to the PostgreSQL database and prints a success or failure message.
- **get_author_details(author_url):** Fetches details about the author from their specific page.
- **page_scraping():** Scrapes quotes, authors, and tags from the website across multiple pages.
- **save_to_db(df):** Saves the scraped data into a PostgreSQL database table.

## Testing
The tests use **pytest** and **unittest.mock** to mock external dependencies and verify the functionality of the main script:

- **test_connect_to_db():** Tests the database connection.
- **test_save_to_db():** Tests if data is successfully saved to the database.
- **test_get_author_details():** Tests the function that retrieves author details.
- **test_page_scraping():** Tests the overall scraping process.

## Contributing
Feel free to fork the repository and submit pull requests. If you encounter any issues, please open an issue in the repository.


<p style="color: magenta;">💖 Happy Coding! 💖</p>
