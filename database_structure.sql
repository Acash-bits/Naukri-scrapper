-- Create Database
CREATE DATABASE IF NOT EXISTS naukri_com 
CHARACTER SET utf8mb4 
COLLATE utf8mb4_unicode_ci;

-- Use Database
USE naukri_com;

-- Create job_postings table
CREATE TABLE IF NOT EXISTS job_postings (
    job_id INT AUTO_INCREMENT PRIMARY KEY,
    category VARCHAR(100) NOT NULL COMMENT 'Job category (e.g., Business Analyst, Data Analyst)',
    job_title VARCHAR(255) NOT NULL COMMENT 'Title of the job posting',
    company_name VARCHAR(255) NOT NULL COMMENT 'Name of the hiring company',
    location VARCHAR(255) DEFAULT NULL COMMENT 'Job location',
    salary VARCHAR(100) DEFAULT NULL COMMENT 'Salary range or "Not disclosed"',
    experience VARCHAR(100) DEFAULT NULL COMMENT 'Required experience in years',
    posting_time VARCHAR(100) DEFAULT NULL COMMENT 'Original posting time text from Naukri',
    time_category VARCHAR(50) DEFAULT NULL COMMENT 'Categorized time: Just Now, Recently Posted, etc.',
    link VARCHAR(500) UNIQUE NOT NULL COMMENT 'Unique job posting URL',
    page_number INT DEFAULT NULL COMMENT 'Page number where job was found',
    scraped_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT 'When the job was scraped',
    email_sent TINYINT(1) DEFAULT 0 COMMENT 'Whether email notification was sent (0=No, 1=Yes)',
    
    -- Indexes for better query performance
    INDEX idx_email_sent (email_sent),
    INDEX idx_time_category (time_category),
    INDEX idx_scraped_time (scraped_time),
    INDEX idx_category (category),
    INDEX idx_company (company_name(100))
) ENGINE=InnoDB 
DEFAULT CHARSET=utf8mb4 
COLLATE=utf8mb4_unicode_ci
COMMENT='Stores scraped job postings from Naukri.com';

-- Verify table creation
DESCRIBE job_postings;

-- Sample queries for reference

-- Get all unsent jobs
-- SELECT * FROM job_postings WHERE email_sent = 0 ORDER BY scraped_time DESC;

-- Get job count by category
-- SELECT category, COUNT(*) as job_count FROM job_postings GROUP BY category;

-- Get recent jobs (last 24 hours)
-- SELECT * FROM job_postings WHERE scraped_time >= DATE_SUB(NOW(), INTERVAL 24 HOUR);

-- Delete old jobs (older than 30 days) - Use with caution!
-- DELETE FROM job_postings WHERE scraped_time < DATE_SUB(NOW(), INTERVAL 30 DAY);

-- Reset email_sent flag (for testing)
-- UPDATE job_postings SET email_sent = 0;