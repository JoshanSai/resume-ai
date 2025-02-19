from jinja2 import Template

# Sample data
data = {
    "name": "John Doe",
    "email": "johndoe@example.com",
    "phone": "123-456-7890",
    "linkedin": "linkedin.com/in/johndoe",
    "summary": "Experienced software engineer specializing in backend development.",
    "experiences": [
        {
            "job_title": "Senior Software Engineer",
            "company": "TechCorp",
            "date_range": "Jan 2021 - Present",
            "responsibilities": [
                "Developed scalable backend services.",
                "Led a team of 5 engineers to improve performance by 30%."
            ]
        }
    ],
    "education_list": [
        {
            "degree": "B.S. in Computer Science",
            "school": "University of Tech",
            "graduation_year": "2020"
        }
    ],
    "skills": ["Python", "Kubernetes", "Docker", "Machine Learning"],
    "projects": [
        {
            "title": "AI Resume Builder",
            "description": "Created a Python-based AI tool to dynamically generate resumes."
        }
    ]
}

# Load the HTML template
with open("resume_template.html", "r") as file:
    template_content = file.read()

# Render the template
template = Template(template_content)
rendered_html = template.render(data)

# Save the rendered HTML
with open("output_resume.html", "w") as output_file:
    output_file.write(rendered_html)
