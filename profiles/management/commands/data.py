
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from profiles.models import Company, Profile

class Command(BaseCommand):
    help = "Populate the database with sample employers and jobseekers."

    def handle(self, *args, **kwargs):
        User = get_user_model()

        employers_data = [
            {
                "username": "google_hr",
                "email": "google.hr@example.com",
                "password": "Google@123",
                "company_name": "Google",
                "company_logo_url": "https://upload.wikimedia.org/wikipedia/commons/2/2f/Google_2015_logo.svg",
                "description": "The world's leading search engine and technology company."
            },
            {
                "username": "microsoft_hr",
                "email": "microsoft.hr@example.com",
                "password": "Microsoft@123",
                "company_name": "Microsoft",
                "company_logo_url": "https://upload.wikimedia.org/wikipedia/commons/4/44/Microsoft_logo.svg",
                "description": "Global leader in software, services, devices, and solutions."
            },
            {
                "username": "amazon_hr",
                "email": "amazon.hr@example.com",
                "password": "Amazon@123",
                "company_name": "Amazon",
                "company_logo_url": "https://upload.wikimedia.org/wikipedia/commons/a/a9/Amazon_logo.svg",
                "description": "The world's largest online retailer and cloud services provider."
            }
        ]

        for emp in employers_data:
            user, created = User.objects.get_or_create(
                username=emp["username"],
                defaults={
                    "email": emp["email"],
                    "is_employer": True
                }
            )
            if created:
                user.set_password(emp["password"])
                user.save()

            company, _ = Company.objects.get_or_create(user=user)
            company.company_name = emp["company_name"]
            company.company_logo_url = emp["company_logo_url"]
            company.description = emp["description"]
            company.save()

        jobseekers_data = [
            {
                "username": "alicej",
                "email": "alice.johnson@example.com",
                "password": "Alice@123",
                "full_name": "Alice Johnson",
                "location": "New York, USA",
                "experience": "3 years as a Software Engineer at a fintech startup.",
                "skills": "Python, Django, REST APIs, SQL",
                "resume_url": "https://drive.google.com/file/d/1alice_resume_link/view"
            },
            {
                "username": "bobsmith",
                "email": "bob.smith@example.com",
                "password": "Bob@123",
                "full_name": "Bob Smith",
                "location": "London, UK",
                "experience": "5 years in Cloud Infrastructure at a major e-commerce company.",
                "skills": "AWS, Docker, Kubernetes, Linux",
                "resume_url": "https://drive.google.com/file/d/1bob_resume_link/view"
            },
            {
                "username": "carollee",
                "email": "carol.lee@example.com",
                "password": "Carol@123",
                "full_name": "Carol Lee",
                "location": "Bangalore, India",
                "experience": "2 years as a Data Analyst at a SaaS company.",
                "skills": "SQL, Tableau, Python, Excel",
                "resume_url": "https://drive.google.com/file/d/1carol_resume_link/view"
            }
        ]

        for js in jobseekers_data:
            user, created = User.objects.get_or_create(
                username=js["username"],
                defaults={
                    "email": js["email"],
                    "is_employer": False
                }
            )
            if created:
                user.set_password(js["password"])
                user.save()

            profile, _ = Profile.objects.get_or_create(user=user)
            profile.full_name = js["full_name"]
            profile.location = js["location"]
            profile.experience = js["experience"]
            profile.skills = js["skills"]
            profile.resume_url = js["resume_url"]
            profile.save()
