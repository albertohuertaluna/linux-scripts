import sys
import os
import subprocess
import shutil
from datetime import datetime
import time

def run_command(command):
    subprocess.run(command, shell=True, check=True)

def setup_gcc_version(version):
    run_command(f"sudo update-alternatives --set gcc /usr/bin/gcc-{version}")
    run_command(f"sudo update-alternatives --set g++ /usr/bin/g++-{version}")

def check_and_clone_repos():
    if os.path.exists("./repos"):
        os.chdir("./repos")
        for root, dirs, files in os.walk("."):
            if ".git" in dirs:
                os.chdir(root)
                print(f"Updating {os.path.basename(root)}")
                run_command("git pull")
                os.chdir("..")
        os.chdir("..")
    else:
        print("Directory 'repos' does not exist. Cloning repositories...")
        os.mkdir("repos")
        os.chdir("repos")
        run_command("git clone --recursive https://github.com/boostorg/boost.git")
        run_command("git clone --recursive https://github.com/assimp/assimp.git")
        run_command("git clone --recursive https://github.com/glfw/glfw.git")
        run_command("git clone --recursive https://github.com/nigels-com/glew.git")
        run_command("git clone --recursive https://github.com/erincatto/box2d.git")
        run_command("git clone --recursive https://github.com/bulletphysics/bullet3.git bullet")
        run_command("git clone --recursive https://github.com/slembcke/Chipmunk2D.git")
        run_command("git clone --recursive https://github.com/g-truc/glm.git")
        run_command("git clone --recursive https://github.com/g-truc/gli.git")
        run_command("git clone https://github.com/nothings/stb.git")
        run_command("git clone --recursive https://github.com/vancegroup/freealut.git")
        run_command("git clone --recursive https://github.com/kcat/openal-soft.git")
        run_command("git clone --recursive https://github.com/freetype/freetype.git")
        run_command("git clone --recursive https://github.com/ocornut/imgui.git")
        os.chdir("..")

def prepare_frameworks():
    if os.path.exists("frameworks"):
        shutil.rmtree("frameworks")
    os.mkdir("frameworks")
    os.chdir("frameworks")
    shutil.copytree("../repos", ".", dirs_exist_ok=True)
    for root, dirs, files in os.walk("."):
        if "build" in dirs and "glew" not in root:
            shutil.rmtree(os.path.join(root, "build"))

def build_boost():
    os.chdir("boost")
    os.mkdir("build")
    os.chdir("build")
    run_command("cmake -DBOOST_RUNTIME_LINK=ON -DCMAKE_INSTALL_PREFIX=../../sdk ..")
    run_command("make -j 16")
    run_command("make install")
    os.chdir("../..")

def build_assimp():
    os.chdir("assimp")
    os.mkdir("build")
    os.chdir("build")
    run_command("cmake -DBUILD_SHARED_LIBS=OFF -DASSIMP_WARNINGS_AS_ERRORS=OFF -DASSIMP_BUILD_TESTS=OFF -DCMAKE_INSTALL_PREFIX=../../sdk ..")
    run_command("make -j 16")
    run_command("make install")
    os.chdir("../..")

def build_glfw():
    os.chdir("glfw")
    os.mkdir("build")
    os.chdir("build")
    run_command("cmake -DGLFW_BUILD_TESTS=OFF -DGLFW_BUILD_EXAMPLES=OFF -DCMAKE_INSTALL_PREFIX=../../sdk ..")
    run_command("make -j 16")
    run_command("make install")
    os.chdir("../..")

def build_glew():
    os.chdir("glew/auto")
    run_command("sed -i 's/PYTHON ?= python/PYTHON ?= python3/' Makefile")
    os.chdir("..")
    run_command("make extensions")
    run_command("make")
    run_command("make install GLEW_DEST=../sdk")
    run_command("mv ../sdk/lib64/* ../sdk/lib")
    run_command("rm -rf ../sdk/lib64")
    run_command("pwd")
    os.chdir("..")
    

def build_box2d():
    os.chdir("box2d")
    os.mkdir("build")
    os.chdir("build")
    run_command("cmake -DBOX2D_SAMPLES=OFF -DBOX2D_BENCHMARKS=OFF -DBOX2D_DOCS=OFF -DBOX2D_PROFILE=OFF -DBOX2D_VALIDATE=OFF -DBOX2D_UNIT_TESTS=OFF -DCMAKE_INSTALL_PREFIX=../../sdk ..")
    run_command("make -j 16")
    run_command("make install")
    os.chdir("..")
    shutil.move("include/box2d", "../sdk/include")
    os.chdir("..")

def build_bullet():
    os.chdir("bullet")
    os.mkdir("build")
    os.chdir("build")
    run_command("cmake -DBUILD_SHARED_LIBS=OFF -DBUILD_EXTRAS=OFF -DBUILD_UNIT_TESTS=OFF -DBUILD_BULLET2_DEMOS=OFF -DBUILD_OPENGL3_DEMOS=OFF -DBUILD_CPU_DEMOS=OFF -DCMAKE_INSTALL_PREFIX=../../sdk ..")
    run_command("make -j 16")
    run_command("make install")
    os.chdir("../..")

def build_chipmunk2d():
    os.chdir("Chipmunk2D")
    os.mkdir("build")
    os.chdir("build")
    run_command("cmake -DINSTALL_STATIC=ON -DBUILD_SHARED=OFF -BUILD_STATIC=ON -DBUILD_DEMOS=OFF -DCMAKE_INSTALL_PREFIX=../../sdk ..")
    run_command("make -j 16")
    run_command("make install")
    os.chdir("../..")

def build_glm():
    os.chdir("glm")
    os.mkdir("build")
    os.chdir("build")
    run_command("cmake -DGLM_ENABLE_SIMD_SSE2=ON -DGLM_ENABLE_SIMD_SSE3=ON -DGLM_ENABLE_SIMD_SSSE3=ON "
                "-DGLM_ENABLE_SIMD_SSE4_1=ON -DGLM_ENABLE_SIMD_SSE4_2=ON -DGLM_ENABLE_SIMD_AVX=ON "
                "-DGLM_ENABLE_SIMD_AVX2=ON -DGLM_BUILD_LIBRARY=ON -DGLM_BUILD_TESTS=OFF -DGLM_ENABLE_CXX_20=ON "
                "-DCMAKE_INSTALL_PREFIX=../../sdk ..")
    run_command("make -j 16")
    run_command("make install")
    os.chdir("../..")

def build_gli():
    os.chdir("gli")
    os.mkdir("build")
    os.chdir("build")
    run_command("cmake -DGLI_TEST_ENABLE=OFF -DCMAKE_INSTALL_PREFIX=../../sdk ..")
    run_command("make -j 16")
    run_command("make install")
    os.chdir("../..")

def build_freealut():
    run_command("git clone --recursive https://github.com/vancegroup/freealut.git")
    os.chdir("freealut")
    os.mkdir("build")
    os.chdir("build")
    run_command("cmake -DBUILD_SHARED_LIBS=OFF -DBUILD_DEMOS=OFF -DCMAKE_INSTALL_PREFIX=../../sdk ..")
    run_command("make -j 16")
    run_command("make install")
    os.chdir("../..")

def build_openal_soft():
    os.chdir("openal-soft")
    os.mkdir("build")
    os.chdir("build")
    run_command("cmake -DLIBTYPE=STATIC -DALSOFT_STATIC_LIBGCC=ON -DALSOFT_TESTS=OFF -DALSOFT_INSTALL_EXAMPLES=OFF "
                "-DALSOFT_EXAMPLES=OFF -DCMAKE_INSTALL_PREFIX=../../sdk ..")
    run_command("make -j 16")
    run_command("make install")
    os.chdir("../..")

def build_freetype():
    os.chdir("freetype")
    os.mkdir("build")
    os.chdir("build")
    run_command("cmake -DBUILD_SHARED_LIBS=false -DCMAKE_INSTALL_PREFIX=../../sdk ..")
    run_command("make -j 16")
    run_command("make install")
    os.chdir("../..")

def cleanup_git_build_dirs():
    for root, dirs, files in os.walk("frameworks"):
        if ".git" in dirs:
            shutil.rmtree(os.path.join(root, ".git"))
        if "build" in dirs:
            shutil.rmtree(os.path.join(root, "build"))

def create_archive(version):
    os.chdir("sdk")
    os.chdir("lib")
    os.mkdir("shared")
    for file in os.listdir("."):
        if file.endswith(".so") or file.endswith(".so.*"):
            shutil.move(file, "shared/")
    for root, dirs, files in os.walk("."):
        for dir in dirs:
            if dir != "shared" and dir != "static":
                shutil.rmtree(os.path.join(root, dir))
    shutil.rmtree("shared")
    os.chdir("../..")
    gccver = subprocess.getoutput("gcc --version | grep gcc | cut -d' ' -f3 | cut -d'-' -f1")
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    run_command(f"tar -cvJf sdk_gcc{version}-{timestamp}.tar.xz sdk")
    shutil.move(f"sdk_gcc{version}-{timestamp}.tar.xz", "../..")
    os.chdir("..")
    shutil.move("sdk", f"sdk-gcc{version}")
    shutil.move(f"sdk-gcc{version}", "..")
    shutil.rmtree("frameworks")    

def main(version):
    start_time = time.time()  
    setup_gcc_version(version)
    check_and_clone_repos()
    prepare_frameworks()
    build_glew()
    build_glfw()
    build_boost()
    build_assimp()
    build_box2d()
    build_bullet()
    build_chipmunk2d()
    build_glm()
    build_gli()
    build_freealut()
    build_openal_soft()
    build_freetype() 
    cleanup_git_build_dirs()
    create_archive(version)

    # Additional build functions can be added here

    # Archive and clean up
    timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    run_command(f"tar -cvJf sdk_gcc{version}-{timestamp}.tar.xz -C sdk .")
    shutil.move(f"sdk_gcc{version}-{timestamp}.tar.xz", "../..")
    shutil.move("sdk", f"sdk-gcc{version}")
    shutil.move(f"sdk-gcc{version}", "../..")
    os.chdir("..")
    shutil.rmtree("frameworks")
    
    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f"Total execution time: {elapsed_time:.2f} seconds")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 build_sdk.py <gcc_version>")
        sys.exit(1)

    version = sys.argv[1]
    main(version)
