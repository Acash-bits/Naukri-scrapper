"""
WHATSAPP JOB ALERTS USING CALLMEBOT
====================================
100% FREE WhatsApp notifications for your job scraper!

SETUP INSTRUCTIONS:
-------------------
1. Add CallMeBot to your WhatsApp contacts
2. Get your API key (see instructions below)
3. Update your .env file
4. Run this test script
5. Integrate into your main scraper

NO CODING KNOWLEDGE NEEDED FOR SETUP!
"""

import requests
import urllib.parse
from datetime import datetime
import os
from dotenv import load_dotenv

load_dotenv()

# ==========================================
# STEP-BY-STEP SETUP GUIDE
# ==========================================

"""
📱 HOW TO GET YOUR WHATSAPP API KEY (3 MINUTES):
------------------------------------------------

1. Save this number in your contacts: +34 644 34 97 24
   Name it: "CallMeBot"

2. Send this EXACT message to that number on WhatsApp:
   I allow callmebot to send me messages

3. Wait 1-2 minutes. You'll receive a reply with your API key like:
   "Your API key is: 123456"

4. Copy that API key number

5. Add to your .env file:
   WHATSAPP_PHONE=917048930137  # Your number with country code (91 for India)
   WHATSAPP_API_KEY=123456       # The key you received

THAT'S IT! ✅
"""

# WhatsApp Configuration
WHATSAPP_CONFIG = {
    'phone': os.getenv('WHATSAPP_PHONE'),  # Format: 917048930137 (country code + number)
    'api_key': os.getenv('WHATSAPP_API_KEY')
}

def send_whatsapp_message(message):
    """
    Send a WhatsApp message using CallMeBot API
    
    Args:
        message (str): The message to send (max 1000 characters recommended)
    
    Returns:
        bool: True if sent successfully, False otherwise
    """
    
    # Validate configuration
    if not WHATSAPP_CONFIG['phone']:
        print("❌ WHATSAPP_PHONE not set in .env file")
        print("Add: WHATSAPP_PHONE=917048930137 (with country code)")
        return False
    
    if not WHATSAPP_CONFIG['api_key']:
        print("❌ WHATSAPP_API_KEY not set in .env file")
        print("Follow setup instructions above to get your API key")
        return False
    
    # CallMeBot API endpoint
    url = "https://api.callmebot.com/whatsapp.php"
    
    # URL encode the message
    encoded_message = urllib.parse.quote(message)
    
    # Construct full URL with parameters
    full_url = f"{url}?phone={WHATSAPP_CONFIG['phone']}&text={encoded_message}&apikey={WHATSAPP_CONFIG['api_key']}"
    
    try:
        print("\n" + "="*60)
        print("SENDING WHATSAPP MESSAGE")
        print("="*60)
        print(f"Phone: +{WHATSAPP_CONFIG['phone']}")
        print(f"Message Length: {len(message)} characters")
        print("="*60)
        print("\nMESSAGE PREVIEW:")
        print("-"*60)
        print(message)
        print("-"*60 + "\n")
        
        # Send request
        response = requests.get(full_url)
        
        if response.status_code == 200:
            print("="*60)
            print("✅ WHATSAPP MESSAGE SENT SUCCESSFULLY!")
            print("="*60)
            print("\n📱 Check your WhatsApp now!")
            print("Message should arrive within 5-10 seconds.\n")
            return True
        else:
            print(f"❌ Failed to send. Status code: {response.status_code}")
            print(f"Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Error sending WhatsApp message: {e}")
        return False

def create_job_whatsapp_message(jobs, max_jobs=5):
    """
    Create a WhatsApp-formatted message with job listings
    
    Args:
        jobs (list): List of job dictionaries
        max_jobs (int): Maximum number of jobs to include
    
    Returns:
        str: Formatted WhatsApp message
    """
    
    if not jobs:
        return "No new jobs found."
    
    # Limit jobs to avoid message being too long
    jobs_to_send = jobs[:max_jobs]
    
    # Create message with emojis and formatting
    message = f"🎯 *{len(jobs)} NEW JOB{'S' if len(jobs) > 1 else ''}!*\n"
    message += f"_{datetime.now().strftime('%B %d, %Y at %I:%M %p')}_\n\n"
    
    for idx, job in enumerate(jobs_to_send, 1):
        message += f"*{idx}. {job['job_title']}*\n"
        message += f"🏢 {job['company_name']}\n"
        message += f"📍 {job['location']}\n"
        message += f"💰 {job['salary']}\n"
        message += f"💼 {job['experience']}\n"
        message += f"⏰ {job['time_category']}\n"
        message += f"🔗 {job['link'][:50]}...\n"  # Shorten long URLs
        message += "\n"
    
    if len(jobs) > max_jobs:
        message += f"_+ {len(jobs) - max_jobs} more jobs. Check your email for full details._\n"
    
    message += "\n✨ _Job Alert System - Powered by Naukri Scraper_"
    
    return message

def send_job_whatsapp_alerts(jobs):
    """
    Send job alerts via WhatsApp
    
    Args:
        jobs (list): List of job dictionaries from your scraper
    
    Returns:
        bool: True if sent successfully
    """
    
    if not jobs:
        print("No jobs to send via WhatsApp")
        return False
    
    # Create formatted message
    message = create_job_whatsapp_message(jobs, max_jobs=5)
    
    # Send via WhatsApp
    return send_whatsapp_message(message)

# ==========================================
# TEST FUNCTIONS
# ==========================================

def test_simple_message():
    """Send a simple test message"""
    message = f"🧪 *Test Message*\n\nThis is a test from your Job Scraper!\n\nTime: {datetime.now().strftime('%I:%M %p')}\n\n✅ If you received this, WhatsApp alerts are working!"
    return send_whatsapp_message(message)

def test_job_alert():
    """Send a sample job alert"""
    sample_jobs = [
        {
            'job_title': 'Senior Business Analyst',
            'company_name': 'Accenture',
            'location': 'Gurgaon',
            'salary': '10-15 LPA',
            'experience': '4-6 Yrs',
            'time_category': 'Posted Just Now',
            'link': 'https://www.naukri.com/job-listings-senior-business-analyst-accenture-gurgaon-4-to-6-years-123456'
        },
        {
            'job_title': 'Data Analyst',
            'company_name': 'Deloitte',
            'location': 'Noida',
            'salary': '8-12 LPA',
            'experience': '3-5 Yrs',
            'time_category': 'Recently Posted',
            'link': 'https://www.naukri.com/job-listings-data-analyst-deloitte-noida-3-to-5-years-789012'
        },
        {
            'job_title': 'Product Manager',
            'company_name': 'Amazon',
            'location': 'Delhi',
            'salary': '15-20 LPA',
            'experience': '5-7 Yrs',
            'time_category': 'Posted This Week',
            'link': 'https://www.naukri.com/job-listings-product-manager-amazon-delhi-5-to-7-years-345678'
        }
    ]
    
    return send_job_whatsapp_alerts(sample_jobs)

# ==========================================
# INTEGRATION WITH YOUR MAIN SCRAPER
# ==========================================

def process_and_send_notifications():
    """
    Updated version of your process_and_send_emails() function
    Now sends BOTH email AND WhatsApp notifications
    """
    print('\n' + '='*80)
    print('PROCESSING EMAIL & WHATSAPP NOTIFICATIONS')
    print("="*80 + "\n")

    # Get unsent jobs (your existing function)
    from your_scraper import get_unsent_jobs, send_job_emails, mark_jobs_as_sent
    
    unsent_jobs = get_unsent_jobs()
    if not unsent_jobs:
        print('No unsent jobs found. All caught up!!!!')
        return
    
    print(f'\nPreparing to send {len(unsent_jobs)} job(s)...')
    
    # Send Email (your existing function)
    email_sent = send_job_emails(unsent_jobs)
    
    # Send WhatsApp
    whatsapp_enabled = os.getenv('WHATSAPP_ENABLED', 'false').lower() == 'true'
    whatsapp_sent = False
    
    if whatsapp_enabled:
        whatsapp_sent = send_job_whatsapp_alerts(unsent_jobs)
    else:
        print("⚠️ WhatsApp notifications disabled. Set WHATSAPP_ENABLED=true in .env to enable.")
    
    # Mark as sent if either method succeeded
    if email_sent or whatsapp_sent:
        job_ids = [job['job_id'] for job in unsent_jobs]
        mark_jobs_as_sent(job_ids)
        print('\n✅ Notification process completed!')
    else:
        print('\n❌ All notification methods failed. Jobs remain unsent.')
    
    print("\n" + "=" * 80 + "\n")

# ==========================================
# MAIN TEST SCRIPT
# ==========================================

if __name__ == "__main__":
    print("\n" + "="*60)
    print("WHATSAPP JOB ALERTS - TEST UTILITY")
    print("="*60 + "\n")
    
    # Check configuration
    if not os.path.exists('.env'):
        print("⚠️ No .env file found!")
        print("\nPlease create a .env file with:\n")
        print("-"*60)
        print("WHATSAPP_PHONE=917048930137  # Your number with country code")
        print("WHATSAPP_API_KEY=123456       # Get from CallMeBot")
        print("WHATSAPP_ENABLED=true")
        print("-"*60)
        print("\n📱 See setup instructions at the top of this script!\n")
        exit(1)
    
    # Show menu
    print("Choose a test option:")
    print("1. Send SIMPLE test message")
    print("2. Send SAMPLE JOB ALERT (3 jobs)")
    print("3. View setup instructions")
    print("4. Exit")
    print()
    
    choice = input("Enter your choice (1-4): ").strip()
    
    if choice == '1':
        test_simple_message()
    elif choice == '2':
        test_job_alert()
    elif choice == '3':
        print("\n" + "="*60)
        print("SETUP INSTRUCTIONS")
        print("="*60)
        print("""
1. Save this number in WhatsApp: +34 644 34 97 24
   (Name it: "CallMeBot")

2. Send this message to that number:
   I allow callmebot to send me messages

3. Wait 1-2 minutes for a reply with your API key

4. Add to your .env file:
   WHATSAPP_PHONE=917048930137  # Country code + your number
   WHATSAPP_API_KEY=123456       # The key you received
   WHATSAPP_ENABLED=true

5. Run this test script again (option 1 or 2)

LIMITATIONS:
- Max 1 message per minute (free tier)
- Messages can be max ~1000 characters
- Perfect for job alerts!
        """)
        print("="*60 + "\n")
    elif choice == '4':
        print("Goodbye! 👋")
    else:
        print("❌ Invalid choice. Please run again and choose 1-4.")