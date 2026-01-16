# 🎯 Naukri.com Job Scraper & Email Alerting System

![Python](https://img.shields.io/badge/python-3.8+-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
![Status](https://img.shields.io/badge/status-active-success.svg)

An automated job scraping system that monitors Naukri.com for new job postings in Delhi NCR, stores them in a MySQL database, and sends beautifully formatted email alerts for new opportunities. The scraper is designed to evade bot detection using stealth techniques and human-like behavior simulation.

## 📋 Table of Contents

- [Features](#-features)
- [Tech Stack](#-tech-stack)
- [Prerequisites](#-prerequisites)
- [Installation](#-installation)
- [Configuration](#-configuration)
- [Database Setup](#-database-setup)
- [Usage](#-usage)
- [Project Structure](#-project-structure)
- [How It Works](#-how-it-works)
- [Email Notifications](#-email-notifications)
- [Customization](#-customization)
- [Troubleshooting](#-troubleshooting)
- [Best Practices](#-best-practices)
- [Contributing](#-contributing)
- [License](#-license)
- [Disclaimer](#-disclaimer)

---

## ✨ Features

### Core Functionality
- 🔍 **Multi-Category Scraping**: Scrapes jobs across 5 categories (Business Analyst, Senior Business Analyst, Data Analyst, Product Manager, Strategy Analyst)
- 🤖 **Bot Detection Evasion**: Uses Playwright Stealth to bypass anti-bot measures
- 👤 **Human-Like Behavior**: Simulates realistic mouse movements, scrolling, and browsing patterns
- 📄 **Multi-Page Support**: Automatically navigates through multiple pages using "Next" button clicks
- 🕒 **Smart Time Categorization**: Categorizes jobs by posting time (Just Now, Recently Posted, This Week, etc.)
- 🗄️ **Database Storage**: Stores all scraped jobs in MySQL with duplicate detection
- 📧 **Email Alerts**: Sends beautifully formatted HTML emails with new job listings
- ⏰ **Scheduled Execution**: Runs automatically at configurable intervals
- 🔄 **Incremental Updates**: Only emails jobs that haven't been sent before

### Advanced Features
- **Duplicate Prevention**: URL-based duplicate detection ensures no job is stored twice
- **Filtering**: Automatically excludes "old" job postings (older than 7 days)
- **Concurrent/Sequential Modes**: Choose between fast concurrent scraping or safer sequential scraping
- **Comprehensive Logging**: Detailed console output for monitoring and debugging
- **Error Handling**: Robust error handling with graceful degradation

---

## 🛠️ Tech Stack

- **Python 3.8+**: Core programming language
- **Playwright**: Browser automation and web scraping
- **Playwright-Stealth**: Anti-bot detection evasion
- **BeautifulSoup4**: HTML parsing
- **MySQL**: Database for job storage
- **Pandas**: Data manipulation and analysis
- **python-dotenv**: Environment variable management
- **smtplib**: Email sending functionality
- **Schedule**: Task scheduling

---

## 📦 Prerequisites

Before you begin, ensure you have the following installed:

- **Python 3.8 or higher**
- **MySQL Server** (v5.7+ or v8.0+)
- **pip** (Python package manager)
- **Git** (for cloning the repository)

### System Requirements
- **OS**: Windows, macOS, or Linux
- **RAM**: Minimum 4GB (8GB recommended)
- **Disk Space**: 500MB for dependencies and browser binaries

---

## 🚀 Installation

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/naukri-job-scraper.git
cd naukri-job-scraper
```

### 2. Create Virtual Environment (Recommended)

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Install Playwright Browsers

```bash
playwright install chromium
```

This downloads the Chromium browser binary required for web scraping.

---

## ⚙️ Configuration

### 1. Environment Variables

Create a `.env` file in the project root directory:

```bash
cp .env.example .env
```

Edit `.env` with your credentials:

```env
# Database Configuration
HOST=localhost
USER=root
PASS=your_mysql_password
DATABASE=naukri_com

# Email Configuration
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SENDER_EMAIL=your_email@gmail.com
SENDER_PASSWORD=your_app_password
RECIPIENT_EMAIL=recipient@gmail.com

# SMS Configuration (Optional - Future Feature)
SMS_ENABLED=false
SMS_PHONE_NUMBER=your_phone_number
SMS_CARRIER=vi
```

### 2. Gmail App Password Setup

**Important**: Don't use your regular Gmail password!

1. Go to [Google Account Security](https://myaccount.google.com/security)
2. Enable **2-Step Verification**
3. Go to **App Passwords** section
4. Generate a new app password for "Mail"
5. Use this 16-character password in `SENDER_PASSWORD`

### 3. Customize Job Categories (Optional)

Edit `naukri_intelligence.py` to modify job search URLs:

```python
job_urls = {
    'Your Custom Category': 'https://www.naukri.com/your-search-url',
    # Add more categories as needed
}
```

### 4. Adjust Scraping Parameters

```python
MAX_PAGES = 50  # Number of pages to scrape per category
SCRAPE_INTERVAL_HOURS = 3  # How often to run the scraper
RUN_IMMEDIATELY = True  # Run on startup or wait for first interval
```

---

## 🗄️ Database Setup

### 1. Create Database

Login to MySQL and create the database:

```sql
CREATE DATABASE naukri_com CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE naukri_com;
```

### 2. Create Table

```sql
CREATE TABLE job_postings (
    job_id INT AUTO_INCREMENT PRIMARY KEY,
    category VARCHAR(100) NOT NULL,
    job_title VARCHAR(255) NOT NULL,
    company_name VARCHAR(255) NOT NULL,
    location VARCHAR(255),
    salary VARCHAR(100),
    experience VARCHAR(100),
    posting_time VARCHAR(100),
    time_category VARCHAR(50),
    link VARCHAR(500) UNIQUE NOT NULL,
    page_number INT,
    scraped_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    email_sent TINYINT(1) DEFAULT 0,
    INDEX idx_email_sent (email_sent),
    INDEX idx_time_category (time_category),
    INDEX idx_scraped_time (scraped_time),
    INDEX idx_category (category)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
```

### 3. Verify Table Creation

```sql
DESCRIBE job_postings;
```

---

## 🎮 Usage

### Running the Scraper

#### Option 1: Scheduled Mode (Recommended)

Run the scraper with automatic scheduling:

```bash
python naukri_intelligence.py
```

This will:
- Run immediately on startup (if `RUN_IMMEDIATELY = True`)
- Schedule subsequent runs every `SCRAPE_INTERVAL_HOURS` hours
- Keep running indefinitely until manually stopped (Ctrl+C)

#### Option 2: One-Time Execution

For testing or manual runs, modify the `if __name__ == "__main__":` section:

```python
if __name__ == "__main__":
    asyncio.run(main())
```

Then run:

```bash
python naukri_intelligence.py
```

### Monitoring the Scraper

Watch the console output for:
- ✅ Successful page scrapes
- 📧 Email sending status
- 🗄️ Database insertion results
- ⚠️ Any errors or warnings

---

## 📁 Project Structure

```
naukri-job-scraper/
│
├── naukri_intelligence.py    # Main scraper script
├── .env                       # Environment variables (DO NOT COMMIT)
├── .env.example              # Template for environment variables
├── .gitignore                # Git ignore rules
├── requirements.txt          # Python dependencies
├── README.md                 # This file
│
├── schema/
│   └── database_schema.sql   # MySQL table creation script
│
├── docs/
│   ├── SETUP_GUIDE.md       # Detailed setup instructions
│   ├── TROUBLESHOOTING.md   # Common issues and solutions
│   └── API_REFERENCE.md     # Code documentation
│
└── screenshots/
    ├── email_sample.png      # Sample email screenshot
    └── terminal_output.png   # Sample terminal output
```

---

## 🔧 How It Works

### 1. **Scraping Process**

```
┌─────────────────────────────────────────────────────────────┐
│  1. Launch Chromium Browser (Stealth Mode)                  │
│  2. Visit Naukri.com Homepage (Session Establishment)        │
│  3. Navigate to Each Job Category URL                       │
│  4. For Each Page:                                          │
│     ├─ Simulate Human Behavior (Scrolling, Mouse Movement) │
│     ├─ Parse Job Listings with BeautifulSoup               │
│     ├─ Extract: Title, Company, Location, Salary, etc.     │
│     ├─ Filter by Time Category (Exclude "Old" Jobs)        │
│     └─ Click "Next" Button to Navigate                     │
│  5. Store Results in MySQL Database                         │
│  6. Send Email Alerts for New Jobs                          │
└─────────────────────────────────────────────────────────────┘
```

### 2. **Time Categorization Logic**

Jobs are categorized based on posting time:

| Time Posted | Category |
|-------------|----------|
| Just now, within hours | Posted Just Now |
| Today, 1-2 days ago | Recently Posted |
| 3-4 days ago | Posted Within 3-4 days |
| 5-7 days ago | Posted This Week |
| Older than 7 days | Old (Filtered Out) |

### 3. **Duplicate Detection**

The database uses a **UNIQUE constraint** on the `link` column. If a job URL already exists, it's skipped via `INSERT IGNORE`.

### 4. **Email Workflow**

```
┌─────────────────────────────────────────────┐
│  1. Query database for unsent jobs         │
│     (WHERE email_sent = 0)                 │
│  2. Generate HTML email with job cards     │
│  3. Send via SMTP (Gmail)                  │
│  4. Mark jobs as sent (email_sent = 1)     │
└─────────────────────────────────────────────┘
```

---

## 📧 Email Notifications

### Email Features

- **Beautiful HTML Design**: Gradient headers, hover effects, responsive layout
- **Job Cards**: Each job displayed in a visually appealing card
- **Color-Coded Badges**: Time categories shown with different colors
- **Direct Links**: One-click access to job application pages
- **Timestamps**: Shows when job was scraped and posted
- **Summary Header**: Total count and current date/time

### Sample Email Content

Each email includes:
- Header with job count and date
- Individual job cards with:
  - Job title and company
  - Location, experience, salary
  - Posting time with color-coded badges
  - Scraped timestamp
  - "View Job Details" button
- Footer with system information

---

## 🎨 Customization

### 1. Change Scraping Frequency

```python
# In naukri_intelligence.py
SCRAPE_INTERVAL_HOURS = 6  # Change from 3 to 6 hours
```

### 2. Modify Job Search Criteria

Update the `job_urls` dictionary:

```python
job_urls = {
    'Software Engineer': 'https://www.naukri.com/software-engineer-jobs-in-delhi-ncr',
    'DevOps Engineer': 'https://www.naukri.com/devops-jobs-in-delhi-ncr',
}
```

### 3. Change Location

Replace `delhi+%2F+ncr` in URLs with your preferred location:
- Mumbai: `mumbai`
- Bangalore: `bangalore`
- Pune: `pune`

### 4. Adjust Maximum Pages

```python
MAX_PAGES = 100  # Scrape more pages (be cautious of rate limiting)
```

### 5. Email Template Customization

Edit the `create_email_html()` function to modify:
- Color scheme (change hex codes in CSS)
- Layout structure
- Badge styles
- Font sizes and families

---

## 🐛 Troubleshooting

### Common Issues

#### 1. **"Connection refused" or "Can't connect to MySQL"**

**Solution:**
- Verify MySQL is running: `sudo systemctl status mysql`
- Check credentials in `.env` file
- Ensure database `naukri_com` exists

#### 2. **"Email sending failed"**

**Solution:**
- Verify Gmail App Password (not regular password)
- Check SMTP settings in `.env`
- Ensure "Less secure app access" is OFF (use App Password instead)
- Check firewall/antivirus blocking port 587

#### 3. **"Next button not found"**

**Solution:**
- Naukri.com may have changed their HTML structure
- Check browser's developer tools for updated selectors
- Update the `next_selectors` list in `click_next_button()`

#### 4. **"Bot detection / Captcha appearing"**

**Solution:**
- Increase delays between requests
- Use sequential mode instead of concurrent
- Reduce `MAX_PAGES`
- Add more randomization to `human_like_behavior()`

#### 5. **"Playwright browser not found"**

**Solution:**
```bash
playwright install chromium
```

### Debug Mode

Enable verbose logging:

```python
# Add at the top of naukri_intelligence.py
import logging
logging.basicConfig(level=logging.DEBUG)
```

---

## 🌟 Best Practices

### 1. **Respect Rate Limits**
- Don't scrape too frequently (minimum 3-hour intervals recommended)
- Use reasonable `MAX_PAGES` values (50 or less)
- Implement longer delays if you encounter blocks

### 2. **Keep Browser Updated**
```bash
playwright install --force chromium
```

### 3. **Monitor Database Size**
- Periodically clean old job postings:
```sql
DELETE FROM job_postings WHERE scraped_time < DATE_SUB(NOW(), INTERVAL 30 DAY);
```

### 4. **Secure Your Credentials**
- Never commit `.env` file to Git
- Use strong MySQL passwords
- Rotate Gmail App Passwords periodically

### 5. **Error Monitoring**
- Set up log file rotation
- Consider implementing alerting for critical errors
- Monitor disk space for database growth

---

## 🤝 Contributing

Contributions are welcome! Here's how you can help:

1. **Fork the repository**
2. **Create a feature branch**
   ```bash
   git checkout -b feature/amazing-feature
   ```
3. **Commit your changes**
   ```bash
   git commit -m 'Add some amazing feature'
   ```
4. **Push to the branch**
   ```bash
   git push origin feature/amazing-feature
   ```
5. **Open a Pull Request**

### Contribution Ideas
- Add support for other job portals (LinkedIn, Indeed, Monster)
- Implement SMS notifications
- Create a web dashboard for viewing jobs
- Add machine learning for job recommendation
- Support for more locations/categories
- Docker containerization
- CI/CD pipeline setup

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

```
MIT License

Copyright (c) 2026 Your Name

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

---

## ⚠️ Disclaimer

This project is for **educational purposes only**. 

- **Web Scraping Ethics**: Always respect a website's `robots.txt` and Terms of Service
- **Rate Limiting**: Implement reasonable delays to avoid overloading servers
- **Legal Compliance**: Ensure your use complies with local laws and regulations
- **No Warranty**: This software is provided "as is" without any warranties
- **User Responsibility**: Users are responsible for their usage and compliance

**Note**: Naukri.com's structure may change over time, requiring updates to selectors and logic.

---

## 📞 Support

### Getting Help
- **Issues**: [GitHub Issues](https://github.com/yourusername/naukri-job-scraper/issues)
- **Discussions**: [GitHub Discussions](https://github.com/yourusername/naukri-job-scraper/discussions)
- **Email**: your.email@example.com

### Useful Resources
- [Playwright Documentation](https://playwright.dev/python/)
- [BeautifulSoup Documentation](https://www.crummy.com/software/BeautifulSoup/bs4/doc/)
- [MySQL Documentation](https://dev.mysql.com/doc/)
- [Python Email Documentation](https://docs.python.org/3/library/email.html)

---

## 🙏 Acknowledgments

- **Playwright Team** - For the excellent browser automation framework
- **BeautifulSoup** - For powerful HTML parsing capabilities
- **Naukri.com** - For being a comprehensive job search platform
- **Open Source Community** - For inspiration and support

---

## 📊 Project Stats

![GitHub stars](https://img.shields.io/github/stars/yourusername/naukri-job-scraper?style=social)
![GitHub forks](https://img.shields.io/github/forks/yourusername/naukri-job-scraper?style=social)
![GitHub issues](https://img.shields.io/github/issues/yourusername/naukri-job-scraper)
![GitHub pull requests](https://img.shields.io/github/issues-pr/yourusername/naukri-job-scraper)

---

<div align="center">

**Made with ❤️ by [Your Name](https://github.com/yourusername)**

**⭐ Star this repository if you found it helpful!**

[Report Bug](https://github.com/yourusername/naukri-job-scraper/issues) · [Request Feature](https://github.com/yourusername/naukri-job-scraper/issues)

</div>