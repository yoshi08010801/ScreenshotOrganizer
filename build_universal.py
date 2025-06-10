import os, shutil, subprocess, sys

if getattr(sys, 'frozen', False):
    print("❌ This script was not meant to be run from inside the built app.")
    sys.exit(1)

app_name = "ScreenshotOrganizer"
src_path = "scripts/screenshot_sorter.py"
dist_x86 = "dist_x86"
dist_arm = "dist_arm"
dist_universal = "dist_universal"
zip_name = f"{app_name}_universal.zip"

# ✅ dist_x86 と dist_arm を削除（dist_universal は後で削除）
for d in [dist_x86, dist_arm]:
    if os.path.exists(d):
        shutil.rmtree(d)

PYTHON_X86 = "/usr/local/bin/python3.11"
PYTHON_ARM = "/usr/bin/python3"

# 🔧 x86 ビルド（ログ付き）
try:
    print("⚙️ Building x86_64 version...")
    subprocess.run([
        "arch", "-x86_64", PYTHON_X86, "-m", "PyInstaller",
        "--noconfirm", "--onedir", "--windowed", "--name", app_name,
        "--hidden-import=tkinter", src_path, "--distpath", dist_x86
    ], check=True)
except subprocess.CalledProcessError as e:
    print("❌ x86_64 build failed!")
    print("Error:", e)
    sys.exit(1)

# 🔧 arm ビルド（ログ付き）
try:
    print("⚙️ Building arm64 version...")
    subprocess.run([
        "arch", "-arm64", PYTHON_ARM, "-m", "PyInstaller",
        "--noconfirm", "--onedir", "--windowed", "--name", app_name,
        "--hidden-import=tkinter", src_path, "--distpath", dist_arm
    ], check=True)
except subprocess.CalledProcessError as e:
    print("❌ arm64 build failed!")
    print("Error:", e)
    sys.exit(1)

# ✅ 実行ファイルパス定義
universal_binary = f"{dist_universal}/{app_name}.app/Contents/MacOS/{app_name}"
x86_bin = f"{dist_x86}/{app_name}.app/Contents/MacOS/{app_name}"
arm_bin = f"{dist_arm}/{app_name}.app/Contents/MacOS/{app_name}"

# 🔍 確認してからマージへ
if not os.path.exists(x86_bin) or not os.path.exists(arm_bin):
    print("❌ One or both architecture builds are missing!")
    print(f"x86 path: {x86_bin}")
    print(f"arm path: {arm_bin}")
    sys.exit(1)

# 🧪 Universal バイナリ作成
print("📦 Creating universal .app...")
if os.path.exists(dist_universal):
    shutil.rmtree(dist_universal)
shutil.copytree(f"{dist_arm}/{app_name}.app", f"{dist_universal}/{app_name}.app")

print("🧪 Merging binaries with lipo...")
subprocess.run(["lipo", "-create", x86_bin, arm_bin, "-output", universal_binary], check=True)

# 🗜 ZIP作成
print("🗜️ Zipping app...")
if os.path.exists(zip_name):
    os.remove(zip_name)
shutil.make_archive(app_name + "_universal", 'zip', dist_universal, f"{app_name}.app")

print("✅ Done!")
print("🟢 Universal ZIP generated at:", os.path.abspath(zip_name))
