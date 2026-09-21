# 🤖 Resume AI

An AI-powered conversational resume builder that lets users **create and update their resume through natural language**.

Instead of filling out a traditional resume form, users can simply talk to an AI agent. The agent understands the user's information and uses structured tools to populate different sections of the resume.

The application is built with **FastAPI, LangChain, Azure OpenAI, Redis, Pydantic, and Jinja2**.

## ✨ Features

* 💬 **Conversational Resume Building**

  * Build a resume by chatting with an AI agent.
  * Users can provide information naturally instead of filling out forms.

* 🧠 **LLM-powered Agent**

  * Uses an Azure OpenAI chat model with LangChain's agent framework.
  * The agent decides which resume-building tool should be used based on the user's request.

* 🧩 **Structured Resume Tools**

  * Personal information
  * Professional summary
  * Work experience
  * Education
  * Skills
  * Projects

* 💾 **Conversation Memory**

  * Uses Redis to store chat history.
  * Conversations are associated with a `session_id`.
  * The agent retains the most recent 10 messages for a session.

* 📝 **Structured Resume Data**

  * Resume information is maintained as structured Python data.
  * The API returns both the AI response and the current resume data.

* 🎨 **HTML Resume Template**

  * Includes an HTML/Jinja2 resume template that can be populated with the generated resume data.

---

## 🏗️ Architecture

```text
                    ┌─────────────────────┐
                    │       Client        │
                    │  Web / Mobile App   │
                    └──────────┬──────────┘
                               │
                               │ POST /talk-to-agent
                               ▼
                    ┌─────────────────────┐
                    │      FastAPI        │
                    │       main.py       │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │   LangChain Agent   │
                    │      agent.py       │
                    └──────┬───────┬──────┘
                           │       │
              ┌────────────┘       └─────────────┐
              ▼                                  ▼
     ┌──────────────────┐              ┌──────────────────┐
     │   Azure OpenAI   │              │      Redis       │
     │      GPT-4o      │              │ Conversation     │
     │                  │              │     Memory       │
     └──────────────────┘              └──────────────────┘
              │
              ▼
     ┌──────────────────────────────┐
     │       Resume Tools           │
     │                              │
     │ Personal Information         │
     │ Professional Summary         │
     │ Experience                   │
     │ Education                    │
     │ Skills                       │
     │ Projects                     │
     └──────────────┬───────────────┘
                    │
                    ▼
          ┌──────────────────┐
          │   Resume Object  │
          │  Structured Data │
          └────────┬─────────┘
                   │
                   ▼
          ┌──────────────────┐
          │ Jinja2 HTML      │
          │ Resume Template  │
          └──────────────────┘
```

---

## 🧠 How It Works

The application exposes a single API endpoint:

```http
POST /talk-to-agent
```

The request contains:

```json
{
  "session_id": "user-123",
  "query": "I worked at Google as a software engineer from 2022 to 2024"
}
```

The request is passed to the LangChain agent.

The agent:

1. Receives the user's message.
2. Uses the conversation history associated with the `session_id`.
3. Determines what resume information is being provided.
4. Selects the appropriate tool.
5. Updates the structured resume object.
6. Generates a natural-language response.
7. Returns the response along with the current resume data.

For example:

```text
User:
I worked at Google as a Software Engineer from 2022 to 2024.
I built scalable backend services using Python.

        ↓

LangChain Agent

        ↓

AddExperience Tool

        ↓

Resume Data

{
  "job_title": "Software Engineer",
  "company": "Google",
  "date_range": "2022 - 2024",
  "responsibilities": [
    "Built scalable backend services using Python"
  ]
}
```

---

## 🧰 Technology Stack

| Technology       | Purpose                   |
| ---------------- | ------------------------- |
| **Python**       | Application language      |
| **FastAPI**      | REST API                  |
| **Pydantic**     | Request/schema validation |
| **LangChain**    | Agent orchestration       |
| **Azure OpenAI** | LLM powering the agent    |
| **Redis**        | Conversation history      |
| **Jinja2**       | HTML resume templating    |
| **HTML/CSS**     | Resume presentation       |

---

## 📁 Project Structure

```text
resume-ai/
│
├── agent.py
├── main.py
├── resume_builder.py
├── resume_template.html
├── tools.py
├── test.py
├── .gitignore
└── README.md
```

### `main.py`

The FastAPI application entry point.

It:

* Creates the FastAPI application.
* Configures CORS.
* Defines the request model.
* Exposes the `/talk-to-agent` endpoint.

The endpoint accepts a `session_id` and `query`, then forwards the request to the AI agent.

### `agent.py`

Contains the main AI-agent implementation.

It:

* Loads environment variables.
* Initializes Azure OpenAI.
* Creates the resume object.
* Registers the resume tools.
* Connects Redis chat history.
* Creates the LangChain agent.
* Executes the user's request.
* Returns the AI response and structured resume data.

### `tools.py`

Contains the structured tools available to the AI agent.

The current tools include:

```text
AddPersonalInformation
AddProfessionalSummary
AddExperience
AddEducation
AddSkills
AddProjects
```

Each tool has a Pydantic schema describing the information it accepts. This allows the LLM to produce structured tool arguments rather than directly manipulating the resume object.

### `resume_builder.py`

Contains the `Resume` class and the initial resume data structure.

The resume contains:

```python
{
    "personal_section": {},
    "summary_section": {},
    "experience_section": [],
    "education_section": {},
    "skills_section": [],
    "projects_section": []
}
```

### `resume_template.html`

Contains the HTML/CSS template used to render the resume. It is designed to be populated using template data.

### `test.py`

Contains an example of rendering the HTML resume template using Jinja2 and sample resume data.

---

# 🚀 Getting Started

## Prerequisites

Make sure you have the following installed:

* Python 3.9+
* Redis
* An Azure OpenAI resource
* An Azure OpenAI deployment

---

## 1. Clone the Repository

```bash
git clone https://github.com/JoshanSai/resume-ai.git
cd resume-ai
```

## 2. Create a Virtual Environment

### Using `venv`

```bash
python -m venv venv
```

Activate it on Windows:

```bash
venv\Scripts\activate
```

On macOS/Linux:

```bash
source venv/bin/activate
```

---

## 3. Install Dependencies

Install the required packages:

```bash
pip install fastapi uvicorn pydantic python-dotenv redis jinja2 langchain langchain-community langchain-openai
```

---

## 4. Configure Environment Variables

Create a `.env` file in the project root:

```env
AZURE_ENDPOINT=your_azure_openai_endpoint
AZURE_API_KEY=your_azure_openai_api_key
REDIS_URL=redis://localhost:6379
```

### Environment Variables

| Variable         | Description           |
| ---------------- | --------------------- |
| `AZURE_ENDPOINT` | Azure OpenAI endpoint |
| `AZURE_API_KEY`  | Azure OpenAI API key  |
| `REDIS_URL`      | Redis connection URL  |

The agent currently uses an Azure OpenAI deployment named:

```text
gpt-4o
```

and API version:

```text
2023-07-01-preview
```

These values are configured directly in `agent.py`.

> **Note:** If your Azure deployment has a different name, update `deployment_name` in `agent.py`.

---

# 🗄️ Redis

Redis is used for conversational memory.

The application creates a Redis-backed chat history using the supplied `session_id`.

For example:

```text
session_id = "user-123"
```

allows multiple requests from the same user/session to share conversation history.

The application currently keeps a window of the most recent **10 messages** in LangChain memory.

### Running Redis Locally

If Redis is installed locally:

```bash
redis-server
```

The default connection is:

```text
redis://localhost:6379
```

---

# ▶️ Running the Application

Start the FastAPI server:

```bash
uvicorn main:app --reload
```

The API will be available at:

```text
http://localhost:8000
```

FastAPI's interactive API documentation will also be available at:

```text
http://localhost:8000/docs
```

---

# 📡 API Reference

## `POST /talk-to-agent`

Send a message to the resume AI agent.

### Request

```json
{
  "session_id": "user-123",
  "query": "My name is John Doe and I am a software engineer."
}
```

### Response

The API returns:

```json
{
  "response": "I've added your personal information to the resume.",
  "resume_data": {
    "personal_section": {
      "name": "John Doe",
      "email": "...",
      "phone": "...",
      "linkedin": "..."
    },
    "summary_section": {},
    "experience_section": [],
    "education_section": {},
    "skills_section": [],
    "projects_section": []
  }
}
```

The exact `resume_data` depends on the information collected during the conversation.

---

# 💬 Example Conversation

### 1. Personal Information

```text
User:
My name is John Doe. My email is john@example.com
and my LinkedIn is linkedin.com/in/johndoe.
```

The agent can use:

```text
AddPersonalInformation
```

---

### 2. Professional Summary

```text
User:
I am a backend engineer specializing in Python,
FastAPI and distributed systems.
```

The agent can use:

```text
AddProfessionalSummary
```

---

### 3. Work Experience

```text
User:
I worked at Acme Corp as a Software Engineer
from January 2022 to December 2024.
I built scalable backend services.
```

The agent can use:

```text
AddExperience
```

---

### 4. Skills

```text
User:
My skills are Python, FastAPI, Docker,
Kubernetes and AWS.
```

The agent can use:

```text
AddSkills
```

---

### 5. Projects

```text
User:
Add a project called AI Resume Builder.
It is an AI-powered application that generates resumes.
```

The agent can use:

```text
AddProjects
```

---

# 🔧 Tool Architecture

The project uses LangChain tools to separate **LLM reasoning** from **resume state management**.

Each tool exposes a structured schema.

For example, the experience tool expects:

```python
{
    "job_title": "...",
    "company": "...",
    "date_range": "...",
    "responsibilities": [...]
}
```

The tool then adds the structured information to:

```python
resume.resume_data["experience_section"]
```

This architecture makes it possible for the LLM to interact with the resume through well-defined operations rather than directly modifying arbitrary application state.

---

# 📝 Resume Data Model

The current resume structure is:

```text
Resume
│
├── personal_section
│   ├── name
│   ├── email
│   ├── phone
│   └── linkedin
│
├── summary_section
│   └── summary
│
├── experience_section[]
│   ├── job_title
│   ├── company
│   ├── date_range
│   └── responsibilities[]
│
├── education_section
│   ├── degree
│   ├── school
│   └── graduation_year
│
├── skills_section[]
│
└── projects_section[]
    ├── title
    └── description
```

---

# 🔄 Request Lifecycle

```text
Client
  │
  │ POST /talk-to-agent
  ▼
FastAPI
  │
  ▼
talkToAgent()
  │
  ├───────────────► Redis
  │                  │
  │                  └── Conversation History
  │
  ▼
Azure OpenAI
  │
  ▼
LangChain Agent
  │
  ├── AddPersonalInformation
  ├── AddProfessionalSummary
  ├── AddExperience
  ├── AddEducation
  ├── AddSkills
  └── AddProjects
  │
  ▼
Resume Object
  │
  ▼
Structured Resume Data
  │
  ▼
API Response
```

---

# 🎨 Rendering a Resume

The repository also contains an HTML resume template that can be rendered using Jinja2.

The general workflow is:

```text
Resume Data
     │
     ▼
Jinja2 Template
     │
     ▼
resume_template.html
     │
     ▼
Rendered HTML
```

A basic example:

```python
from jinja2 import Template

with open("resume_template.html", "r") as file:
    template_content = file.read()

template = Template(template_content)

rendered_html = template.render(data)

with open("output_resume.html", "w") as output_file:
    output_file.write(rendered_html)
```

The repository's `test.py` demonstrates this template-rendering approach with sample resume data.

---

# 🔐 Security Considerations

Before deploying this application publicly, consider:

* Restricting CORS instead of allowing all origins.
* Storing API keys exclusively in environment variables or a secrets manager.
* Adding authentication and authorization.
* Validating and sanitizing user-provided resume content.
* Securing the Redis instance with authentication and network restrictions.
* Avoiding verbose agent logs in production.
* Adding rate limiting to the API.
* Using HTTPS in production.

The current FastAPI configuration allows requests from all origins, so the CORS configuration should be tightened for production deployments.

---

# 🚧 Future Improvements

Potential improvements include:

* [ ] Add a frontend chat interface.
* [ ] Generate PDF resumes.
* [ ] Support multiple resume templates.
* [ ] Add resume editing/deletion tools.
* [ ] Add authentication.
* [ ] Persist completed resumes in a database.
* [ ] Add resume versioning.
* [ ] Add job-description analysis.
* [ ] Add ATS optimization.
* [ ] Allow users to upload an existing resume.
* [ ] Generate tailored resumes for specific job descriptions.
* [ ] Add streaming AI responses.
* [ ] Add automated tests for all resume tools.
* [ ] Containerize the application with Docker.
* [ ] Add production deployment configuration.

---

# 🤝 Contributing

Contributions are welcome.

1. Fork the repository.
2. Create a feature branch:

```bash
git checkout -b feature/my-feature
```

3. Make your changes.
4. Commit your changes:

```bash
git commit -m "Add my feature"
```

5. Push the branch:

```bash
git push origin feature/my-feature
```

6. Open a Pull Request.

---

# 📄 License

No license is currently specified for this repository.

If you intend to make the project open source, consider adding an appropriate `LICENSE` file.

---

## ⭐ Project

Built with:

**Python · FastAPI · LangChain · Azure OpenAI · Redis · Jinja2**

Repository: [github.com/JoshanSai/resume-ai](https://github.com/JoshanSai/resume-ai?utm_source=chatgpt.com)
