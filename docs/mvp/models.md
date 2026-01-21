# MVP models
- User
- Project (1 project = 1 skill)
- Part (1 project = many parts (part 1, part 2 etc)) (1 project = 1 skill)
- - Practice (theory)
- - Milestone (checkpoint)
- Milestone (1 project = multiple key milestones aka checkpoints (code quality assurance))
- Submission (submitted tasks)
- Review (for submitted tasks)
- Skill (skills aquired during progress)

# Long-term
- Sertificates (few skill(s) acquired - can pass atestation now)

## User
- id (pk)
- username (str)
- first_name (str)
- surname (str)
- isPaid (bool)
- plan (predefined list)
- last_active (datetime)
- is_online (bool)
- active_project (id, progress etc)
- parts (passed by user)
- projects (passed)


# Part(s)
- id (pk)
- title
- description / content
- order (influences the URL, too - part-1, part-2 or step-1, step-2)
- project (one related project)
- user(s) - multiple users can be here
- - activeFor user (user who stepped into this task - for progress & measuring)
- - submittedBy user (user who submitted this task)


## Project
- id (pk)
- user(s) - who signed up for this project
- title 
- description (for the Dashboard)
- image (from uploads)
- icon (just a class - str - for icon)
- order (int)

Relations with models:
- programming languages (predefined select, multiple options) -> multiselect with predefined values, never change, filled programmatically
- Difficulty -> Difficulty model with predefined values (easy, moderate, hard), could be change / added / removed via admin panel
- stages (list of predefined key development stages like markup, JS logic, server development, database, hosting, testing etc) -> Stage model, because could be changed any time
- skills (for the Dashboard) -> Skill model with id, name
- parts (?) -> Part model, one project, many parts -> parts of the project (1, 2, 3 etc)