# Database Blueprint

## 1. Users Table

| Column Name | Data Type    | Constraints      |
| ----------- | ------------ | ---------------- |
| user_id     | INT          | PRIMARY KEY      |
| username    | VARCHAR(255) | NOT NULL         |
| email       | VARCHAR(255) | UNIQUE, NOT NULL |
| password    | VARCHAR(255) | NOT NULL         |
| is_employer | BOOLEAN      | DEFAULT FALSE    |
| created_at  | TIMESTAMP    | DEFAULT now()    |

## 2. Profiles Table (Job Seeker Info)

| Column Name | Data Type    | Constraints                           |
| ----------- | ------------ | ------------------------------------- |
| profile_id  | INT          | PRIMARY KEY                           |
| user_id     | INT          | FOREIGN KEY REFERENCES Users(user_id) |
| full_name   | VARCHAR(255) |                                       |
| location    | VARCHAR(255) |                                       |
| experience  | TEXT         |                                       |
| skills      | TEXT         |                                       |
| resume_url  | VARCHAR(255) |                                       |

## 3. Companies Table (Employer Info)

| Column Name  | Data Type    | Constraints                           |
| ------------ | ------------ | ------------------------------------- |
| company_id   | INT          | PRIMARY KEY                           |
| user_id      | INT          | FOREIGN KEY REFERENCES Users(user_id) |
| company_name | VARCHAR(255) |                                       |
| company_logo | VARCHAR(255) |                                       |
| description  | TEXT         |                                       |

## 4. Jobs Table

| Column Name | Data Type    | Constraints                                  |
| ----------- | ------------ | -------------------------------------------- |
| job_id      | INT          | PRIMARY KEY                                  |
| company_id  | INT          | FOREIGN KEY REFERENCES Companies(company_id) |
| title       | VARCHAR(255) |                                              |
| description | TEXT         |                                              |
| location    | VARCHAR(255) |                                              |
| salary      | VARCHAR(255) |                                              |
| posted_on   | TIMESTAMP    | DEFAULT now()                                |

## 5. Applications Table

| Column Name    | Data Type   | Constraints                           |
| -------------- | ----------- | ------------------------------------- |
| application_id | INT         | PRIMARY KEY                           |
| job_id         | INT         | FOREIGN KEY REFERENCES Jobs(job_id)   |
| user_id        | INT         | FOREIGN KEY REFERENCES Users(user_id) |
| applied_on     | TIMESTAMP   | DEFAULT now()                         |
| status         | VARCHAR(50) | DEFAULT 'Applied'                     |

## 6. SavedJobs Table

| Column Name  | Data Type | Constraints                           |
| ------------ | --------- | ------------------------------------- |
| saved_job_id | INT       | PRIMARY KEY                           |
| job_id       | INT       | FOREIGN KEY REFERENCES Jobs(job_id)   |
| user_id      | INT       | FOREIGN KEY REFERENCES Users(user_id) |
| saved_on     | TIMESTAMP | DEFAULT now()                         |

## 7. LikedJobs Table

| Column Name  | Data Type | Constraints                           |
| ------------ | --------- | ------------------------------------- |
| liked_job_id | INT       | PRIMARY KEY                           |
| user_id      | INT       | FOREIGN KEY REFERENCES Users(user_id) |
| job_id       | INT       | FOREIGN KEY REFERENCES Jobs(job_id)   |
| liked_on     | TIMESTAMP | DEFAULT now()                         |

## 8. DislikedJobs Table

| Column Name     | Data Type | Constraints                           |
| --------------- | --------- | ------------------------------------- |
| disliked_job_id | INT       | PRIMARY KEY                           |
| user_id         | INT       | FOREIGN KEY REFERENCES Users(user_id) |
| job_id          | INT       | FOREIGN KEY REFERENCES Jobs(job_id)   |
| disliked_on     | TIMESTAMP | DEFAULT now()                         |

## 9. CompanyReviews Table

| Column Name | Data Type | Constraints                                  |
| ----------- | --------- | -------------------------------------------- |
| review_id   | INT       | PRIMARY KEY                                  |
| company_id  | INT       | FOREIGN KEY REFERENCES Companies(company_id) |
| user_id     | INT       | FOREIGN KEY REFERENCES Users(user_id)        |
| rating      | INT       | CHECK (rating BETWEEN 1 AND 5)               |
| review_text | TEXT      |                                              |
| created_at  | TIMESTAMP | DEFAULT now()                                |

## 10. CompanyFollows Table

| Column Name | Data Type | Constraints                                  |
| ----------- | --------- | -------------------------------------------- |
| follow_id   | INT       | PRIMARY KEY                                  |
| user_id     | INT       | FOREIGN KEY REFERENCES Users(user_id)        |
| company_id  | INT       | FOREIGN KEY REFERENCES Companies(company_id) |
| followed_on | TIMESTAMP | DEFAULT now()                                |
