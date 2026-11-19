"""
Generate the complete DevOps Course Project Report Word Document (.docx)
with student details, abstract, introduction, code snippets, execution logs,
and all 12 embedded screenshots for Ramaiah Institute of Technology.
"""
import os
import docx
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import parse_xml
from docx.oxml.ns import nsdecls

def set_cell_background(cell, fill_hex):
    tcPr = cell._element.get_or_add_tcPr()
    shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{fill_hex}"/>')
    tcPr.append(shd)

def set_cell_margins(cell, top=100, bottom=100, left=120, right=120):
    tcPr = cell._element.get_or_add_tcPr()
    tcMar = parse_xml(f'<w:tcMar {nsdecls("w")}><w:top w:w="{top}" w:type="dxa"/><w:bottom w:w="{bottom}" w:type="dxa"/><w:left w:w="{left}" w:type="dxa"/><w:right w:w="{right}" w:type="dxa"/></w:tcMar>')
    tcPr.append(tcMar)

def add_callout(doc, text, title="NOTE"):
    table = doc.add_table(rows=1, cols=1)
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    cell = table.cell(0, 0)
    cell.width = Inches(6.5)
    set_cell_background(cell, "F0F4F8")
    set_cell_margins(cell, top=120, bottom=120, left=180, right=180)
    tcPr = cell._element.get_or_add_tcPr()
    borders = parse_xml(f'<w:tcBorders {nsdecls("w")}><w:top w:val="none"/><w:left w:val="single" w:sz="24" w:space="0" w:color="003366"/><w:bottom w:val="none"/><w:right w:val="none"/></w:tcBorders>')
    tcPr.append(borders)
    p = cell.paragraphs[0]
    p.paragraph_format.space_before = Pt(2)
    p.paragraph_format.space_after = Pt(2)
    p.paragraph_format.line_spacing = 1.15
    rt = p.add_run(f"[{title}] ")
    rt.bold = True
    rt.font.name = "Arial"
    rt.font.size = Pt(10)
    rt.font.color.rgb = RGBColor(0, 51, 102)
    rx = p.add_run(text)
    rx.font.name = "Arial"
    rx.font.size = Pt(10)
    rx.font.color.rgb = RGBColor(51, 51, 51)
    doc.add_paragraph().paragraph_format.space_after = Pt(4)

def add_code_block(doc, code_str, caption=None):
    if caption:
        p_cap = doc.add_paragraph()
        p_cap.paragraph_format.space_before = Pt(6)
        p_cap.paragraph_format.space_after = Pt(2)
        rc = p_cap.add_run(f"Listing / Terminal: {caption}")
        rc.bold = True
        rc.font.name = "Arial"
        rc.font.size = Pt(9.5)
        rc.font.color.rgb = RGBColor(0, 51, 102)

    table = doc.add_table(rows=1, cols=1)
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    cell = table.cell(0, 0)
    cell.width = Inches(6.5)
    set_cell_background(cell, "1E1E1E")
    set_cell_margins(cell, top=120, bottom=120, left=160, right=160)
    p = cell.paragraphs[0]
    p.paragraph_format.space_before = Pt(0)
    p.paragraph_format.space_after = Pt(0)
    p.paragraph_format.line_spacing = 1.1
    r = p.add_run(code_str.strip())
    r.font.name = "Consolas"
    r.font.size = Pt(9)
    r.font.color.rgb = RGBColor(220, 220, 220)
    doc.add_paragraph().paragraph_format.space_after = Pt(6)

def style_heading(p, text, level, font_size=14, bold=True, space_before=14, space_after=6, color_rgb=(0, 51, 102)):
    p.paragraph_format.space_before = Pt(space_before)
    p.paragraph_format.space_after = Pt(space_after)
    p.paragraph_format.keep_with_next = True
    r = p.add_run(text)
    r.bold = bold
    r.font.name = "Arial"
    r.font.size = Pt(font_size)
    r.font.color.rgb = RGBColor(*color_rgb)

def add_body_p(doc, text, bold_prefix=None, space_after=6):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(0)
    p.paragraph_format.space_after = Pt(space_after)
    p.paragraph_format.line_spacing = 1.15
    if bold_prefix:
        rp = p.add_run(bold_prefix)
        rp.bold = True
        rp.font.name = "Arial"
        rp.font.size = Pt(11)
        rp.font.color.rgb = RGBColor(34, 34, 34)
    r = p.add_run(text)
    r.font.name = "Arial"
    r.font.size = Pt(11)
    r.font.color.rgb = RGBColor(51, 51, 51)
    return p

def add_screenshots_section(doc, screenshots):
    for caption, img_p in screenshots:
        if os.path.exists(img_p):
            p_img = doc.add_paragraph()
            p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
            p_img.paragraph_format.space_before = Pt(8)
            p_img.paragraph_format.space_after = Pt(2)
            run_img = p_img.add_run()
            run_img.add_picture(img_p, width=Inches(6.2))
            
            p_c = doc.add_paragraph()
            p_c.alignment = WD_ALIGN_PARAGRAPH.CENTER
            p_c.paragraph_format.space_before = Pt(2)
            p_c.paragraph_format.space_after = Pt(12)
            rc = p_c.add_run(caption)
            rc.bold = True
            rc.font.name = "Arial"
            rc.font.size = Pt(9.5)
            rc.font.color.rgb = RGBColor(0, 51, 102)

def create_report():
    doc = Document()
    for s in doc.sections:
        s.top_margin = Inches(1.0)
        s.bottom_margin = Inches(1.0)
        s.left_margin = Inches(1.0)
        s.right_margin = Inches(1.0)

    # 1. TITLE PAGE
    p_inst = doc.add_paragraph()
    p_inst.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_inst.paragraph_format.space_before = Pt(10)
    p_inst.paragraph_format.space_after = Pt(4)
    r = p_inst.add_run("RAMAIAH INSTITUTE OF TECHNOLOGY")
    r.bold = True
    r.font.name = "Arial"
    r.font.size = Pt(16)
    r.font.color.rgb = RGBColor(0, 51, 102)

    p_sub = doc.add_paragraph()
    p_sub.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_sub.paragraph_format.space_after = Pt(16)
    r = p_sub.add_run("(Autonomous Institute Affiliated to VTU)\nMSR Nagar, MSRIT Post, Bangalore - 560054, Karnataka")
    r.font.name = "Arial"
    r.font.size = Pt(10)
    r.font.color.rgb = RGBColor(100, 100, 100)

    p_dept = doc.add_paragraph()
    p_dept.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_dept.paragraph_format.space_after = Pt(20)
    r = p_dept.add_run("DEPARTMENT OF COMPUTER SCIENCE AND ENGINEERING\n(ARTIFICIAL INTELLIGENCE & MACHINE LEARNING)")
    r.bold = True
    r.font.name = "Arial"
    r.font.size = Pt(12)
    r.font.color.rgb = RGBColor(0, 51, 102)

    p_rep = doc.add_paragraph()
    p_rep.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_rep.paragraph_format.space_after = Pt(6)
    r = p_rep.add_run("SELF LEARNING ACTIVITY REPORT")
    r.bold = True
    r.font.name = "Arial"
    r.font.size = Pt(15)
    r.font.color.rgb = RGBColor(180, 0, 0)

    p_on = doc.add_paragraph()
    p_on.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_on.paragraph_format.space_after = Pt(8)
    r = p_on.add_run("ON")
    r.font.name = "Arial"
    r.font.size = Pt(11)

    p_title = doc.add_paragraph()
    p_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_title.paragraph_format.space_after = Pt(25)
    r = p_title.add_run("AUTOMATED END-TO-END DEVOPS CI/CD PIPELINE\nWITH JENKINS, ANSIBLE, DOCKER & KUBERNETES")
    r.bold = True
    r.font.name = "Arial"
    r.font.size = Pt(17)
    r.font.color.rgb = RGBColor(0, 51, 102)

    p_req = doc.add_paragraph()
    p_req.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_req.paragraph_format.space_after = Pt(25)
    r = p_req.add_run("Submitted in partial fulfilment of the requirements for the course\nDevOps (Course Code: 24CIAEC59 / 25CIAEC59)\n5th Semester Bachelor of Engineering")
    r.font.name = "Arial"
    r.font.size = Pt(11)
    r.italic = True

    table = doc.add_table(rows=1, cols=2)
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    c_left, c_right = table.cell(0, 0), table.cell(0, 1)
    c_left.width, c_right.width = Inches(3.25), Inches(3.25)
    p_sl = c_left.paragraphs[0]
    r1 = p_sl.add_run("Submitted By:\n")
    r1.bold = True
    r2 = p_sl.add_run("GAUTAM RAJESH\nUSN: 1MS24CI045\nSemester: V (CSE - AI & ML)")
    r2.font.size = Pt(10.5)

    p_sr = c_right.paragraphs[0]
    p_sr.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    r1 = p_sr.add_run("Under the Guidance of:\n")
    r1.bold = True
    r2 = p_sr.add_run("Mr. Prashanth Reddy C\nSenior Lecturer\nDept. of CSE (AI & ML) and CSE (Cyber Security)")
    r2.font.size = Pt(10.5)

    p_acad = doc.add_paragraph()
    p_acad.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_acad.paragraph_format.space_before = Pt(30)
    r = p_acad.add_run("Academic Year: 2026 - 2027")
    r.bold = True
    r.font.name = "Arial"
    r.font.size = Pt(11)

    doc.add_page_break()

    # 2. CERTIFICATE PAGE
    p_cinst = doc.add_paragraph()
    p_cinst.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_cinst.paragraph_format.space_before = Pt(10)
    r = p_cinst.add_run("RAMAIAH INSTITUTE OF TECHNOLOGY\nDEPARTMENT OF COMPUTER SCIENCE AND ENGINEERING (AI & ML)")
    r.bold = True
    r.font.name = "Arial"
    r.font.size = Pt(13)
    r.font.color.rgb = RGBColor(0, 51, 102)

    p_cert_title = doc.add_paragraph()
    p_cert_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_cert_title.paragraph_format.space_before = Pt(20)
    p_cert_title.paragraph_format.space_after = Pt(20)
    r = p_cert_title.add_run("CERTIFICATE")
    r.bold = True
    r.font.name = "Arial"
    r.font.size = Pt(16)
    r.underline = True
    r.font.color.rgb = RGBColor(180, 0, 0)

    p_cert_body = doc.add_paragraph()
    p_cert_body.paragraph_format.line_spacing = 1.3
    p_cert_body.paragraph_format.space_after = Pt(20)
    r = p_cert_body.add_run("This is to certify that the project based learning activity work on the DevOps course entitled ")
    r.font.name = "Arial"
    r.font.size = Pt(11)
    r_proj = p_cert_body.add_run('"AUTOMATED END-TO-END DEVOPS CI/CD PIPELINE WITH JENKINS, ANSIBLE, DOCKER & KUBERNETES" ')
    r_proj.bold = True
    r_rest = p_cert_body.add_run("is a bonafide record of work done by ")
    r_name = p_cert_body.add_run("GAUTAM RAJESH (USN: 1MS24CI045) ")
    r_name.bold = True
    r_end = p_cert_body.add_run("under my supervision and guidance, in partial fulfilment of the requirements for the award of the Bachelor of Engineering in Computer Science & Engineering (Artificial Intelligence and Machine Learning) from Ramaiah Institute of Technology, Bangalore for the academic year 2026-2027.")
    r_end.font.name = "Arial"

    doc.add_paragraph().paragraph_format.space_after = Pt(45)
    sig_table = doc.add_table(rows=1, cols=3)
    sig_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    c1, c2, c3 = sig_table.cell(0, 0), sig_table.cell(0, 1), sig_table.cell(0, 2)
    c1.width, c2.width, c3.width = Inches(2.2), Inches(2.1), Inches(2.2)
    p1 = c1.paragraphs[0]
    p1.add_run("_____________________\nCandidate Sign\n(Gautam Rajesh)")
    p2 = c2.paragraphs[0]
    p2.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p2.add_run("_____________________\nFaculty Sign\n(Mr. Prashanth Reddy C)")
    p3 = c3.paragraphs[0]
    p3.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    p3.add_run("_____________________\nHead of Department\nDept. of CSE (AI & ML)")

    doc.add_page_break()

    # 3. LIST OF ACTIVITIES & RUBRICS
    p_list = doc.add_paragraph()
    style_heading(p_list, "LIST OF PROJECT BASED LEARNING COMPONENTS", 1, font_size=14)
    add_body_p(doc, "COURSE NAME: DevOps   |   COURSE CODE: 24CIAEC59   |   CREDITS: 1:0:0   |   MAX. MARKS: 20", bold_prefix=None)
    
    t_comp = doc.add_table(rows=3, cols=3)
    t_comp.alignment = WD_TABLE_ALIGNMENT.CENTER
    comp_headers = ["Sl. No", "Description", "Marks"]
    for i, h in enumerate(comp_headers):
        c = t_comp.cell(0, i)
        set_cell_background(c, "003366")
        set_cell_margins(c, 80, 80, 100, 100)
        p = c.paragraphs[0]
        r = p.add_run(h)
        r.bold = True
        r.font.name = "Arial"
        r.font.size = Pt(9.5)
        r.font.color.rgb = RGBColor(255, 255, 255)

    comp_rows = [
        ("1", "CI/CD Pipeline using Git, Maven/Gradle and Jenkins: Set up a version-controlled build pipeline for a REST API. Create a Git repo, use feature branching and merging, configure build/testing, integrate into a Jenkins job that pulls from SCM, triggers automatically on commit, executes build, archives artifacts, and add one CI enhancement.", "10"),
        ("2", "Configuration Management with Ansible and Deployment on Kubernetes: Write an Ansible playbook (using variables, handlers, and at least one role) to configure and deploy the application. Containerize with a multi-stage Dockerfile and write Kubernetes manifests (Deployment, Service, ConfigMap). Deploy on Minikube, demonstrate scaling (3->5->3), and add one deployment enhancement (rollback/probes/ConfigMap).", "10")
    ]
    for r_idx, row_data in enumerate(comp_rows, start=1):
        for c_idx, val in enumerate(row_data):
            c = t_comp.cell(r_idx, c_idx)
            set_cell_background(c, "F7F9FB" if r_idx % 2 == 0 else "FFFFFF")
            set_cell_margins(c, 70, 70, 100, 100)
            p = c.paragraphs[0]
            r = p.add_run(val)
            r.font.name = "Arial"
            r.font.size = Pt(9)

    doc.add_page_break()

    # 4. COMPONENT 1 REPORT
    p_c1 = doc.add_paragraph()
    style_heading(p_c1, "COMPONENT 1: CI/CD PIPELINE USING GIT, BUILD TOOL & JENKINS (10 MARKS)", 1, font_size=15)
    
    add_body_p(doc, "This activity implements an automated Continuous Integration (CI) pipeline for an enterprise Task and Workflow REST API microservice developed in Python 3.12 and Flask. The application source code is maintained under distributed Git version control employing strict feature-branching workflows and merge validation. A Jenkins Declarative Pipeline was engineered to automate repository polling, static code quality linting, and automated unit testing using Pytest, generating JUnit XML reports. Upon successful validation, the pipeline packages the application into release bundles and builds container images dynamically versioned with the Git commit SHA, archiving artifacts for complete build reproducibility and traceability.", "Abstract: ")

    add_body_p(doc, "DevOps culture bridges software development and system operations through end-to-end automation, shared ownership, and continuous feedback. Continuous Integration (CI) serves as the first automated safeguard in this pipeline. In this implementation, a modular Python REST API microservice was engineered with thread-safe in-memory task persistence, health checking, and telemetry metrics. Git manages isolated workspaces via branches, allowing non-disruptive development on feature/rest-api-endpoints before merging into main. Jenkins acts as the central orchestration engine, polling the repository automatically, executing static analysis and automated unit tests before packaging, building versioned release artifacts, and providing immediate feedback on commit health.", "Introduction: ")

    add_body_p(doc, "OS: Ubuntu 22.04 LTS (WSL2) / Windows 11 64-bit | Git 2.44.0 | Python 3.12.3 / Flask 3.1.3 / Gunicorn 21.2.0 | Pytest 9.2.0 / Flake8 7.1.0 | Jenkins 2.450 LTS | Public Repository: https://github.com/gautamrajesh/devops-todo-microservice-pipeline", "Development Environment: ")

    add_body_p(doc, "The repository was initialized locally with distinct branching hygiene. A feature branch named feature/rest-api-endpoints was branched off main, containing the endpoint implementations, in-memory repository, and test cases. The work was committed and merged back into main using a non-fast-forward merge (--no-ff) to explicitly record the branch bifurcation and merge node in the history.", "Step 1 - Git Repository & Branching: ")

    add_body_p(doc, "Dependencies are strictly pinned in requirements.txt (Flask, werkzeug, gunicorn, pytest, flake8). The build and test execution were validated locally prior to pipeline integration, running 11 automated test cases with zero warnings.", "Step 2 - Build Configuration & Automated Unit Tests: ")

    add_body_p(doc, "The Declarative Jenkins pipeline automates testing, code quality, packaging, and versioned Docker builds on every Git commit trigger using pollSCM('H/2 * * * *'). The pipeline manages 6 distinct stages: Checkout SCM -> Code Quality & Lint -> Automated Unit Tests -> Package Build Artifact -> Container Image Build & Versioning -> Smoke & Health Verification. In the post-build phase, the compressed artifact dist/*.tar.gz and JUnit XML reports are archived.", "Step 3 - Jenkins Declarative Pipeline: ")

    add_body_p(doc, "1. Automated Unit Tests in CI: Integrated a pre-build Pytest stage executing 11 unit tests covering all endpoints, schema validation, and health checks, emitting JUnit XML statistics.\n2. Image and Build Versioning: Release artifacts and Docker container images are automatically stamped with the build number and Git commit SHA (todo-api:14-19732cd), eliminating version collision.\n3. Dual-CI with GitHub Actions: Configured .github/workflows/ci.yml executing parallel test runs across Python 3.10, 3.11, and 3.12 matrices on all pushes and pull requests.", "Step 4 - CI Enhancements Implemented: ")

    add_body_p(doc, "The microservice was developed with explicit test isolation in tests/test_api.py. When code was committed and pushed to the remote repository, Jenkins detected the commit without manual intervention, executed PEP8 linting, ran the 11 unit tests, packaged the application into a compressed tarball, tagged the Docker container with the exact commit SHA, executed a smoke test against /health, and archived the resulting artifacts with cryptographic fingerprinting.", "Description of the Activity: ")

    # Insert Component 1 Screenshots
    p_c1_res = doc.add_paragraph()
    style_heading(p_c1_res, "Component 1 Verification Results & Screenshots", 2, font_size=13)

    screenshots_comp1 = [
        ("Figure 1: Git Branch & Commit History Graph (Showing Feature Branch & Merge)", r"C:\Users\gautu\SEM V\to-ag\dev-ops\report\screenshots\git_branch_history.png"),
        ("Figure 2: Automated Unit Test Suite Execution (11/11 Passed in 0.39s)", r"C:\Users\gautu\SEM V\to-ag\dev-ops\report\screenshots\pytest_results.png"),
        ("Figure 3: Jenkins Pipeline Stage View Dashboard (Builds #12, #13, #14 Succeeded)", r"C:\Users\gautu\SEM V\to-ag\dev-ops\report\screenshots\jenkins_pipeline_dashboard.png"),
        ("Figure 4: Jenkins Build Console Output Showing SCM Checkout, Lint, Test & Docker Tagging", r"C:\Users\gautu\SEM V\to-ag\dev-ops\report\screenshots\jenkins_build_console.png"),
        ("Figure 5: Jenkins Archived Build Artifacts & Commit SHA Fingerprint Verification", r"C:\Users\gautu\SEM V\to-ag\dev-ops\report\screenshots\archived_artifacts.png"),
        ("Figure 6: GitHub Actions CI Enhancement Matrix Run Across Python 3.10, 3.11, and 3.12", r"C:\Users\gautu\SEM V\to-ag\dev-ops\report\screenshots\github_actions_ci.png")
    ]
    add_screenshots_section(doc, screenshots_comp1)

    add_body_p(doc, "Component 1 proved how Git branching, automated unit testing, and Jenkins declarative pipelines eliminate human error from the build process. Automating testing and artifact versioning directly inside CI ensures that broken code is halted before deployment, while every binary is immutably tied back to its originating source commit.", "Component 1 Conclusion: ")

    doc.add_page_break()

    # 5. COMPONENT 2 REPORT
    p_c2 = doc.add_paragraph()
    style_heading(p_c2, "COMPONENT 2: CONFIGURATION MANAGEMENT (ANSIBLE) & KUBERNETES DEPLOYMENT (10 MARKS)", 1, font_size=15)

    add_body_p(doc, "Component 2 advances the containerized REST API microservice into automated server configuration, containerization, and Kubernetes cluster orchestration. An Ansible playbook was authored incorporating an inventory, reusable variables, event-driven handlers, and a modular role to configure system dependencies, deploy code into an isolated virtual environment, and manage the systemd service unit. The application was packaged using a multi-stage Dockerfile that eliminates compiler dependencies from the runtime image and enforces non-root container execution. The service was deployed to a local Kubernetes cluster with an initial 3-pod baseline, a NodePort service, and externalized configuration via a ConfigMap. Automated Liveness and Readiness probes actively monitor service health, horizontal pod scaling (3 -> 5 -> 3 replicas) was demonstrated in real time, and an automated rollback was proven using kubectl rollout undo.", "Abstract: ")

    add_body_p(doc, "While Continuous Integration validates application logic, Continuous Deployment and Configuration Management govern runtime stability and scalability. Ansible provides agentless, idempotent server automation, replacing fragile shell scripts with declarative playbooks and reusable roles. Kubernetes orchestrates containers at scale, managing pod lifecycle, traffic routing, health monitoring, and autoscaling. In this component, Ansible first provisions the host environment and deploys the systemd service unit. Next, the microservice is packaged into an optimized multi-stage Docker container and deployed across a Kubernetes cluster with self-healing health probes, demonstrating real-world scaling and zero-downtime rollback recovery.", "Introduction: ")

    add_body_p(doc, "Ansible 2.16.5 | Docker Engine 26.1.0 with Buildx | Kubernetes v1.30.0 (Minikube cluster) | Kubectl CLI v1.30.0 | Gunicorn 21.2.0 WSGI server (3 workers) | Base image: python:3.12-slim", "Development Environment: ")

    add_body_p(doc, "The configuration is organized under ansible/roles/todo_app. The tasks file creates a dedicated system user 'devops', sets up directory permissions (/opt/todo-api), installs dependencies in a virtual environment, deploys the systemd service template, and invokes handlers (Reload systemd daemon, Restart todo-app service) only when changes are made, demonstrating idempotency.", "Step 1 - Ansible Playbook & Roles: ")

    add_body_p(doc, "A Multi-Stage Dockerfile was engineered (Deployment Enhancement) to isolate build tooling from runtime binaries. Stage 1 ('builder') generates compiled Python wheels; Stage 2 ('runtime') starts from an ultra-lightweight python:3.12-slim base, copies the pre-built wheels, installs them without compiler bloat, and runs under a non-root UID 10001 (appuser) with an integrated healthcheck instruction. Final image size is only 138MB.", "Step 2 - Multi-Stage Containerization (Dockerfile): ")

    add_body_p(doc, "The microservice was deployed onto a local Kubernetes cluster using declarative manifests: ConfigMap (k8s/configmap.yaml) for externalizing settings (PORT, APP_ENV, LOG_LEVEL); Deployment (k8s/deployment.yaml) with 3 replicas, resource limits (256Mi), and automated Liveness and Readiness probes pointing at /health; and Service (k8s/service.yaml) exposing pods via NodePort on port 30080.", "Step 3 - Kubernetes Deployment, Service & ConfigMap: ")

    add_body_p(doc, "Horizontal pod autoscaling was tested by scaling from 3 to 5 replicas in real time using 'kubectl scale deployment todo-api-deployment --replicas=5'. Kubernetes instantly scheduled 2 new pods across the cluster, reaching 5 healthy running pods. After confirming traffic distribution, the deployment was scaled back down to 3 replicas.", "Step 4 - Kubernetes Horizontal Scaling Demonstration: ")

    add_body_p(doc, "1. ConfigMap for Externalized Settings: Configuration (PORT, APP_ENV, LOG_LEVEL) is injected into pods from todo-api-config without modifying Docker image layers.\n2. Liveness & Readiness Probes: Configured with httpGet on /health. The readinessProbe prevents incoming HTTP traffic until Gunicorn is fully loaded; the livenessProbe automatically restarts deadlocked containers.\n3. Multi-Stage Dockerfile: Drastically reduces container footprint and eliminates security attack surface from build utilities.\n4. Automated Rollback Demo: A faulty container image (todo-api:invalid-tag) was intentionally applied, causing ImagePullBackOff / Readiness failure. The command 'kubectl rollout undo deployment/todo-api-deployment' restored the service instantaneously without traffic interruption.", "Step 5 - Deployment Enhancements Implemented: ")

    # Insert Component 2 Screenshots
    p_c2_res = doc.add_paragraph()
    style_heading(p_c2_res, "Component 2 Verification Results & Screenshots", 2, font_size=13)

    screenshots_comp2 = [
        ("Figure 7: Ansible Playbook Run - Task Execution, Handlers & Health Check Verification", r"C:\Users\gautu\SEM V\to-ag\dev-ops\report\screenshots\ansible_playbook_run.png"),
        ("Figure 8: Docker Multi-Stage Image Build and Optimization (138MB Hardened Image)", r"C:\Users\gautu\SEM V\to-ag\dev-ops\report\screenshots\docker_build_run.png"),
        ("Figure 9: Kubernetes Cluster Baseline (3 Pods Running & NodePort 30080 Service)", r"C:\Users\gautu\SEM V\to-ag\dev-ops\report\screenshots\k8s_pods_initial.png"),
        ("Figure 10: Kubernetes Horizontal Scaling Demonstration (3 Replicas -> 5 Replicas -> 3 Replicas)", r"C:\Users\gautu\SEM V\to-ag\dev-ops\report\screenshots\k8s_scaling_demo.png"),
        ("Figure 11: HTTP Endpoint & Health Probe Verification (curl on /health and /api/todos)", r"C:\Users\gautu\SEM V\to-ag\dev-ops\report\screenshots\app_curl_verification.png"),
        ("Figure 12: Kubernetes Automated Rollback Demonstration (Zero-Downtime Rollout Undo)", r"C:\Users\gautu\SEM V\to-ag\dev-ops\report\screenshots\k8s_rollback_recovery.png")
    ]
    add_screenshots_section(doc, screenshots_comp2)

    add_body_p(doc, "Component 2 demonstrated how configuration management and container orchestration ensure resilience and elasticity. Ansible guarantees repeatable server states, while Kubernetes automates scaling, health probing, and instant rollback, providing a self-healing operational foundation.", "Component 2 Conclusion: ")

    doc.add_page_break()

    # 6. CONCLUSION, RESUME & REFERENCES
    p_h3 = doc.add_paragraph()
    style_heading(p_h3, "OVERALL CONCLUSION & RESUME FRAMING", 1, font_size=15)

    add_body_p(doc, "This project successfully realized a unified, fully automated DevOps delivery pipeline. By linking Git version control, Jenkins continuous integration, Ansible configuration management, Docker multi-stage containerization, and Kubernetes cluster orchestration, manual overhead was eliminated across all stages. Testing, image building, artifact versioning, server provisioning, and deployment scaling function in unison.", "Project Summary & Outcomes: ")

    t_res = doc.add_table(rows=3, cols=2)
    t_res.alignment = WD_TABLE_ALIGNMENT.CENTER
    res_data = [
        ("Component 1: Continuous Integration", "Automated build-and-test CI pipeline using Jenkins declarative pipelines and GitHub Actions triggered on Git push, integrating automated pytest unit testing, code quality linting, dynamic Git SHA versioning, and automated artifact archival."),
        ("Component 2: Ansible & Kubernetes Deployment", "Configured automated host provisioning with an Ansible role and handlers; containerized the service using a multi-stage Dockerfile and deployed to Kubernetes with ConfigMap configuration, liveness/readiness self-healing probes, zero-downtime scaling, and automated rollback support."),
        ("Pipeline Impact & Value", "Reduced deployment cycle time from hours to minutes, ensured 100% test pass verification prior to artifact publication, and achieved high availability through Kubernetes self-healing and zero-downtime rollback recovery.")
    ]
    for idx, (title, desc) in enumerate(res_data):
        row = t_res.rows[idx]
        c0, c1 = row.cells[0], row.cells[1]
        c0.width, c1.width = Inches(2.2), Inches(4.3)
        set_cell_background(c0, "EBF3FA")
        set_cell_background(c1, "FAFAFA")
        set_cell_margins(c0, 100, 100, 100, 100)
        set_cell_margins(c1, 100, 100, 100, 100)
        p0 = c0.paragraphs[0]
        r = p0.add_run(title)
        r.bold = True
        r.font.name = "Arial"
        r.font.size = Pt(9.5)
        p1 = c1.paragraphs[0]
        r = p1.add_run(desc)
        r.font.name = "Arial"
        r.font.size = Pt(9.5)

    doc.add_paragraph().paragraph_format.space_after = Pt(12)
    p_href = doc.add_paragraph()
    style_heading(p_href, "REFERENCES", 2, font_size=13)

    refs = [
        "1. Humble, J., & Farley, D. (2010). Continuous Delivery: Reliable Software Releases through Build, Test, and Deployment Automation. Addison-Wesley Professional.",
        "2. Davis, J., & Daniels, K. (2021). Effective DevOps: Building a Culture of Collaboration, Affinity, and Tooling. O'Reilly Media.",
        "3. Jenkins Project. (2024). Pipeline Syntax & Declarative Pipelines Documentation. https://www.jenkins.io/doc/book/pipeline/",
        "4. Red Hat Ansible Documentation. (2024). Roles and Handlers in Playbook Automation. https://docs.ansible.com/",
        "5. Kubernetes Documentation. (2024). Deployments, Services, ConfigMaps, and Pod Probes. https://kubernetes.io/docs/concepts/",
        "6. Docker Documentation. (2024). Use Multi-Stage Builds for Lightweight Container Images. https://docs.docker.com/build/building/multi-stage/",
        "7. GitHub Actions Documentation. (2024). Workflow syntax for GitHub Actions. https://docs.github.com/en/actions"
    ]
    for ref in refs:
        p_r = doc.add_paragraph()
        p_r.paragraph_format.space_before = Pt(0)
        p_r.paragraph_format.space_after = Pt(4)
        run = p_r.add_run(ref)
        run.font.name = "Arial"
        run.font.size = Pt(9.5)
        run.font.color.rgb = RGBColor(60, 60, 60)

    # Output paths
    output_paths = [
        r"C:\Users\gautu\SEM V\to-ag\dev-ops\DevOps_Course_Project_Report_1MS24CI045.docx",
        r"C:\Users\gautu\Downloads\DevOps_Course_Project_Report_1MS24CI045.docx",
        r"C:\Users\gautu\.gemini\antigravity\scratch\dev-ops\DevOps_Course_Project_Report_1MS24CI045.docx"
    ]
    for p in output_paths:
        os.makedirs(os.path.dirname(p), exist_ok=True)
        doc.save(p)
        print(f"[OK] Saved report to {p}")

if __name__ == "__main__":
    create_report()
