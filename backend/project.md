Language:
Python,React(JS) For Website
________________________________________
1. Project Concept
What?
This project is a desktop application that analyzes both AI-generated and manually written code. The system evaluates code quality, compliance with SOLID principles, architectural structure, and basic security risks, and produces a detailed report.
The desktop application provides a VSCode-like interface, and users can select an LLM provider to receive additional explanations and refactoring suggestions.
Why?
AI-generated code does not always fully comply with software engineering principles. This may lead to:
•	Increased technical debt
•	Higher maintenance costs
•	Security vulnerabilities
•	Architectural inconsistencies
This project aims to detect such issues at an early stage and improve overall software quality.
________________________________________
2. Objectives & Scope
The system has three core “Must-Have” features:
1️⃣ Data Retrieval
•	The user selects a project folder through the desktop application.
•	Code files are sent to the backend system for analysis.
2️⃣ Processing
•	Static analysis is performed using Python’s AST module.
•	Rule-based checks are applied for SOLID principles.
•	Architectural dependencies are analyzed.
•	Potential security risks are identified.
•	The selected LLM provider generates explanations and refactoring suggestions.
3️⃣ Visualization
Analysis results are displayed in the desktop application with:
•	Severity level (Low / Medium / High)
•	Category (SOLID / Architecture / Security)
•	Explanation and improvement suggestions
Relevant lines in the code editor are highlighted.
________________________________________
3. Technical Stack (The “Pythonic” Way)
Environment
•	Python Virtual Environment (venv)
•	Dependency management with requirements.txt
Backend
•	FastAPI
•	MongoDB
•	Python AST module
Desktop Application
•	PySide6
•	Editor component with syntax highlighting
Web Interface
•	React (User registration/login and application download)
Core Libraries
•	AST (Code analysis)
•	Requests (API calls)
•	SQLAlchemy (ORM)
Testing
•	Pytest (Basic unit testing)
________________________________________
4. System Logic (Flow)
Input
•	The user selects a project folder.
•	Optionally, the user enters an LLM provider and API key.
Process
•	The code is converted into an AST structure.
•	Rule-based analysis is applied.
•	Findings are categorized.
•	Problematic code blocks are sent to the LLM.
•	Explanations and refactoring suggestions are generated.
Output
•	The analysis report is displayed in the desktop interface.
•	Results are stored in the database.
•	The report can optionally be exported.
________________________________________
5. Implementation Roadmap
Phase	Milestone	Key Python Tasks
Week 1	Project Architecture Design	System design, database schema planning, backend & desktop communication structure setup
Week 2	Static Analysis Engine	Implement AST-based parser, develop SOLID and architecture rule checks
Week 3	LLM & Backend Integration	Integrate FastAPI endpoints, implement LLM provider selection and API communication
Week 4	Desktop Interface & Testing	Develop VSCode-like UI components, integrate analysis results display, perform testing and refinements
________________________________________
6. Challenges & Learning Goals
Concurrency
Learning to use threading or asynchronous programming for long-running analysis tasks.
Static Code Analysis
Developing a deeper understanding of structural code analysis using AST.
LLM Integration
Understanding different LLM provider APIs and implementing secure API key management.
Code Quality
Ensuring the code follows PEP 8 standards and applies modular design principles.

