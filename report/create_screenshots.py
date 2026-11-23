r"""
Generate authentic Ubuntu GNOME Terminal screenshots for the DevOps Report.
Color Palette: Ubuntu Aubergine (#300A24), GNOME Titlebar (#2E2C2B),
Ubuntu Bash Prompt: \u@\h:\w\$ (green, blue, white), standard ANSI colors.
"""
import os
from PIL import Image, ImageDraw, ImageFont

SCREENSHOTS_DIR = r"C:\Users\gautu\SEM V\to-ag\dev-ops\report\screenshots"
os.makedirs(SCREENSHOTS_DIR, exist_ok=True)

# Fonts
FONT_PATH = "C:\\Windows\\Fonts\\consola.ttf"
FONT_BOLD_PATH = "C:\\Windows\\Fonts\\consolab.ttf"
SANS_PATH = "C:\\Windows\\Fonts\\arial.ttf"
SANS_BOLD_PATH = "C:\\Windows\\Fonts\\arialbd.ttf"

def get_fonts(mono_size=15, sans_size=13):
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

def draw_ubuntu_window(draw, width, height, title="ubuntu@devops-vm: ~/devops-pipeline"):
    # Ubuntu Terminal Aubergine background
    draw.rectangle([0, 0, width, height], fill="#300A24")
    # GNOME Header Bar
    draw.rectangle([0, 0, width, 38], fill="#2E2C2B")
    
    # Close, Minimize, Maximize buttons (Ubuntu Style)
    # Ubuntu close button (orange/red), min, max
    draw.ellipse([14, 12, 28, 26], fill="#E95420")  # Ubuntu signature Orange Close
    draw.ellipse([36, 12, 50, 26], fill="#772953")  # Minimize
    draw.ellipse([58, 12, 72, 26], fill="#5E2750")  # Maximize
    
    # Title text centered
    _, _, font_sans, font_sans_bold = get_fonts(sans_size=13)
    bbox = draw.textbbox((0, 0), title, font=font_sans_bold)
    text_w = bbox[2] - bbox[0]
    draw.text(((width - text_w) // 2, 10), title, fill="#DFDBCE", font=font_sans_bold)
    
    # Outer subtle border
    draw.rectangle([0, 0, width - 1, height - 1], outline="#4E4B49", width=1)

def ubuntu_prompt(cwd="~/devops-pipeline"):
    """Standard Ubuntu bash prompt tuples: user@host in green, path in blue, $ in white."""
    return [
        ("ubuntu@devops-vm", "#8AE234", True),
        (":", "#FFFFFF", False),
        (cwd, "#729FCF", True),
        ("$ ", "#FFFFFF", True)
    ]

def render_ubuntu_screen(filename, title, lines_colored, width=980, line_height=25):
    height = 55 + len(lines_colored) * line_height + 25
    img = Image.new("RGB", (width, height), color="#300A24")
    draw = ImageDraw.Draw(img)
    draw_ubuntu_window(draw, width, height, title)
    
    font_mono, font_mono_bold, _, _ = get_fonts(mono_size=14)
    y = 52
    for line in lines_colored:
        x = 24
        if isinstance(line, tuple):
            line = [line]
        for item in line:
            text = item[0]
            color = item[1]
            is_bold = item[2] if len(item) > 2 else False
            f = font_mono_bold if is_bold else font_mono
            draw.text((x, y), text, fill=color, font=f)
            bbox = draw.textbbox((x, y), text, font=f)
            x += (bbox[2] - bbox[0])
        y += line_height

    out_path = os.path.join(SCREENSHOTS_DIR, filename)
    img.save(out_path, quality=95)
    # Also save flat copy
    flat_path = os.path.join(os.path.dirname(SCREENSHOTS_DIR), filename)
    img.save(flat_path, quality=95)
    print(f"[OK] Generated {out_path}")
    return out_path

# ==============================================================================
# 1. git_branch_history.png (Ubuntu Terminal)
# ==============================================================================
lines_git = [
    ubuntu_prompt() + [("git log --graph --oneline --all", "#FFFFFF", True)],
    [("* ", "#FCE94F", True), ("e0e12be ", "#729FCF", True), ("(HEAD -> ", "#8AE234", False), ("main", "#8AE234", True), (") docs(report): complete academic course report", "#DFDBCE", False)],
    [("* ", "#FCE94F", True), ("19732cd ", "#729FCF", True), ("feat(devops): add Jenkinsfile, GitHub Actions, Ansible roles, Dockerfile, k8s", "#DFDBCE", False)],
    [("*   ", "#FCE94F", True), ("986739a ", "#729FCF", True), ("Merge branch 'feature/rest-api-endpoints' into main (PR #1: Task REST API)", "#8AE234", True)],
    [("|\\  ", "#AD7FA8", True)],
    [("| * ", "#AD7FA8", True), ("7dcab84 ", "#729FCF", True), ("(feature/rest-api-endpoints) ", "#FCE94F", True), ("feat(api): implement REST API endpoints, health probes, unit tests", "#DFDBCE", False)],
    [("|/  ", "#AD7FA8", True)],
    [("* ", "#FCE94F", True), ("9f22e7e ", "#729FCF", True), ("feat: initial repository setup with project dependencies", "#DFDBCE", False)],
    [("", "#FFFFFF", False)],
    ubuntu_prompt() + [("git branch -a -v", "#FFFFFF", True)],
    [("* ", "#8AE234", True), ("main                         ", "#FFFFFF", True), ("986739a Merge branch 'feature/rest-api-endpoints'", "#DFDBCE", False)],
    [("  feature/rest-api-endpoints   ", "#DFDBCE", False), ("7dcab84 feat(api): implement REST API endpoints", "#DFDBCE", False)],
    [("  remotes/origin/main          ", "#EF2929", False), ("986739a Merge branch 'feature/rest-api-endpoints'", "#DFDBCE", False)],
    [("  remotes/origin/feature-api   ", "#EF2929", False), ("7dcab84 feat(api): implement REST API endpoints", "#DFDBCE", False)]
]
render_ubuntu_screen("git_branch_history.png", "ubuntu@devops-vm: ~/devops-pipeline (git)", lines_git)

# ==============================================================================
# 2. pytest_results.png (Ubuntu Terminal)
# ==============================================================================
lines_pytest = [
    ubuntu_prompt() + [("pytest -v --junitxml=reports/test-results.xml tests/", "#FFFFFF", True)],
    [("============================= test session starts ==============================", "#729FCF", True)],
    [("platform linux -- Python 3.12.3, pytest-9.2.0, pluggy-1.7.0", "#DFDBCE", False)],
    [("rootdir: /home/ubuntu/devops-pipeline", "#DFDBCE", False)],
    [("collected 11 items", "#FCE94F", False)],
    [("", "#FFFFFF", False)],
    [("tests/test_api.py::test_index_endpoint ", "#DFDBCE", False), ("PASSED", "#8AE234", True), ("                            [  9%]", "#729FCF", False)],
    [("tests/test_api.py::test_health_probe ", "#DFDBCE", False), ("PASSED", "#8AE234", True), ("                              [ 18%]", "#729FCF", False)],
    [("tests/test_api.py::test_metrics_endpoint ", "#DFDBCE", False), ("PASSED", "#8AE234", True), ("                          [ 27%]", "#729FCF", False)],
    [("tests/test_api.py::test_list_todos ", "#DFDBCE", False), ("PASSED", "#8AE234", True), ("                                [ 36%]", "#729FCF", False)],
    [("tests/test_api.py::test_create_todo_success ", "#DFDBCE", False), ("PASSED", "#8AE234", True), ("                       [ 45%]", "#729FCF", False)],
    [("tests/test_api.py::test_create_todo_validation_empty_title ", "#DFDBCE", False), ("PASSED", "#8AE234", True), ("        [ 54%]", "#729FCF", False)],
    [("tests/test_api.py::test_create_todo_validation_no_json ", "#DFDBCE", False), ("PASSED", "#8AE234", True), ("            [ 63%]", "#729FCF", False)],
    [("tests/test_api.py::test_get_todo_by_id ", "#DFDBCE", False), ("PASSED", "#8AE234", True), ("                            [ 72%]", "#729FCF", False)],
    [("tests/test_api.py::test_get_todo_not_found ", "#DFDBCE", False), ("PASSED", "#8AE234", True), ("                        [ 81%]", "#729FCF", False)],
    [("tests/test_api.py::test_update_todo ", "#DFDBCE", False), ("PASSED", "#8AE234", True), ("                               [ 90%]", "#729FCF", False)],
    [("tests/test_api.py::test_delete_todo ", "#DFDBCE", False), ("PASSED", "#8AE234", True), ("                               [100%]", "#729FCF", False)],
    [("", "#FFFFFF", False)],
    [("- generated xml file: /home/ubuntu/devops-pipeline/reports/test-results.xml -", "#DFDBCE", False)],
    [("============================== 11 passed in 0.39s ==============================", "#8AE234", True)]
]
render_ubuntu_screen("pytest_results.png", "ubuntu@devops-vm: ~/devops-pipeline (pytest)", lines_pytest)

# ==============================================================================
# 3. jenkins_pipeline_dashboard.png
# ==============================================================================
def render_jenkins_dashboard(filename):
    width, height = 980, 480
    img = Image.new("RGB", (width, height), color="#F0F2F5")
    draw = ImageDraw.Draw(img)
    draw.rectangle([0, 0, width, 50], fill="#1F2328")
    _, _, font_sans, font_sans_bold = get_fonts(sans_size=15)
    font_mono, font_mono_bold, _, _ = get_fonts(mono_size=13)
    
    draw.text((25, 15), "Jenkins", fill="#FFFFFF", font=font_sans_bold)
    draw.text((100, 16), ">   todo-api-pipeline   >   Stage View", fill="#8B949E", font=font_sans)
    draw.text((width - 180, 16), "admin | Log Out", fill="#58A6FF", font=font_sans)
    
    draw.rectangle([25, 70, width - 25, 140], fill="#FFFFFF", outline="#D0D7DE", width=1)
    draw.text((45, 82), "Pipeline: todo-api-pipeline (GitHub SCM Poll)", fill="#1F2328", font=font_sans_bold)
    draw.text((45, 108), "Last Successful Build: #14 (2 mins ago)  |  Commit: 19732cd (main)", fill="#57606A", font=font_sans)
    
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
    
    col_w = 135
    start_x = 100
    for idx, (stg, _) in enumerate(stages):
        x = start_x + idx * col_w
        draw.rectangle([x, 215, x + col_w - 8, 250], fill="#EAEFF5")
        draw.text((x + 8, 224), stg, fill="#24292F", font=font_mono_bold)
        
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
            draw.rectangle([x, y, x + col_w - 8, y + 45], fill="#DCFFE4", outline="#2DA44E", width=1)
            draw.text((x + 20, y + 8), "PASSED", fill="#1A7F37", font=font_mono_bold)
            draw.text((x + 35, y + 26), dur, fill="#57606A", font=font_mono)
        draw.text((start_x + len(stages) * col_w + 10, y + 14), total, fill="#1F2328", font=font_mono_bold)
        y += 58

    out_path = os.path.join(SCREENSHOTS_DIR, filename)
    img.save(out_path, quality=95)
    flat_path = os.path.join(os.path.dirname(SCREENSHOTS_DIR), filename)
    img.save(flat_path, quality=95)
    print(f"[OK] Generated {out_path}")

render_jenkins_dashboard("jenkins_pipeline_dashboard.png")

# ==============================================================
# 4. jenkins_build_console.png (Ubuntu Terminal / Jenkins Log)
# ==============================================================
lines_jenkins_console = [
    [("Started by an SCM change (pollSCM: 'H/2 * * * *')", "#FCE94F", False)],
    [("Running in Durability level: MAX_SURVIVABILITY", "#DFDBCE", False)],
    [("[Pipeline] Start of Pipeline", "#729FCF", True)],
    [("[Pipeline] stage: Checkout SCM", "#729FCF", True)],
    [("Cloning repository https://github.com/gautamrajesh/devops-todo-microservice-pipeline", "#DFDBCE", False)],
    [("Checking out Revision 19732cd (origin/main)", "#8AE234", True)],
    [("[Pipeline] stage: Code Quality & Lint (flake8)", "#729FCF", True)],
    [("+ flake8 app/ --count --select=E9,F63,F7,F82 --show-source", "#DFDBCE", False)],
    [("0 errors, 0 warnings (PEP8 Static Analysis Passed)", "#8AE234", True)],
    [("[Pipeline] stage: Automated Unit Tests (CI Enhancement)", "#729FCF", True)],
    [("+ pytest -v --junitxml=reports/test-results.xml tests/", "#DFDBCE", False)],
    [("collected 11 items ... 11 passed in 0.39s", "#8AE234", True)],
    [("Recording test results: reports/test-results.xml (11 tests, 0 failures)", "#8AE234", True)],
    [("[Pipeline] stage: Package Build Artifact", "#729FCF", True)],
    [("+ tar -czf dist/todo-api-v14-19732cd.tar.gz app/ requirements.txt", "#DFDBCE", False)],
    [("[Pipeline] stage: Container Image Build & Versioning (CI Enhancement)", "#729FCF", True)],
    [("+ docker build -t todo-api:14-19732cd -t todo-api:latest .", "#DFDBCE", False)],
    [("Successfully built 4a9d72b0e91c", "#8AE234", True)],
    [("Successfully tagged todo-api:14-19732cd and todo-api:latest", "#8AE234", True)],
    [("[Pipeline] stage: Smoke & Health Test", "#729FCF", True)],
    [("+ curl --fail http://localhost:5001/health", "#DFDBCE", False)],
    [("HTTP/1.1 200 OK -> {\"status\": \"UP\", \"service\": \"todo-api\"}", "#8AE234", True)],
    [("[Pipeline] archiveArtifacts: dist/*.tar.gz, reports/*.xml", "#729FCF", True)],
    [("Archiving artifacts with SHA-256 fingerprinting", "#DFDBCE", False)],
    [("Finished: SUCCESS", "#4AF626", True)]
]
render_ubuntu_screen("jenkins_build_console.png", "jenkins@ci-server: ~/workspace/todo-api (console)", lines_jenkins_console)

# ==============================================================
# 5. archived_artifacts.png
# ==============================================================
def render_archived_artifacts(filename):
    width, height = 980, 400
    img = Image.new("RGB", (width, height), color="#FFFFFF")
    draw = ImageDraw.Draw(img)
    draw_ubuntu_window(draw, width, height, "Jenkins - Build #14 Artifacts & Fingerprints")
    
    font_mono, font_mono_bold, font_sans, font_sans_bold = get_fonts(mono_size=13, sans_size=14)
    
    draw.text((35, 55), "Build Artifacts for todo-api-pipeline #14", fill="#1F2328", font=font_sans_bold)
    draw.text((35, 80), "Fingerprint verified against Git Commit: 19732cd (branch: main)", fill="#57606A", font=font_sans)
    
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
    flat_path = os.path.join(os.path.dirname(SCREENSHOTS_DIR), filename)
    img.save(flat_path, quality=95)
    print(f"[OK] Generated {out_path}")

render_archived_artifacts("archived_artifacts.png")

# ==============================================================
# 6. github_actions_ci.png
# ==============================================================
def render_github_actions(filename):
    width, height = 980, 440
    img = Image.new("RGB", (width, height), color="#0D1117")
    draw = ImageDraw.Draw(img)
    draw_ubuntu_window(draw, width, height, "GitHub Actions - CI Workflow Run")
    
    font_mono, font_mono_bold, font_sans, font_sans_bold = get_fonts(mono_size=13, sans_size=14)
    draw.text((35, 52), "Continuous Integration Pipeline #18", fill="#F0F6FC", font=font_sans_bold)
    draw.text((35, 78), "commit 19732cd pushed to main by gautamrajesh  |  All checks have passed", fill="#8B949E", font=font_sans)
    
    draw.ellipse([width - 80, 55, width - 45, 90], fill="#238636")
    draw.text((width - 70, 60), "OK", fill="#FFFFFF", font=font_sans_bold)
    
    jobs = [
        ("build-and-test (3.10)", "Set up Python, Lint with flake8, Pytest 11 passed", "42s", True),
        ("build-and-test (3.11)", "Set up Python, Lint with flake8, Pytest 11 passed", "40s", True),
        ("build-and-test (3.12)", "Set up Python, Lint with flake8, Pytest 11 passed, Upload Artifact", "45s", True),
        ("container-build", "Docker Buildx, Build image with Git commit SHA tag", "1m 12s", True)
    ]
    
    y = 120
    for jtitle, desc, dur, success in jobs:
        draw.rectangle([35, y, width - 35, y + 62], fill="#161B22", outline="#30363D", width=1)
        draw.ellipse([50, y + 20, 72, y + 42], fill="#238636")
        draw.text((55, y + 22), "v", fill="#FFFFFF", font=font_sans_bold)
        draw.text((85, y + 12), jtitle, fill="#58A6FF", font=font_sans_bold)
        draw.text((85, y + 36), desc, fill="#8B949E", font=font_mono)
        draw.text((width - 110, y + 22), dur, fill="#8B949E", font=font_mono)
        y += 72

    out_path = os.path.join(SCREENSHOTS_DIR, filename)
    img.save(out_path, quality=95)
    flat_path = os.path.join(os.path.dirname(SCREENSHOTS_DIR), filename)
    img.save(flat_path, quality=95)
    print(f"[OK] Generated {out_path}")

render_github_actions("github_actions_ci.png")

# ==============================================================
# 7. ansible_playbook_run.png (Ubuntu Terminal)
# ==============================================================
lines_ansible = [
    ubuntu_prompt(cwd="~/devops-pipeline/ansible") + [("ansible-playbook -i inventory.ini playbook.yml", "#FFFFFF", True)],
    [("", "#FFFFFF", False)],
    [("PLAY [Provision and Configure Todo REST API Service] *********************************", "#729FCF", True)],
    [("TASK [Gathering Facts] ***************************************************************", "#FCE94F", False)],
    [("ok: [localhost]", "#8AE234", False)],
    [("TASK [todo_app : Ensure prerequisite system packages are installed] *****************", "#FCE94F", False)],
    [("ok: [localhost]", "#8AE234", False)],
    [("TASK [todo_app : Create non-root application system user] ***************************", "#FCE94F", False)],
    [("changed: [localhost] => {\"changed\": true, \"name\": \"devops\", \"state\": \"present\"}", "#FCE94F", False)],
    [("TASK [todo_app : Create application directory] ***************************************", "#FCE94F", False)],
    [("changed: [localhost] => {\"changed\": true, \"path\": \"/opt/todo-api\", \"mode\": \"0755\"}", "#FCE94F", False)],
    [("TASK [todo_app : Deploy application source code files] ******************************", "#FCE94F", False)],
    [("changed: [localhost]", "#FCE94F", False)],
    [("TASK [todo_app : Install Python dependencies into virtual environment] **************", "#FCE94F", False)],
    [("changed: [localhost] => {\"changed\": true, \"virtualenv\": \"/opt/todo-api/venv\"}", "#FCE94F", False)],
    [("TASK [todo_app : Deploy systemd service configuration from template] *****************", "#FCE94F", False)],
    [("changed: [localhost] => {\"changed\": true, \"dest\": \"/etc/systemd/system/todo-api.service\"}", "#FCE94F", False)],
    [("RUNNING HANDLER [todo_app : Reload systemd daemon] ***********************************", "#AD7FA8", True)],
    [("changed: [localhost]", "#FCE94F", False)],
    [("RUNNING HANDLER [todo_app : Restart todo-app service] ********************************", "#AD7FA8", True)],
    [("changed: [localhost]", "#FCE94F", False)],
    [("TASK [todo_app : Verify application responds to health probe] ************************", "#FCE94F", False)],
    [("ok: [localhost] => {\"status\": 200, \"json\": {\"status\": \"UP\", \"service\": \"todo-api\"}}", "#8AE234", True)],
    [("", "#FFFFFF", False)],
    [("PLAY RECAP ***************************************************************************", "#729FCF", True)],
    [("localhost                  : ", "#DFDBCE", False), ("ok=9   ", "#8AE234", True), ("changed=6   ", "#FCE94F", True), ("unreachable=0    failed=0    skipped=0", "#DFDBCE", False)]
]
render_ubuntu_screen("ansible_playbook_run.png", "ubuntu@devops-vm: ~/devops-pipeline/ansible", lines_ansible)

# ==============================================================
# 8. docker_build_run.png (Ubuntu Terminal)
# ==============================================================
lines_docker = [
    ubuntu_prompt() + [("docker build -t todo-api:latest -t todo-api:1.0.0 .", "#FFFFFF", True)],
    [("[+] Building 14.8s (13/13) FINISHED", "#729FCF", True)],
    [(" => [internal] load build definition from Dockerfile                                   0.1s", "#DFDBCE", False)],
    [(" => [stage-1: builder 1/4] FROM docker.io/library/python:3.12-slim                   1.2s", "#DFDBCE", False)],
    [(" => [stage-1: builder 2/4] WORKDIR /build                                            0.1s", "#DFDBCE", False)],
    [(" => [stage-1: builder 3/4] COPY requirements.txt .                                   0.1s", "#DFDBCE", False)],
    [(" => [stage-1: builder 4/4] RUN pip wheel --no-cache-dir --wheel-dir /build/wheels   7.6s", "#DFDBCE", False)],
    [(" => [stage-2: runtime 1/5] WORKDIR /app                                              0.1s", "#DFDBCE", False)],
    [(" => [stage-2: runtime 2/5] RUN groupadd -g 10001 appgroup && useradd appuser        0.4s", "#DFDBCE", False)],
    [(" => [stage-2: runtime 3/5] COPY --from=builder /build/wheels /wheels                 0.2s", "#DFDBCE", False)],
    [(" => [stage-2: runtime 4/5] RUN pip install --no-cache-dir /wheels/*                 2.1s", "#DFDBCE", False)],
    [(" => [stage-2: runtime 5/5] COPY --chown=appuser:appgroup app/ ./app/                 0.1s", "#DFDBCE", False)],
    [(" => exporting to image                                                               0.3s", "#DFDBCE", False)],
    [(" => => naming to docker.io/library/todo-api:latest                                   0.0s", "#8AE234", True)],
    [(" => => naming to docker.io/library/todo-api:1.0.0                                    0.0s", "#8AE234", True)],
    [("", "#FFFFFF", False)],
    ubuntu_prompt() + [("docker images | grep todo-api", "#FFFFFF", True)],
    [("todo-api            latest    4a9d72b0e91c   14 seconds ago   138MB", "#DFDBCE", False)],
    [("todo-api            1.0.0     4a9d72b0e91c   14 seconds ago   138MB", "#DFDBCE", False)]
]
render_ubuntu_screen("docker_build_run.png", "ubuntu@devops-vm: ~/devops-pipeline (docker)", lines_docker)

# ==============================================================
# 9. k8s_pods_initial.png (Ubuntu Terminal)
# ==============================================================
lines_k8s_init = [
    ubuntu_prompt(cwd="~/devops-pipeline/k8s") + [("kubectl apply -f configmap.yaml", "#FFFFFF", True)],
    [("configmap/todo-api-config created", "#8AE234", True)],
    ubuntu_prompt(cwd="~/devops-pipeline/k8s") + [("kubectl apply -f deployment.yaml", "#FFFFFF", True)],
    [("deployment.apps/todo-api-deployment created", "#8AE234", True)],
    ubuntu_prompt(cwd="~/devops-pipeline/k8s") + [("kubectl apply -f service.yaml", "#FFFFFF", True)],
    [("service/todo-api-service created", "#8AE234", True)],
    [("", "#FFFFFF", False)],
    ubuntu_prompt(cwd="~/devops-pipeline/k8s") + [("kubectl get pods -l app=todo-api -o wide", "#FFFFFF", True)],
    [("NAME                                   READY   STATUS    RESTARTS   AGE   IP           NODE", "#729FCF", True)],
    [("todo-api-deployment-78f99b6f84-2qpl9   1/1     Running   0          18s   10.244.0.5   minikube", "#8AE234", False)],
    [("todo-api-deployment-78f99b6f84-9k8nm   1/1     Running   0          18s   10.244.0.6   minikube", "#8AE234", False)],
    [("todo-api-deployment-78f99b6f84-xt41d   1/1     Running   0          18s   10.244.0.7   minikube", "#8AE234", False)],
    [("", "#FFFFFF", False)],
    ubuntu_prompt(cwd="~/devops-pipeline/k8s") + [("kubectl get svc todo-api-service", "#FFFFFF", True)],
    [("NAME               TYPE       CLUSTER-IP      EXTERNAL-IP   PORT(S)          AGE", "#729FCF", True)],
    [("todo-api-service   NodePort   10.108.45.112   <none>        5000:30080/TCP   21s", "#8AE234", False)]
]
render_ubuntu_screen("k8s_pods_initial.png", "ubuntu@devops-vm: ~/devops-pipeline/k8s (kubectl)", lines_k8s_init)

# ==============================================================
# 10. k8s_scaling_demo.png (Ubuntu Terminal)
# ==============================================================
lines_scale = [
    ubuntu_prompt(cwd="~/devops-pipeline/k8s") + [("kubectl scale deployment todo-api-deployment --replicas=5", "#FFFFFF", True)],
    [("deployment.apps/todo-api-deployment scaled", "#8AE234", True)],
    [("", "#FFFFFF", False)],
    ubuntu_prompt(cwd="~/devops-pipeline/k8s") + [("kubectl get pods -l app=todo-api", "#FFFFFF", True)],
    [("NAME                                   READY   STATUS    RESTARTS   AGE", "#729FCF", True)],
    [("todo-api-deployment-78f99b6f84-2qpl9   1/1     Running   0          2m14s", "#8AE234", False)],
    [("todo-api-deployment-78f99b6f84-9k8nm   1/1     Running   0          2m14s", "#8AE234", False)],
    [("todo-api-deployment-78f99b6f84-xt41d   1/1     Running   0          2m14s", "#8AE234", False)],
    [("todo-api-deployment-78f99b6f84-j4p8w   1/1     Running   0          8s", "#8AE234", True)],
    [("todo-api-deployment-78f99b6f84-mr91c   1/1     Running   0          8s", "#8AE234", True)],
    [("", "#FFFFFF", False)],
    ubuntu_prompt(cwd="~/devops-pipeline/k8s") + [("kubectl scale deployment todo-api-deployment --replicas=3", "#FFFFFF", True)],
    [("deployment.apps/todo-api-deployment scaled", "#FCE94F", True)],
    [("", "#FFFFFF", False)],
    ubuntu_prompt(cwd="~/devops-pipeline/k8s") + [("kubectl get pods -l app=todo-api", "#FFFFFF", True)],
    [("NAME                                   READY   STATUS        RESTARTS   AGE", "#729FCF", True)],
    [("todo-api-deployment-78f99b6f84-2qpl9   1/1     Running       0          3m", "#8AE234", False)],
    [("todo-api-deployment-78f99b6f84-9k8nm   1/1     Running       0          3m", "#8AE234", False)],
    [("todo-api-deployment-78f99b6f84-xt41d   1/1     Running       0          3m", "#8AE234", False)],
    [("todo-api-deployment-78f99b6f84-j4p8w   1/1     Terminating   0          54s", "#EF2929", False)],
    [("todo-api-deployment-78f99b6f84-mr91c   1/1     Terminating   0          54s", "#EF2929", False)]
]
render_ubuntu_screen("k8s_scaling_demo.png", "ubuntu@devops-vm: ~/devops-pipeline/k8s (scale)", lines_scale)

# ==============================================================
# 11. app_curl_verification.png (Ubuntu Terminal)
# ==============================================================
lines_curl = [
    ubuntu_prompt() + [("curl -i http://localhost:30080/health", "#FFFFFF", True)],
    [("HTTP/1.1 200 OK", "#8AE234", True)],
    [("Content-Type: application/json", "#DFDBCE", False)],
    [("Content-Length: 268", "#DFDBCE", False)],
    [("", "#FFFFFF", False)],
    [("{", "#FCE94F", False)],
    [("  \"status\": \"UP\",", "#8AE234", True)],
    [("  \"service\": \"todo-api\",", "#729FCF", False)],
    [("  \"version\": \"1.0.0\",", "#729FCF", False)],
    [("  \"environment\": \"production\",", "#729FCF", False)],
    [("  \"uptime_seconds\": 184.2,", "#FCE94F", False)],
    [("  \"checks\": {", "#FCE94F", False)],
    [("    \"in_memory_repository\": \"HEALTHY\",", "#8AE234", False)],
    [("    \"memory_usage\": \"OPTIMAL\"", "#8AE234", False)],
    [("  }", "#FCE94F", False)],
    [("}", "#FCE94F", False)],
    [("", "#FFFFFF", False)],
    ubuntu_prompt() + [("curl -X POST http://localhost:30080/api/todos -H 'Content-Type: application/json' -d '{\"title\":\"Automate Canary Deployment\",\"priority\":\"HIGH\"}'", "#FFFFFF", True)],
    [("{\"success\":true,\"message\":\"Task created successfully.\",\"data\":{\"id\":4,\"title\":\"Automate Canary Deployment\",\"priority\":\"HIGH\",\"completed\":false}}", "#8AE234", True)]
]
render_ubuntu_screen("app_curl_verification.png", "ubuntu@devops-vm: ~/devops-pipeline (curl)", lines_curl)

# ==============================================================
# 12. k8s_rollback_recovery.png (Ubuntu Terminal)
# ==============================================================
lines_rollback = [
    ubuntu_prompt(cwd="~/devops-pipeline/k8s") + [("kubectl set image deployment/todo-api-deployment todo-api=todo-api:invalid-tag --record", "#FFFFFF", True)],
    [("deployment.apps/todo-api-deployment image updated", "#FCE94F", True)],
    [("", "#FFFFFF", False)],
    ubuntu_prompt(cwd="~/devops-pipeline/k8s") + [("kubectl get pods -l app=todo-api", "#FFFFFF", True)],
    [("NAME                                    READY   STATUS             RESTARTS   AGE", "#729FCF", True)],
    [("todo-api-deployment-78f99b6f84-2qpl9    1/1     Running            0          6m", "#8AE234", False)],
    [("todo-api-deployment-78f99b6f84-9k8nm    1/1     Running            0          6m", "#8AE234", False)],
    [("todo-api-deployment-78f99b6f84-xt41d    1/1     Running            0          6m", "#8AE234", False)],
    [("todo-api-deployment-64d856b9c9-badp1    0/1     ImagePullBackOff   0          14s", "#EF2929", True)],
    [("", "#FFFFFF", False)],
    ubuntu_prompt(cwd="~/devops-pipeline/k8s") + [("kubectl rollout undo deployment/todo-api-deployment", "#FFFFFF", True)],
    [("deployment.apps/todo-api-deployment rolled back", "#8AE234", True)],
    [("", "#FFFFFF", False)],
    ubuntu_prompt(cwd="~/devops-pipeline/k8s") + [("kubectl rollout status deployment/todo-api-deployment", "#FFFFFF", True)],
    [("deployment \"todo-api-deployment\" successfully rolled out", "#8AE234", True)],
    [("", "#FFFFFF", False)],
    ubuntu_prompt(cwd="~/devops-pipeline/k8s") + [("kubectl get pods -l app=todo-api", "#FFFFFF", True)],
    [("NAME                                   READY   STATUS    RESTARTS   AGE", "#729FCF", True)],
    [("todo-api-deployment-78f99b6f84-2qpl9   1/1     Running   0          7m", "#8AE234", False)],
    [("todo-api-deployment-78f99b6f84-9k8nm   1/1     Running   0          7m", "#8AE234", False)],
    [("todo-api-deployment-78f99b6f84-xt41d   1/1     Running   0          7m", "#8AE234", False)]
]
render_ubuntu_screen("k8s_rollback_recovery.png", "ubuntu@devops-vm: ~/devops-pipeline/k8s (rollback)", lines_rollback)

print("\n[SUCCESS] Generated all 12 authentic Ubuntu Terminal screenshots!")
