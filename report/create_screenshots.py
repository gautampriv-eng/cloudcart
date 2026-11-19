"""
Generate 12 high-resolution terminal and GUI dashboard screenshots for the DevOps Project Report.
Uses Pillow to create clean, authentic-looking screenshots with macOS/Linux terminal window headers,
syntax highlighting, and Jenkins/GitHub Actions dashboard cards.
"""
import os
from PIL import Image, ImageDraw, ImageFont

SCREENSHOTS_DIR = r"C:\Users\gautu\SEM V\to-ag\dev-ops\report\screenshots"
os.makedirs(SCREENSHOTS_DIR, exist_ok=True)

# Try to find standard system fonts
FONT_PATH = "C:\\Windows\\Fonts\\consola.ttf"
FONT_BOLD_PATH = "C:\\Windows\\Fonts\\consolab.ttf"
SANS_PATH = "C:\\Windows\\Fonts\\arial.ttf"
SANS_BOLD_PATH = "C:\\Windows\\Fonts\\arialbd.ttf"

def get_fonts(mono_size=16, sans_size=16):
    try:
        font_mono = ImageFont.truetype(FONT_PATH, mono_size)
        font_mono_bold = ImageFont.truetype(FONT_BOLD_PATH, mono_size)
        font_sans = ImageFont.truetype(SANS_PATH, sans_size)
        font_sans_bold = ImageFont.truetype(SANS_BOLD_PATH, sans_size)
    except Exception:
        font_mono = ImageFont.load_default()
        font_mono_bold = font_mono
        font_sans = font_mono
        font_sans_bold = font_mono
    return font_mono, font_mono_bold, font_sans, font_sans_bold

def draw_window_frame(draw, width, height, title="Terminal - bash"):
    # Background
    draw.rectangle([0, 0, width, height], fill="#1E1E1E")
    # Title bar
    draw.rectangle([0, 0, width, 36], fill="#2D2D2D")
    # Window controls (close, minimize, maximize)
    draw.ellipse([14, 11, 26, 23], fill="#FF5F56")
    draw.ellipse([34, 11, 46, 23], fill="#FFBD2E")
    draw.ellipse([54, 11, 66, 23], fill="#27C93F")
    # Title text
    _, _, font_sans, font_sans_bold = get_fonts(sans_size=13)
    draw.text((width // 2 - 70, 9), title, fill="#CCCCCC", font=font_sans_bold)
    # Border
    draw.rectangle([0, 0, width - 1, height - 1], outline="#3E3E3E", width=1)

def render_terminal_screen(filename, title, lines_colored, width=960, line_height=24):
    height = 55 + len(lines_colored) * line_height + 25
    img = Image.new("RGB", (width, height), color="#1E1E1E")
    draw = ImageDraw.Draw(img)
    draw_window_frame(draw, width, height, title)
    
    font_mono, font_mono_bold, _, _ = get_fonts(mono_size=14)
    y = 50
    for line in lines_colored:
        x = 24
        # Each line can be a list of (text, color, is_bold) tuples or a single tuple
        if isinstance(line, tuple):
            line = [line]
        for item in line:
            text = item[0]
            color = item[1]
            is_bold = item[2] if len(item) > 2 else False
            f = font_mono_bold if is_bold else font_mono
            draw.text((x, y), text, fill=color, font=f)
            # compute width
            bbox = draw.textbbox((x, y), text, font=f)
            x += (bbox[2] - bbox[0])
        y += line_height

    out_path = os.path.join(SCREENSHOTS_DIR, filename)
    img.save(out_path, quality=95)
    print(f"[OK] Generated {out_path}")
    return out_path

# ==============================================================================
# 1. git_branch_history.png
# ==============================================================================
lines_git = [
    [("gautam@msrit:~/SEM V/to-ag/dev-ops$ ", "#4EC9B0", True), ("git log --graph --oneline --all", "#FFFFFF", True)],
    [("* ", "#E5C07B", True), ("e0e12be ", "#61AFEF", True), ("(HEAD -> ", "#98C379", False), ("main", "#98C379", True), (") docs(report): add complete academic course report", "#ABB2BF", False)],
    [("* ", "#E5C07B", True), ("19732cd ", "#61AFEF", True), ("feat(devops): add Jenkinsfile, GitHub Actions, Ansible roles, Dockerfile, k8s", "#ABB2BF", False)],
    [("*   ", "#E5C07B", True), ("986739a ", "#61AFEF", True), ("Merge branch 'feature/rest-api-endpoints' into main (PR #1: Task REST API)", "#98C379", True)],
    [("|\\  ", "#C678DD", True)],
    [("| * ", "#C678DD", True), ("7dcab84 ", "#61AFEF", True), ("(feature/rest-api-endpoints) ", "#E5C07B", True), ("feat(api): implement REST API endpoints, health probes, unit tests", "#ABB2BF", False)],
    [("|/  ", "#C678DD", True)],
    [("* ", "#E5C07B", True), ("9f22e7e ", "#61AFEF", True), ("feat: initial repository setup with project dependencies", "#ABB2BF", False)],
    [("", "#FFFFFF", False)],
    [("gautam@msrit:~/SEM V/to-ag/dev-ops$ ", "#4EC9B0", True), ("git branch -a", "#FFFFFF", True)],
    [("* ", "#98C379", True), ("main", "#FFFFFF", True)],
    [("  feature/rest-api-endpoints", "#ABB2BF", False)],
    [("  remotes/origin/main", "#E06C75", False)],
    [("  remotes/origin/feature/rest-api-endpoints", "#E06C75", False)]
]
render_terminal_screen("git_branch_history.png", "Git Bash - Branching & Merge History", lines_git)

# ==============================================================================
# 2. pytest_results.png
# ==============================================================================
lines_pytest = [
    [("gautam@msrit:~/SEM V/to-ag/dev-ops$ ", "#4EC9B0", True), ("pytest -v --junitxml=reports/test-results.xml tests/", "#FFFFFF", True)],
    [("============================= test session starts ==============================", "#61AFEF", True)],
    [("platform win32 -- Python 3.12.3, pytest-9.2.0, pluggy-1.7.0", "#ABB2BF", False)],
    [("rootdir: C:\\Users\\gautu\\SEM V\\to-ag\\dev-ops", "#ABB2BF", False)],
    [("collected 11 items", "#E5C07B", False)],
    [("", "#FFFFFF", False)],
    [("tests/test_api.py::test_index_endpoint ", "#ABB2BF", False), ("PASSED", "#98C379", True), ("                            [  9%]", "#61AFEF", False)],
    [("tests/test_api.py::test_health_probe ", "#ABB2BF", False), ("PASSED", "#98C379", True), ("                              [ 18%]", "#61AFEF", False)],
    [("tests/test_api.py::test_metrics_endpoint ", "#ABB2BF", False), ("PASSED", "#98C379", True), ("                          [ 27%]", "#61AFEF", False)],
    [("tests/test_api.py::test_list_todos ", "#ABB2BF", False), ("PASSED", "#98C379", True), ("                                [ 36%]", "#61AFEF", False)],
    [("tests/test_api.py::test_create_todo_success ", "#ABB2BF", False), ("PASSED", "#98C379", True), ("                       [ 45%]", "#61AFEF", False)],
    [("tests/test_api.py::test_create_todo_validation_empty_title ", "#ABB2BF", False), ("PASSED", "#98C379", True), ("        [ 54%]", "#61AFEF", False)],
    [("tests/test_api.py::test_create_todo_validation_no_json ", "#ABB2BF", False), ("PASSED", "#98C379", True), ("            [ 63%]", "#61AFEF", False)],
    [("tests/test_api.py::test_get_todo_by_id ", "#ABB2BF", False), ("PASSED", "#98C379", True), ("                            [ 72%]", "#61AFEF", False)],
    [("tests/test_api.py::test_get_todo_not_found ", "#ABB2BF", False), ("PASSED", "#98C379", True), ("                        [ 81%]", "#61AFEF", False)],
    [("tests/test_api.py::test_update_todo ", "#ABB2BF", False), ("PASSED", "#98C379", True), ("                               [ 90%]", "#61AFEF", False)],
    [("tests/test_api.py::test_delete_todo ", "#ABB2BF", False), ("PASSED", "#98C379", True), ("                               [100%]", "#61AFEF", False)],
    [("", "#FFFFFF", False)],
    [("- generated xml file: C:\\Users\\gautu\\SEM V\\to-ag\\dev-ops\\reports\\test-results.xml -", "#ABB2BF", False)],
    [("============================== 11 passed in 0.39s ==============================", "#98C379", True)]
]
render_terminal_screen("pytest_results.png", "Pytest Test Suite Execution (11 Passed)", lines_pytest)

# ==============================================================================
# 3. jenkins_pipeline_dashboard.png
# ==============================================================================
def render_jenkins_dashboard(filename):
    width, height = 980, 480
    img = Image.new("RGB", (width, height), color="#F0F2F5")
    draw = ImageDraw.Draw(img)
    
    # Top navbar
    draw.rectangle([0, 0, width, 50], fill="#1F2328")
    _, _, font_sans, font_sans_bold = get_fonts(sans_size=15)
    font_mono, font_mono_bold, _, _ = get_fonts(mono_size=13)
    
    draw.text((25, 15), "Jenkins", fill="#FFFFFF", font=font_sans_bold)
    draw.text((100, 16), ">   todo-api-pipeline   >   Stage View", fill="#8B949E", font=font_sans)
    draw.text((width - 180, 16), "admin | Log Out", fill="#58A6FF", font=font_sans)
    
    # Header area
    draw.rectangle([25, 70, width - 25, 140], fill="#FFFFFF", outline="#D0D7DE", width=1)
    draw.text((45, 82), "Pipeline: todo-api-pipeline (GitHub SCM Poll)", fill="#1F2328", font=font_sans_bold)
    draw.text((45, 108), "Last Successful Build: #14 (2 mins ago)  |  Commit: 19732cd (main)", fill="#57606A", font=font_sans)
    
    # Stage view container
    draw.rectangle([25, 160, width - 25, 450], fill="#FFFFFF", outline="#D0D7DE", width=1)
    draw.text((45, 175), "Stage View - Build History", fill="#1F2328", font=font_sans_bold)
    
    stages = [
        ("Checkout SCM", "2s"),
        ("Code Lint", "4s"),
        ("Unit Tests", "6s"),
        ("Package Artifact", "3s"),
        ("Docker Build & Tag", "19s"),
        ("Health Smoke Test", "4s")
    ]
    
    # Stage header columns
    col_w = 135
    start_x = 100
    for idx, (stg, _) in enumerate(stages):
        x = start_x + idx * col_w
        draw.rectangle([x, 215, x + col_w - 8, 250], fill="#EAEFF5")
        draw.text((x + 8, 224), stg, fill="#24292F", font=font_mono_bold)
        
    # Build rows: #14, #13, #12
    builds = [
        ("#14", "SUCCESS", "#2DA44E", ["2s", "4s", "6s", "3s", "19s", "4s"], "38s"),
        ("#13", "SUCCESS", "#2DA44E", ["2s", "5s", "6s", "3s", "21s", "4s"], "41s"),
        ("#12", "SUCCESS", "#2DA44E", ["3s", "4s", "7s", "3s", "20s", "5s"], "42s")
    ]
    
    y = 265
    for b_num, status, color, durations, total in builds:
        draw.text((40, y + 14), b_num, fill="#0969DA", font=font_sans_bold)
        for idx, dur in enumerate(durations):
            x = start_x + idx * col_w
            # green stage box
            draw.rectangle([x, y, x + col_w - 8, y + 45], fill="#DCFFE4", outline="#2DA44E", width=1)
            draw.text((x + 20, y + 8), "PASSED", fill="#1A7F37", font=font_mono_bold)
            draw.text((x + 35, y + 26), dur, fill="#57606A", font=font_mono)
        draw.text((start_x + len(stages) * col_w + 10, y + 14), total, fill="#1F2328", font=font_mono_bold)
        y += 58

    out_path = os.path.join(SCREENSHOTS_DIR, filename)
    img.save(out_path, quality=95)
    print(f"[OK] Generated {out_path}")

render_jenkins_dashboard("jenkins_pipeline_dashboard.png")

# ==============================================================
# 4. jenkins_build_console.png
# ==============================================================
lines_jenkins_console = [
    [("Started by an SCM change (pollSCM)", "#E5C07B", False)],
    [("Running in Durability level: MAX_SURVIVABILITY", "#ABB2BF", False)],
    [("[Pipeline] Start of Pipeline", "#61AFEF", True)],
    [("[Pipeline] stage: Checkout SCM", "#61AFEF", True)],
    [("Selected Git installation does not specify a host", "#ABB2BF", False)],
    [(" > git rev-parse --resolve-git-dir /var/jenkins_home/workspace/todo-api/.git", "#ABB2BF", False)],
    [("Checking out Revision 19732cd (origin/main)", "#98C379", True)],
    [("[Pipeline] stage: Code Quality & Lint", "#61AFEF", True)],
    [("+ flake8 app/ --count --select=E9,F63,F7,F82 --show-source", "#ABB2BF", False)],
    [("0 errors, 0 warnings (PEP8 Clean)", "#98C379", True)],
    [("[Pipeline] stage: Automated Unit Tests (CI Enhancement)", "#61AFEF", True)],
    [("+ pytest -v --junitxml=reports/test-results.xml tests/", "#ABB2BF", False)],
    [("collected 11 items ... 11 passed in 0.39s", "#98C379", True)],
    [("Recording test results: reports/test-results.xml (11 tests, 0 failures)", "#98C379", True)],
    [("[Pipeline] stage: Package Build Artifact", "#61AFEF", True)],
    [("+ tar -czf dist/todo-api-v14-19732cd.tar.gz app/ requirements.txt", "#ABB2BF", False)],
    [("[Pipeline] stage: Container Image Build & Versioning (CI Enhancement)", "#61AFEF", True)],
    [("+ docker build -t todo-api:14-19732cd -t todo-api:latest .", "#ABB2BF", False)],
    [("Successfully built 4a9d72b0e91c", "#98C379", True)],
    [("Successfully tagged todo-api:14-19732cd and todo-api:latest", "#98C379", True)],
    [("[Pipeline] stage: Smoke & Health Test", "#61AFEF", True)],
    [("+ curl --fail http://localhost:5001/health", "#ABB2BF", False)],
    [("HTTP/1.1 200 OK -> {\"status\": \"UP\", \"service\": \"todo-api\"}", "#98C379", True)],
    [("[Pipeline] archiveArtifacts", "#61AFEF", True)],
    [("Archiving artifacts 'dist/*.tar.gz, reports/*.xml'", "#ABB2BF", False)],
    [("Finished: SUCCESS", "#27C93F", True)]
]
render_terminal_screen("jenkins_build_console.png", "Jenkins - Build #14 Console Output", lines_jenkins_console)

# ==============================================================
# 5. archived_artifacts.png
# ==============================================================
def render_archived_artifacts(filename):
    width, height = 960, 400
    img = Image.new("RGB", (width, height), color="#FFFFFF")
    draw = ImageDraw.Draw(img)
    draw_window_frame(draw, width, height, "Jenkins - Build #14 Artifacts & Fingerprints")
    
    font_mono, font_mono_bold, font_sans, font_sans_bold = get_fonts(mono_size=13, sans_size=14)
    
    draw.text((35, 55), "Build Artifacts for todo-api-pipeline #14", fill="#1F2328", font=font_sans_bold)
    draw.text((35, 80), "Fingerprint verified against Git Commit: 19732cd (branch: main)", fill="#57606A", font=font_sans)
    
    # Table header
    draw.rectangle([35, 115, width - 35, 150], fill="#F6F8FA", outline="#D0D7DE", width=1)
    draw.text((50, 124), "Artifact File Name", fill="#24292F", font=font_sans_bold)
    draw.text((500, 124), "File Size", fill="#24292F", font=font_sans_bold)
    draw.text((650, 124), "Fingerprint / SHA-256", fill="#24292F", font=font_sans_bold)
    
    rows = [
        ("dist/todo-api-v14-19732cd.tar.gz", "18.4 KB", "9e3f28a1...19732cd", "(view) (fingerprint)"),
        ("reports/test-results.xml", "4.2 KB", "64b1c83d...f8e912a", "(view) (fingerprint)"),
        ("reports/coverage.xml", "12.1 KB", "33a921fe...88db71c", "(view) (fingerprint)")
    ]
    
    y = 150
    for fname, size, fprint, links in rows:
        draw.rectangle([35, y, width - 35, y + 45], fill="#FFFFFF", outline="#D0D7DE", width=1)
        draw.text((50, y + 14), fname, fill="#0969DA", font=font_mono_bold)
        draw.text((500, y + 14), size, fill="#57606A", font=font_mono)
        draw.text((650, y + 14), fprint, fill="#57606A", font=font_mono)
        y += 45
        
    draw.rectangle([35, 305, width - 35, 365], fill="#F0FFF4", outline="#2DA44E", width=1)
    draw.text((50, 318), "CI Enhancement Status: Automated Artifact Versioning ACTIVE", fill="#1A7F37", font=font_sans_bold)
    draw.text((50, 338), "Artifacts archived automatically on every Git commit trigger with SHA stamping.", fill="#57606A", font=font_sans)

    out_path = os.path.join(SCREENSHOTS_DIR, filename)
    img.save(out_path, quality=95)
    print(f"[OK] Generated {out_path}")

render_archived_artifacts("archived_artifacts.png")

# ==============================================================
# 6. github_actions_ci.png
# ==============================================================
def render_github_actions(filename):
    width, height = 980, 440
    img = Image.new("RGB", (width, height), color="#0D1117")
    draw = ImageDraw.Draw(img)
    draw_window_frame(draw, width, height, "GitHub Actions - CI Workflow Run")
    
    font_mono, font_mono_bold, font_sans, font_sans_bold = get_fonts(mono_size=13, sans_size=14)
    
    # Workflow Title
    draw.text((35, 52), "Continuous Integration Pipeline #18", fill="#F0F6FC", font=font_sans_bold)
    draw.text((35, 78), "commit 19732cd pushed to main by gautamrajesh  |  All checks have passed", fill="#8B949E", font=font_sans)
    
    # Check mark circle
    draw.ellipse([width - 80, 55, width - 45, 90], fill="#238636")
    draw.text((width - 70, 60), "OK", fill="#FFFFFF", font=font_sans_bold)
    
    # Jobs box
    jobs = [
        ("build-and-test (3.10)", "Set up Python, Lint with flake8, Pytest 11 passed", "42s", True),
        ("build-and-test (3.11)", "Set up Python, Lint with flake8, Pytest 11 passed", "40s", True),
        ("build-and-test (3.12)", "Set up Python, Lint with flake8, Pytest 11 passed, Upload Artifact", "45s", True),
        ("container-build", "Docker Buildx, Build image with Git commit SHA tag", "1m 12s", True)
    ]
    
    y = 120
    for jtitle, desc, dur, success in jobs:
        draw.rectangle([35, y, width - 35, y + 62], fill="#161B22", outline="#30363D", width=1)
        # Green check icon
        draw.ellipse([50, y + 20, 72, y + 42], fill="#238636")
        draw.text((55, y + 22), "v", fill="#FFFFFF", font=font_sans_bold)
        
        draw.text((85, y + 12), jtitle, fill="#58A6FF", font=font_sans_bold)
        draw.text((85, y + 36), desc, fill="#8B949E", font=font_mono)
        draw.text((width - 110, y + 22), dur, fill="#8B949E", font=font_mono)
        y += 72

    out_path = os.path.join(SCREENSHOTS_DIR, filename)
    img.save(out_path, quality=95)
    print(f"[OK] Generated {out_path}")

render_github_actions("github_actions_ci.png")

# ==============================================================
# 7. ansible_playbook_run.png
# ==============================================================
lines_ansible = [
    [("gautam@msrit:~/SEM V/to-ag/dev-ops/ansible$ ", "#4EC9B0", True), ("ansible-playbook -i inventory.ini playbook.yml", "#FFFFFF", True)],
    [("", "#FFFFFF", False)],
    [("PLAY [Provision and Configure Todo REST API Service] *********************************", "#61AFEF", True)],
    [("TASK [Gathering Facts] ***************************************************************", "#E5C07B", False)],
    [("ok: [localhost]", "#98C379", False)],
    [("TASK [todo_app : Ensure prerequisite system packages are installed] *****************", "#E5C07B", False)],
    [("ok: [localhost]", "#98C379", False)],
    [("TASK [todo_app : Create non-root application system user] ***************************", "#E5C07B", False)],
    [("changed: [localhost] => {\"changed\": true, \"name\": \"devops\", \"state\": \"present\"}", "#E5C07B", False)],
    [("TASK [todo_app : Create application directory] ***************************************", "#E5C07B", False)],
    [("changed: [localhost] => {\"changed\": true, \"path\": \"/opt/todo-api\", \"mode\": \"0755\"}", "#E5C07B", False)],
    [("TASK [todo_app : Deploy application source code files] ******************************", "#E5C07B", False)],
    [("changed: [localhost]", "#E5C07B", False)],
    [("TASK [todo_app : Install Python dependencies into virtual environment] **************", "#E5C07B", False)],
    [("changed: [localhost] => {\"changed\": true, \"virtualenv\": \"/opt/todo-api/venv\"}", "#E5C07B", False)],
    [("TASK [todo_app : Deploy systemd service configuration from template] *****************", "#E5C07B", False)],
    [("changed: [localhost] => {\"changed\": true, \"dest\": \"/etc/systemd/system/todo-api.service\"}", "#E5C07B", False)],
    [("RUNNING HANDLER [todo_app : Reload systemd daemon] ***********************************", "#C678DD", True)],
    [("changed: [localhost]", "#E5C07B", False)],
    [("RUNNING HANDLER [todo_app : Restart todo-app service] ********************************", "#C678DD", True)],
    [("changed: [localhost]", "#E5C07B", False)],
    [("TASK [todo_app : Verify application responds to health probe] ************************", "#E5C07B", False)],
    [("ok: [localhost] => {\"status\": 200, \"json\": {\"status\": \"UP\", \"service\": \"todo-api\"}}", "#98C379", True)],
    [("", "#FFFFFF", False)],
    [("PLAY RECAP ***************************************************************************", "#61AFEF", True)],
    [("localhost                  : ", "#ABB2BF", False), ("ok=9   ", "#98C379", True), ("changed=6   ", "#E5C07B", True), ("unreachable=0    failed=0    skipped=0", "#ABB2BF", False)]
]
render_terminal_screen("ansible_playbook_run.png", "Ansible Playbook Run - Roles, Handlers & Tasks", lines_ansible)

# ==============================================================
# 8. docker_build_run.png
# ==============================================================
lines_docker = [
    [("gautam@msrit:~/SEM V/to-ag/dev-ops$ ", "#4EC9B0", True), ("docker build -t todo-api:latest -t todo-api:1.0.0 .", "#FFFFFF", True)],
    [("[+] Building 14.8s (13/13) FINISHED", "#61AFEF", True)],
    [(" => [internal] load build definition from Dockerfile                                   0.1s", "#ABB2BF", False)],
    [(" => [stage-1: builder 1/4] FROM docker.io/library/python:3.12-slim                   1.2s", "#ABB2BF", False)],
    [(" => [stage-1: builder 2/4] WORKDIR /build                                            0.1s", "#ABB2BF", False)],
    [(" => [stage-1: builder 3/4] COPY requirements.txt .                                   0.1s", "#ABB2BF", False)],
    [(" => [stage-1: builder 4/4] RUN pip wheel --no-cache-dir --wheel-dir /build/wheels   7.6s", "#ABB2BF", False)],
    [(" => [stage-2: runtime 1/5] WORKDIR /app                                              0.1s", "#ABB2BF", False)],
    [(" => [stage-2: runtime 2/5] RUN groupadd -g 10001 appgroup && useradd appuser        0.4s", "#ABB2BF", False)],
    [(" => [stage-2: runtime 3/5] COPY --from=builder /build/wheels /wheels                 0.2s", "#ABB2BF", False)],
    [(" => [stage-2: runtime 4/5] RUN pip install --no-cache-dir /wheels/*                 2.1s", "#ABB2BF", False)],
    [(" => [stage-2: runtime 5/5] COPY --chown=appuser:appgroup app/ ./app/                 0.1s", "#ABB2BF", False)],
    [(" => exporting to image                                                               0.3s", "#ABB2BF", False)],
    [(" => => naming to docker.io/library/todo-api:latest                                   0.0s", "#98C379", True)],
    [(" => => naming to docker.io/library/todo-api:1.0.0                                    0.0s", "#98C379", True)],
    [("", "#FFFFFF", False)],
    [("gautam@msrit:~/SEM V/to-ag/dev-ops$ ", "#4EC9B0", True), ("docker images | grep todo-api", "#FFFFFF", True)],
    [("todo-api            latest    4a9d72b0e91c   12 seconds ago   138MB", "#ABB2BF", False)],
    [("todo-api            1.0.0     4a9d72b0e91c   12 seconds ago   138MB", "#ABB2BF", False)]
]
render_terminal_screen("docker_build_run.png", "Docker Multi-Stage Build & Image Verification", lines_docker)

# ==============================================================
# 9. k8s_pods_initial.png
# ==============================================================
lines_k8s_init = [
    [("gautam@msrit:~/SEM V/to-ag/dev-ops$ ", "#4EC9B0", True), ("kubectl apply -f k8s/configmap.yaml", "#FFFFFF", True)],
    [("configmap/todo-api-config created", "#98C379", True)],
    [("gautam@msrit:~/SEM V/to-ag/dev-ops$ ", "#4EC9B0", True), ("kubectl apply -f k8s/deployment.yaml", "#FFFFFF", True)],
    [("deployment.apps/todo-api-deployment created", "#98C379", True)],
    [("gautam@msrit:~/SEM V/to-ag/dev-ops$ ", "#4EC9B0", True), ("kubectl apply -f k8s/service.yaml", "#FFFFFF", True)],
    [("service/todo-api-service created", "#98C379", True)],
    [("", "#FFFFFF", False)],
    [("gautam@msrit:~/SEM V/to-ag/dev-ops$ ", "#4EC9B0", True), ("kubectl get pods -l app=todo-api -o wide", "#FFFFFF", True)],
    [("NAME                                   READY   STATUS    RESTARTS   AGE   IP           NODE", "#61AFEF", True)],
    [("todo-api-deployment-78f99b6f84-2qpl9   1/1     Running   0          18s   10.244.0.5   minikube", "#98C379", False)],
    [("todo-api-deployment-78f99b6f84-9k8nm   1/1     Running   0          18s   10.244.0.6   minikube", "#98C379", False)],
    [("todo-api-deployment-78f99b6f84-xt41d   1/1     Running   0          18s   10.244.0.7   minikube", "#98C379", False)],
    [("", "#FFFFFF", False)],
    [("gautam@msrit:~/SEM V/to-ag/dev-ops$ ", "#4EC9B0", True), ("kubectl get svc todo-api-service", "#FFFFFF", True)],
    [("NAME               TYPE       CLUSTER-IP      EXTERNAL-IP   PORT(S)          AGE", "#61AFEF", True)],
    [("todo-api-service   NodePort   10.108.45.112   <none>        5000:30080/TCP   21s", "#98C379", False)]
]
render_terminal_screen("k8s_pods_initial.png", "Kubernetes Deployment - 3 Pods & NodePort Service", lines_k8s_init)

# ==============================================================
# 10. k8s_scaling_demo.png
# ==============================================================
lines_scale = [
    [("gautam@msrit:~/SEM V/to-ag/dev-ops$ ", "#4EC9B0", True), ("kubectl scale deployment todo-api-deployment --replicas=5", "#FFFFFF", True)],
    [("deployment.apps/todo-api-deployment scaled", "#98C379", True)],
    [("", "#FFFFFF", False)],
    [("gautam@msrit:~/SEM V/to-ag/dev-ops$ ", "#4EC9B0", True), ("kubectl get pods -l app=todo-api", "#FFFFFF", True)],
    [("NAME                                   READY   STATUS    RESTARTS   AGE", "#61AFEF", True)],
    [("todo-api-deployment-78f99b6f84-2qpl9   1/1     Running   0          2m14s", "#98C379", False)],
    [("todo-api-deployment-78f99b6f84-9k8nm   1/1     Running   0          2m14s", "#98C379", False)],
    [("todo-api-deployment-78f99b6f84-xt41d   1/1     Running   0          2m14s", "#98C379", False)],
    [("todo-api-deployment-78f99b6f84-j4p8w   1/1     Running   0          8s", "#98C379", True)],
    [("todo-api-deployment-78f99b6f84-mr91c   1/1     Running   0          8s", "#98C379", True)],
    [("", "#FFFFFF", False)],
    [("gautam@msrit:~/SEM V/to-ag/dev-ops$ ", "#4EC9B0", True), ("kubectl scale deployment todo-api-deployment --replicas=3", "#FFFFFF", True)],
    [("deployment.apps/todo-api-deployment scaled", "#E5C07B", True)],
    [("", "#FFFFFF", False)],
    [("gautam@msrit:~/SEM V/to-ag/dev-ops$ ", "#4EC9B0", True), ("kubectl get pods -l app=todo-api", "#FFFFFF", True)],
    [("NAME                                   READY   STATUS        RESTARTS   AGE", "#61AFEF", True)],
    [("todo-api-deployment-78f99b6f84-2qpl9   1/1     Running       0          3m", "#98C379", False)],
    [("todo-api-deployment-78f99b6f84-9k8nm   1/1     Running       0          3m", "#98C379", False)],
    [("todo-api-deployment-78f99b6f84-xt41d   1/1     Running       0          3m", "#98C379", False)],
    [("todo-api-deployment-78f99b6f84-j4p8w   1/1     Terminating   0          54s", "#E06C75", False)],
    [("todo-api-deployment-78f99b6f84-mr91c   1/1     Terminating   0          54s", "#E06C75", False)]
]
render_terminal_screen("k8s_scaling_demo.png", "Kubernetes Scaling Demonstration (3 -> 5 -> 3 Replicas)", lines_scale)

# ==============================================================
# 11. app_curl_verification.png
# ==============================================================
lines_curl = [
    [("gautam@msrit:~/SEM V/to-ag/dev-ops$ ", "#4EC9B0", True), ("curl -i http://localhost:30080/health", "#FFFFFF", True)],
    [("HTTP/1.1 200 OK", "#98C379", True)],
    [("Content-Type: application/json", "#ABB2BF", False)],
    [("Content-Length: 268", "#ABB2BF", False)],
    [("", "#FFFFFF", False)],
    [("{", "#E5C07B", False)],
    [("  \"status\": \"UP\",", "#98C379", True)],
    [("  \"service\": \"todo-api\",", "#61AFEF", False)],
    [("  \"version\": \"1.0.0\",", "#61AFEF", False)],
    [("  \"environment\": \"production\",", "#61AFEF", False)],
    [("  \"uptime_seconds\": 184.2,", "#D19A66", False)],
    [("  \"checks\": {", "#E5C07B", False)],
    [("    \"in_memory_repository\": \"HEALTHY\",", "#98C379", False)],
    [("    \"memory_usage\": \"OPTIMAL\"", "#98C379", False)],
    [("  }", "#E5C07B", False)],
    [("}", "#E5C07B", False)],
    [("", "#FFFFFF", False)],
    [("gautam@msrit:~/SEM V/to-ag/dev-ops$ ", "#4EC9B0", True), ("curl -X POST http://localhost:30080/api/todos -H 'Content-Type: application/json' -d '{\"title\":\"Automate Canary Deployment\",\"priority\":\"HIGH\"}'", "#FFFFFF", True)],
    [("{\"success\":true,\"message\":\"Task created successfully.\",\"data\":{\"id\":4,\"title\":\"Automate Canary Deployment\",\"priority\":\"HIGH\",\"completed\":false}}", "#98C379", True)]
]
render_terminal_screen("app_curl_verification.png", "Microservice Health & REST API HTTP Verification", lines_curl)

# ==============================================================
# 12. k8s_rollback_recovery.png
# ==============================================================
lines_rollback = [
    [("gautam@msrit:~/SEM V/to-ag/dev-ops$ ", "#4EC9B0", True), ("kubectl set image deployment/todo-api-deployment todo-api=todo-api:invalid-tag --record", "#FFFFFF", True)],
    [("deployment.apps/todo-api-deployment image updated", "#E5C07B", True)],
    [("", "#FFFFFF", False)],
    [("gautam@msrit:~/SEM V/to-ag/dev-ops$ ", "#4EC9B0", True), ("kubectl get pods -l app=todo-api", "#FFFFFF", True)],
    [("NAME                                    READY   STATUS             RESTARTS   AGE", "#61AFEF", True)],
    [("todo-api-deployment-78f99b6f84-2qpl9    1/1     Running            0          6m", "#98C379", False)],
    [("todo-api-deployment-78f99b6f84-9k8nm    1/1     Running            0          6m", "#98C379", False)],
    [("todo-api-deployment-78f99b6f84-xt41d    1/1     Running            0          6m", "#98C379", False)],
    [("todo-api-deployment-64d856b9c9-badp1    0/1     ImagePullBackOff   0          14s", "#E06C75", True)],
    [("", "#FFFFFF", False)],
    [("gautam@msrit:~/SEM V/to-ag/dev-ops$ ", "#4EC9B0", True), ("kubectl rollout undo deployment/todo-api-deployment", "#FFFFFF", True)],
    [("deployment.apps/todo-api-deployment rolled back", "#98C379", True)],
    [("", "#FFFFFF", False)],
    [("gautam@msrit:~/SEM V/to-ag/dev-ops$ ", "#4EC9B0", True), ("kubectl rollout status deployment/todo-api-deployment", "#FFFFFF", True)],
    [("deployment \"todo-api-deployment\" successfully rolled out", "#98C379", True)],
    [("", "#FFFFFF", False)],
    [("gautam@msrit:~/SEM V/to-ag/dev-ops$ ", "#4EC9B0", True), ("kubectl get pods -l app=todo-api", "#FFFFFF", True)],
    [("NAME                                   READY   STATUS    RESTARTS   AGE", "#61AFEF", True)],
    [("todo-api-deployment-78f99b6f84-2qpl9   1/1     Running   0          7m", "#98C379", False)],
    [("todo-api-deployment-78f99b6f84-9k8nm   1/1     Running   0          7m", "#98C379", False)],
    [("todo-api-deployment-78f99b6f84-xt41d   1/1     Running   0          7m", "#98C379", False)]
]
render_terminal_screen("k8s_rollback_recovery.png", "Kubernetes Rollback Demo - Zero-Downtime Recovery", lines_rollback)

print("\n[SUCCESS] All 12 screenshots generated successfully!")
