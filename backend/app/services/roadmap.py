"""Skill-level learning roadmaps (roadmap.sh + curated docs/practice) and step builder."""

from __future__ import annotations

from app.schemas import LearningResource, LearningStep
from app.services.taxonomy import SKILLS

_CATEGORY_ROADMAP_DEFAULTS: dict[str, tuple[str, str]] = {
    "Programming": ("https://roadmap.sh/computer-science", "roadmap.sh/computer-science"),
    "Backend": ("https://roadmap.sh/backend", "roadmap.sh/backend"),
    "Frontend": ("https://roadmap.sh/frontend", "roadmap.sh/frontend"),
    "Databases": ("https://roadmap.sh/sql", "roadmap.sh/sql"),
    "DevOps": ("https://roadmap.sh/devops", "roadmap.sh/devops"),
    "Developer Tools": ("https://roadmap.sh/git-github", "roadmap.sh/git-github"),
    "Systems": ("https://roadmap.sh/linux", "roadmap.sh/linux"),
    "Cloud": ("https://roadmap.sh/devops", "roadmap.sh/devops"),
    "AI/ML": ("https://roadmap.sh/machine-learning", "roadmap.sh/machine-learning"),
    "Data": ("https://roadmap.sh/data-analyst", "roadmap.sh/data-analyst"),
    "Data Engineering": ("https://roadmap.sh/data-engineer", "roadmap.sh/data-engineer"),
    "Engineering Practices": ("https://roadmap.sh/software-design-architecture", "roadmap.sh/software-design-architecture"),
}

# Exact verified roadmap.sh track paths and curated companion resources for all 54 taxonomy skills.
_SKILL_CATALOG: dict[str, dict[str, object]] = {
    "Python": {
        "roadmap": ("https://roadmap.sh/python", "roadmap.sh/python"),
        "hours": "6–10 hrs",
        "resources": [
            ("Python Official Tutorial", "https://docs.python.org/3/tutorial/", "docs"),
            ("Exercism Python Track", "https://exercism.org/tracks/python", "practice"),
        ],
        "task": "Complete a focused Python fundamentals track, then practise functions, data structures and testing.",
        "project": "Build a CLI expense tracker with CSV import, validation and unit tests.",
        "bullet": "Built a modular Python CLI application with automated input validation and pytest unit test coverage.",
    },
    "Java": {
        "roadmap": ("https://roadmap.sh/java", "roadmap.sh/java"),
        "hours": "8–12 hrs",
        "resources": [
            ("Dev.java Learn", "https://dev.java/learn/", "docs"),
            ("Exercism Java Track", "https://exercism.org/tracks/java", "practice"),
        ],
        "task": "Review Java collections, streams, exception handling, OOP interfaces and Maven/Gradle builds.",
        "project": "Build a library management REST service in Java with JUnit 5 tests.",
        "bullet": "Developed an object-oriented Java service using Collections, Streams, and JUnit 5 automated tests.",
    },
    "JavaScript": {
        "roadmap": ("https://roadmap.sh/javascript", "roadmap.sh/javascript"),
        "hours": "6–10 hrs",
        "resources": [
            ("MDN JavaScript Guide", "https://developer.mozilla.org/en-US/docs/Web/JavaScript/Guide", "docs"),
            ("JavaScript.info", "https://javascript.info/", "course"),
        ],
        "task": "Practise ES modules, async/await, Promises, DOM events, fetch APIs and debugging.",
        "project": "Build a searchable job-board interface that consumes a public API.",
        "bullet": "Implemented an asynchronous JavaScript web interface integrating external REST APIs and client-side filtering.",
    },
    "TypeScript": {
        "roadmap": ("https://roadmap.sh/typescript", "roadmap.sh/typescript"),
        "hours": "5–8 hrs",
        "resources": [
            ("TypeScript Handbook", "https://www.typescriptlang.org/docs/handbook/intro.html", "docs"),
            ("Type Challenges", "https://github.com/type-challenges/type-challenges", "practice"),
        ],
        "task": "Learn strict interfaces, union/discriminated types, generics and typing React/API payloads.",
        "project": "Convert a small JavaScript app to strict TypeScript with typed API responses.",
        "bullet": "Migrated frontend state and API contracts to strict TypeScript, eliminating runtime type mismatches.",
    },
    "C++": {
        "roadmap": ("https://roadmap.sh/cpp", "roadmap.sh/cpp"),
        "hours": "8–12 hrs",
        "resources": [
            ("learncpp.com", "https://www.learncpp.com/", "course"),
            ("cppreference.com", "https://en.cppreference.com/w/", "docs"),
        ],
        "task": "Practise STL containers, smart pointers, RAII, move semantics and complexity analysis.",
        "project": "Implement an LRU cache and CLI benchmark tool using modern C++17/20 STL.",
        "bullet": "Engineered a low-overhead C++17 data processing utility leveraging STL containers and smart pointers.",
    },
    "Go": {
        "roadmap": ("https://roadmap.sh/golang", "roadmap.sh/golang"),
        "hours": "6–10 hrs",
        "resources": [
            ("A Tour of Go", "https://go.dev/tour/", "practice"),
            ("Go by Example", "https://gobyexample.com/", "docs"),
        ],
        "task": "Learn Go structs, interfaces, error handling, goroutines, channels and net/http.",
        "project": "Build a concurrent URL health-checker CLI and JSON API in Go.",
        "bullet": "Built a concurrent Go HTTP health-check service using goroutines, channels, and standard library net/http.",
    },
    "SQL": {
        "roadmap": ("https://roadmap.sh/sql", "roadmap.sh/sql"),
        "hours": "5–8 hrs",
        "resources": [
            ("SQLBolt Interactive Lessons", "https://sqlbolt.com/", "practice"),
            ("PostgreSQL SQL Tutorial", "https://www.postgresql.org/docs/current/tutorial-sql.html", "docs"),
        ],
        "task": "Practise INNER/LEFT JOINs, GROUP BY aggregations, CTEs, window functions and indexes.",
        "project": "Design a relational schema and write analytics queries for a placement portal.",
        "bullet": "Authored normalized SQL queries using joins, CTEs, and window functions to aggregate application analytics.",
    },
    "HTML": {
        "roadmap": ("https://roadmap.sh/html", "roadmap.sh/html"),
        "hours": "3–5 hrs",
        "resources": [
            ("MDN HTML Guide", "https://developer.mozilla.org/en-US/docs/Learn/HTML", "docs"),
            ("web.dev Learn HTML", "https://web.dev/learn/html", "course"),
        ],
        "task": "Master semantic landmarks, accessible forms, ARIA attributes and responsive metadata.",
        "project": "Create an accessible multi-section developer portfolio passing Lighthouse Accessibility 95+.",
        "bullet": "Structured semantic, WCAG-friendly HTML5 forms and layouts achieving 95+ Lighthouse accessibility score.",
    },
    "CSS": {
        "roadmap": ("https://roadmap.sh/css", "roadmap.sh/css"),
        "hours": "4–6 hrs",
        "resources": [
            ("MDN CSS Guide", "https://developer.mozilla.org/en-US/docs/Learn/CSS", "docs"),
            ("web.dev Learn CSS", "https://web.dev/learn/css", "course"),
        ],
        "task": "Practise Flexbox, CSS Grid, responsive breakpoints, custom properties and focus states.",
        "project": "Design a responsive analytics card dashboard supporting mobile and desktop layouts cleanly.",
        "bullet": "Styled responsive multi-column dashboards with CSS Grid, Flexbox, and accessible keyboard focus indicators.",
    },
    "React": {
        "roadmap": ("https://roadmap.sh/react", "roadmap.sh/react"),
        "hours": "8–12 hrs",
        "resources": [
            ("React Official Learn", "https://react.dev/learn", "docs"),
            ("React Tutorial (Tic-Tac-Toe)", "https://react.dev/learn/tutorial-tic-tac-toe", "practice"),
        ],
        "task": "Practise component composition, hooks (useState/useEffect), forms and client-side filtering.",
        "project": "Build a role-comparison dashboard with filters and reusable components.",
        "bullet": "Built modular React UI components with custom hooks and state-driven filtering for real-time comparisons.",
    },
    "Next.js": {
        "roadmap": ("https://roadmap.sh/nextjs", "roadmap.sh/nextjs"),
        "hours": "6–10 hrs",
        "resources": [
            ("Next.js Official Learn", "https://nextjs.org/learn", "course"),
            ("Next.js Docs", "https://nextjs.org/docs", "docs"),
        ],
        "task": "Learn App Router, Server vs Client Components, dynamic routing and route handlers.",
        "project": "Build a portfolio and project showcase with dynamic routes and server metadata.",
        "bullet": "Shipped a server-rendered Next.js web application using the App Router, dynamic routes, and API handlers.",
    },
    "Vue.js": {
        "roadmap": ("https://roadmap.sh/vue", "roadmap.sh/vue"),
        "hours": "6–9 hrs",
        "resources": [
            ("Vue Official Tutorial", "https://vuejs.org/tutorial/", "practice"),
            ("Vue 3 Guide", "https://vuejs.org/guide/introduction.html", "docs"),
        ],
        "task": "Practise Composition API, computed refs, component props/emits and Vue Router.",
        "project": "Create an interactive task tracker with Pinia state persistence and filter views.",
        "bullet": "Built reactive single-page components in Vue 3 using the Composition API and modular state stores.",
    },
    "Tailwind CSS": {
        "roadmap": ("https://roadmap.sh/frontend", "roadmap.sh/frontend"),
        "hours": "3–5 hrs",
        "resources": [
            ("Tailwind CSS Docs", "https://tailwindcss.com/docs", "docs"),
            ("Frontend Roadmap (roadmap.sh)", "https://roadmap.sh/frontend", "roadmap"),
        ],
        "task": "Learn utility-first layout tokens, responsive modifiers, dark mode classes and card grids.",
        "project": "Rebuild an existing UI screen cleanly with Tailwind responsive utilities and dark theme tokens.",
        "bullet": "Implemented responsive dark/light UI design systems using Tailwind CSS utility tokens and grid layouts.",
    },
    "Node.js": {
        "roadmap": ("https://roadmap.sh/nodejs", "roadmap.sh/nodejs"),
        "hours": "6–10 hrs",
        "resources": [
            ("Node.js Official Learn", "https://nodejs.org/en/learn", "docs"),
            ("Backend Roadmap (roadmap.sh)", "https://roadmap.sh/backend", "roadmap"),
        ],
        "task": "Learn the event loop, async I/O, streams, environment config and HTTP API services.",
        "project": "Build a rate-limited Node.js webhook receiver with structured logging and tests.",
        "bullet": "Built asynchronous Node.js backend services with structured validation, error handling, and integration tests.",
    },
    "Express.js": {
        "roadmap": ("https://roadmap.sh/nodejs", "roadmap.sh/nodejs"),
        "hours": "4–6 hrs",
        "resources": [
            ("Express.js Official Guide", "https://expressjs.com/en/guide/routing.html", "docs"),
            ("Node.js Roadmap (roadmap.sh)", "https://roadmap.sh/nodejs", "roadmap"),
        ],
        "task": "Practise Express routing, middleware pipelines, request validation and error handlers.",
        "project": "Create a REST API in Express.js with Zod validation, CORS and Supertest coverage.",
        "bullet": "Developed modular Express.js REST endpoints with middleware validation and automated Supertest suites.",
    },
    "FastAPI": {
        "roadmap": ("https://roadmap.sh/python", "roadmap.sh/python"),
        "hours": "4–7 hrs",
        "resources": [
            ("FastAPI Official Tutorial", "https://fastapi.tiangolo.com/tutorial/", "docs"),
            ("Full-Stack FastAPI Template", "https://fastapi.tiangolo.com/project-generation/", "practice"),
        ],
        "task": "Practise Pydantic schemas, dependency injection, HTTP status codes and TestClient tests.",
        "project": "Build a validated FastAPI microservice with OpenAPI docs and pytest coverage.",
        "bullet": "Designed typed FastAPI microservices with Pydantic request validation, OpenAPI docs, and pytest TestClient tests.",
    },
    "Flask": {
        "roadmap": ("https://roadmap.sh/python", "roadmap.sh/python"),
        "hours": "4–6 hrs",
        "resources": [
            ("Flask Official Tutorial", "https://flask.palletsprojects.com/en/stable/tutorial/", "docs"),
            ("Python Roadmap (roadmap.sh)", "https://roadmap.sh/python", "roadmap"),
        ],
        "task": "Learn Flask Blueprints, request/response lifecycle, SQLite integration and pytest fixtures.",
        "project": "Build a lightweight Flask URL shortener API organized with Blueprints.",
        "bullet": "Created modular Flask REST services using Blueprints, input validation, and automated test fixtures.",
    },
    "Django": {
        "roadmap": ("https://roadmap.sh/django", "roadmap.sh/django"),
        "hours": "8–12 hrs",
        "resources": [
            ("Django Official Tutorial", "https://docs.djangoproject.com/en/stable/intro/tutorial01/", "docs"),
            ("Django REST Framework Docs", "https://www.django-rest-framework.org/", "docs"),
        ],
        "task": "Practise Django ORM models, migrations, class-based views, serializers and authentication.",
        "project": "Build an internship tracker API with Django REST Framework serializers and filtering.",
        "bullet": "Built database-backed REST APIs with Django ORM and DRF serializers, migrations, and permission checks.",
    },
    "Spring Boot": {
        "roadmap": ("https://roadmap.sh/spring-boot", "roadmap.sh/spring-boot"),
        "hours": "8–12 hrs",
        "resources": [
            ("Spring Boot Quickstart", "https://spring.io/quickstart", "practice"),
            ("Spring Guides", "https://spring.io/guides", "docs"),
        ],
        "task": "Learn dependency injection, @RestController, Spring Data JPA and Slice/MockMvc testing.",
        "project": "Build a CRUD service with Spring Boot, PostgreSQL and MockMvc tests.",
        "bullet": "Engineered RESTful Java microservices using Spring Boot, Spring Data JPA, and MockMvc integration tests.",
    },
    "REST APIs": {
        "roadmap": ("https://roadmap.sh/api-design", "roadmap.sh/api-design"),
        "hours": "4–6 hrs",
        "resources": [
            ("roadmap.sh API Design", "https://roadmap.sh/api-design", "roadmap"),
            ("Swagger OpenAPI Guide", "https://swagger.io/docs/specification/about/", "docs"),
        ],
        "task": "Study HTTP methods, status semantics (200/201/400/422), pagination and API contract testing.",
        "project": "Create a documented REST API with OpenAPI spec, input validation and automated tests.",
        "bullet": "Designed versioned RESTful API contracts with clear 4xx validation errors and automated integration coverage.",
    },
    "GraphQL": {
        "roadmap": ("https://roadmap.sh/graphql", "roadmap.sh/graphql"),
        "hours": "5–8 hrs",
        "resources": [
            ("GraphQL Official Learn", "https://graphql.org/learn/", "docs"),
            ("roadmap.sh GraphQL", "https://roadmap.sh/graphql", "roadmap"),
        ],
        "task": "Learn SDL schemas, queries, mutations, resolvers and solving N+1 queries with DataLoader.",
        "project": "Expose a typed GraphQL endpoint over a relational database with resolver tests.",
        "bullet": "Implemented a strongly typed GraphQL API schema and resolvers, reducing client over-fetching.",
    },
    "PostgreSQL": {
        "roadmap": ("https://roadmap.sh/postgresql-dba", "roadmap.sh/postgresql-dba"),
        "hours": "5–8 hrs",
        "resources": [
            ("PostgreSQL Tutorial", "https://www.postgresql.org/docs/current/tutorial.html", "docs"),
            ("PGExercises Interactive", "https://pgexercises.com/", "practice"),
        ],
        "task": "Practise schema normalization, foreign-key constraints, B-tree indexes and EXPLAIN plans.",
        "project": "Persist analysis history using a normalized PostgreSQL schema with indexed queries.",
        "bullet": "Modeled normalized PostgreSQL schemas with composite indexes, lowering query latency via EXPLAIN ANALYZE.",
    },
    "MySQL": {
        "roadmap": ("https://roadmap.sh/sql", "roadmap.sh/sql"),
        "hours": "4–7 hrs",
        "resources": [
            ("MySQL Getting Started", "https://dev.mysql.com/doc/mysql-getting-started/en/", "docs"),
            ("SQLBolt Practice", "https://sqlbolt.com/", "practice"),
        ],
        "task": "Practise InnoDB keys, joins, transactions, indexing and stored backup workflows.",
        "project": "Design an order-tracking MySQL database with foreign keys and analytical summary views.",
        "bullet": "Built relational MySQL schemas enforcing referential integrity, transactions, and indexed reporting queries.",
    },
    "SQLite": {
        "roadmap": ("https://roadmap.sh/sql", "roadmap.sh/sql"),
        "hours": "3–5 hrs",
        "resources": [
            ("SQLite Official Docs", "https://www.sqlite.org/docs.html", "docs"),
            ("Python sqlite3 Guide", "https://docs.python.org/3/library/sqlite3.html", "docs"),
        ],
        "task": "Practise lightweight embedded schemas, parameterized SQL queries and WAL mode basics.",
        "project": "Add zero-config SQLite persistence and query benchmarks to a Python CLI or web tool.",
        "bullet": "Added embedded SQLite storage with parameterized queries and zero external database operational overhead.",
    },
    "MongoDB": {
        "roadmap": ("https://roadmap.sh/mongodb", "roadmap.sh/mongodb"),
        "hours": "5–8 hrs",
        "resources": [
            ("MongoDB University", "https://learn.mongodb.com/", "course"),
            ("MongoDB CRUD & Aggregation Docs", "https://www.mongodb.com/docs/manual/", "docs"),
        ],
        "task": "Practise document modeling, embedding vs referencing, compound indexes and aggregation pipelines.",
        "project": "Build a resume/job catalog API backed by MongoDB aggregation pipelines.",
        "bullet": "Modeled document schemas and multi-stage MongoDB aggregation pipelines with indexed filter lookups.",
    },
    "Redis": {
        "roadmap": ("https://roadmap.sh/redis", "roadmap.sh/redis"),
        "hours": "4–6 hrs",
        "resources": [
            ("Redis University / Docs", "https://redis.io/learn/", "course"),
            ("Try Redis Commands", "https://redis.io/docs/latest/commands/", "docs"),
        ],
        "task": "Learn strings, hashes, sorted sets, TTL eviction, cache-aside patterns and rate limiting.",
        "project": "Add a Redis cache-aside layer and sliding-window rate limiter in front of a REST API.",
        "bullet": "Integrated Redis TTL caching and sliding-window rate limiting to cut repeated API compute latency.",
    },
    "Docker": {
        "roadmap": ("https://roadmap.sh/docker", "roadmap.sh/docker"),
        "hours": "5–8 hrs",
        "resources": [
            ("Docker Getting Started", "https://docs.docker.com/get-started/", "docs"),
            ("Docker Compose Guide", "https://docs.docker.com/compose/gettingstarted/", "practice"),
        ],
        "task": "Learn images, multi-stage Dockerfiles, volumes, bridge networks and Docker Compose.",
        "project": "Containerize a multi-service web app + database with reproducible docker-compose up.",
        "bullet": "Containerized application and database services with multi-stage Docker builds and Docker Compose.",
    },
    "Kubernetes": {
        "roadmap": ("https://roadmap.sh/kubernetes", "roadmap.sh/kubernetes"),
        "hours": "8–12 hrs",
        "resources": [
            ("Kubernetes Basics Tutorial", "https://kubernetes.io/docs/tutorials/kubernetes-basics/", "practice"),
            ("Kubernetes Concepts", "https://kubernetes.io/docs/concepts/", "docs"),
        ],
        "task": "Learn Pods, Deployments, Services, ConfigMaps, Secrets and liveness/readiness probes.",
        "project": "Deploy a containerized API locally using kind or minikube with health probes.",
        "bullet": "Orchestrated containerized services on Kubernetes using Deployment manifests, ConfigMaps, and readiness probes.",
    },
    "CI/CD": {
        "roadmap": ("https://roadmap.sh/devops", "roadmap.sh/devops"),
        "hours": "4–6 hrs",
        "resources": [
            ("GitHub Actions Quickstart", "https://docs.github.com/en/actions/quickstart", "docs"),
            ("DevOps Roadmap (roadmap.sh)", "https://roadmap.sh/devops", "roadmap"),
        ],
        "task": "Learn automated lint/test pipelines, artifact caching and deployment gates.",
        "project": "Configure an automated CI pipeline that runs pytest, lint checks and Docker build verification.",
        "bullet": "Automated test, lint, and container build checks across pull requests via repeatable CI/CD pipelines.",
    },
    "GitHub Actions": {
        "roadmap": ("https://roadmap.sh/devops", "roadmap.sh/devops"),
        "hours": "3–5 hrs",
        "resources": [
            ("GitHub Actions Docs", "https://docs.github.com/en/actions", "docs"),
            ("Workflow Syntax Reference", "https://docs.github.com/en/actions/using-workflows/workflow-syntax-for-github-actions", "docs"),
        ],
        "task": "Practise YAML workflow triggers, matrix builds, pip/npm dependency caching and secrets.",
        "project": "Automate Python pytest and container image verification on every commit with GitHub Actions.",
        "bullet": "Configured GitHub Actions CI workflows with dependency caching to run unit and UI tests automatically.",
    },
    "Git": {
        "roadmap": ("https://roadmap.sh/git-github", "roadmap.sh/git-github"),
        "hours": "3–5 hrs",
        "resources": [
            ("Learn Git Branching (Visual)", "https://learngitbranching.js.org/", "practice"),
            ("Pro Git Free Book", "https://git-scm.com/book/en/v2", "docs"),
        ],
        "task": "Practise feature branching, interactive rebase, conflict resolution and clean PR commits.",
        "project": "Practice branching, rebasing and pull-request reviews cleanly on a collaborative Git repo.",
        "bullet": "Managed feature branches, clean rebase workflows, and code-reviewed pull requests with Git and GitHub.",
    },
    "Unit Testing": {
        "roadmap": ("https://roadmap.sh/qa", "roadmap.sh/qa"),
        "hours": "4–7 hrs",
        "resources": [
            ("pytest Getting Started", "https://docs.pytest.org/en/stable/getting-started.html", "docs"),
            ("QA Roadmap (roadmap.sh)", "https://roadmap.sh/qa", "roadmap"),
        ],
        "task": "Study fixtures, parametrized tests, mocking/monkeypatch and regression boundary cases.",
        "project": "Add unit and API integration tests reaching 85%+ coverage on an API module.",
        "bullet": "Wrote parametrized pytest unit and endpoint tests covering edge cases, negations, and schema validation.",
    },
    "Linux": {
        "roadmap": ("https://roadmap.sh/linux", "roadmap.sh/linux"),
        "hours": "5–8 hrs",
        "resources": [
            ("OverTheWire Bandit Wargame", "https://overthewire.org/wargames/bandit/", "practice"),
            ("Linux Journey", "https://linuxjourney.com/", "course"),
        ],
        "task": "Practise bash scripting, file permissions, grep/awk pipelines, systemd/processes and networking.",
        "project": "Write an automated bash log-parser and service health-monitor script on Ubuntu.",
        "bullet": "Automated log inspection, process diagnostics, and deployment tasks using Linux shell tools and Bash scripts.",
    },
    "AWS": {
        "roadmap": ("https://roadmap.sh/aws", "roadmap.sh/aws"),
        "hours": "8–12 hrs",
        "resources": [
            ("AWS Skill Builder", "https://explore.skillbuilder.aws/", "course"),
            ("AWS Core Docs", "https://docs.aws.amazon.com/", "docs"),
        ],
        "task": "Learn IAM least-privilege roles, S3 buckets, EC2/ECS containers, RDS and VPC basics.",
        "project": "Deploy a containerized backend and static site with IAM roles and environment secrets.",
        "bullet": "Deployed cloud services using IAM least-privilege policies, S3 storage, and containerized AWS compute.",
    },
    "Azure": {
        "roadmap": ("https://roadmap.sh/devops", "roadmap.sh/devops"),
        "hours": "6–10 hrs",
        "resources": [
            ("Microsoft Learn Azure Fundamentals", "https://learn.microsoft.com/en-us/training/azure/", "course"),
            ("Azure Documentation", "https://learn.microsoft.com/en-us/azure/", "docs"),
        ],
        "task": "Learn Resource Groups, Azure App Service / Container Apps, RBAC and managed databases.",
        "project": "Containerize and deploy a Python web app to Azure Container Apps with CI triggers.",
        "bullet": "Provisioned Azure Container Apps with RBAC-scoped environment configuration and CI deployment.",
    },
    "Google Cloud": {
        "roadmap": ("https://roadmap.sh/devops", "roadmap.sh/devops"),
        "hours": "6–10 hrs",
        "resources": [
            ("Google Cloud Skills Boost", "https://www.cloudskillsboost.google/", "course"),
            ("Google Cloud Run Docs", "https://cloud.google.com/run/docs", "docs"),
        ],
        "task": "Learn IAM, Cloud Run serverless containers, Cloud SQL and Artifact Registry.",
        "project": "Deploy a stateless FastAPI container cleanly on Google Cloud Run.",
        "bullet": "Deployed autoscaling containerized APIs on Google Cloud Run backed by IAM and Artifact Registry.",
    },
    "Machine Learning": {
        "roadmap": ("https://roadmap.sh/machine-learning", "roadmap.sh/machine-learning"),
        "hours": "8–14 hrs",
        "resources": [
            ("Kaggle Intro to ML", "https://www.kaggle.com/learn/intro-to-machine-learning", "course"),
            ("Google ML Crash Course", "https://developers.google.com/machine-learning/crash-course", "course"),
        ],
        "task": "Review supervised vs unsupervised learning, leakage-free splits, precision/recall and calibration.",
        "project": "Train and compare a baseline classifier against rule baselines with an explicit F1 benchmark.",
        "bullet": "Evaluated supervised baselines with leakage-free train/test splits and macro-F1 diagnostic metrics.",
    },
    "Deep Learning": {
        "roadmap": ("https://roadmap.sh/ai-data-scientist", "roadmap.sh/ai-data-scientist"),
        "hours": "10–16 hrs",
        "resources": [
            ("fast.ai Practical Deep Learning", "https://course.fast.ai/", "course"),
            ("DeepLearning.AI / PyTorch Learn", "https://pytorch.org/tutorials/beginner/deep_learning_60min_blitz.html", "practice"),
        ],
        "task": "Study backpropagation, regularization, optimization schedules and transfer learning.",
        "project": "Fine-tune a pretrained neural encoder and track validation loss and confusion matrices.",
        "bullet": "Trained and fine-tuned neural architectures with validation checkpoints and overfitting controls.",
    },
    "NLP": {
        "roadmap": ("https://roadmap.sh/ai-engineer", "roadmap.sh/ai-engineer"),
        "hours": "8–12 hrs",
        "resources": [
            ("Hugging Face NLP Course", "https://huggingface.co/learn/nlp-course/", "course"),
            ("spaCy 101 Guide", "https://spacy.io/usage/spacy-101", "docs"),
        ],
        "task": "Study tokenization, boundary/entity extraction, embeddings and precision/recall evaluation.",
        "project": "Build a skill/entity extraction benchmark with annotated examples and negation handling.",
        "bullet": "Built an explainable NLP extraction pipeline combining normalized phrase patterns with semantic embeddings.",
    },
    "PyTorch": {
        "roadmap": ("https://roadmap.sh/machine-learning", "roadmap.sh/machine-learning"),
        "hours": "8–12 hrs",
        "resources": [
            ("PyTorch Official Tutorials", "https://pytorch.org/tutorials/", "docs"),
            ("Learn the Basics (PyTorch)", "https://pytorch.org/tutorials/beginner/basics/intro.html", "practice"),
        ],
        "task": "Practise tensors, Dataset/DataLoader batching, nn.Module training loops and evaluation mode.",
        "project": "Train and evaluate a text classifier in PyTorch on a labeled dataset.",
        "bullet": "Implemented custom PyTorch Dataset pipelines, training loops, and validation F1 evaluation scripts.",
    },
    "TensorFlow": {
        "roadmap": ("https://roadmap.sh/machine-learning", "roadmap.sh/machine-learning"),
        "hours": "8–12 hrs",
        "resources": [
            ("TensorFlow Official Tutorials", "https://www.tensorflow.org/tutorials", "docs"),
            ("Keras Developer Guides", "https://keras.io/guides/", "practice"),
        ],
        "task": "Learn tf.data pipelines, Keras Functional/Sequential APIs, callbacks and SavedModel export.",
        "project": "Train and export a text or tabular classifier using TensorFlow/Keras pipelines.",
        "bullet": "Built tf.data input pipelines and Keras classification models with early-stopping callbacks.",
    },
    "scikit-learn": {
        "roadmap": ("https://roadmap.sh/machine-learning", "roadmap.sh/machine-learning"),
        "hours": "5–8 hrs",
        "resources": [
            ("scikit-learn User Guide", "https://scikit-learn.org/stable/user_guide.html", "docs"),
            ("scikit-learn Tutorials", "https://scikit-learn.org/stable/tutorial/index.html", "practice"),
        ],
        "task": "Learn ColumnTransformer, Pipelines, cross_val_score, TF-IDF vectorizers and classification_report.",
        "project": "Build a scikit-learn TF-IDF + LogisticRegression baseline with macro-F1 reporting.",
        "bullet": "Built leakage-free scikit-learn Pipelines pairing TF-IDF features with cross-validated linear classifiers.",
    },
    "pandas": {
        "roadmap": ("https://roadmap.sh/data-analyst", "roadmap.sh/data-analyst"),
        "hours": "5–8 hrs",
        "resources": [
            ("pandas 10 Minutes & Tutorials", "https://pandas.pydata.org/docs/getting_started/intro_tutorials/index.html", "docs"),
            ("Kaggle pandas Course", "https://www.kaggle.com/learn/pandas", "practice"),
        ],
        "task": "Practise DataFrame filtering, groupby aggregations, merges/joins and missing-value cleaning.",
        "project": "Clean and summarize a public job-market CSV dataset into reproducible KPI tables.",
        "bullet": "Transformed multi-source tabular datasets using vectorized pandas aggregations, joins, and validation checks.",
    },
    "NumPy": {
        "roadmap": ("https://roadmap.sh/ai-data-scientist", "roadmap.sh/ai-data-scientist"),
        "hours": "4–6 hrs",
        "resources": [
            ("NumPy Quickstart", "https://numpy.org/doc/stable/user/quickstart.html", "docs"),
            ("NumPy Learn Hub", "https://numpy.org/learn/", "course"),
        ],
        "task": "Master ndarray broadcasting, vectorization, dot products (cosine similarity) and matrix ops.",
        "project": "Implement a vectorized cosine-similarity retriever over normalized embedding matrices in NumPy.",
        "bullet": "Vectorized numerical matrix and cosine-similarity computations in NumPy for sub-millisecond scoring.",
    },
    "Jupyter": {
        "roadmap": ("https://roadmap.sh/data-analyst", "roadmap.sh/data-analyst"),
        "hours": "2–4 hrs",
        "resources": [
            ("Jupyter Official Docs", "https://docs.jupyter.org/en/latest/", "docs"),
            ("Kaggle Notebooks Guide", "https://www.kaggle.com/code", "practice"),
        ],
        "task": "Learn reproducible notebook hygiene, pinned environments and separating exploration from src modules.",
        "project": "Create an interactive exploratory notebook that calls tested Python modules for charts.",
        "bullet": "Built reproducible Jupyter experiment notebooks cleanly backed by version-controlled Python modules.",
    },
    "Data Analysis": {
        "roadmap": ("https://roadmap.sh/data-analyst", "roadmap.sh/data-analyst"),
        "hours": "6–10 hrs",
        "resources": [
            ("roadmap.sh Data Analyst", "https://roadmap.sh/data-analyst", "roadmap"),
            ("Kaggle Data Cleaning", "https://www.kaggle.com/learn/data-cleaning", "practice"),
        ],
        "task": "Practise cohort slicing, outlier detection, metric definitions and writing crisp insight summaries.",
        "project": "Publish an end-to-end exploratory analysis comparing skill demand across internship roles.",
        "bullet": "Conducted structured exploratory data analysis identifying cohort trends, anomalies, and hiring-skill gaps.",
    },
    "Data Visualization": {
        "roadmap": ("https://roadmap.sh/data-analyst", "roadmap.sh/data-analyst"),
        "hours": "4–6 hrs",
        "resources": [
            ("Plotly Python Graphing Library", "https://plotly.com/python/", "docs"),
            ("Kaggle Data Visualization", "https://www.kaggle.com/learn/data-visualization", "practice"),
        ],
        "task": "Learn visual encoding hierarchy, direct data labels, accessible palettes and interactive tooltips.",
        "project": "Create an interactive Plotly dashboard visualizing category coverage and role rankings.",
        "bullet": "Designed interactive Plotly gauges and comparative bar charts turning complex metrics into scannable visuals.",
    },
    "Statistics": {
        "roadmap": ("https://roadmap.sh/ai-data-scientist", "roadmap.sh/ai-data-scientist"),
        "hours": "6–10 hrs",
        "resources": [
            ("StatQuest Video Library", "https://statquest.org/", "course"),
            ("Seeing Theory (Visual Stats)", "https://seeing-theory.brown.edu/", "practice"),
        ],
        "task": "Review probability distributions, confidence intervals, p-values, A/B testing and correlation limits.",
        "project": "Design and simulate an A/B experiment comparing two matching thresholds with confidence intervals.",
        "bullet": "Applied hypothesis testing, confidence intervals, and F1 evaluation statistics to validate system thresholds.",
    },
    "Sentence Transformers": {
        "roadmap": ("https://roadmap.sh/ai-engineer", "roadmap.sh/ai-engineer"),
        "hours": "4–7 hrs",
        "resources": [
            ("SBERT Documentation", "https://www.sbert.net/", "docs"),
            ("AI Engineer Roadmap (roadmap.sh)", "https://roadmap.sh/ai-engineer", "roadmap"),
        ],
        "task": "Learn bi-encoder embeddings, cosine normalization, fragment chunking and retrieval evaluation.",
        "project": "Compare MiniLM bi-encoder fragment matching against TF-IDF on 30 annotated skill pairs.",
        "bullet": "Integrated normalized all-MiniLM-L6-v2 sentence embeddings for semantic resume-fragment alignment.",
    },
    "spaCy": {
        "roadmap": ("https://roadmap.sh/ai-engineer", "roadmap.sh/ai-engineer"),
        "hours": "4–7 hrs",
        "resources": [
            ("spaCy 101 Official Guide", "https://spacy.io/usage/spacy-101", "docs"),
            ("Advanced NLP with spaCy", "https://course.spacy.io/", "practice"),
        ],
        "task": "Learn PhraseMatcher, dependency spans, custom entity pipelines and linguistic boundary rules.",
        "project": "Build a custom spaCy EntityRuler + PhraseMatcher pipeline extracting technical skills with context spans.",
        "bullet": "Built high-throughput NLP skill extractors using custom phrase matchers and linguistic span boundaries.",
    },
    "Apache Spark": {
        "roadmap": ("https://roadmap.sh/data-engineer", "roadmap.sh/data-engineer"),
        "hours": "8–12 hrs",
        "resources": [
            ("PySpark Official Docs", "https://spark.apache.org/docs/latest/api/python/", "docs"),
            ("Data Engineer Roadmap (roadmap.sh)", "https://roadmap.sh/data-engineer", "roadmap"),
        ],
        "task": "Learn Spark DataFrames, lazy evaluation, partitioning, shuffles and Parquet storage.",
        "project": "Process a multi-million-row event log CSV into partitioned Parquet summaries with PySpark.",
        "bullet": "Built distributed PySpark ETL transformations outputting partitioned Parquet datasets for analytics.",
    },
    "Kafka": {
        "roadmap": ("https://roadmap.sh/data-engineer", "roadmap.sh/data-engineer"),
        "hours": "6–10 hrs",
        "resources": [
            ("Apache Kafka Quickstart", "https://kafka.apache.org/quickstart", "docs"),
            ("Confluent Developer Learn", "https://developer.confluent.io/learn-kafka/", "course"),
        ],
        "task": "Learn topics, partitions, consumer groups, offsets and idempotent event producers.",
        "project": "Create a producer/consumer Python pipeline streaming job-posting events via Kafka + Docker.",
        "bullet": "Implemented fault-tolerant Kafka producers and consumer groups for asynchronous event ingestion.",
    },
    "Object-Oriented Programming": {
        "roadmap": ("https://roadmap.sh/software-design-architecture", "roadmap.sh/software-design-architecture"),
        "hours": "5–8 hrs",
        "resources": [
            ("Refactoring Guru Design Patterns", "https://refactoring.guru/design-patterns", "docs"),
            ("Software Design Roadmap", "https://roadmap.sh/software-design-architecture", "roadmap"),
        ],
        "task": "Practise SOLID principles, composition over inheritance, abstract interfaces and clean encapsulation.",
        "project": "Refactor a procedural script into loosely coupled service classes with dependency injection.",
        "bullet": "Applied SOLID object-oriented design patterns and clean interfaces to keep analysis services extensible.",
    },
    "Data Structures & Algorithms": {
        "roadmap": ("https://roadmap.sh/datastructures-and-algorithms", "roadmap.sh/datastructures-and-algorithms"),
        "hours": "12–20 hrs",
        "resources": [
            ("roadmap.sh DSA Track", "https://roadmap.sh/datastructures-and-algorithms", "roadmap"),
            ("NeetCode 150 Practice", "https://neetcode.io/practice", "practice"),
        ],
        "task": "Master hash maps, trees, graphs, heaps, sliding windows and Big-O time/space tradeoffs.",
        "project": "Solve 30 curated patterns (2/day across arrays, trees, graphs, DP) with complexity notes.",
        "bullet": "Solved 100+ algorithmic problems spanning graphs, dynamic programming, and hash-indexed structures.",
    },
}


def get_skill_learning_guide(skill: str, category: str = "") -> dict[str, object]:
    """Return roadmap.sh URL, curated companion resources, tasks and bullet tips for a skill."""
    cat = category or str((SKILLS.get(skill) or {}).get("category", ""))
    default_roadmap = _CATEGORY_ROADMAP_DEFAULTS.get(cat, ("https://roadmap.sh/", "roadmap.sh"))
    entry = _SKILL_CATALOG.get(skill, {})
    roadmap_url, roadmap_label = entry.get("roadmap", default_roadmap)  # type: ignore[misc]

    raw_resources = entry.get("resources") or [
        (roadmap_label, roadmap_url, "roadmap"),
    ]
    resources = [
        LearningResource(title=title, url=url, kind=kind)
        for title, url, kind in raw_resources  # type: ignore[misc]
    ]
    return {
        "roadmap_url": roadmap_url,
        "roadmap_label": roadmap_label,
        "estimated_hours": entry.get("hours", "4–8 hrs"),
        "resources": resources,
        "task": entry.get(
            "task",
            f"Review core {skill} concepts on {roadmap_label} and complete structured exercises.",
        ),
        "project_idea": entry.get(
            "project",
            f"Build a small end-to-end project demonstrating {skill} with unit tests and a README.",
        ),
        "resume_bullet_tip": entry.get(
            "bullet",
            f"Implemented and verified a practical module using {skill}, backed by reproducible tests.",
        ),
    }


def build_roadmap(
    missing_skills: list[str],
    partial_skills: list[str],
    *,
    skill_meta: dict[str, dict[str, float | str]] | None = None,
    total_weight: float = 1.0,
) -> list[LearningStep]:
    """Build prioritized learning steps with roadmap.sh links and score-impact estimates."""
    steps: list[LearningStep] = []
    meta_map = skill_meta or {}
    denom = total_weight or 1.0

    ordered = [
        (skill, "missing", "High", "Required or unverified skill not detected")
        for skill in missing_skills
    ]
    ordered += [
        (skill, "partial", "Medium", "Related or partial evidence detected; deepen direct proof")
        for skill in partial_skills
    ]

    for skill, status, priority, reason in ordered:
        guide = get_skill_learning_guide(skill)
        info = meta_map.get(skill, {})
        weight = float(info.get("weight", 1.0))
        match_value = float(info.get("match_value", 0.5 if status == "partial" else 0.0))
        category = str(info.get("category") or (SKILLS.get(skill) or {}).get("category", ""))
        impact = round(100.0 * max(0.0, 1.0 - match_value) * weight / denom, 1)

        steps.append(
            LearningStep(
                skill=skill,
                category=category,
                status=status,
                priority=priority,
                weight=weight,
                score_impact_pct=impact,
                estimated_hours=str(guide["estimated_hours"]),
                reason=reason,
                task=str(guide["task"]),
                project_idea=str(guide["project_idea"]),
                resume_bullet_tip=str(guide["resume_bullet_tip"]),
                roadmap_url=str(guide["roadmap_url"]),
                roadmap_label=str(guide["roadmap_label"]),
                resources=guide["resources"],  # type: ignore[arg-type]
            )
        )
    return steps[:12]
