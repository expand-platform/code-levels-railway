from django.contrib.auth import get_user_model
from django.test import TestCase, override_settings
from django.urls import reverse

from code_levels.settings.features.feature_flags import DASHBOARD, FeatureFlag

from platform_web.models.base.social_media_link import SocialMediaLink
from platform_web.models.base.website_config import WebsiteConfig
from platform_web.models.project.Course import Course, CourseType
from platform_web.models.project.ProgrammingLanguage import ProgrammingLanguage
from platform_web.models.project.Project import Project, ProjectType
from platform_web.models.project.Skill import Skill


class ConceptsPageTests(TestCase):
	def test_page_groups_only_concepts_by_language_and_links_to_details(self):
		language = ProgrammingLanguage.objects.create(name="Django")
		concept = Project.objects.create(
			title="Authentication",
			type=ProjectType.CONCEPT,
			slug="authentication-concept",
		)
		concept.programming_languages.add(language)
		Project.objects.create(
			title="Django project",
			type="project",
			slug="django-project",
		).programming_languages.add(language)

		response = self.client.get(reverse("concepts"))

		self.assertEqual(response.status_code, 200)
		self.assertContains(response, "Django")
		self.assertContains(response, "Authentication")
		self.assertContains(response, reverse("project_details", args=[concept.slug]))
		self.assertNotContains(response, "Django project")

		detail_response = self.client.get(
			reverse("project_details", args=[concept.slug])
		)

		self.assertEqual(detail_response.status_code, 200)
		self.assertContains(detail_response, 'href="/concepts/"')


class JobTrackLayoutTests(TestCase):
	def test_roadmap_hides_courses_without_skills_and_keeps_empty_skill_tracks(self):
		empty_track = Course.objects.create(
			title="Empty Track",
			slug="empty-track",
			type=CourseType.JOB,
		)
		skill_only = Course.objects.create(
			title="Skill Only Track",
			slug="skill-only-track",
			type=CourseType.JOB,
		)
		Skill.objects.create(name="Waiting on projects", related_course=skill_only)
		Course.objects.create(
			title="Empty Project Course",
			slug="empty-project-course",
			type=CourseType.REGULAR,
		)

		response = self.client.get(reverse("job_tracks"))

		self.assertNotContains(response, empty_track.title)
		self.assertContains(response, skill_only.title)
		self.assertContains(response, "Waiting on projects")
		self.assertNotContains(
			response, reverse("job_tracks_by_course", args=[empty_track.slug])
		)
		self.assertContains(
			response, reverse("job_tracks_by_course", args=[skill_only.slug])
		)
		self.assertNotContains(response, "Empty Project Course")

		detail = self.client.get(
			reverse("job_tracks_by_course", args=[empty_track.slug])
		)
		self.assertEqual(detail.status_code, 404)

		skill_detail = self.client.get(
			reverse("job_tracks_by_course", args=[skill_only.slug])
		)
		self.assertEqual(skill_detail.status_code, 200)
		self.assertContains(skill_detail, "Waiting on projects")

		projects_roadmap = self.client.get(
			reverse("projects"), {"view": "roadmap"}
		)
		self.assertNotContains(projects_roadmap, "Empty Project Course")
		self.assertNotContains(projects_roadmap, "Empty Track")


class LanguageCourseTests(TestCase):
	def test_roadmaps_page_and_sidebar_filter_language_courses(self):
		empty_language = Course.objects.create(
			title="Empty Language",
			slug="empty-language",
			type=CourseType.LANGUAGE,
		)
		language_course = Course.objects.create(
			title="Python Language",
			slug="python-language",
			type=CourseType.LANGUAGE,
		)
		Skill.objects.create(name="Syntax", related_course=language_course)
		regular_with_skill = Course.objects.create(
			title="Regular With Skill",
			slug="regular-with-skill",
			type=CourseType.REGULAR,
		)
		Skill.objects.create(name="Unused skill", related_course=regular_with_skill)

		roadmaps = self.client.get(reverse("roadmaps"))

		self.assertContains(roadmaps, empty_language.title)
		self.assertContains(roadmaps, "No skills yet.")
		self.assertContains(roadmaps, language_course.title)
		self.assertContains(roadmaps, "Syntax")
		self.assertContains(
			roadmaps, reverse("roadmaps_by_course", args=[language_course.slug])
		)
		self.assertNotContains(
			roadmaps, reverse("roadmaps_by_course", args=[empty_language.slug])
		)
		self.assertContains(
			roadmaps, reverse("projects_by_course", args=[regular_with_skill.slug])
		)

		detail = self.client.get(
			reverse("roadmaps_by_course", args=[language_course.slug])
		)
		self.assertEqual(detail.status_code, 200)
		self.assertContains(detail, "Syntax")

		projects = self.client.get(reverse("projects"))
		self.assertNotContains(projects, "Empty Language")
		self.assertContains(
			projects, reverse("roadmaps_by_course", args=[language_course.slug])
		)

		projects_roadmap = self.client.get(reverse("projects"), {"view": "roadmap"})
		self.assertNotContains(
			projects_roadmap,
			reverse("projects_by_course", args=[language_course.slug]),
		)
		self.assertContains(
			projects_roadmap,
			reverse("roadmaps_by_course", args=[language_course.slug]),
		)

		old_languages = self.client.get("/languages/")
		self.assertRedirects(old_languages, reverse("roadmaps"), status_code=301, fetch_redirect_response=False)
		self.assertContains(
			projects_roadmap,
			reverse("projects_by_course", args=[regular_with_skill.slug]),
		)


class SkillContentTimelineTests(TestCase):
	def test_content_list_shows_only_when_skill_has_no_projects(self):
		course = Course.objects.create(
			title="Backend Track",
			slug="backend-track",
			type=CourseType.JOB,
		)
		Skill.objects.create(
			name="HTTP",
			related_course=course,
			contents="<ol><li>Requests</li><li>Responses</li></ol>",
		)
		with_projects = Skill.objects.create(
			name="Django",
			related_course=course,
			contents="<ol><li>Hidden outline</li></ol>",
		)
		project = Project.objects.create(
			title="Blog app",
			type=ProjectType.PROJECT,
			slug="blog-app",
			is_active=True,
		)
		with_projects.projects.add(project)

		response = self.client.get(reverse("job_tracks"))

		self.assertContains(response, "Requests")
		self.assertContains(response, "Responses")
		self.assertContains(response, "Blog app")
		self.assertNotContains(response, "Hidden outline")

		regular = Course.objects.create(
			title="Web Basics",
			slug="web-basics",
			type=CourseType.REGULAR,
		)
		Skill.objects.create(
			name="Markup",
			related_course=regular,
			contents="<ol><li>Elements</li></ol>",
		)
		projects_roadmap = self.client.get(reverse("projects"), {"view": "roadmap"})
		self.assertContains(projects_roadmap, "Elements")

		concepts = self.client.get(
			reverse("projects"), {"view": "roadmap", "content": "concepts"}
		)
		self.assertContains(concepts, "Elements")


class ConceptsTimelineTests(TestCase):
	def test_concepts_only_hides_projects_and_sidebar_link(self):
		course = Course.objects.create(
			title="Web Development",
			slug="web-development",
			type=CourseType.REGULAR,
		)
		skill = Skill.objects.create(name="HTML basics", related_course=course)
		project = Project.objects.create(
			title="Captain card",
			type=ProjectType.PROJECT,
			slug="captain-card",
			is_active=True,
		)
		skill.projects.add(project)

		roadmap = self.client.get(reverse("projects"), {"view": "roadmap"})
		self.assertContains(roadmap, "HTML basics")
		self.assertContains(roadmap, "Captain card")
		self.assertNotContains(roadmap, 'data-route="concepts"')

		concepts = self.client.get(
			reverse("projects"), {"view": "roadmap", "content": "concepts"}
		)
		self.assertContains(concepts, "HTML basics")
		self.assertNotContains(concepts, "Captain card")


class CourseAdminProjectTabsTests(TestCase):
	def setUp(self):
		user = get_user_model().objects.create_superuser(
			username="course-admin",
			email="course-admin@example.com",
			password="course-admin-pass",
		)
		self.client.force_login(user)

	def test_project_tabs_render_only_when_that_relation_exists(self):
		course = Course.objects.create(
			title="Django Track",
			slug="django-track",
			type=CourseType.JOB,
		)
		url = reverse("admin:platform_web_course_change", args=[course.pk])
		empty = self.client.get(url)
		self.assertEqual(empty.status_code, 200)
		self.assertNotContains(empty, "Projects by course")
		self.assertNotContains(empty, "Projects by skills")

		owned = Project.objects.create(
			title="Owned project",
			slug="owned-project",
			type=ProjectType.PROJECT,
			course=course,
			course_order=2,
			is_active=False,
		)
		by_course = self.client.get(url)
		self.assertContains(by_course, "Projects by course")
		self.assertContains(by_course, "Owned project")
		self.assertContains(
			by_course,
			reverse("admin:platform_web_project_change", args=[owned.pk]),
		)
		self.assertNotContains(by_course, "Projects by skills")

		library = Course.objects.create(
			title="Library course",
			slug="library-course",
			type=CourseType.REGULAR,
		)
		borrowed = Project.objects.create(
			title="Borrowed project",
			slug="borrowed-project",
			type=ProjectType.PROJECT,
			course=library,
			skill_order=4,
			is_active=True,
		)
		first_skill = Skill.objects.create(
			name="APIs",
			related_course=course,
			order=1,
		)
		second_skill = Skill.objects.create(
			name="Django ORM",
			related_course=course,
			order=0,
		)
		first_skill.projects.add(borrowed)
		second_skill.projects.add(borrowed)
		Skill.objects.create(name="Empty skill", related_course=course, order=2)

		by_both = self.client.get(url)
		self.assertContains(by_both, "Projects by course")
		self.assertContains(by_both, "Projects by skills")
		html = by_both.content.decode()
		course_pane = html.split('id="projects-by-course-tab"', 1)[1].split(
			'id="projects-by-skills-tab"', 1
		)[0]
		skills_pane = html.split('id="projects-by-skills-tab"', 1)[1]
		self.assertIn("Owned project", course_pane)
		self.assertNotIn("Borrowed project", course_pane)
		self.assertIn("Borrowed project", skills_pane)
		self.assertIn("Library course", skills_pane)
		self.assertNotIn("Owned project", skills_pane)
		self.assertNotIn("Empty skill", skills_pane)
		self.assertLess(skills_pane.index("Django ORM"), skills_pane.index("APIs"))
		self.assertEqual(skills_pane.count("Borrowed project"), 2)

		add = self.client.get(reverse("admin:platform_web_course_add"))
		self.assertEqual(add.status_code, 200)
		self.assertNotContains(add, "Projects by course")
		self.assertNotContains(add, "Projects by skills")


class UserDashboardTests(TestCase):
	def setUp(self):
		self.user = get_user_model().objects.create_user(
			username="student",
			password="student-pass",
		)
		self.staff = get_user_model().objects.create_user(
			username="staff",
			password="staff-pass",
			is_staff=True,
		)
		self.project = Project.objects.create(
			title="Build an API",
			type=ProjectType.PROJECT,
			slug="build-an-api",
			description="<p>Ship a small JSON API.</p>",
		)
		Project.objects.create(
			title="HTTP basics",
			type=ProjectType.TOPIC,
			slug="http-basics",
		)
		Project.objects.create(
			title="Auth concept",
			type=ProjectType.CONCEPT,
			slug="auth-concept",
		)
		Project.objects.create(
			title="Hidden project",
			type=ProjectType.PROJECT,
			slug="hidden-project",
			is_active=False,
		)
		config = WebsiteConfig.objects.create(site_name="CodeLevels")
		SocialMediaLink.objects.create(
			website_config=config,
			name="Discord",
			url="https://discord.gg/codelevels",
		)
		SocialMediaLink.objects.create(
			website_config=config,
			name="Telegram",
			url="https://t.me/codelevels",
		)

	def test_anonymous_user_is_sent_to_login(self):
		response = self.client.get(reverse("dashboard"))
		self.assertEqual(response.status_code, 302)
		self.assertIn("/account/login/", response.url)
		self.assertIn("next=/projects/", response.url)

	def test_student_is_forbidden_while_flag_is_off(self):
		self.client.force_login(self.user)
		for name in ("dashboard", "dashboard_payment", "dashboard_chat", "settings"):
			response = self.client.get(reverse(name))
			self.assertEqual(response.status_code, 403)

	@override_settings(FEATURE_FLAGS={})
	def test_student_is_forbidden_when_flag_is_missing(self):
		self.client.force_login(self.user)
		response = self.client.get(reverse("dashboard"))
		self.assertEqual(response.status_code, 403)

	@override_settings(FEATURE_FLAGS={DASHBOARD: FeatureFlag(True)})
	def test_student_can_open_dashboard_when_flag_is_on(self):
		self.client.force_login(self.user)
		response = self.client.get(reverse("dashboard"))
		self.assertEqual(response.status_code, 200)

	def test_index_lists_active_recommendations_and_shell(self):
		self.client.force_login(self.staff)
		response = self.client.get(reverse("dashboard"))

		self.assertEqual(response.status_code, 200)
		self.assertContains(response, "Build an API")
		self.assertContains(response, "Ship a small JSON API.")
		self.assertNotContains(response, "&lt;p&gt;")
		self.assertContains(response, reverse("project_details", args=[self.project.slug]))
		self.assertContains(response, "HTTP basics")
		self.assertContains(response, "Auth concept")
		self.assertNotContains(response, "Hidden project")
		self.assertContains(response, reverse("dashboard_payment"))
		self.assertContains(response, reverse("dashboard_chat"))
		self.assertContains(response, reverse("settings"))
		self.assertContains(response, "https://discord.gg/codelevels")
		self.assertContains(response, "https://t.me/codelevels")
		self.assertContains(response, "user-dash__main")

	def test_slot_pages_require_login_and_keep_the_shell(self):
		for name in ("dashboard_payment", "dashboard_chat", "settings"):
			anonymous = self.client.get(reverse(name))
			self.assertEqual(anonymous.status_code, 302)
			self.assertIn("/account/login/", anonymous.url)
			self.assertIn("next=/projects/", anonymous.url)

		self.client.force_login(self.staff)
		payment = self.client.get(reverse("dashboard_payment"))
		chat = self.client.get(reverse("dashboard_chat"))
		settings = self.client.get(reverse("settings"))

		self.assertContains(payment, "Current plan")
		self.assertContains(chat, "Message the mentor")
		self.assertContains(settings, 'id="username"')
		for page in (payment, chat, settings):
			self.assertContains(page, "user-dash__sidebar")
