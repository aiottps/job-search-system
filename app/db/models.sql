-- 1. User Preferences
IF NOT EXISTS (SELECT * FROM sys.tables WHERE name = 'user_preferences')
CREATE TABLE user_preferences (
    id INT IDENTITY(1,1) PRIMARY KEY,
    user_email NVARCHAR(255) NOT NULL,
    keywords NVARCHAR(MAX) NOT NULL,
    locations NVARCHAR(MAX) NOT NULL,
    work_modes NVARCHAR(100) NOT NULL,
    min_annual_salary INT NOT NULL DEFAULT 700000,
    salary_step INT NOT NULL DEFAULT 100000,
    sources NVARCHAR(255) NOT NULL,
    language NVARCHAR(50) NOT NULL DEFAULT N'zh-TW',
    is_active BIT NOT NULL DEFAULT 1,
    created_at DATETIME2 NOT NULL DEFAULT SYSUTCDATETIME()
);

-- 2. Jobs
IF NOT EXISTS (SELECT * FROM sys.tables WHERE name = 'jobs')
CREATE TABLE jobs (
    id INT IDENTITY(1,1) PRIMARY KEY,
    source NVARCHAR(50) NOT NULL,
    source_job_id NVARCHAR(255) NULL,
    title NVARCHAR(500) NOT NULL,
    company_name NVARCHAR(500) NOT NULL,
    location NVARCHAR(255) NULL,
    work_mode NVARCHAR(50) NULL,
    salary_text NVARCHAR(255) NULL,
    annual_salary_min INT NULL,
    annual_salary_max INT NULL,
    salary_is_estimated BIT NOT NULL DEFAULT 0,
    salary_note NVARCHAR(MAX) NULL,
    jd_text NVARCHAR(MAX) NULL,
    job_url NVARCHAR(1000) NOT NULL,
    first_seen_at DATETIME2 NOT NULL DEFAULT SYSUTCDATETIME(),
    last_seen_at DATETIME2 NOT NULL DEFAULT SYSUTCDATETIME(),
    content_hash NVARCHAR(128) NOT NULL,
    is_active BIT NOT NULL DEFAULT 1
);

-- 3. Companies
IF NOT EXISTS (SELECT * FROM sys.tables WHERE name = 'companies')
CREATE TABLE companies (
    id INT IDENTITY(1,1) PRIMARY KEY,
    company_name NVARCHAR(500) NOT NULL,
    official_website NVARCHAR(1000) NULL,
    industry NVARCHAR(255) NULL,
    company_size NVARCHAR(255) NULL,
    market_summary NVARCHAR(MAX) NULL,
    updated_at DATETIME2 NOT NULL DEFAULT SYSUTCDATETIME()
);

-- 4. Company Reviews
IF NOT EXISTS (SELECT * FROM sys.tables WHERE name = 'company_reviews')
CREATE TABLE company_reviews (
    id INT IDENTITY(1,1) PRIMARY KEY,
    company_name NVARCHAR(500) NOT NULL,
    review_type NVARCHAR(50) NOT NULL,
    source_name NVARCHAR(255) NOT NULL,
    source_url NVARCHAR(1000) NOT NULL,
    summary NVARCHAR(MAX) NOT NULL,
    reliability_score INT NOT NULL,
    collected_at DATETIME2 NOT NULL DEFAULT SYSUTCDATETIME()
);

-- 5. Interview Guides
IF NOT EXISTS (SELECT * FROM sys.tables WHERE name = 'interview_guides')
CREATE TABLE interview_guides (
    id INT IDENTITY(1,1) PRIMARY KEY,
    job_id INT NOT NULL,
    jd_summary NVARCHAR(MAX) NULL,
    resume_focus NVARCHAR(MAX) NULL,
    required_skills NVARCHAR(MAX) NULL,
    bonus_skills NVARCHAR(MAX) NULL,
    company_market_analysis NVARCHAR(MAX) NULL,
    mock_questions NVARCHAR(MAX) NULL,
    portfolio_suggestions NVARCHAR(MAX) NULL,
    risk_warnings NVARCHAR(MAX) NULL,
    generated_by NVARCHAR(50) NOT NULL DEFAULT N'Gemini',
    created_at DATETIME2 NOT NULL DEFAULT SYSUTCDATETIME(),
    CONSTRAINT FK_interview_guides_jobs FOREIGN KEY (job_id) REFERENCES jobs(id)
);

-- 6. Email Logs
IF NOT EXISTS (SELECT * FROM sys.tables WHERE name = 'email_logs')
CREATE TABLE email_logs (
    id INT IDENTITY(1,1) PRIMARY KEY,
    user_email NVARCHAR(255) NOT NULL,
    email_subject NVARCHAR(500) NOT NULL,
    job_count INT NOT NULL,
    sent_at DATETIME2 NOT NULL DEFAULT SYSUTCDATETIME(),
    status NVARCHAR(50) NOT NULL,
    error_message NVARCHAR(MAX) NULL
);
