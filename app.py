from flask import Flask, request, session, redirect, url_for, send_file, render_template
from flask_session import Session
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
import asyncio
from crawl4ai import AsyncWebCrawler, CrawlerRunConfig, CacheMode
from bs4 import BeautifulSoup, NavigableString
from urllib.parse import urljoin
import pandas as pd
from io import BytesIO
import os

# Configure application
app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'your-secret-key-123')

# Configure database-based sessions
app.config['SESSION_TYPE'] = 'sqlalchemy'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///sessions.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize database
db = SQLAlchemy(app)

# Configure Flask-Session with existing SQLAlchemy instance
app.config['SESSION_SQLALCHEMY'] = db
Session(app)

def init_db():
    with app.app_context():
        db.create_all()

# Ensure session data is serializable
def make_serializable(data):
    if isinstance(data, dict):
        return {key: make_serializable(value) for key, value in data.items()}
    elif isinstance(data, list):
        return [make_serializable(item) for item in data]
    elif isinstance(data, NavigableString):
        return str(data)
    return data

def get_absolute_url(base, path):
    return urljoin(base, path)

async def crawl_website(start_url):
    async with AsyncWebCrawler() as crawler:
        config_params = {
            'cache_mode': CacheMode.BYPASS,
            'word_count_threshold': 100
        }
        
        if hasattr(CrawlerRunConfig, 'bypass_cache_checks'):
            config_params['bypass_cache_checks'] = True
            
        config = CrawlerRunConfig(**config_params)
        homepage_result = await crawler.arun(url=start_url, config=config)
        if not homepage_result.success:
            return []

        html_content = getattr(homepage_result, 'html', str(homepage_result))
        soup = BeautifulSoup(html_content, 'html.parser')
        
        # Cleanup navigation elements
        for element in soup.find_all(['nav', 'footer', 'header', 'script', 'style']):
            element.decompose()
            
        links = [a['href'] for a in soup.find_all('a', href=True)]
        absolute_links = [get_absolute_url(start_url, link) for link in links]
        valid_links = list(set(
            link for link in absolute_links if link.startswith(start_url)
        ))[:30]

        results = []
        if valid_links:
            crawl_results = await crawler.arun_many(valid_links, config=config)
            for result in crawl_results:
                if result.success:
                    results.append({
                        'url': result.url,
                        'content': result.markdown,
                        'title': soup.title.string if soup.title else 'No Title',
                        'crawled_at': pd.Timestamp.now().isoformat()
                    })
        return results

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        url = request.form['url']
        try:
            crawled_data = asyncio.run(crawl_website(url))
            session['history'] = make_serializable(session.get('history', []) + crawled_data)
            session.modified = True
        except Exception as e:
            return render_template('index.html', error=str(e))
        return redirect(url_for('index'))
    
    return render_template('index.html', history=session.get('history', []), error=request.args.get('error'))

@app.route('/download')
def download():
    history = session.get('history', [])
    if not history:
        return redirect(url_for('index', error='No data to download'))
    
    df = pd.DataFrame(history)
    csv_buffer = BytesIO()
    df.to_csv(csv_buffer, index=False)
    csv_buffer.seek(0)
    
    return send_file(
        csv_buffer,
        mimetype='text/csv',
        as_attachment=True,
        download_name='crawled_data.csv'
    )

@app.route('/clear')
def clear_history():
    session.clear()
    return redirect(url_for('index'))

if __name__ == '__main__':
    init_db()
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
