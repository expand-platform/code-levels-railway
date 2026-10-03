from django.test import TestCase
from django.urls import reverse

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

		response = self.client.get(reverse("roadmap"))

		self.assertNotContains(response, empty_track.title)
		self.assertContains(response, skill_only.title)
		self.assertContains(response, "Waiting on projects")
		self.assertNotContains(
			response, reverse("roadmap_by_course", args=[empty_track.slug])
		)
		self.assertContains(
			response, reverse("roadmap_by_course", args=[skill_only.slug])
		)
		self.assertNotContains(response, "Empty Project Course")

		detail = self.client.get(
			reverse("roadmap_by_course", args=[empty_track.slug])
		)
		self.assertEqual(detail.status_code, 404)

		skill_detail = self.client.get(
			reverse("roadmap_by_course", args=[skill_only.slug])
		)
		self.assertEqual(skill_detail.status_code, 200)
		self.assertContains(skill_detail, "Waiting on projects")

		projects_roadmap = self.client.get(
			reverse("projects"), {"view": "roadmap"}
		)
		self.assertNotContains(projects_roadmap, "Empty Project Course")
		self.assertNotContains(projects_roadmap, "Empty Track")


class LanguageCourseTests(TestCase):
	def test_languages_page_and_sidebar_filter_language_courses(self):
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

		languages = self.client.get(reverse("languages"))

		self.assertContains(languages, empty_language.title)
		self.assertContains(languages, "No skills yet.")
		self.assertContains(languages, language_course.title)
		self.assertContains(languages, "Syntax")
		self.assertContains(
			languages, reverse("languages_by_course", args=[language_course.slug])
		)
		self.assertNotContains(
			languages, reverse("languages_by_course", args=[empty_language.slug])
		)
		self.assertContains(
			languages, reverse("projects_by_course", args=[regular_with_skill.slug])
		)

		detail = self.client.get(
			reverse("languages_by_course", args=[language_course.slug])
		)
		self.assertEqual(detail.status_code, 200)
		self.assertContains(detail, "Syntax")

		projects = self.client.get(reverse("projects"))
		self.assertNotContains(projects, "Empty Language")
		self.assertContains(
			projects, reverse("languages_by_course", args=[language_course.slug])
		)

		projects_roadmap = self.client.get(reverse("projects"), {"view": "roadmap"})
		self.assertNotContains(
			projects_roadmap,
			reverse("projects_by_course", args=[language_course.slug]),
		)
		self.assertContains(
			projects_roadmap,
			reverse("languages_by_course", args=[language_course.slug]),
		)
		self.assertContains(
			projects_roadmap,
			reverse("projects_by_course", args=[regular_with_skill.slug]),
		)


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
		self.assertContains(roadmap, 'for="projects-content-projects">Projects</label>')
		self.assertContains(roadmap, "Concepts only")
		self.assertContains(roadmap, "HTML basics")
		self.assertContains(roadmap, "Captain card")
		self.assertNotContains(roadmap, 'data-route="concepts"')

		concepts = self.client.get(
			reverse("projects"), {"view": "roadmap", "content": "concepts"}
		)
		self.assertContains(concepts, "HTML basics")
		self.assertNotContains(concepts, "Captain card")
		self.assertContains(concepts, "Concepts only")
