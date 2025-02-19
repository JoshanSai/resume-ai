from typing import Type, Optional, List
from langchain_core.callbacks import CallbackManagerForToolRun
from langchain_core.tools import BaseTool
from pydantic import BaseModel, Field

from resume_builder import Resume


class PersonalInformationSchema(BaseModel):
    name: str = Field(description="Full name of the user.")
    email: str = Field(description="Email of the user.")
    phone: str = Field(description="Mobile number of the user.")
    linkedin: str = Field(description="LinkedIn profile URL of the user.")


class PersonalInformation(BaseTool):
    name: str = "AddPersonalInformation"
    description: str = "Use this tool when to add personal information of the user in the resume."
    args_schema: Type[BaseModel] = PersonalInformationSchema
    return_direct: bool = False
    resume: Resume = None

    def _run(self, name: str, email: str, phone: str, linkedin: str,
             run_manager: Optional[CallbackManagerForToolRun] = None):
        self.resume.resume_data["personal_section"] = {"name": name, "email": email, "phone": phone, "linkedin": linkedin}
        return {"output": "Successfully added personal information"}


# Schema and Tool for Professional Summary
class ProfessionalSummarySchema(BaseModel):
    summary: str = Field(description="Brief professional summary of the user.")


class ProfessionalSummaryTool(BaseTool):
    name: str = "AddProfessionalSummary"
    description: str = "Tool to capture the professional summary of the user."
    args_schema: Type[BaseModel] = ProfessionalSummarySchema
    return_direct: bool = False
    resume: Resume = None

    def _run(self, summary: str, run_manager: Optional[CallbackManagerForToolRun] = None):
        self.resume.resume_data["summary_section"] = {"summary": summary}
        return {"output": "Successfully added professional summary."}


# Schema and Tool for Work Experience
class ExperienceSchema(BaseModel):
    job_title: str = Field(description="Job title of the user.")
    company: str = Field(description="Company name.")
    date_range: str = Field(description="Time period of employment in a single string, example: '2022 Jan - 2023 Jan'.")
    responsibilities: List[str] = Field(description="List of job responsibilities.")


class ExperienceTool(BaseTool):
    name: str = "AddExperience"
    description: str = "Tool to capture work experience details."
    args_schema: Type[BaseModel] = ExperienceSchema
    return_direct: bool = False
    resume: Resume = None

    def _run(self, job_title: str, company: str, date_range: str, responsibilities: List[str],
             run_manager: Optional[CallbackManagerForToolRun] = None):
        existing_data = self.resume.resume_data["experience_section"]
        existing_data.append({"job_title": job_title,
                              "company": company,
                              "date_range": date_range,
                              "responsibilities": responsibilities})
        self.resume.resume_data["experience_section"] = existing_data
        return {"output": "Successfully added experience."}


# Schema and Tool for Education
class EducationSchema(BaseModel):
    degree: str = Field(description="Degree obtained.")
    school: str = Field(description="Name of the educational institution.")
    graduation_year: str = Field(description="Year of graduation, example: '2022'")


class EducationTool(BaseTool):
    name: str = "AddEducation"
    description: str = "Tool to capture Latest education details."
    args_schema: Type[BaseModel] = EducationSchema
    return_direct: bool = False
    resume: Resume = None

    def _run(self, degree: str, school: str, graduation_year: str,
             run_manager: Optional[CallbackManagerForToolRun] = None):
        self.resume.resume_data["education_section"] = {"degree": degree,
                                                        "school": school,
                                                        "graduation_year": graduation_year}
        return {"output": "Successfully added education."}


# Schema and Tool for Skills
class SkillsSchema(BaseModel):
    skills: List[str] = Field(description="List of professional skills.")


class SkillsTool(BaseTool):
    name: str = "AddSkills"
    description: str = "Tool to capture user skills."
    args_schema: Type[BaseModel] = SkillsSchema
    return_direct: bool = False
    resume: Resume = None

    def _run(self, skills: List[str], run_manager: Optional[CallbackManagerForToolRun] = None):
        self.resume.resume_data["skills_section"] = skills
        return {"output": "Successfully added skills."}


# Schema and Tool for Projects
class ProjectsSchema(BaseModel):
    title: str = Field(description="Project title.")
    description: str = Field(description="Brief description of the project.")


class ProjectsTool(BaseTool):
    name: str = "AddProjects"
    description: str = "Tool to capture project details."
    args_schema: Type[BaseModel] = ProjectsSchema
    return_direct: bool = False
    resume: Resume = None

    def _run(self, title: str, description: str, run_manager: Optional[CallbackManagerForToolRun] = None):
        existing_data = self.resume.resume_data["projects_section"]
        existing_data.append({"title": title,
                              "description": description
                              })
        self.resume.resume_data["projects_section"] = existing_data
        return {"output": "Successfully added projects."}
