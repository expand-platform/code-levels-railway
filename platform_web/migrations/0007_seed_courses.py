
from django.db import migrations

def seed_courses(apps, schema_editor):
	Course = apps.get_model("platform_web", "Course")
	# List of (value, display) tuples from COURSE_CHOICES
	course_choices = [
		("Web Development", "Web Development"),
		("Desktop Applications", "Desktop Applications"),
		("Mobile Applications", "Mobile Applications"),
		("Telegram Bots", "Telegram Bots"),
		("Data Science", "Data Science"),
		("Security", "Security"),
		("HTML & CSS", "HTML & CSS Fundamentals"),
		("JavaScript Basics", "JavaScript Basics"),
		("Advanced JavaScript", "Advanced JavaScript"),
		("Vue.js Crash Course", "Vue.js Crash Course"),
		("React for Beginners", "React for Beginners"),
		("APIs with FastAPI", "APIs with FastAPI"),
		("Django Essentials", "Django Essentials"),
		("Python for Web Development", "Python for Web Development"),
		("Database Design & SQL", "Database Design & SQL"),
		("Testing & Debugging", "Testing & Debugging"),
		("Deployment & DevOps", "Deployment & DevOps"),
		("Version Control with Git", "Version Control with Git"),
		("UI/UX Design Principles", "UI/UX Design Principles"),
		("Backend Development with Node.js", "Backend Development with Node.js"),
		("Full Stack Web Development", "Full Stack Web Development"),
	]
	for order, (value, display) in enumerate(course_choices, start=1):
		Course.objects.get_or_create(title=value, defaults={"order": order, "description": display})

def unseed_courses(apps, schema_editor):
	Course = apps.get_model("platform_web", "Course")
	titles = [
		"Web Development",
		"Desktop Applications",
		"Mobile Applications",
		"Telegram Bots",
		"Data Science",
		"Security",
		"HTML & CSS",
		"JavaScript Basics",
		"Advanced JavaScript",
		"Vue.js Crash Course",
		"React for Beginners",
		"APIs with FastAPI",
		"Django Essentials",
		"Python for Web Development",
		"Database Design & SQL",
		"Testing & Debugging",
		"Deployment & DevOps",
		"Version Control with Git",
		"UI/UX Design Principles",
		"Backend Development with Node.js",
		"Full Stack Web Development",
	]
	Course.objects.filter(title__in=titles).delete()

class Migration(migrations.Migration):
	dependencies = [
		("platform_web", "0006_seed_stages"),
	]

	operations = [
		migrations.RunPython(seed_courses, unseed_courses),
	]
