#!/usr/bin/env python3
"""
Daily Tech News Fetcher
Fetches technology news from NewsAPI and sends a formatted email newsletter.
"""

import os
import sys
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
import requests

# Load environment variables from .env file (for local testing)
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass  # dotenv not required in GitHub Actions


def fetch_tech_news(api_key):
    """
    Fetch top technology headlines from NewsAPI.
    
    Args:
        api_key (str): NewsAPI.org API key
        
    Returns:
        list: List of news articles
    """
    url = "https://newsapi.org/v2/top-headlines"
    params = {
        "category": "technology",
        "language": "en",
        "pageSize": 10,
        "apiKey": api_key
    }
    
    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        if data.get("status") == "ok":
            return data.get("articles", [])
        else:
            print(f"API Error: {data.get('message', 'Unknown error')}")
            return []
    except requests.exceptions.RequestException as e:
        print(f"Error fetching news: {e}")
        return []


def create_html_email(articles):
    """
    Create an HTML formatted email from news articles.
    
    Args:
        articles (list): List of news articles
        
    Returns:
        str: HTML formatted email content
    """
    current_date = datetime.now().strftime("%B %d, %Y")
    
    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <style>
            body {{
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                line-height: 1.6;
                color: #333;
                max-width: 800px;
                margin: 0 auto;
                padding: 20px;
                background-color: #f5f5f5;
            }}
            .container {{
                background-color: white;
                border-radius: 10px;
                padding: 30px;
                box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            }}
            .header {{
                text-align: center;
                border-bottom: 3px solid #2563eb;
                padding-bottom: 20px;
                margin-bottom: 30px;
            }}
            .header h1 {{
                color: #1e40af;
                margin: 0;
                font-size: 32px;
            }}
            .date {{
                color: #6b7280;
                font-size: 14px;
                margin-top: 10px;
            }}
            .article {{
                margin-bottom: 30px;
                padding-bottom: 25px;
                border-bottom: 1px solid #e5e7eb;
            }}
            .article:last-child {{
                border-bottom: none;
            }}
            .article-title {{
                font-size: 20px;
                font-weight: bold;
                margin-bottom: 10px;
            }}
            .article-title a {{
                color: #1e40af;
                text-decoration: none;
            }}
            .article-title a:hover {{
                color: #2563eb;
                text-decoration: underline;
            }}
            .article-meta {{
                color: #6b7280;
                font-size: 13px;
                margin-bottom: 10px;
            }}
            .article-description {{
                color: #4b5563;
                line-height: 1.6;
            }}
            .source {{
                color: #2563eb;
                font-weight: 600;
            }}
            .footer {{
                text-align: center;
                margin-top: 40px;
                padding-top: 20px;
                border-top: 2px solid #e5e7eb;
                color: #6b7280;
                font-size: 12px;
            }}
            .no-articles {{
                text-align: center;
                color: #6b7280;
                padding: 40px;
                font-size: 16px;
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>🚀 Daily Tech News</h1>
                <div class="date">{current_date}</div>
            </div>
    """
    
    if not articles:
        html += """
            <div class="no-articles">
                <p>No technology news available today. Please check back tomorrow!</p>
            </div>
        """
    else:
        for i, article in enumerate(articles, 1):
            title = article.get("title", "No title")
            description = article.get("description", "No description available.")
            url = article.get("url", "#")
            source = article.get("source", {}).get("name", "Unknown Source")
            published_at = article.get("publishedAt", "")
            
            # Format the published date
            if published_at:
                try:
                    pub_date = datetime.fromisoformat(published_at.replace('Z', '+00:00'))
                    published_at = pub_date.strftime("%B %d, %Y at %I:%M %p")
                except:
                    published_at = ""
            
            html += f"""
            <div class="article">
                <div class="article-title">
                    <a href="{url}" target="_blank">{i}. {title}</a>
                </div>
                <div class="article-meta">
                    <span class="source">{source}</span>
                    {f" • {published_at}" if published_at else ""}
                </div>
                <div class="article-description">
                    {description}
                </div>
            </div>
            """
    
    html += """
            <div class="footer">
                <p>This is an automated daily newsletter powered by NewsAPI.org</p>
                <p>Delivered by GitHub Actions</p>
            </div>
        </div>
    </body>
    </html>
    """
    
    return html


def send_email(recipient, subject, html_content, smtp_user, smtp_password):
    """
    Send an email using SMTP.
    
    Args:
        recipient (str): Recipient email address
        subject (str): Email subject
        html_content (str): HTML email content
        smtp_user (str): SMTP username
        smtp_password (str): SMTP password
        
    Returns:
        bool: True if email sent successfully, False otherwise
    """
    # Create message
    msg = MIMEMultipart('alternative')
    msg['Subject'] = subject
    msg['From'] = smtp_user
    msg['To'] = recipient
    
    # Attach HTML content
    html_part = MIMEText(html_content, 'html')
    msg.attach(html_part)
    
    # Determine SMTP server based on email provider
    smtp_server = "smtp.gmail.com"
    smtp_port = 587
    
    # Check if using a different email provider
    if "@outlook.com" in smtp_user or "@hotmail.com" in smtp_user:
        smtp_server = "smtp-mail.outlook.com"
    elif "@yahoo.com" in smtp_user:
        smtp_server = "smtp.mail.yahoo.com"
    
    try:
        # Connect to SMTP server
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(smtp_user, smtp_password)
        
        # Send email
        server.send_message(msg)
        server.quit()
        
        print(f"✅ Email sent successfully to {recipient}")
        return True
        
    except Exception as e:
        print(f"❌ Error sending email: {e}")
        return False


def main():
    """Main function to fetch news and send email."""
    # Get environment variables
    news_api_key = os.getenv("NEWS_API_KEY")
    email_username = os.getenv("EMAIL_USERNAME")
    email_password = os.getenv("EMAIL_PASSWORD")
    recipient_email = os.getenv("RECIPIENT_EMAIL")
    
    # Validate environment variables
    missing_vars = []
    if not news_api_key:
        missing_vars.append("NEWS_API_KEY")
    if not email_username:
        missing_vars.append("EMAIL_USERNAME")
    if not email_password:
        missing_vars.append("EMAIL_PASSWORD")
    if not recipient_email:
        missing_vars.append("RECIPIENT_EMAIL")
    
    if missing_vars:
        print(f"❌ Error: Missing required environment variables: {', '.join(missing_vars)}")
        sys.exit(1)
    
    print("📰 Fetching technology news...")
    articles = fetch_tech_news(news_api_key)
    
    if articles:
        print(f"✅ Found {len(articles)} articles")
    else:
        print("⚠️  No articles found, but continuing to send email...")
    
    print("📧 Creating email content...")
    html_content = create_html_email(articles)
    
    current_date = datetime.now().strftime("%B %d, %Y")
    subject = f"🚀 Daily Tech News - {current_date}"
    
    print("📤 Sending email...")
    success = send_email(recipient_email, subject, html_content, email_username, email_password)
    
    if success:
        print("🎉 Daily tech news delivered successfully!")
        sys.exit(0)
    else:
        print("❌ Failed to deliver daily tech news")
        sys.exit(1)


if __name__ == "__main__":
    main()
