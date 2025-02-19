# Web-Crawler

🚀 Innovative Web Scraper: Transforming Websites into LLM Knowledge Instantly

I developed a cutting-edge web scraping tool that allows users to convert any website into searchable knowledge for large language models (LLMs). This project leverages the powerful capabilities of Python and several libraries, including:

>Crawl4AI for efficient web crawling and data extraction
>SQLite3 for robust data storage and management
>Flask as the web framework to create a seamless user interface
>Requests for handling HTTP requests and responses
>SQLAlchemy for database interaction and ORM capabilities
>Pandas for data manipulation and analysis

My web scraper is designed to provide instant access to rich information from a variety of online sources, streamlining the process of knowledge extraction. It empowers users to gather insights, enhance learning, and integrate web data into their LLM applications effortlessly.

💻 Key Features:
>Rapid and efficient data scraping from any website
>User-friendly interface for ease of use
>Scalable architecture to support a wide range of applications
>Reliable storage and retrieval of scraped data


## Sample Picture 

![Web Crawler](<Screenshot 2025-01-31 233035.png>)

![Code](<Screenshot 2025-01-31 233114.png>)

![Terminal Logs](<Screenshot 2025-01-31 233258.png>)

![Final Web page](<Screenshot 2025-01-31 233326.png>)
## A Simple Example
```python
# save this as app.py
@app.route('/clear')
def clear_history():
    session.clear()
    return redirect(url_for('index'))

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
```

## Install the requirements

```
pip install -r requirements.txt

```

## Run the application

```
$env:FLASK_APP = "app.py"
python -m flask run --port 5000 --debug
```
