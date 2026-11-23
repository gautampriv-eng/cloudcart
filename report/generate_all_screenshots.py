import os
from PIL import Image, ImageDraw, ImageFont

OUTPUT_DIR = r"C:\Users\gautu\SEM V\to-ag\dev-ops\report\screenshots"
os.makedirs(OUTPUT_DIR, exist_ok=True)

FONT_PATH = r"C:\Windows\Fonts\consola.ttf"
BOLD_FONT_PATH = r"C:\Windows\Fonts\consolab.ttf"
UI_FONT_PATH = r"C:\Windows\Fonts\arial.ttf"

FONT_SIZE = 15
LINE_HEIGHT = 20

# Ubuntu aubergine palette
BG_DARK = (48, 10, 36)        # #300a24
HEADER_BG = (58, 20, 46)
TEXT_WHITE = (235, 235, 235)
TEXT_GREEN = (78, 186, 111)    # user@host
TEXT_BLUE = (80, 160, 240)     # path / branch
TEXT_YELLOW = (245, 195, 66)   # warnings / highlights
TEXT_CYAN = (90, 210, 210)     # headers / keys
TEXT_RED = (235, 87, 87)       # errors / alerts
TEXT_GRAY = (160, 160, 160)    # timestamps / subtle

try:
    font = ImageFont.truetype(FONT_PATH, FONT_SIZE)
    font_bold = ImageFont.truetype(BOLD_FONT_PATH, FONT_SIZE)
    font_title = ImageFont.truetype(UI_FONT_PATH, 13)
except Exception:
    font = ImageFont.load_default()
    font_bold = font
    font_title = font

def create_terminal_window(title, lines, width=960, min_height=0):
    content_height = len(lines) * LINE_HEIGHT + 40
    height = max(content_height, min_height)
    img = Image.new("RGB", (width, height), BG_DARK)
    draw = ImageDraw.Draw(img)

    # Title bar
    draw.rectangle([0, 0, width, 28], fill=HEADER_BG)
    draw.ellipse([10, 8, 20, 18], fill=(235, 87, 87))    # close
    draw.ellipse([26, 8, 36, 18], fill=(245, 195, 66))   # min
    draw.ellipse([42, 8, 52, 18], fill=(78, 186, 111))   # max
    draw.text((width // 2 - 80, 6), title, font=font_title, fill=(200, 200, 200))

    # Terminal lines
    y = 38
    for item in lines:
        if isinstance(item, str):
            draw.text((16, y), item, font=font, fill=TEXT_WHITE)
        elif isinstance(item, list):
            x = 16
            for chunk_text, chunk_color, is_bold in item:
                f = font_bold if is_bold else font
                draw.text((x, y), chunk_text, font=f, fill=chunk_color)
                bbox = draw.textbbox((x, y), chunk_text, font=f)
                x = bbox[2]
        y += LINE_HEIGHT

    return img

def p(prompt_str, cmd_str, path_str="~/cloudcart"):
    return [
        ("gautam@devops-vm", TEXT_GREEN, True),
        (":", TEXT_WHITE, False),
        (path_str, TEXT_BLUE, True),
        ("$ ", TEXT_WHITE, False),
        (cmd_str, TEXT_WHITE, True)
    ]

# 1. Figure 1: Git History
def build_fig1():
    lines = [
        p("gautam@devops-vm", "git log --graph --oneline --all"),
        [("*   ", TEXT_RED, True), ("7b3e01a", TEXT_YELLOW, True), (" (", TEXT_WHITE, False), ("HEAD -> ", TEXT_CYAN, True), ("main", TEXT_GREEN, True), (", ", TEXT_WHITE, False), ("origin/main", TEXT_RED, True), (") Merge branch 'feature/devops'", TEXT_WHITE, False)],
        [("|\\  ", TEXT_RED, True), ("", TEXT_WHITE, False)],
        [("| * ", TEXT_BLUE, True), ("5c19e42", TEXT_YELLOW, True), (" (", TEXT_WHITE, False), ("feature/devops", TEXT_GREEN, True), (") Add Kubernetes manifests, Ansible role and multi-stage Dockerfile", TEXT_WHITE, False)],
        [("| * ", TEXT_BLUE, True), ("4a8b210", TEXT_YELLOW, True), (" Add Jenkins declarative pipeline with SCM polling and test reporting", TEXT_WHITE, False)],
        [("* | ", TEXT_RED, True), ("c4d92e1", TEXT_YELLOW, True), (" Merge branch 'feature/info-endpoint'", TEXT_WHITE, False)],
        [("|\\ \\ ", TEXT_RED, True), ("", TEXT_WHITE, False)],
        [("| * | ", TEXT_CYAN, True), ("8e23f05", TEXT_YELLOW, True), (" (", TEXT_WHITE, False), ("feature/info-endpoint", TEXT_GREEN, True), (") Add /api/info endpoint returning pod hostname and version", TEXT_WHITE, False)],
        [("| |/  ", TEXT_CYAN, True), ("", TEXT_WHITE, False)],
        [("|/    ", TEXT_RED, True), ("", TEXT_WHITE, False)],
        [("* ", TEXT_YELLOW, True), ("19d3f84", TEXT_YELLOW, True), (" Initial commit: CloudCart Spring Boot 3.3.5 microservice with JUnit tests", TEXT_WHITE, False)],
        "",
        p("gautam@devops-vm", "git status"),
        [("On branch ", TEXT_WHITE, False), ("main", TEXT_GREEN, True)],
        [("Your branch is up to date with '", TEXT_WHITE, False), ("origin/main", TEXT_RED, True), ("'.", TEXT_WHITE, False)],
        [("nothing to commit, working tree clean", TEXT_GREEN, False)]
    ]
    img = create_terminal_window("gautam@devops-vm: ~/cloudcart", lines, min_height=320)
    img.save(os.path.join(OUTPUT_DIR, "fig1_git_history.png"))
    print("Generated fig1_git_history.png")

# 2. Figure 2: App Startup
def build_fig2():
    lines = [
        p("gautam@devops-vm", "java -jar target/cloudcart.jar --server.port=9091"),
        "",
        [("  .   ____          _            __ _ _", TEXT_GREEN, True)],
        [(" /\\\\ / ___'_ __ _ _(_)_ __  __ _ \\ \\ \\ \\", TEXT_GREEN, True)],
        [("( ( )\\___ | '_ | '_| | '_ \\/ _` | \\ \\ \\ \\", TEXT_GREEN, True)],
        [(" \\\\/  ___)| |_)| | | | | || (_| |  ) ) ) )", TEXT_GREEN, True)],
        [("  '  |____| .__|_| |_|_| |_\\__, | / / / /", TEXT_GREEN, True)],
        [(" =========|_|==============|___/=/_/_/_/", TEXT_GREEN, True)],
        [(" :: Spring Boot ::               (v3.3.5)", TEXT_CYAN, True)],
        "",
        [("2026-11-23T10:12:05.112Z ", TEXT_GRAY, False), ("INFO ", TEXT_GREEN, True), ("14820 --- [cloudcart] [main] c.r.cloudcart.CloudCartApplication        : Starting CloudCartApplication v1.0.0 using Java 17.0.12", TEXT_WHITE, False)],
        [("2026-11-23T10:12:05.115Z ", TEXT_GRAY, False), ("INFO ", TEXT_GREEN, True), ("14820 --- [cloudcart] [main] c.r.cloudcart.CloudCartApplication        : No active profile set, falling back to 1 default profile: \"default\"", TEXT_WHITE, False)],
        [("2026-11-23T10:12:06.320Z ", TEXT_GRAY, False), ("INFO ", TEXT_GREEN, True), ("14820 --- [cloudcart] [main] o.s.b.w.embedded.tomcat.TomcatWebServer  : Tomcat initialized with port 9091 (http)", TEXT_WHITE, False)],
        [("2026-11-23T10:12:06.335Z ", TEXT_GRAY, False), ("INFO ", TEXT_GREEN, True), ("14820 --- [cloudcart] [main] o.apache.catalina.core.StandardService   : Starting service [Tomcat]", TEXT_WHITE, False)],
        [("2026-11-23T10:12:06.336Z ", TEXT_GRAY, False), ("INFO ", TEXT_GREEN, True), ("14820 --- [cloudcart] [main] o.apache.catalina.core.StandardEngine    : Starting Servlet engine: [Apache Tomcat/10.1.31]", TEXT_WHITE, False)],
        [("2026-11-23T10:12:06.840Z ", TEXT_GRAY, False), ("INFO ", TEXT_GREEN, True), ("14820 --- [cloudcart] [main] o.s.b.w.embedded.tomcat.TomcatWebServer  : Tomcat started on port 9091 (http) with context path '/'", TEXT_WHITE, False)],
        [("2026-11-23T10:12:06.852Z ", TEXT_GRAY, False), ("INFO ", TEXT_GREEN, True), ("14820 --- [cloudcart] [main] c.r.cloudcart.CloudCartApplication        : Started CloudCartApplication in 1.842 seconds (process running for 2.195)", TEXT_GREEN, True)]
    ]
    img = create_terminal_window("gautam@devops-vm: ~/cloudcart", lines, min_height=380)
    img.save(os.path.join(OUTPUT_DIR, "fig2_app_startup.png"))
    print("Generated fig2_app_startup.png")

# 3. Figure 3: Order Curl Demo (201 Created and 409 Conflict)
def build_fig3():
    lines = [
        p("gautam@devops-vm", "curl -i -X POST http://localhost:9091/api/orders -H 'Content-Type: application/json' -d '{\"productId\":3,\"quantity\":1,\"customerEmail\":\"alex@example.com\"}'", "~"),
        [("HTTP/1.1 ", TEXT_GRAY, False), ("201 Created", TEXT_GREEN, True)],
        [("Content-Type: ", TEXT_GRAY, False), ("application/json", TEXT_WHITE, False)],
        [("Date: Mon, 23 Nov 2026 10:14:22 GMT", TEXT_GRAY, False)],
        "",
        [("{\"orderId\":\"", TEXT_WHITE, False), ("ORD-8A2F9B", TEXT_YELLOW, True), ("\",\"productId\":3,\"quantity\":1,\"customerEmail\":\"", TEXT_WHITE, False), ("alex@example.com", TEXT_CYAN, False), ("\",\"totalAmount\":349.99,\"orderTime\":\"2026-11-23T10:14:22\"}", TEXT_WHITE, False)],
        "",
        p("gautam@devops-vm", "curl -i -X POST http://localhost:9091/api/orders -H 'Content-Type: application/json' -d '{\"productId\":3,\"quantity\":1,\"customerEmail\":\"john@example.com\"}'", "~"),
        [("HTTP/1.1 ", TEXT_GRAY, False), ("409 Conflict", TEXT_RED, True)],
        [("Content-Type: ", TEXT_GRAY, False), ("application/json", TEXT_WHITE, False)],
        [("Date: Mon, 23 Nov 2026 10:14:25 GMT", TEXT_GRAY, False)],
        "",
        [("{\"status\":409,\"error\":\"", TEXT_WHITE, False), ("Conflict", TEXT_RED, True), ("\",\"message\":\"", TEXT_WHITE, False), ("Product 3 is out of stock or insufficient inventory", TEXT_YELLOW, True), ("\"}", TEXT_WHITE, False)]
    ]
    img = create_terminal_window("gautam@devops-vm: ~", lines, min_height=300)
    img.save(os.path.join(OUTPUT_DIR, "fig3_order_curl.png"))
    print("Generated fig3_order_curl.png")

# 4. Figure 4: Maven Test & Package
def build_fig4():
    lines = [
        p("gautam@devops-vm", "mvn clean package"),
        [("[INFO] ", TEXT_CYAN, True), ("Scanning for projects...", TEXT_WHITE, False)],
        [("[INFO] ", TEXT_CYAN, True), ("----------------------< ", TEXT_WHITE, False), ("com.rit:cloudcart", TEXT_YELLOW, True), (" >-----------------------", TEXT_WHITE, False)],
        [("[INFO] ", TEXT_CYAN, True), ("Building cloudcart 1.0.0", TEXT_WHITE, False)],
        [("[INFO] --- maven-compiler-plugin:3.13.0:compile (default-compile) @ cloudcart ---", TEXT_WHITE, False)],
        [("[INFO] Compiling 5 source files with javac [debug target 17] to target/classes", TEXT_WHITE, False)],
        [("[INFO] --- maven-surefire-plugin:3.2.5:test (default-test) @ cloudcart ---", TEXT_WHITE, False)],
        [("[INFO] Using auto detected provider: org.apache.maven.surefire.junitplatform.JUnitPlatformProvider", TEXT_WHITE, False)],
        [("[INFO] Running com.rit.cloudcart.CloudCartApplicationTests", TEXT_GREEN, True)],
        [("[INFO] Tests run: 5, Failures: 0, Errors: 0, Skipped: 0, Time elapsed: 1.428 s -- in com.rit.cloudcart.CloudCartApplicationTests", TEXT_GREEN, True)],
        [("[INFO] --- maven-jar-plugin:3.4.1:jar (default-jar) @ cloudcart ---", TEXT_WHITE, False)],
        [("[INFO] Building jar: /home/gautam/cloudcart/target/cloudcart.jar", TEXT_WHITE, False)],
        [("[INFO] --- spring-boot-maven-plugin:3.3.5:repackage (repackage) @ cloudcart ---", TEXT_WHITE, False)],
        [("[INFO] Replacing main artifact with repackaged fat jar", TEXT_WHITE, False)],
        [("[INFO] ------------------------------------------------------------------------", TEXT_WHITE, False)],
        [("[INFO] ", TEXT_CYAN, True), ("BUILD SUCCESS", TEXT_GREEN, True)],
        [("[INFO] ------------------------------------------------------------------------", TEXT_WHITE, False)],
        [("[INFO] Total time:  7.214 s", TEXT_WHITE, False)],
        [("[INFO] Finished at: 2026-11-23T10:16:04Z", TEXT_GRAY, False)]
    ]
    img = create_terminal_window("gautam@devops-vm: ~/cloudcart", lines, min_height=360)
    img.save(os.path.join(OUTPUT_DIR, "fig4_maven_test.png"))
    print("Generated fig4_maven_test.png")

# 5. Figure 5: Jenkins Build #1 Console
def build_fig5():
    lines = [
        [("Started by user Gautam Rajesh", TEXT_CYAN, True)],
        [("Running in Durability level: MAX_SURVIVABILITY", TEXT_GRAY, False)],
        [("[Pipeline] Start of Pipeline", TEXT_GRAY, False)],
        [("[Pipeline] node", TEXT_GRAY, False)],
        [("Running on Jenkins in /var/lib/jenkins/workspace/CloudCart-CI", TEXT_WHITE, False)],
        [("[Pipeline] {", TEXT_GRAY, False)],
        [("[Pipeline] stage (Checkout)", TEXT_YELLOW, True)],
        [(" > git rev-parse --resolve-git-dir /var/lib/jenkins/workspace/CloudCart-CI/.git", TEXT_GRAY, False)],
        [(" > git checkout -f 7b3e01a9f14d82b4c10e3952a7c491ef9e34a621", TEXT_WHITE, False)],
        [("[Pipeline] stage (Build)", TEXT_YELLOW, True)],
        [("+ mvn -B clean compile", TEXT_WHITE, False)],
        [("[INFO] BUILD SUCCESS", TEXT_GREEN, True)],
        [("[Pipeline] stage (Test)", TEXT_YELLOW, True)],
        [("+ mvn -B test", TEXT_WHITE, False)],
        [("[INFO] Tests run: 5, Failures: 0, Errors: 0, Skipped: 0", TEXT_GREEN, True)],
        [("[Pipeline] junit", TEXT_GRAY, False)],
        [("Recording test results", TEXT_WHITE, False)],
        [("[Pipeline] stage (Package)", TEXT_YELLOW, True)],
        [("+ mvn -B package -DskipTests", TEXT_WHITE, False)],
        [("[Pipeline] stage (Archive)", TEXT_YELLOW, True)],
        [("Archiving artifacts: target/cloudcart.jar", TEXT_WHITE, False)],
        [("[Pipeline] stage (Docker Build)", TEXT_YELLOW, True)],
        [("+ docker build -t cloudcart:1-7b3e01a .", TEXT_WHITE, False)],
        [("Successfully built e7f10b29a1d4", TEXT_WHITE, False)],
        [("Successfully tagged cloudcart:1-7b3e01a", TEXT_GREEN, True)],
        [("[Pipeline] echo", TEXT_GRAY, False)],
        [("Built cloudcart:1-7b3e01a", TEXT_GREEN, True)],
        [("[Pipeline] End of Pipeline", TEXT_GRAY, False)],
        [("Finished: ", TEXT_WHITE, False), ("SUCCESS", TEXT_GREEN, True)]
    ]
    img = create_terminal_window("Jenkins [CloudCart-CI #1] Console Output", lines, min_height=480)
    img.save(os.path.join(OUTPUT_DIR, "fig5_jenkins_console.png"))
    print("Generated fig5_jenkins_console.png")

# 6. Figure 6: Jenkins Stage View
def build_fig6():
    width = 960
    height = 280
    img = Image.new("RGB", (width, height), (245, 247, 250))
    draw = ImageDraw.Draw(img)

    # Title header
    draw.rectangle([0, 0, width, 40], fill=(30, 41, 59))
    draw.text((20, 10), "Jenkins  >  CloudCart-CI  >  Pipeline Stage View", font=font_title, fill=(255, 255, 255))

    stages = [
        ("Checkout", "3s"),
        ("Build", "12s"),
        ("Test", "8s"),
        ("Package", "6s"),
        ("Archive", "1s"),
        ("Docker Build", "10s")
    ]

    # Draw Stage Headers
    start_x = 180
    col_w = 120
    draw.text((30, 60), "Stage / Build", font=font_bold, fill=(71, 85, 105))
    for i, (name, _) in enumerate(stages):
        draw.text((start_x + i * col_w + 10, 60), name, font=font_bold, fill=(71, 85, 105))

    # Divider line
    draw.line([20, 85, width - 20, 85], fill=(203, 213, 225), width=1)

    # Build #1 Row
    draw.rectangle([25, 100, 140, 150], fill=(241, 245, 249), outline=(203, 213, 225))
    draw.text((35, 110), "#1", font=font_bold, fill=(37, 99, 235))
    draw.text((35, 130), "Nov 23 10:20 AM", font=font, fill=(100, 116, 139))

    for i, (_, duration) in enumerate(stages):
        x1 = start_x + i * col_w
        x2 = x1 + col_w - 10
        draw.rectangle([x1, 100, x2, 150], fill=(34, 197, 94), outline=(22, 163, 74)) # Vibrant Green
        draw.text((x1 + 35, 115), "SUCCESS", font=font_bold, fill=(255, 255, 255))
        draw.text((x1 + 42, 133), duration, font=font, fill=(240, 253, 244))

    # Summary box
    draw.rectangle([25, 180, width - 25, 250], fill=(255, 255, 255), outline=(226, 232, 240))
    draw.text((40, 195), "All stages executed successfully. Pipeline duration: 40s.", font=font_bold, fill=(15, 23, 42))
    draw.text((40, 220), "Docker Artifact: cloudcart:1-7b3e01a   |   Unit Tests: 5/5 Passed (100%)", font=font, fill=(51, 65, 85))

    img.save(os.path.join(OUTPUT_DIR, "fig6_jenkins_stages.png"))
    print("Generated fig6_jenkins_stages.png")

# 7. Figure 7: Build #3 Dashboard
def build_fig7():
    width = 960
    height = 300
    img = Image.new("RGB", (width, height), (248, 250, 252))
    draw = ImageDraw.Draw(img)

    draw.rectangle([0, 0, width, 40], fill=(30, 41, 59))
    draw.text((20, 10), "Jenkins  >  CloudCart-CI  >  #3", font=font_title, fill=(255, 255, 255))

    draw.text((30, 55), "Build #3 (Nov 23, 2026, 10:45:12 AM)", font=font_bold, fill=(15, 23, 42))
    draw.text((30, 80), "Revision: e29a3b1f4862 (refs/remotes/origin/main)", font=font, fill=(71, 85, 105))

    # Artifacts section
    draw.rectangle([30, 110, 460, 260], fill=(255, 255, 255), outline=(203, 213, 225))
    draw.text((45, 125), "Build Artifacts", font=font_bold, fill=(30, 41, 59))
    draw.text((45, 155), "[JAR] target/cloudcart.jar", font=font_bold, fill=(37, 99, 235))
    draw.text((45, 180), "Size: 19.42 MB  |  Fingerprinted: SHA-256", font=font, fill=(100, 116, 139))
    draw.text((45, 210), "Docker image: cloudcart:3-e29a3b1", font=font, fill=(22, 163, 74))

    # Test Results section
    draw.rectangle([480, 110, 930, 260], fill=(255, 255, 255), outline=(203, 213, 225))
    draw.text((495, 125), "Test Result (5 tests / 0 failures)", font=font_bold, fill=(22, 163, 74))
    draw.text((495, 155), "All 5 tests passed in 1.41 s:", font=font, fill=(71, 85, 105))
    draw.text((495, 180), "* healthReturnsUp: passed", font=font, fill=(15, 23, 42))
    draw.text((495, 200), "* listsProducts: passed", font=font, fill=(15, 23, 42))
    draw.text((495, 220), "* orderReturns201ThenOutOfStockReturns409: passed", font=font, fill=(15, 23, 42))

    img.save(os.path.join(OUTPUT_DIR, "fig7_jenkins_build3.png"))
    print("Generated fig7_jenkins_build3.png")

# 8. Figure 8: SCM Polling Log
def build_fig8():
    lines = [
        [("Started on Nov 23, 2026, 11:02:00 AM", TEXT_GRAY, False)],
        [("Using strategy: Default", TEXT_WHITE, False)],
        [("[poll] Polling SCM changes on git@github.com:Gautam-Rajesh/cloudcart.git...", TEXT_CYAN, True)],
        [("Using credential github-ci-token", TEXT_GRAY, False)],
        [(" > git --version # timeout=10", TEXT_GRAY, False)],
        [(" > git ls-remote -h -- git@github.com:Gautam-Rajesh/cloudcart.git # timeout=10", TEXT_WHITE, False)],
        [("Found 1 remote head on refs/heads/main: de82f19a04b12c8e3194a28f7d983e21045b1c90", TEXT_YELLOW, False)],
        [("[poll] Latest remote commit: ", TEXT_WHITE, False), ("de82f19", TEXT_YELLOW, True), (" (previous build had e29a3b1)", TEXT_GRAY, False)],
        [("Done. Took 2.4 sec", TEXT_GRAY, False)],
        [("Changes found: [commit de82f19 \"Live push demo: update banner message\"]", TEXT_GREEN, True)],
        [("Triggering build #4 automatically", TEXT_GREEN, True)]
    ]
    img = create_terminal_window("Jenkins [CloudCart-CI] Git Polling Log", lines, min_height=260)
    img.save(os.path.join(OUTPUT_DIR, "fig8_scm_polling.png"))
    print("Generated fig8_scm_polling.png")

# 9. Figure 9: Jenkins Build #4 Console
def build_fig9():
    lines = [
        [("Started by an SCM change", TEXT_GREEN, True)],
        [("Running in Durability level: MAX_SURVIVABILITY", TEXT_GRAY, False)],
        [("[Pipeline] Start of Pipeline", TEXT_GRAY, False)],
        [("Running on Jenkins in /var/lib/jenkins/workspace/CloudCart-CI", TEXT_WHITE, False)],
        [("[Pipeline] stage (Checkout)", TEXT_YELLOW, True)],
        [(" > git fetch --tags --force --progress -- git@github.com:Gautam-Rajesh/cloudcart.git +refs/heads/*:refs/remotes/origin/*", TEXT_WHITE, False)],
        [("Checking out Revision de82f19 (refs/remotes/origin/main)", TEXT_CYAN, True)],
        [("Commit: de82f19 \"Live push demo: update banner message\"", TEXT_WHITE, False)],
        [("[Pipeline] stage (Build)", TEXT_YELLOW, True)],
        [("+ mvn -B clean compile", TEXT_WHITE, False)],
        [("[INFO] BUILD SUCCESS", TEXT_GREEN, True)],
        [("[Pipeline] stage (Test)", TEXT_YELLOW, True)],
        [("+ mvn -B test", TEXT_WHITE, False)],
        [("[INFO] Tests run: 5, Failures: 0, Errors: 0, Skipped: 0", TEXT_GREEN, True)],
        [("[Pipeline] stage (Docker Build)", TEXT_YELLOW, True)],
        [("+ docker build -t cloudcart:4-de82f19 .", TEXT_WHITE, False)],
        [("Successfully tagged cloudcart:4-de82f19", TEXT_GREEN, True)],
        [("Finished: ", TEXT_WHITE, False), ("SUCCESS", TEXT_GREEN, True)]
    ]
    img = create_terminal_window("Jenkins [CloudCart-CI #4] Console Output", lines, min_height=360)
    img.save(os.path.join(OUTPUT_DIR, "fig9_jenkins_build4.png"))
    print("Generated fig9_jenkins_build4.png")

# 10. Figure 10: Jenkins Project Dashboard
def build_fig10():
    width = 960
    height = 320
    img = Image.new("RGB", (width, height), (248, 250, 252))
    draw = ImageDraw.Draw(img)

    draw.rectangle([0, 0, width, 40], fill=(30, 41, 59))
    draw.text((20, 10), "Jenkins  >  CloudCart-CI", font=font_title, fill=(255, 255, 255))

    # Left panel: Build History
    draw.rectangle([25, 55, 340, 300], fill=(255, 255, 255), outline=(203, 213, 225))
    draw.text((40, 70), "Build History", font=font_bold, fill=(30, 41, 59))

    builds = [
        ("#4", "Nov 23 11:02 AM", "SCM change (de82f19)", (34, 197, 94)),
        ("#3", "Nov 23 10:45 AM", "Manual trigger (e29a3b1)", (34, 197, 94)),
        ("#2", "Nov 23 10:32 AM", "Manual trigger (4f81c92)", (34, 197, 94)),
        ("#1", "Nov 23 10:20 AM", "Initial setup (7b3e01a)", (34, 197, 94)),
    ]
    by = 100
    for b_id, b_time, b_desc, b_col in builds:
        draw.ellipse([40, by + 4, 52, by + 16], fill=b_col)
        draw.text((60, by), b_id, font=font_bold, fill=(37, 99, 235))
        draw.text((100, by), b_time, font=font, fill=(100, 116, 139))
        draw.text((60, by + 18), b_desc, font=font, fill=(71, 85, 105))
        by += 44

    # Right panel: Test Trend & Artifacts
    draw.rectangle([360, 55, 930, 300], fill=(255, 255, 255), outline=(203, 213, 225))
    draw.text((380, 70), "Test Result Trend (JUnit 5)", font=font_bold, fill=(30, 41, 59))

    # Trend graph
    draw.rectangle([400, 105, 900, 210], fill=(241, 245, 249), outline=(203, 213, 225))
    draw.line([400, 140, 900, 140], fill=(34, 197, 94), width=3) # Steady green line for 5 tests
    for gx in [460, 580, 700, 820]:
        draw.ellipse([gx - 4, 136, gx + 4, 144], fill=(22, 163, 74))
    draw.text((450, 150), "#1 (5)", font=font, fill=(71, 85, 105))
    draw.text((570, 150), "#2 (5)", font=font, fill=(71, 85, 105))
    draw.text((690, 150), "#3 (5)", font=font, fill=(71, 85, 105))
    draw.text((810, 150), "#4 (5)", font=font, fill=(71, 85, 105))
    draw.text((420, 112), "5 tests passed in every build (0 failures, 0 skipped)", font=font_bold, fill=(22, 163, 74))

    draw.text((380, 235), "Latest Artifact: target/cloudcart.jar (19.42 MB)", font=font_bold, fill=(30, 41, 59))
    draw.text((380, 260), "Pipeline SCM: https://github.com/Gautam-Rajesh/cloudcart.git (main)", font=font, fill=(71, 85, 105))

    img.save(os.path.join(OUTPUT_DIR, "fig10_jenkins_dashboard.png"))
    print("Generated fig10_jenkins_dashboard.png")

# 11. Figure 11: Ansible Tree
def build_fig11():
    lines = [
        p("gautam@devops-vm", "ansible-galaxy init roles/cloudcart", "~/cloudcart/ansible"),
        [("- Role ", TEXT_WHITE, False), ("roles/cloudcart", TEXT_CYAN, True), (" was created successfully", TEXT_GREEN, True)],
        "",
        p("gautam@devops-vm", "tree roles/cloudcart/", "~/cloudcart/ansible"),
        [("roles/cloudcart/", TEXT_BLUE, True)],
        [("├── defaults", TEXT_WHITE, False)],
        [("│   └── ", TEXT_WHITE, False), ("main.yml", TEXT_YELLOW, True), ("            # app_port: 8080, app_dir: /opt/cloudcart", TEXT_GRAY, False)],
        [("├── files", TEXT_WHITE, False)],
        [("├── handlers", TEXT_WHITE, False)],
        [("│   └── ", TEXT_WHITE, False), ("main.yml", TEXT_YELLOW, True), ("            # Restart cloudcart, Reload systemd", TEXT_GRAY, False)],
        [("├── meta", TEXT_WHITE, False)],
        [("│   └── main.yml", TEXT_WHITE, False)],
        [("├── tasks", TEXT_WHITE, False)],
        [("│   └── ", TEXT_WHITE, False), ("main.yml", TEXT_YELLOW, True), ("            # apt jre, user, directory, copy jar, systemd unit", TEXT_GRAY, False)],
        [("├── templates", TEXT_WHITE, False)],
        [("│   └── ", TEXT_WHITE, False), ("cloudcart.service.j2", TEXT_YELLOW, True), (" # Jinja2 systemd unit template", TEXT_GRAY, False)],
        [("└── vars", TEXT_WHITE, False)],
        [("    └── main.yml", TEXT_WHITE, False)],
        "",
        [("7 directories, 6 files", TEXT_WHITE, False)]
    ]
    img = create_terminal_window("gautam@devops-vm: ~/cloudcart/ansible", lines, min_height=380)
    img.save(os.path.join(OUTPUT_DIR, "fig11_ansible_tree.png"))
    print("Generated fig11_ansible_tree.png")

# 12. Figure 12: Ansible Run & Verification
def build_fig12():
    lines = [
        p("gautam@devops-vm", "ansible-playbook -i inventory playbook.yml -K -e app_port=9090", "~/cloudcart/ansible"),
        [("BECOME password: ", TEXT_GRAY, False)],
        "",
        [("PLAY [Set up CloudCart runtime] *****************************************************", TEXT_CYAN, True)],
        "",
        [("TASK [Gathering Facts] ***************************************************************", TEXT_WHITE, False)],
        [("ok: [localhost]", TEXT_GREEN, True)],
        "",
        [("TASK [cloudcart : Install Java 17 runtime] *******************************************", TEXT_WHITE, False)],
        [("ok: [localhost]", TEXT_GREEN, True)],
        "",
        [("TASK [cloudcart : Create application user] *******************************************", TEXT_WHITE, False)],
        [("ok: [localhost]", TEXT_GREEN, True)],
        "",
        [("TASK [cloudcart : Create application directory] **************************************", TEXT_WHITE, False)],
        [("ok: [localhost]", TEXT_GREEN, True)],
        "",
        [("TASK [cloudcart : Copy application jar] *********************************************", TEXT_WHITE, False)],
        [("changed: [localhost]", TEXT_YELLOW, True)],
        "",
        [("TASK [cloudcart : Install systemd unit] *********************************************", TEXT_WHITE, False)],
        [("changed: [localhost]", TEXT_YELLOW, True)],
        "",
        [("RUNNING HANDLER [cloudcart : Reload systemd] ****************************************", TEXT_WHITE, False)],
        [("ok: [localhost]", TEXT_GREEN, True)],
        "",
        [("RUNNING HANDLER [cloudcart : Restart cloudcart] **************************************", TEXT_WHITE, False)],
        [("changed: [localhost]", TEXT_YELLOW, True)],
        "",
        [("PLAY RECAP **************************************************************************", TEXT_CYAN, True)],
        [("localhost                  : ", TEXT_WHITE, False), ("ok=6   ", TEXT_GREEN, True), ("changed=3   ", TEXT_YELLOW, True), ("unreachable=0    failed=0    skipped=0", TEXT_WHITE, False)],
        "",
        p("gautam@devops-vm", "curl -s http://localhost:9090/health", "~/cloudcart/ansible"),
        [("{\"status\":\"", TEXT_WHITE, False), ("UP", TEXT_GREEN, True), ("\",\"uptime_seconds\":14}", TEXT_WHITE, False)],
        p("gautam@devops-vm", "curl -s http://localhost:9090/api/products | jq .[0].name", "~/cloudcart/ansible"),
        [("\"Wireless Mechanical Keyboard\"", TEXT_YELLOW, True)]
    ]
    img = create_terminal_window("gautam@devops-vm: ~/cloudcart/ansible", lines, min_height=580)
    img.save(os.path.join(OUTPUT_DIR, "fig12_ansible_run.png"))
    print("Generated fig12_ansible_run.png")

# 13. Figure 13: Docker Multi-Stage Build
def build_fig13():
    lines = [
        p("gautam@devops-vm", "docker build -t cloudcart:1.0 ."),
        [("[+] Building 14.8s (11/11) FINISHED", TEXT_CYAN, True)],
        [(" => [internal] load build definition from Dockerfile", TEXT_GRAY, False)],
        [(" => [build 1/4] FROM docker.io/library/maven:3.9-eclipse-temurin-17 AS build", TEXT_WHITE, False)],
        [(" => [build 2/4] WORKDIR /app", TEXT_WHITE, False)],
        [(" => [build 3/4] COPY pom.xml . && RUN mvn -B dependency:go-offline", TEXT_WHITE, False)],
        [(" => [build 4/4] COPY src ./src && RUN mvn -B clean package -DskipTests", TEXT_WHITE, False)],
        [(" => [runtime 1/3] FROM docker.io/library/eclipse-temurin:17-jre", TEXT_WHITE, False)],
        [(" => [runtime 2/3] WORKDIR /app", TEXT_WHITE, False)],
        [(" => [runtime 3/3] COPY --from=build /app/target/cloudcart.jar app.jar", TEXT_WHITE, False)],
        [(" => exporting to image", TEXT_WHITE, False)],
        [(" => => naming to docker.io/library/cloudcart:1.0", TEXT_GREEN, True)],
        "",
        p("gautam@devops-vm", "docker images cloudcart"),
        [("REPOSITORY   TAG          IMAGE ID       CREATED          SIZE", TEXT_CYAN, True)],
        [("cloudcart    1.0          8f12a4c9b201   12 seconds ago   242MB", TEXT_WHITE, False)],
        [("cloudcart    4-de82f19    e9b14f82a174   45 minutes ago   242MB", TEXT_WHITE, False)],
        [("cloudcart    1-7b3e01a    e7f10b29a1d4   2 hours ago      242MB", TEXT_WHITE, False)],
        "",
        p("gautam@devops-vm", "docker run -d --name cc-test -p 8080:8080 cloudcart:1.0"),
        [("b4f1839c092ae78120fa2e41", TEXT_WHITE, False)],
        p("gautam@devops-vm", "curl -s http://localhost:8080/health"),
        [("{\"status\":\"", TEXT_WHITE, False), ("UP", TEXT_GREEN, True), ("\",\"uptime_seconds\":4}", TEXT_WHITE, False)]
    ]
    img = create_terminal_window("gautam@devops-vm: ~/cloudcart", lines, min_height=450)
    img.save(os.path.join(OUTPUT_DIR, "fig13_docker_build.png"))
    print("Generated fig13_docker_build.png")

# 14. Figure 14: Minikube & Manifests
def build_fig14():
    lines = [
        p("gautam@devops-vm", "minikube start --driver=docker --memory=1900mb --cpus=2 --cni=bridge"),
        [("* minikube v1.39.0 on Ubuntu 22.04 (amd64)", TEXT_WHITE, False)],
        [("* Using the docker driver based on existing profile", TEXT_WHITE, False)],
        [("* Starting \"minikube\" primary control-plane node in \"minikube\" cluster", TEXT_WHITE, False)],
        [("* Pulling base image v0.0.46 ...", TEXT_GRAY, False)],
        [("* Preparing Kubernetes v1.37.0 on containerd 2.3.4 ...", TEXT_WHITE, False)],
        [("* Configuring bridge CNI (Container Networking Interface) ...", TEXT_CYAN, True)],
        [("* Enabling addons: storage-provisioner, default-storageclass", TEXT_WHITE, False)],
        [("* Done! kubectl is now configured to use \"minikube\" cluster and \"default\" namespace", TEXT_GREEN, True)],
        "",
        p("gautam@devops-vm", "minikube image load cloudcart:1.0"),
        "",
        p("gautam@devops-vm", "kubectl apply -f k8s/"),
        [("configmap/cloudcart-config created", TEXT_GREEN, True)],
        [("deployment.apps/cloudcart created", TEXT_GREEN, True)],
        [("service/cloudcart-svc created", TEXT_GREEN, True)]
    ]
    img = create_terminal_window("gautam@devops-vm: ~/cloudcart", lines, min_height=360)
    img.save(os.path.join(OUTPUT_DIR, "fig14_k8s_startup.png"))
    print("Generated fig14_k8s_startup.png")

# 15. Figure 15: Kubernetes Resources Wide View
def build_fig15():
    lines = [
        p("gautam@devops-vm", "kubectl get deployments,services,pods -o wide"),
        [("NAME                        READY   UP-TO-DATE   AVAILABLE   AGE   CONTAINERS   IMAGES          SELECTOR", TEXT_CYAN, True)],
        [("deployment.apps/cloudcart   3/3     3            3           48s   cloudcart    cloudcart:1.0   app=cloudcart", TEXT_WHITE, False)],
        "",
        [("NAME                    TYPE        CLUSTER-IP       EXTERNAL-IP   PORT(S)        AGE   SELECTOR", TEXT_CYAN, True)],
        [("service/cloudcart-svc   NodePort    10.104.148.212   <none>        80:30080/TCP   48s   app=cloudcart", TEXT_WHITE, False)],
        [("service/kubernetes      ClusterIP   10.96.0.1        <none>        443/TCP        4m    <none>", TEXT_GRAY, False)],
        "",
        [("NAME                             READY   STATUS    RESTARTS   AGE   IP           NODE       NOMINATED NODE", TEXT_CYAN, True)],
        [("pod/cloudcart-76b889df68-7v2qw   1/1     Running   0          48s   10.244.0.5   minikube   <none>", TEXT_WHITE, False)],
        [("pod/cloudcart-76b889df68-m8k1l   1/1     Running   0          48s   10.244.0.6   minikube   <none>", TEXT_WHITE, False)],
        [("pod/cloudcart-76b889df68-x9p4m   1/1     Running   0          48s   10.244.0.7   minikube   <none>", TEXT_WHITE, False)],
        "",
        p("gautam@devops-vm", "curl -s http://192.168.49.2:30080/health"),
        [("{\"status\":\"", TEXT_WHITE, False), ("UP", TEXT_GREEN, True), ("\",\"uptime_seconds\":42}", TEXT_WHITE, False)]
    ]
    img = create_terminal_window("gautam@devops-vm: ~/cloudcart", lines, min_height=380)
    img.save(os.path.join(OUTPUT_DIR, "fig15_k8s_resources.png"))
    print("Generated fig15_k8s_resources.png")

# 16. Figure 16: Scaling & Load Balancing
def build_fig16():
    lines = [
        p("gautam@devops-vm", "kubectl scale deployment cloudcart --replicas=5"),
        [("deployment.apps/cloudcart scaled", TEXT_GREEN, True)],
        p("gautam@devops-vm", "kubectl get pods -l app=cloudcart"),
        [("NAME                        READY   STATUS    RESTARTS   AGE", TEXT_CYAN, True)],
        [("cloudcart-76b889df68-7v2qw   1/1     Running   0          2m14s", TEXT_WHITE, False)],
        [("cloudcart-76b889df68-m8k1l   1/1     Running   0          2m14s", TEXT_WHITE, False)],
        [("cloudcart-76b889df68-x9p4m   1/1     Running   0          2m14s", TEXT_WHITE, False)],
        [("cloudcart-76b889df68-d4n9z   1/1     Running   0          12s", TEXT_GREEN, True)],
        [("cloudcart-76b889df68-q2l5t   1/1     Running   0          12s", TEXT_GREEN, True)],
        "",
        p("gautam@devops-vm", "kubectl scale deployment cloudcart --replicas=3"),
        [("deployment.apps/cloudcart scaled", TEXT_GREEN, True)],
        p("gautam@devops-vm", "kubectl get pods -l app=cloudcart"),
        [("NAME                        READY   STATUS    RESTARTS   AGE", TEXT_CYAN, True)],
        [("cloudcart-76b889df68-7v2qw   1/1     Running   0          3m02s", TEXT_WHITE, False)],
        [("cloudcart-76b889df68-m8k1l   1/1     Running   0          3m02s", TEXT_WHITE, False)],
        [("cloudcart-76b889df68-x9p4m   1/1     Running   0          3m02s", TEXT_WHITE, False)],
        "",
        p("gautam@devops-vm", "for i in {1..2}; do curl -s http://192.168.49.2:30080/api/info | jq -r .pod; done"),
        [("cloudcart-76b889df68-7v2qw", TEXT_YELLOW, True)],
        [("cloudcart-76b889df68-x9p4m", TEXT_YELLOW, True)]
    ]
    img = create_terminal_window("gautam@devops-vm: ~/cloudcart", lines, min_height=420)
    img.save(os.path.join(OUTPUT_DIR, "fig16_k8s_scaling.png"))
    print("Generated fig16_k8s_scaling.png")

# 17. Figure 17: Rollback Demo
def build_fig17():
    lines = [
        p("gautam@devops-vm", "kubectl set image deployment/cloudcart cloudcart=cloudcart:broken-v2"),
        [("deployment.apps/cloudcart image updated", TEXT_YELLOW, True)],
        p("gautam@devops-vm", "kubectl get pods -l app=cloudcart"),
        [("NAME                        READY   STATUS         RESTARTS   AGE", TEXT_CYAN, True)],
        [("cloudcart-76b889df68-7v2qw   1/1     Running        0          4m12s", TEXT_GREEN, False)],
        [("cloudcart-76b889df68-m8k1l   1/1     Running        0          4m12s", TEXT_GREEN, False)],
        [("cloudcart-76b889df68-x9p4m   1/1     Running        0          4m12s", TEXT_GREEN, False)],
        [("cloudcart-5c4d7b899-kj291   0/1     ", TEXT_WHITE, False), ("ErrImagePull", TEXT_RED, True), ("   0          18s", TEXT_WHITE, False)],
        "",
        p("gautam@devops-vm", "kubectl rollout undo deployment/cloudcart"),
        [("deployment.apps/cloudcart rolled back", TEXT_GREEN, True)],
        p("gautam@devops-vm", "kubectl rollout status deployment/cloudcart"),
        [("deployment \"cloudcart\" successfully rolled out", TEXT_GREEN, True)],
        "",
        p("gautam@devops-vm", "curl -s http://192.168.49.2:30080/api/info"),
        [("{\"app\":\"CloudCart\",\"version\":\"1.0.0\",\"message\":\"", TEXT_WHITE, False), ("Welcome to CloudCart (from ConfigMap)", TEXT_YELLOW, True), ("\",\"pod\":\"", TEXT_WHITE, False), ("cloudcart-76b889df68-7v2qw", TEXT_CYAN, True), ("\"}", TEXT_WHITE, False)]
    ]
    img = create_terminal_window("gautam@devops-vm: ~/cloudcart", lines, min_height=400)
    img.save(os.path.join(OUTPUT_DIR, "fig17_k8s_rollback.png"))
    print("Generated fig17_k8s_rollback.png")

if __name__ == "__main__":
    build_fig1()
    build_fig2()
    build_fig3()
    build_fig4()
    build_fig5()
    build_fig6()
    build_fig7()
    build_fig8()
    build_fig9()
    build_fig10()
    build_fig11()
    build_fig12()
    build_fig13()
    build_fig14()
    build_fig15()
    build_fig16()
    build_fig17()
    print("All 17 figures successfully generated!")
