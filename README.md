# 🚀 Daily Tech News Email Workflow

Automated GitHub Actions workflow that fetches the latest technology news daily and sends it to your email as a beautifully formatted newsletter.

## ✨ Features

- 📰 Fetches top 10 technology headlines from NewsAPI.org
- 📧 Sends formatted HTML email newsletter
- ⏰ Runs automatically every day at 8:00 AM UTC
- 🎨 Beautiful, responsive email design
- 🔧 Easy to customize and configure
- 🆓 Uses free tier APIs

## 🛠️ Setup Instructions

### 1. Get a NewsAPI Key

1. Visit [NewsAPI.org](https://newsapi.org/register)
2. Sign up for a free account
3. Copy your API key (free tier includes 100 requests/day)

### 2. Configure GitHub Secrets

Add the following secrets to your GitHub repository:

1. Go to your repository on GitHub
2. Click **Settings** → **Secrets and variables** → **Actions**
3. Click **New repository secret** and add each of the following:

| Secret Name | Description | Example |
|-------------|-------------|---------|
| `NEWS_API_KEY` | Your NewsAPI.org API key | `abc123def456...` |
| `EMAIL_USERNAME` | Your SMTP email address | `yourname@gmail.com` |
| `EMAIL_PASSWORD` | Your email app password | `abcd efgh ijkl mnop` |
| `RECIPIENT_EMAIL` | Email where you want to receive news | `yourname@gmail.com` |

### 3. Email Provider Setup

#### For Gmail Users (Recommended)

> [!IMPORTANT]
> Gmail requires an **App Password** instead of your regular password.

1. Enable 2-Factor Authentication on your Google account
2. Go to [Google App Passwords](https://myaccount.google.com/apppasswords)
3. Select **Mail** and **Other (Custom name)**
4. Enter "GitHub Actions" as the name
5. Click **Generate**
6. Copy the 16-character password (remove spaces)
7. Use this as your `EMAIL_PASSWORD` secret

#### For Outlook/Hotmail Users

1. Use your regular Outlook email and password
2. Make sure "Less secure app access" is enabled if required

#### For Yahoo Users

1. Generate an app password from [Yahoo Account Security](https://login.yahoo.com/account/security)
2. Use the app password as your `EMAIL_PASSWORD`

### 4. Customize Schedule (Optional)

The workflow runs daily at **8:00 AM UTC** by default. To change this:

1. Open [`.github/workflows/daily-tech-news.yml`](.github/workflows/daily-tech-news.yml)
2. Modify the cron expression:

```yaml
schedule:
  - cron: '0 8 * * *'  # Format: minute hour day month day-of-week
```

**Examples:**
- `'0 12 * * *'` - Noon UTC (12:00 PM)
- `'30 6 * * *'` - 6:30 AM UTC
- `'0 0 * * 1'` - Midnight UTC every Monday

> [!TIP]
> Use [crontab.guru](https://crontab.guru/) to help create cron expressions.

### 5. Test the Workflow

#### Manual Trigger

1. Go to your repository on GitHub
2. Click **Actions** tab
3. Select **Daily Tech News Email** workflow
4. Click **Run workflow** → **Run workflow**
5. Wait for the workflow to complete
6. Check your email inbox

#### View Logs

1. Click on the workflow run
2. Click on the **send-tech-news** job
3. Expand each step to see detailed logs

## 🧪 Local Testing

To test the script locally before deploying:

1. Clone the repository:
```bash
git clone <your-repo-url>
cd news_updates
```

2. Create a `.env` file from the example:
```bash
cp .env.example .env
```

3. Edit `.env` and add your credentials:
```bash
NEWS_API_KEY=your_actual_api_key
EMAIL_USERNAME=your_email@gmail.com
EMAIL_PASSWORD=your_app_password
RECIPIENT_EMAIL=your_email@gmail.com
```

4. Install dependencies:
```bash
pip install -r requirements.txt
```

5. Run the script:
```bash
python fetch_news.py
```

## 📧 Email Preview

The email newsletter includes:
- 📰 Top 10 technology headlines
- 🔗 Clickable article links
- 📅 Publication dates and times
- 🏢 News source attribution
- 🎨 Clean, modern design

## 🔧 Troubleshooting

### Workflow Not Running

- Check that the workflow file is in `.github/workflows/` directory
- Verify GitHub Actions is enabled in repository settings
- Check the Actions tab for any error messages

### Email Not Received

- Verify all GitHub secrets are set correctly
- Check spam/junk folder
- Review workflow logs for error messages
- For Gmail: Ensure you're using an App Password, not your regular password
- Test with manual workflow trigger first

### API Errors

- Verify your NewsAPI key is valid
- Check you haven't exceeded the free tier limit (100 requests/day)
- Ensure the API key is correctly set in GitHub secrets

### SMTP Authentication Failed

- **Gmail**: Must use App Password with 2FA enabled
- **Outlook**: Check if "Less secure app access" needs to be enabled
- **Yahoo**: Use app-specific password
- Verify `EMAIL_USERNAME` and `EMAIL_PASSWORD` are correct

## 🎨 Customization

### Change News Category

Edit `fetch_news.py` and modify the API parameters:

```python
params = {
    "category": "technology",  # Change to: business, science, health, etc.
    "language": "en",
    "pageSize": 10,
    "apiKey": api_key
}
```

### Change Number of Articles

Modify `pageSize` in the API parameters (max: 100 for free tier):

```python
"pageSize": 15,  # Get 15 articles instead of 10
```

### Customize Email Design

Edit the HTML template in the `create_html_email()` function in `fetch_news.py`.

## 📝 License

This project is open source and available under the MIT License.

## 🤝 Contributing

Contributions, issues, and feature requests are welcome!

## 📬 Support

If you encounter any issues, please check the troubleshooting section or open an issue on GitHub.

---

**Powered by:**
- [NewsAPI.org](https://newsapi.org/) - News aggregation
- [GitHub Actions](https://github.com/features/actions) - Automation
- Python 3.11+ - Script execution
