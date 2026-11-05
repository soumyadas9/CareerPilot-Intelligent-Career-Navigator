import re
import time
from collections import Counter
from datetime import date, timedelta
import pandas as pd
import streamlit as st


# ---------------------------------------------------------------------
# PAGE CONFIGURATION AND BRAND SYSTEM
# ---------------------------------------------------------------------
st.set_page_config(
    page_title="CareerPilot | Intelligent Career Navigator",
    page_icon="🧭",
    layout="wide",
    initial_sidebar_state="collapsed",
)

st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700;800&family=Manrope:wght@500;600;700;800&display=swap');

    :root {
        --ink: #172554;
        --muted: #64748B;
        --brand: #4F46E5;
        --brand-dark: #3730A3;
        --cyan: #0891B2;
        --surface: #FFFFFF;
        --line: #E2E8F0;
        --canvas: #F8FAFC;
        --soft: #EEF2FF;
    }

    html, body, [class*="css"] {
        font-family: 'DM Sans', sans-serif;
    }
    

  .stApp {
        background:
            radial-gradient(circle at 12% 10%, rgba(99, 102, 241, 0.15), transparent 35rem),
            radial-gradient(circle at 92% 15%, rgba(8, 145, 178, 0.12), transparent 30rem),
            #F8FAFC !important;
        color: #0F172A;
    }

    [data-testid="stHeader"] {
        background: rgba(248,250,252,.82);
    }

    [data-testid="stSidebar"] {
        background: #FFFFFF;
        border-right: 1px solid #E2E8F0;
    }

    [data-testid="stMetric"] {
        background: #FFFFFF;
        border: 1px solid #E2E8F0;
        border-radius: 16px;
        padding: 17px 18px;
        box-shadow: 0 5px 18px rgba(15,23,42,.045);
    }

    [data-testid="stMetricLabel"] {
        color: #64748B;
        font-weight: 600;
    }

    [data-testid="stMetricValue"] {
        color: #1E3A8A;
        font-family: 'Manrope', sans-serif;
        font-weight: 800;
    }

    div[data-testid="stVerticalBlockBorderWrapper"] {
        border-color: #E2E8F0 !important;
        border-radius: 16px !important;
        box-shadow: 0 4px 14px rgba(15,23,42,.035);
        background: rgba(255,255,255,.88);
    }

    .hero {
        padding: 34px 36px;
        border-radius: 22px;
        color: #FFFFFF !important;
        background: linear-gradient(135deg, #1E1B4B 0%, #2E2A87 45%, #3730A3 70%, #0E7490 100%) !important;
        box-shadow: 0 16px 40px rgba(49, 46, 129, 0.22);
        margin-bottom: 26px;
        border: 1px solid rgba(255, 255, 255, 0.08);
    }

    /* Force all child fonts inside the hero to remain high-contrast crisp white */
    .hero h1, .hero p, .hero div, .hero span, .hero-kicker {
        color: #FFFFFF !important;
        -webkit-text-fill-color: #FFFFFF !important;
    }

    .hero-kicker {
        color: #C7D2FE !important;
        -webkit-text-fill-color: #C7D2FE !important;
        text-transform: uppercase;
        letter-spacing: .14em;
        font-size: .75rem;
        font-weight: 800;
        margin-bottom: 10px;
    }

    .hero h1 {
        font-family: 'Manrope', sans-serif;
        color: white;
        font-size: clamp(2rem, 4vw, 3rem);
        line-height: 1.12;
        margin: 0 0 10px 0;
        font-weight: 800;
    }
    .hero p {
            color: #E0E7FF !important;
            -webkit-text-fill-color: #E0E7FF !important;
            opacity: 0.95;
        }

    .section-eyebrow {
        color: #4F46E5;
        font-weight: 800;
        letter-spacing: .12em;
        text-transform: uppercase;
        font-size: .68rem;
    }

    .job-company {
        color: #64748B;
        font-size: .88rem;
        font-weight: 600;
    }

    .score-pill {
        display: inline-block;
        padding: 6px 11px;
        border-radius: 999px;
        background: #EEF2FF;
        color: #3730A3;
        font-weight: 800;
        font-size: .85rem;
    }

    .tag {
        display: inline-block;
        background: #F1F5F9;
        color: #334155;
        border: 1px solid #E2E8F0;
        border-radius: 999px;
        padding: 4px 9px;
        margin: 3px 4px 3px 0;
        font-size: .76rem;
        font-weight: 600;
    }

    .success-note {
        border-left: 4px solid #10B981;
        background: #ECFDF5;
        padding: 12px 14px;
        border-radius: 9px;
        color: #065F46;
        margin: 8px 0;
    }

    .info-note {
        border-left: 4px solid #6366F1;
        background: #EEF2FF;
        padding: 12px 14px;
        border-radius: 9px;
        color: #312E81;
        margin: 8px 0;
    }

    .phase-heading {
        font-family: 'Manrope', sans-serif;
        font-weight: 800;
        color: #1E293B;
        font-size: 1.1rem;
        padding-bottom: 8px;
        border-bottom: 1px solid #E2E8F0;
        margin-bottom: 12px;
    }


/* --------------------------------------------------
   GLOBAL TEXT COLOUR FIX
-------------------------------------------------- */

.stApp,
.stApp p,
.stApp label,
.stApp li,
.stApp span,
.stApp div {
    color: #0F172A;
}

/* Keep muted descriptions readable */
.stApp small,
.stCaption,
[data-testid="stCaptionContainer"] p {
    color: #64748B !important;
}

/* Input fields */
[data-baseweb="input"] input,
[data-baseweb="textarea"] textarea,
.stTextInput input,
.stTextArea textarea {
    background-color: #FFFFFF !important;
    color: #0F172A !important;
    -webkit-text-fill-color: #0F172A !important;
    border-color: #CBD5E1 !important;
    caret-color: #0F172A !important;
}

/* Placeholder text */
[data-baseweb="input"] input::placeholder,
[data-baseweb="textarea"] textarea::placeholder {
    color: #94A3B8 !important;
    -webkit-text-fill-color: #94A3B8 !important;
    opacity: 1 !important;
}

/* Dropdowns and multiselects */
[data-baseweb="select"] > div {
    background-color: #FFFFFF !important;
    color: #0F172A !important;
    border-color: #CBD5E1 !important;
}

[data-baseweb="select"] input {
    color: #0F172A !important;
    -webkit-text-fill-color: #0F172A !important;
}

[data-baseweb="select"] span {
    color: #0F172A !important;
}

/* Dropdown menus */
[data-baseweb="popover"],
[data-baseweb="menu"],
[role="listbox"] {
    background-color: #FFFFFF !important;
    color: #0F172A !important;
}

[role="option"] {
    color: #0F172A !important;
    background-color: #FFFFFF !important;
}

[role="option"]:hover {
    background-color: #FEE2E2 !important;
    color: #991B1B !important;
}

/* Checkbox and radio labels */
[data-testid="stCheckbox"] label,
[data-testid="stRadio"] label {
    color: #0F172A !important;
}

/* --------------------------------------------------
   BUTTON DESIGN
   Default: black text on white
   Hover / click: red
-------------------------------------------------- */

div.stButton > button {
    background: #FFFFFF !important;
    color: #111827 !important;
    border: 1px solid #CBD5E1 !important;
    border-radius: 11px !important;
    font-weight: 700 !important;
    transition: all .18s ease !important;
}

/* Primary buttons also start with dark text */
div.stButton > button[kind="primary"] {
    background: #EEF2FF !important;
    color: #111827 !important;
    border: 1px solid #C7D2FE !important;
}

/* Red on hover */
div.stButton > button:hover,
div.stButton > button[kind="primary"]:hover {
    background: #DC2626 !important;
    color: #FFFFFF !important;
    border-color: #B91C1C !important;
    transform: translateY(-1px);
    box-shadow: 0 5px 14px rgba(220, 38, 38, .20);
}

/* Red while clicking */
div.stButton > button:active,
div.stButton > button[kind="primary"]:active {
    background: #991B1B !important;
    color: #FFFFFF !important;
    border-color: #991B1B !important;
    transform: translateY(0);
}

/* Keyboard focus */
div.stButton > button:focus-visible {
    outline: 3px solid rgba(220, 38, 38, .35) !important;
    outline-offset: 3px !important;
}

/* --------------------------------------------------
   TABS
-------------------------------------------------- */

div[data-baseweb="tab-list"] {
    gap: 8px;
    border-bottom: 1px solid #E2E8F0;
}

button[data-baseweb="tab"] {
    background: transparent !important;
    border: none !important;
    color: #64748B !important;
    font-weight: 600 !important;
    padding: 10px 16px !important;
     transition: color 0.2s ease, border-color 0.2s ease !important;
}

button[data-baseweb="tab"] p {
    color: inherit !important;
}

button[data-baseweb="tab"][aria-selected="true"] {
    color: #DC2626 !important;
    border-bottom: 3px solid #DC2626 !important;
    font-weight: 700 !important;
}

button[data-baseweb="tab"]:hover {
    color: #DC2626 !important;
}


    div[data-baseweb="tab-list"] {
        gap: 8px;
    }

    button[data-baseweb="tab"] {
        border-radius: 10px 10px 0 0;
        font-weight: 700;
    }

    .footer {
        color: #94A3B8;
        font-size: .78rem;
        text-align: center;
        padding: 28px 0 10px 0;
    }

    #MainMenu, footer {
        visibility: hidden;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


# ---------------------------------------------------------------------
# DEMO AUTHENTICATION
# ---------------------------------------------------------------------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    st.markdown("<div style='height:7vh'></div>", unsafe_allow_html=True)
    left, center, right = st.columns([1, 1.15, 1])
    with center:
        st.markdown(
            """
            <div class="hero" style="text-align:center; padding:30px 24px;">
                <div class="hero-kicker">INTELLIGENT CAREER NAVIGATOR</div>
                <h1 style="font-size:2.25rem;">Your next move,<br>made clearer.</h1>
                <p style="margin:0 auto;">A smarter way to discover roles, understand your fit, and build a career action plan.</p>
            </div>
            """,
            unsafe_allow_html=True,
        )
        with st.container(border=True):
            st.markdown("### 🔐 Welcome to CareerPilot")
            st.caption("Sign in to open your personalized career workspace.")
            username = st.text_input("Username", placeholder="Enter demo username")
            password = st.text_input("Password", type="password", placeholder="Enter demo password")
            st.info("Demo access: username `admin` · password `password123`")
            if st.button("🔓 Authenticate & Enter Portal", type="primary", use_container_width=True):
                if username.strip() == "admin" and password == "password123":
                    st.session_state.logged_in = True
                    st.rerun()
                else:
                    st.error("Those credentials do not match. Please use the demo credentials shown above.")
    st.stop()


# ---------------------------------------------------------------------
# DATA: SYNTHETIC DEMO JOBS
# ---------------------------------------------------------------------
MASTER_SKILLS = [
    "Python", "SQL", "Excel", "Power BI", "Tableau", "Data Analysis",
    "Data Visualization", "Statistics", "A/B Testing", "Product Strategy",
    "Product Management", "User Research", "Figma", "UI/UX", "Wireframing",
    "Prototyping", "Agile", "Jira", "User Stories", "Requirements Gathering",
    "Stakeholder Management", "Market Research", "Competitive Analysis",
    "Communication", "Presentation", "JavaScript", "React", "TypeScript",
    "HTML", "CSS", "Node.js", "REST APIs", "Git", "Machine Learning",
    "Generative AI", "Prompt Engineering", "Automation", "Documentation",
    "Problem Solving", "Customer Success", "CRM", "Growth Marketing",
    "SEO", "Experimentation", "Business Analysis", "Flask", "Pandas",
]

JOBS = [
    {
        "id": "J001", "title": "Associate Product Manager Intern", "company": "Northstar Labs",
        "location": "Mumbai", "type": "Internship", "experience": "Student / Fresher",
        "skills": ["Product Strategy", "User Research", "SQL", "Agile", "Communication", "Data Analysis"],
        "interests": ["Product Management", "AI", "Consumer Technology"],
        "description": "Support discovery, prioritization, product experiments, and cross-functional execution for a B2B SaaS product.",
        "responsibilities": ["Translate user problems into clear product requirements", "Track adoption and product metrics", "Coordinate with design and engineering"],
        "topics": ["Product sense and prioritization", "Metrics and funnels", "User stories and acceptance criteria", "SQL fundamentals", "Stakeholder communication"],
    },
    {
        "id": "J002", "title": "Business Analyst Intern", "company": "BluePeak Systems",
        "location": "Pune", "type": "Internship", "experience": "Student / Fresher",
        "skills": ["Excel", "SQL", "Requirements Gathering", "Documentation", "Business Analysis", "Communication"],
        "interests": ["Business Analysis", "Enterprise Software", "Data Analysis"],
        "description": "Work with business teams to document workflows, analyze operational data, and support solution delivery.",
        "responsibilities": ["Document As-Is and To-Be workflows", "Prepare user stories and acceptance criteria", "Support UAT and stakeholder reviews"],
        "topics": ["Requirement elicitation", "Process mapping", "BRD versus FRD", "UAT scenarios", "SQL and Excel case questions"],
    },
    {
        "id": "J003", "title": "Product Analyst – Graduate", "company": "MetricMint",
        "location": "Remote", "type": "Full-time", "experience": "0–1 years",
        "skills": ["SQL", "Excel", "Data Analysis", "A/B Testing", "Product Management", "Data Visualization"],
        "interests": ["Product Analytics", "Data Analysis", "Consumer Technology"],
        "description": "Help product teams understand user behavior through funnel analysis, experiments, and actionable insights.",
        "responsibilities": ["Analyze activation and retention funnels", "Build recurring performance reports", "Communicate insights to product managers"],
        "topics": ["SQL joins and aggregations", "North-star metrics", "Funnels and retention", "A/B testing", "Insight storytelling"],
    },
    {
        "id": "J004", "title": "Frontend Developer Intern", "company": "PixelForge",
        "location": "Mumbai", "type": "Internship", "experience": "Student / Fresher",
        "skills": ["JavaScript", "React", "TypeScript", "HTML", "CSS", "REST APIs", "Git"],
        "interests": ["Frontend Development", "Design Systems", "Web Applications"],
        "description": "Build accessible product interfaces and collaborate with designers and backend engineers.",
        "responsibilities": ["Develop reusable React components", "Integrate REST APIs", "Test responsive UI behavior"],
        "topics": ["JavaScript fundamentals", "React state and props", "API integration", "Responsive layouts", "Debugging approach"],
    },
    {
        "id": "J005", "title": "AI Product Operations Intern", "company": "Orbit AI",
        "location": "Hyderabad", "type": "Internship", "experience": "Student / Fresher",
        "skills": ["Generative AI", "Prompt Engineering", "Automation", "Documentation", "Product Management", "Python"],
        "interests": ["AI", "Product Operations", "Automation"],
        "description": "Improve AI product workflows through prompt evaluation, operational analysis, and structured feedback loops.",
        "responsibilities": ["Evaluate AI workflow outputs", "Document product issues and edge cases", "Coordinate experiments and release feedback"],
        "topics": ["LLM capabilities and limitations", "Prompt evaluation", "AI product metrics", "Human-in-the-loop workflows", "Operational prioritization"],
    },
    {
        "id": "J006", "title": "Data Analyst Trainee", "company": "FinEdge",
        "location": "Pune", "type": "Full-time", "experience": "0–1 years",
        "skills": ["Python", "SQL", "Excel", "Pandas", "Statistics", "Power BI"],
        "interests": ["Data Analysis", "FinTech", "Business Intelligence"],
        "description": "Transform business data into reliable reports and insights for financial services teams.",
        "responsibilities": ["Clean and validate datasets", "Write SQL queries", "Build dashboards and summarize trends"],
        "topics": ["SQL query writing", "Data cleaning", "Descriptive statistics", "Dashboard interpretation", "Business case analysis"],
    },
    {
        "id": "J007", "title": "UX Research Intern", "company": "Humanly",
        "location": "Mumbai", "type": "Internship", "experience": "Student / Fresher",
        "skills": ["User Research", "Figma", "UI/UX", "Wireframing", "Prototyping", "Presentation"],
        "interests": ["UX Research", "Design", "Consumer Technology"],
        "description": "Help the design team understand user needs and turn research findings into product improvements.",
        "responsibilities": ["Plan user interviews and usability tests", "Synthesize qualitative feedback", "Share findings with designers and PMs"],
        "topics": ["Research planning", "Interview bias", "Usability testing", "Affinity mapping", "Turning insights into design decisions"],
    },
    {
        "id": "J008", "title": "Implementation Analyst", "company": "CloudSpring",
        "location": "Hyderabad", "type": "Full-time", "experience": "0–1 years",
        "skills": ["Requirements Gathering", "SQL", "Documentation", "Customer Success", "REST APIs", "Communication"],
        "interests": ["Enterprise Software", "Implementation", "Business Analysis"],
        "description": "Support customer onboarding, configuration, requirements clarification, and implementation quality.",
        "responsibilities": ["Understand customer workflows", "Coordinate configuration and issue resolution", "Maintain implementation documentation"],
        "topics": ["Client discovery", "API basics", "Issue triage", "Scope management", "Clear documentation"],
    },
    {
        "id": "J009", "title": "Growth Product Intern", "company": "Looply",
        "location": "Remote", "type": "Internship", "experience": "Student / Fresher",
        "skills": ["A/B Testing", "Growth Marketing", "Product Strategy", "Data Analysis", "SEO", "Experimentation"],
        "interests": ["Growth", "Product Management", "Consumer Technology"],
        "description": "Identify activation and retention opportunities through experimentation and user behavior analysis.",
        "responsibilities": ["Analyze acquisition and activation funnels", "Propose growth experiments", "Measure experiment outcomes"],
        "topics": ["AARRR funnel", "Activation metrics", "Experiment design", "Retention levers", "Prioritization"],
    },
    {
        "id": "J010", "title": "Junior Software Engineer", "company": "StackWorks",
        "location": "Pune", "type": "Full-time", "experience": "0–1 years",
        "skills": ["Python", "JavaScript", "REST APIs", "Git", "Problem Solving", "SQL"],
        "interests": ["Software Engineering", "Backend Development", "AI"],
        "description": "Contribute to API development, debugging, testing, and engineering delivery in a product team.",
        "responsibilities": ["Implement and test API features", "Debug application issues", "Collaborate through code reviews"],
        "topics": ["Programming fundamentals", "REST API design", "SQL basics", "Debugging", "Data structures"],
    },
]


# ---------------------------------------------------------------------
# SEMANTIC-STYLE RELATEDNESS MAP
# Transparent heuristic mappings, not an external AI model.
# ---------------------------------------------------------------------
RELATED_SKILLS = {
    "python": {"data analysis", "pandas", "automation", "machine learning"},
    "pandas": {"python", "data analysis", "data visualization"},
    "sql": {"data analysis", "business analysis", "product analytics"},
    "excel": {"data analysis", "business analysis", "data visualization"},
    "power bi": {"data visualization", "data analysis", "tableau"},
    "tableau": {"data visualization", "data analysis", "power bi"},
    "figma": {"ui/ux", "wireframing", "prototyping", "user research"},
    "ui/ux": {"figma", "wireframing", "prototyping", "user research"},
    "wireframing": {"figma", "ui/ux", "prototyping"},
    "prototyping": {"figma", "ui/ux", "wireframing"},
    "user research": {"ui/ux", "product management", "market research"},
    "product management": {"product strategy", "user research", "agile", "product analytics"},
    "product strategy": {"product management", "market research", "competitive analysis"},
    "javascript": {"react", "typescript", "html", "css"},
    "react": {"javascript", "typescript", "html", "css"},
    "typescript": {"javascript", "react"},
    "rest apis": {"node.js", "python", "implementation", "backend development"},
    "generative ai": {"prompt engineering", "python", "automation"},
    "prompt engineering": {"generative ai", "automation"},
    "a/b testing": {"experimentation", "statistics", "data analysis", "growth marketing"},
    "experimentation": {"a/b testing", "data analysis", "growth marketing"},
    "growth marketing": {"seo", "experimentation", "a/b testing"},
    "requirements gathering": {"business analysis", "documentation", "user stories"},
    "business analysis": {"requirements gathering", "sql", "documentation"},
    "communication": {"presentation", "stakeholder management", "customer success"},
    "presentation": {"communication", "data visualization"},
    "machine learning": {"python", "data analysis", "statistics"},
}


def normalize(value):
    return re.sub(r"\s+", " ", str(value).strip().lower())


def semantic_relatedness(candidate_terms, job_terms):
    candidate_normalized = {normalize(item) for item in candidate_terms}
    job_normalized = {normalize(item) for item in job_terms}
    direct = candidate_normalized.intersection(job_normalized)
    related_pairs = []
    for candidate_term in candidate_normalized:
        related = RELATED_SKILLS.get(candidate_term, set())
        for job_term in job_normalized:
            if job_term in related:
                related_pairs.append((candidate_term, job_term))
    return direct, related_pairs


def calculate_match(candidate, job):
    candidate_skills = candidate["skills"]
    job_skills = job["skills"]
    direct_skills, related_skill_pairs = semantic_relatedness(candidate_skills, job_skills)

    direct_interests, related_interest_pairs = semantic_relatedness(
        candidate["interests"], job["interests"]
    )

    skill_score = (len(direct_skills) / max(len(job_skills), 1)) * 55
    interest_score = min(20, len(direct_interests) * 7 + len(related_interest_pairs) * 3)
    experience_score = 15 if candidate["experience"] in ("Student / Fresher", "0–1 years") and job["experience"] in ("Student / Fresher", "0–1 years") else 7
    location_match = candidate["location"] == "Any location" or job["location"] == "Remote" or candidate["location"] == job["location"]
    location_score = 10 if location_match else 0

    semantic_pair_count = len(related_skill_pairs) + len(related_interest_pairs)
    semantic_bonus = min(15, semantic_pair_count * 3)
    if semantic_pair_count > 0:
        semantic_bonus = max(8, semantic_bonus)

    baseline = skill_score + interest_score + experience_score + location_score
    location_floor = 12 if location_match else 0
    total = min(100, max(baseline, location_floor) + semantic_bonus)

    matched_skills = sorted(direct_skills)
    missing_skills = sorted({normalize(skill) for skill in job_skills} - direct_skills)
    related_explanations = [f"{source.title()} ↔ {target.title()}" for source, target in related_skill_pairs]

    return {
        "score": round(total),
        "baseline": round(baseline),
        "semantic_bonus": round(semantic_bonus),
        "skill_score": round(skill_score),
        "interest_score": round(interest_score),
        "experience_score": round(experience_score),
        "location_score": round(location_score),
        "location_match": location_match,
        "matched_skills": matched_skills,
        "missing_skills": missing_skills,
        "related_explanations": related_explanations,
        "direct_interest_matches": sorted(direct_interests),
    }


def make_interview_cheat_sheet(candidate, job, result):
    missing = result["missing_skills"]
    title = job["title"].lower()
    if "product" in title or "growth" in title:
        framing = (
            "Anchor your answers in how you identify user problems, prioritize opportunities, "
            "define success metrics, and work with design and engineering. Use a project example "
            "to show structured product thinking rather than presenting yourself as someone who "
            "already knows every tool."
        )
        missing_advice = (
            "For gaps such as SQL or experimentation, be candid about your current level. "
            "Connect your existing analytical work to the same problem-solving process, explain "
            "what you can already do, and describe the specific query or experiment you are learning "
            "to build next."
        )
    elif "analyst" in title:
        framing = (
            "Structure answers as: business question → information gathered → analysis or workflow "
            "mapped → recommendation → measurable outcome. Emphasize clear documentation, careful "
            "assumptions, and stakeholder communication."
        )
        missing_advice = (
            "For gaps in SQL, Excel, or formal requirements methods, connect adjacent experience "
            "such as data cleaning, project logic, user interviews, or documentation. Explain how "
            "you would validate requirements and test the result instead of overstating tool fluency."
        )
    elif "ux" in title:
        framing = (
            "Walk the interviewer through a user-centered process: research question, participant "
            "selection, observation, synthesis, design implication, and validation. Explain what "
            "you learned from users and how it changed a design decision."
        )
        missing_advice = (
            "If a research method or design tool is unfamiliar, explain the closest method you have "
            "used and how you would learn the missing technique. Show that you can separate user "
            "evidence from assumptions."
        )
    elif "frontend" in title or "software" in title:
        framing = (
            "Use a concrete build or debugging example. Explain the requirement, your implementation "
            "choices, how data moved through the system, how you tested it, and what you would improve."
        )
        missing_advice = (
            "For technologies you have not used deeply, distinguish fundamentals from production "
            "experience. Explain the related concepts you understand, how you would read the existing "
            "codebase, and how you would verify a small change."
        )
    elif "ai" in title:
        framing = (
            "Discuss the user or operational problem before the model. Cover input quality, prompt or "
            "workflow design, evaluation, failure handling, human review, and the metric that would "
            "show whether the AI feature is useful."
        )
        missing_advice = (
            "For gaps in Python, automation, or prompt evaluation, relate your current project work "
            "to structured testing and iteration. Be specific about what you have personally built "
            "and what you would need to validate before deployment."
        )
    else:
        framing = (
            "Use a concise STAR structure and keep the focus on the problem, your individual action, "
            "the trade-off you considered, and the result."
        )
        missing_advice = (
            "Treat missing skills as a learning plan: explain the closest transferable skill, your "
            "current level, and one practical step you would take to close the gap."
        )

    missing_text = ", ".join(missing[:5]) if missing else "No direct skill gaps in the listed requirements"
    matched_text = ", ".join(skill.title() for skill in result["matched_skills"][:6]) or "transferable project experience"
    return {
        "opening": f"For **{job['title']} at {job['company']}**, position yourself around {matched_text}.",
        "framing": framing,
        "gap": f"Your listed gaps: **{missing_text}**. {missing_advice}",
        "proof": f"Prepare one detailed example that demonstrates {', '.join(job['skills'][:3])}. Explain your own contribution and the outcome.",
    }


def build_candidate_roadmap(candidate, top_jobs):
    frequent_gaps = Counter()
    for job, result in top_jobs[:3]:
        frequent_gaps.update(result["missing_skills"])
    priority_gaps = [skill.title() for skill, _ in frequent_gaps.most_common(4)]
    if not priority_gaps:
        priority_gaps = ["SQL", "Product Metrics", "Interview Storytelling"]

    phase_one = [
        ("road_1", f"Review fundamentals for {priority_gaps[0]}", "Complete one focused tutorial and write a short summary."),
        ("road_2", f"Practice {priority_gaps[1] if len(priority_gaps) > 1 else 'role-specific fundamentals'}", "Solve two practical exercises and note what you found difficult."),
        ("road_3", "Study role-specific interview concepts", "Review the recurring topics shown in the interview preparation panels."),
    ]
    phase_two = [
        ("road_4", "Build a small proof-of-skill project", "Create a compact artifact that demonstrates one priority skill."),
        ("road_5", "Document the project as a case study", "Write the problem, approach, decisions, result, and next iteration."),
        ("road_6", "Tailor one application and rehearse answers", "Map your strongest evidence to the role requirements and practice aloud."),
    ]
    return phase_one, phase_two, priority_gaps


# ---------------------------------------------------------------------
# SESSION STATE DEFAULTS
# ---------------------------------------------------------------------
defaults = {
    "candidate_name": "Soumya",
    "education": "B.Tech / Undergraduate Graduate",
    "experience": "Student / Fresher",
    "location": "Mumbai",
    "interests": ["Product Management", "AI", "Data Analysis"],
    "skills": ["Python", "SQL", "Figma", "UI/UX", "React", "Data Analysis"],
    "opportunity_types": ["Internship", "Full-time"],
    "workspace": "Build Candidate Profile",
    "profile_saved": False,
    "resume_text": "",
    "resume_scan_message": "",
    "weekly_hours": 8,
    "verification_checked": False,
}
if "interview_mode" not in st.session_state:
    st.session_state.interview_mode = None

if "interview_job_id" not in st.session_state:
    st.session_state.interview_job_id = None
for key, value in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = value


# ---------------------------------------------------------------------
# SIDEBAR: IDENTITY AND PLATFORM STATUS ONLY
# ---------------------------------------------------------------------
with st.sidebar:
    st.markdown("## 🧭 CareerPilot")
    st.caption("Your career navigation workspace")

    st.divider()

    st.markdown("### 👤 Candidate")
    st.markdown(f"**{st.session_state.candidate_name or 'Candidate'}**")
    st.caption(st.session_state.education)

    st.markdown(
        f"<span class='tag'>{st.session_state.experience}</span>",
        unsafe_allow_html=True,
    )

    st.divider()
    st.markdown("### Platform status")
    st.success("Demo environment active")
    st.caption("Synthetic job dataset")
    st.caption("Rule-based matching engine")

    st.divider()

    if st.button("Log out", use_container_width=True):
        st.session_state.logged_in = False
        st.rerun()


# ---------------------------------------------------------------------
# WORKSPACE NAVIGATION
# ---------------------------------------------------------------------
st.markdown(
    """
    <div class="hero">
        <div class="hero-kicker">CAREERPILOT · INTELLIGENT CAREER NAVIGATOR</div>
        <h1>Your career, with a clearer direction.</h1>
        <p>Build your candidate profile, discover relevant opportunities,
        identify skill gaps, and create a practical plan to become
        application-ready.</p>
    </div>
    """,
    unsafe_allow_html=True,
)

workspace = st.radio(
    "Choose your workspace",
    ["Build Candidate Profile", "Explore Personalized Dashboard"],
    horizontal=True,
    key="workspace",
)

st.divider()


# ---------------------------------------------------------------------
# WORKSPACE 1: CANDIDATE PROFILE BUILDER
# ---------------------------------------------------------------------
if workspace == "Build Candidate Profile":

    st.markdown("### 👤 Build your candidate profile")
    st.caption(
        "Tell CareerPilot about your education, experience, skills, "
        "and career preferences. Your dashboard will use this information "
        "to calculate role-fit indicators."
    )

    profile_left, profile_right = st.columns([1.1, 0.9], gap="large")

    with profile_left:
        with st.container(border=True):
            st.markdown("#### 1. Basic information")

            st.text_input(
                "Your name",
                key="candidate_name",
                placeholder="Enter your name",
            )

            st.selectbox(
                "Education",
                [
                    "B.Tech / Undergraduate Graduate",
                    "B.E. / B.Sc. Graduate",
                    "Postgraduate",
                    "Diploma",
                    "Other",
                ],
                key="education",
            )

            st.selectbox(
                "Experience level",
                [
                    "Student / Fresher",
                    "0–1 years",
                    "1–2 years",
                    "2+ years",
                ],
                key="experience",
            )

            st.selectbox(
                "Preferred location",
                [
                    "Mumbai",
                    "Pune",
                    "Hyderabad",
                    "Remote",
                    "Any location",
                ],
                key="location",
            )

        with st.container(border=True):
            st.markdown("#### 2. Skills and capabilities")

            st.multiselect(
                "Your current skills",
                options=MASTER_SKILLS,
                key="skills",
                help="Select skills you can genuinely demonstrate.",
            )

            st.caption(
                "Tip: Include technical skills, analytical capabilities, "
                "product skills, and tools you have used in projects or internships."
            )

        with st.container(border=True):
            st.markdown("#### 3. Career preferences")

            st.multiselect(
                "Career interests",
                options=[
                    "Product Management",
                    "Product Analytics",
                    "Data Analysis",
                    "AI",
                    "Business Analysis",
                    "UX Research",
                    "Design",
                    "Frontend Development",
                    "Backend Development",
                    "Enterprise Software",
                    "FinTech",
                    "Consumer Technology",
                    "Growth",
                    "Automation",
                    "Product Operations",
                    "Software Engineering",
                    "Implementation",
                ],
                key="interests",
            )

            st.multiselect(
                "What opportunities are you open to?",
                ["Internship", "Full-time"],
                key="opportunity_types",
            )

    with profile_right:

        with st.container(border=True):
            st.markdown("#### 📄 Resume skill scanner")
            st.caption(
                "Paste your resume or LinkedIn profile text. "
                "CareerPilot will identify matching skills from its "
                "master skill library."
            )

            st.text_area(
                "Resume / LinkedIn text",
                key="resume_text",
                height=245,
                placeholder=(
                    "Soumya Das\n"
                    "B.Tech Information Technology | 2026 Graduate\n"
                    "Skills: Python, SQL, React, Figma, UI/UX, Data Analysis\n"
                    "Experience: Software Development Intern\n"
                    "Projects: AI Study Manager, Smart Timetable Generator\n"
                    "Interests: Product Management, AI, Analytics"
                ),
            )

            if st.button(
                "🔍 Scan Resume & Extract Skills",
                type="primary",
                use_container_width=True,
            ):
                resume_text = st.session_state.resume_text

                if not resume_text.strip():
                    st.warning("Paste your resume text before scanning.")
                else:
                    with st.spinner("Analysing resume keywords..."):
                        time.sleep(1.2)

                        resume_lower = normalize(resume_text)

                        detected = [
                            skill
                            for skill in MASTER_SKILLS
                            if re.search(
                                r"(?<![a-z0-9])"
                                + re.escape(skill.lower())
                                + r"(?![a-z0-9])",
                                resume_lower,
                            )
                        ]

                        if detected:
                            st.session_state.skills = detected
                            st.session_state.resume_scan_message = (
                                f"Detected {len(detected)} skills: "
                                + ", ".join(detected)
                            )
                            st.toast("Resume scan completed!", icon="✅")
                            st.rerun()
                        else:
                            st.session_state.resume_scan_message = (
                                "No exact skill keywords were detected. "
                                "You can still select skills manually."
                            )

            if st.session_state.resume_scan_message:
                st.success(st.session_state.resume_scan_message)

            st.caption(
                "This prototype uses keyword matching against MASTER_SKILLS. "
                "It does not use an external AI model or parse uploaded PDFs."
            )

        with st.container(border=True):
            st.markdown("#### Profile completeness")

            completion_checks = [
                bool(st.session_state.candidate_name.strip()),
                bool(st.session_state.education),
                bool(st.session_state.experience),
                bool(st.session_state.location),
                bool(st.session_state.skills),
                bool(st.session_state.interests),
                bool(st.session_state.opportunity_types),
            ]

            completeness = sum(completion_checks) / len(completion_checks)

            st.progress(completeness)
            st.metric(
                "Profile completion",
                f"{round(completeness * 100)}%",
            )

            st.caption(
                "A more complete profile helps produce more useful "
                "recommendations in this demo."
            )

    st.divider()

    # ---------------------------------------------------------------
    # SAVE PROFILE AND NAVIGATE TO DASHBOARD
    # ---------------------------------------------------------------

    def go_to_dashboard():
        if not st.session_state.candidate_name.strip():
            st.session_state.profile_error = "Please enter your name before continuing."
            return

        if not st.session_state.skills:
            st.session_state.profile_error = "Please add at least one skill to your profile."
            return

        st.session_state.profile_error = ""
        st.session_state.profile_saved = True
        st.session_state.workspace = "Explore Personalized Dashboard"

    st.button(
        "Save Profile & Explore My Dashboard →",
        type="primary",
        use_container_width=True,
        on_click=go_to_dashboard,
    )

    if st.session_state.get("profile_error"):
        st.error(st.session_state.profile_error)


# ------------------------------------------
# PAGE 2: EXPLORE PERSONALIZED DASHBOARD
# ------------------------------------------

elif workspace == "Explore Personalized Dashboard":

    if not st.session_state.profile_saved:
        st.info(
            "You can explore the dashboard now, but save your candidate "
            "profile first for more meaningful recommendations."
        )

    # ---------------------------------------------------------------
    # BUILD CURRENT CANDIDATE AND MATCH RESULTS
    # ---------------------------------------------------------------
    candidate = {
        "name": st.session_state.candidate_name,
        "education": st.session_state.education,
        "experience": st.session_state.experience,
        "location": st.session_state.location,
        "skills": st.session_state.skills,
        "interests": st.session_state.interests,
        "opportunity_types": st.session_state.opportunity_types,
    }

    filtered_jobs = [
        job for job in JOBS
        if (
            not candidate["opportunity_types"]
            or job["type"] in candidate["opportunity_types"]
        )
    ]

    ranked_jobs = []

    for job in filtered_jobs:
        result = calculate_match(candidate, job)
        ranked_jobs.append((job, result))

    ranked_jobs.sort(
        key=lambda item: item[1]["score"],
        reverse=True,
    )

    top_match_score = (
        ranked_jobs[0][1]["score"] if ranked_jobs else 0
    )

    average_score = (
        round(
            sum(result["score"] for _, result in ranked_jobs)
            / len(ranked_jobs)
        )
        if ranked_jobs else 0
    )

    strong_matches = sum(
        1 for _, result in ranked_jobs
        if result["score"] >= 70
    )

    # ---------------------------------------------------------------
    # DASHBOARD OVERVIEW
    # ---------------------------------------------------------------
    st.markdown(
        f"### Welcome back, {candidate['name'] or 'Candidate'}!"
    )

    st.caption(
        "Here is your current career-fit overview based on your "
        "candidate profile."
    )

    metric_a, metric_b, metric_c, metric_d = st.columns(4)

    metric_a.metric("Roles analysed", len(ranked_jobs))
    metric_b.metric("Top match score", f"{top_match_score}%")
    metric_c.metric("Strong matches", strong_matches)
    metric_d.metric("Average fit score", f"{average_score}%")

    st.markdown(
        """
        <div class="info-note">
            <b>Important: Match-score transparency.</b>
            These scores are prototype fit indicators, not probabilities
            of getting hired. They are calculated using direct skill overlap,
            related-skill rules, interests, experience, and location.
            Related-skill bonuses are heuristic rules, not outputs from
            a trained machine-learning model. All displayed jobs are
            synthetic demo records, not live vacancies.
        </div>
        """,
        unsafe_allow_html=True,
    )

    # ---------------------------------------------------------------
    # DASHBOARD TABS
    # ---------------------------------------------------------------
    tab_matches, tab_gaps, tab_roadmap, tab_verification = st.tabs(
        [
            "🎯 Job Matches",
            "🧩 Skill Gap Analysis",
            "🗺️ Learning Roadmap",
            "🔎 Job Verification",
        ]
    )

    # ---------------------------------------------------------------
    # TAB 1: JOB MATCHES
    # ---------------------------------------------------------------
    with tab_matches:

        st.markdown("### Roles ranked around your profile")
        st.caption(
            "Expand a role to understand its fit score, skill overlap, "
            "related-skill signals, and interview preparation resources."
        )

        if not ranked_jobs:
            st.warning(
                "Select at least one opportunity type in your profile "
                "to see role recommendations."
            )

        else:
            for job, result in ranked_jobs:

                with st.expander(
                    f"{job['title']} · {job['company']} · "
                    f"{result['score']}% fit",
                    expanded=(job == ranked_jobs[0][0]),
                ):

                    title_col, score_col = st.columns([4, 1])

                    with title_col:
                        st.markdown(f"#### {job['title']}")
                        st.markdown(
                            f"<div class='job-company'>"
                            f"{job['company']} · {job['location']} · "
                            f"{job['type']}</div>",
                            unsafe_allow_html=True,
                        )

                    with score_col:
                        st.markdown(
                            f"<div class='score-pill'>"
                            f"{result['score']}% MATCH</div>",
                            unsafe_allow_html=True,
                        )

                    st.write(job["description"])
                    st.progress(result["score"] / 100)

                    score_cols = st.columns(4)

                    score_cols[0].metric(
                        "Skill overlap",
                        f"{result['skill_score']}/55",
                    )
                    score_cols[1].metric(
                        "Interest fit",
                        f"{result['interest_score']}/20",
                    )
                    score_cols[2].metric(
                        "Experience",
                        f"{result['experience_score']}/15",
                    )
                    score_cols[3].metric(
                        "Location",
                        f"{result['location_score']}/10",
                    )

                    st.markdown("**Skills you already list**")

                    if result["matched_skills"]:
                        st.markdown(
                            "".join(
                                f"<span class='tag'>{skill.title()}</span>"
                                for skill in result["matched_skills"]
                            ),
                            unsafe_allow_html=True,
                        )
                    else:
                        st.caption(
                            "No exact skill-name overlap yet. "
                            "Review the related-skill signals below."
                        )

                    st.markdown("**Related-skill signals**")

                    if result["related_explanations"]:
                        st.write(
                            " · ".join(result["related_explanations"])
                        )
                        st.caption(
                            f"Rule-based related-skill bonus: "
                            f"+{result['semantic_bonus']} points"
                        )
                    else:
                        st.caption(
                            "No related-skill signal detected for this role."
                        )

                    st.markdown("**Skills to strengthen**")

                    if result["missing_skills"]:
                        st.write(
                            ", ".join(
                                skill.title()
                                for skill in result["missing_skills"]
                            )
                        )
                    else:
                        st.success(
                            "Your listed skills cover all skills "
                            "in this demo role profile."
                        )

                    with st.expander("Role responsibilities"):
                        for responsibility in job["responsibilities"]:
                            st.markdown(f"- {responsibility}")

                    st.divider()



                    # ---------------------------------------------------
                    # JOB-SPECIFIC INTERVIEW PREPARATION
                    # ---------------------------------------------------

                    action_col, prep_col = st.columns(2)

                    with action_col:
                        if st.button(
                            "✨ Generate Interview Cheat Sheet",
                            key=f"cheat_{job['id']}",
                            type="primary",
                            use_container_width=True,
                        ):
                            if (
                                st.session_state.interview_job_id == job["id"]
                                and st.session_state.interview_mode == "cheat"
                            ):
                                # Close if already open
                                st.session_state.interview_mode = None
                                st.session_state.interview_job_id = None
                            else:
                                # Open this job's cheat sheet
                                st.session_state.interview_job_id = job["id"]
                                st.session_state.interview_mode = "cheat"

                    with prep_col:
                        if st.button(
                            "🎤 Interview Practice",
                            key=f"prep_{job['id']}",
                            use_container_width=True,
                        ):
                            if (
                                st.session_state.interview_job_id == job["id"]
                                and st.session_state.interview_mode == "practice"
                            ):
                                # Close if already open
                                st.session_state.interview_mode = None
                                st.session_state.interview_job_id = None
                            else:
                                # Open this job's interview practice
                                st.session_state.interview_job_id = job["id"]
                                st.session_state.interview_mode = "practice"

                    # ---------------------------------------------------
                    # CHEAT SHEET
                    # ---------------------------------------------------

                    if (
                        st.session_state.interview_job_id == job["id"]
                        and st.session_state.interview_mode == "cheat"
                    ):
                        with st.container(border=True):

                            st.markdown("### ✨ Your interview cheat sheet")

                            with st.spinner("Building role-specific talking points..."):
                                time.sleep(0.5)

                                cheat = make_interview_cheat_sheet(
                                    candidate,
                                    job,
                                    result,
                                )

                            st.markdown(cheat["opening"])

                            st.markdown("**How to position your experience**")
                            st.write(cheat["framing"])

                            st.markdown("**How to address missing skills**")
                            st.write(cheat["gap"])

                            st.markdown("**Proof point to prepare**")
                            st.write(cheat["proof"])

                            st.caption(
                                "Generated from your current profile and "
                                "this specific synthetic role description. "
                                "This is a rule-based preparation aid, "
                                "not a live generative AI service."
                            )

                    # ---------------------------------------------------
                    # INTERVIEW PRACTICE
                    # ---------------------------------------------------

                    elif (
                        st.session_state.interview_job_id == job["id"]
                        and st.session_state.interview_mode == "practice"
                    ):
                        with st.container(border=True):

                            st.markdown("### 🎤 Interview preparation")

                            st.markdown("**Topics to revise for this role**")

                            for topic in job["topics"]:
                                st.markdown(f"- {topic}")

                            st.markdown("**Representative practice questions**")

                            practice_questions = [
                                (
                                    f"Walk me through a project that best "
                                    f"demonstrates your fit for a "
                                    f"{job['title']} role."
                                ),
                                (
                                    f"How would you approach a real business "
                                    f"or user problem relevant to "
                                    f"{job['company']}?"
                                ),
                                (
                                    "Which skill in this role description "
                                    "would you strengthen first, and how?"
                                ),
                            ]

                            for index, question in enumerate(
                                practice_questions,
                                start=1,
                            ):
                                st.markdown(f"{index}. {question}")

                            st.caption(
                                "These are representative role-based "
                                "practice prompts, not verified historical "
                                "interview questions."
                            )

                    st.divider()

    # ---------------------------------------------------------------
    # TAB 2: SKILL GAP ANALYSIS
    # ---------------------------------------------------------------
    with tab_gaps:

        st.markdown("### Your highest-value skill gaps")
        st.caption(
            "These gaps are calculated from your three highest-ranked roles. "
            "The market-value estimates below are illustrative simulations, "
            "not guaranteed salary increases."
        )

        if ranked_jobs:

            gap_counter = Counter()

            for job, result in ranked_jobs[:3]:
                gap_counter.update(result["missing_skills"])

            simulated_market_values = {
                "sql": 45000,
                "python": 50000,
                "data analysis": 40000,
                "excel": 25000,
                "power bi": 35000,
                "product management": 60000,
                "product strategy": 55000,
                "a/b testing": 40000,
                "figma": 30000,
                "react": 45000,
                "javascript": 40000,
                "generative ai": 65000,
                "prompt engineering": 45000,
                "business analysis": 40000,
                "requirements gathering": 35000,
                "communication": 30000,
                "statistics": 35000,
                "pandas": 35000,
            }

            if gap_counter:

                gap_rows = []

                for skill, count in gap_counter.most_common(10):

                    estimated_value = simulated_market_values.get(
                        normalize(skill),
                        30000,
                    )

                    gap_rows.append(
                        {
                            "Skill to strengthen": skill.title(),
                            "Occurrences in top 3 roles": count,
                            "Illustrative annual market-value signal": (
                                f"₹{estimated_value:,}"
                            ),
                        }
                    )

                gap_df = pd.DataFrame(gap_rows)

                st.dataframe(
                    gap_df,
                    use_container_width=True,
                    hide_index=True,
                )

                top_gap = gap_counter.most_common(1)[0][0]
                top_gap_value = simulated_market_values.get(
                    normalize(top_gap),
                    30000,
                )

                value_col, frequency_col = st.columns(2)

                value_col.metric(
                    "Top priority skill",
                    top_gap.title(),
                )

                frequency_col.metric(
                    "Illustrative market-value signal",
                    f"₹{top_gap_value:,}",
                    help=(
                        "Simulated annual value indicator for the "
                        "prototype. Not a salary prediction."
                    ),
                )

                st.markdown("#### Role-by-role breakdown")

                for job, result in ranked_jobs[:3]:

                    with st.container(border=True):

                        st.markdown(
                            f"**{job['title']} · "
                            f"{result['score']}% fit**"
                        )

                        if result["missing_skills"]:
                            st.write(
                                ", ".join(
                                    skill.title()
                                    for skill in result["missing_skills"]
                                )
                            )
                        else:
                            st.success(
                                "No listed skill gaps for this role."
                            )

                st.caption(
                    "Market-value signals are simulated demonstration "
                    "metrics. They are not sourced from salary surveys, "
                    "job postings, or compensation databases."
                )

            else:
                st.success(
                    "No skill gaps were found in the top three roles."
                )

        else:
            st.info(
                "Add an opportunity type to calculate skill gaps."
            )

    # ---------------------------------------------------------------
    # TAB 3: LEARNING ROADMAP
    # ---------------------------------------------------------------
    with tab_roadmap:

        st.markdown("### Turn your gaps into momentum")

        phase_one, phase_two, priority_gaps = build_candidate_roadmap(
            candidate,
            ranked_jobs,
        )

        roadmap_items = phase_one + phase_two

        total_tasks = len(roadmap_items)

        completed = sum(
            1
            for key, _, _ in roadmap_items
            if st.session_state.get(f"roadmap_{key}", False)
        )

        progress = (
            completed / total_tasks
            if total_tasks else 0
        )

        progress_left, progress_right = st.columns([3, 1])

        with progress_left:
            st.markdown("**Your learning journey**")
            st.progress(progress)

        with progress_right:
            st.metric(
                "Tasks completed",
                f"{completed}/{total_tasks}",
            )

        st.caption(
            "Priority skills based on your highest-ranked roles: "
            + ", ".join(priority_gaps)
        )

        phase_left, phase_right = st.columns(2, gap="large")

        with phase_left:

            st.markdown(
                "<div class='phase-heading'>"
                "🚀 Phase 1: Foundation Building</div>",
                unsafe_allow_html=True,
            )

            for key, task, detail in phase_one:

                with st.container(border=True):

                    st.checkbox(
                        task,
                        key=f"roadmap_{key}",
                    )

                    st.caption(detail)

        with phase_right:

            st.markdown(
                "<div class='phase-heading'>"
                "🛠️ Phase 2: Project Deployment</div>",
                unsafe_allow_html=True,
            )

            for key, task, detail in phase_two:

                with st.container(border=True):

                    st.checkbox(
                        task,
                        key=f"roadmap_{key}",
                    )

                    st.caption(detail)

        # Calculate progress after displaying the checkboxes
        completed = sum(
            1
            for key, _, _ in roadmap_items
            if st.session_state.get(f"roadmap_{key}", False)
        )

        progress = completed / total_tasks if total_tasks else 0

        st.divider()

        st.markdown("#### ⏱️ Your weekly learning commitment")

        weekly_hours = st.slider(
            "How many hours can you dedicate each week?",
            min_value=2,
            max_value=30,
            step=1,
            key="weekly_hours",
        )

        # Illustrative readiness estimate:
        # Six tasks are treated as a finite learning sprint.
        estimated_total_hours = 48
        weeks_needed = max(
            1,
            round(estimated_total_hours / weekly_hours),
        )

        readiness_date = date.today() + timedelta(
            weeks=weeks_needed
        )

        estimate_col, date_col = st.columns(2)

        estimate_col.metric(
            "Estimated learning sprint",
            f"{weeks_needed} weeks",
        )

        date_col.metric(
            "Illustrative application-ready date",
            readiness_date.strftime("%d %b %Y"),
        )

        st.caption(
            "This is a simulated planning estimate based on a 48-hour "
            "learning sprint and your selected weekly study hours. "
            "It is not a guarantee of interview or hiring readiness."
        )

        st.divider()

        st.markdown("#### Suggested learning resources")

        resources = {
            "SQL": (
                "SQLBolt interactive lessons",
                "https://sqlbolt.com/",
            ),
            "Python": (
                "Python official tutorial",
                "https://docs.python.org/3/tutorial/",
            ),
            "Data Analysis": (
                "Pandas getting started",
                "https://pandas.pydata.org/docs/getting_started/",
            ),
            "Figma": (
                "Figma learning resources",
                "https://help.figma.com/hc/en-us/categories/360002051613-Learn-design",
            ),
            "UI/UX": (
                "Nielsen Norman Group articles",
                "https://www.nngroup.com/articles/",
            ),
            "Product Management": (
                "Product School resources",
                "https://productschool.com/resources",
            ),
            "A/B Testing": (
                "Optimizely experimentation guide",
                "https://www.optimizely.com/optimization-glossary/ab-testing/",
            ),
            "React": (
                "React documentation",
                "https://react.dev/learn",
            ),
            "Generative AI": (
                "OpenAI API documentation",
                "https://platform.openai.com/docs/",
            ),
            "Prompt Engineering": (
                "OpenAI prompt engineering guide",
                "https://platform.openai.com/docs/guides/prompt-engineering",
            ),
        }

        for skill in priority_gaps[:3]:

            resource = resources.get(skill)

            if resource:
                st.markdown(
                    f"- **{skill}:** "
                    f"[{resource[0]}]({resource[1]})"
                )
            else:
                st.markdown(
                    f"- **{skill}:** Build a small role-relevant "
                    "project and document your approach."
                )

        if completed == total_tasks:
            st.success(
                "🎉 Roadmap complete. You have finished every task "
                "in this learning sprint."
            )

    # ---------------------------------------------------------------
    # TAB 4: JOB FRESHNESS AND SOURCE VERIFICATION
    # ---------------------------------------------------------------
    with tab_verification:

        st.markdown("### Job freshness and source transparency")

        st.markdown(
            """
            <div class="info-note">
                <b>Demo integrity notice:</b> All opportunities in this
                prototype are synthetic records. They are not live vacancies
                and have not been verified by employers or external job sources.
            </div>
            """,
            unsafe_allow_html=True,
        )

        if not st.session_state.verification_checked:

            with st.status(
                "Running local demo validation...",
                expanded=True,
            ) as status:

                st.write("Checking local job records...")
                time.sleep(0.5)

                st.write("Validating required job fields...")
                time.sleep(0.5)

                st.write("Checking source metadata labels...")
                time.sleep(0.5)

                status.update(
                    label="Local demo validation complete",
                    state="complete",
                    expanded=False,
                )

            st.session_state.verification_checked = True

        st.caption(
            "This animation validates the local synthetic dataset only. "
            "It does not ping an external server, job board, employer, "
            "or recruitment API."
        )

        verification_df = pd.DataFrame(
            [
                {
                    "Role": job["title"],
                    "Company": job["company"],
                    "Location": job["location"],
                    "Record type": "Synthetic demo data",
                    "Source status": "⚠️ Unverified cold pipeline",
                    "Freshness": "No live timestamp",
                }
                for job in JOBS
            ]
        )

        st.dataframe(
            verification_df,
            use_container_width=True,
            hide_index=True,
        )

        st.markdown("#### Understanding source labels")

        source_col_a, source_col_b = st.columns(2)

        with source_col_a:
            st.markdown(
                """
                **⚠️ Unverified cold pipeline**

                A record that has not been checked against an
                authorized external source. It must not be
                presented as a confirmed active vacancy.
                """
            )

        with source_col_b:
            st.markdown(
                """
                **✓ Verified API feed**

                A future production status reserved for records
                retrieved from an authorized job-board or employer
                API, with a source URL and a recent verification time.
                """
            )

        st.caption(
            "No record in this prototype qualifies for the verified API "
            "feed label. A production deployment would need authorized "
            "integrations, source URLs, timestamps, and listing-status checks."
        )


# ---------------------------------------------------------------------
# FOOTER
# ---------------------------------------------------------------------
st.markdown(
    """
    <div class="footer">
        CAREERPILOT · INTELLIGENT CAREER NAVIGATOR<br>
        Prototype powered by synthetic job data and transparent
        rule-based matching.
    </div>
    """,
    unsafe_allow_html=True,
)
