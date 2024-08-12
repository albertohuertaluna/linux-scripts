import subprocess
import os
import shutil
import datetime

def run_command(command, log_file):
    """Executes a shell command and logs its output and errors."""
    with open(log_file, 'a') as log:
        try:
            print(f"Executing: {command}")
            result = subprocess.run(command, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            log.write(result.stdout)
        except subprocess.CalledProcessError as e:
            log.write(f"Command failed: {command}\n")
            log.write(f"Return code: {e.returncode}\n")
            log.write(f"Stdout:\n{e.stdout}\n")
            log.write(f"Stderr:\n{e.stderr}\n")
            log.write("="*40 + "\n")

def main(gcc_version):
    timestamp = datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    log_file = f'build_errors_{gcc_version}_{timestamp}.log'

    # Set GCC version
    run_command(f'sudo update-alternatives --set gcc /usr/bin/gcc-{gcc_version}', log_file)
    run_command(f'sudo update-alternatives --set g++ /usr/bin/g++-{gcc_version}', log_file)

    # Clean up and create directories
    if os.path.exists('frameworks'):
        shutil.rmtree('frameworks')
    os.makedirs('frameworks')
    os.chdir('frameworks')

    # Clone, build, and install GLFW
    run_command('git clone --recursive https://github.com/glfw/glfw.git', log_file)
    os.chdir('glfw')
    os.makedirs('build', exist_ok=True)
    os.chdir('build')
    run_command('cmake -DCMAKE_BUILD_TYPE=Release -DCMAKE_INSTALL_PREFIX=../../sdk ..', log_file)
    run_command('make -j 16', log_file)
    run_command('make install', log_file)
    os.chdir('../../..')

    # Clone, build, and install GLEW
    run_command('git clone --recursive https://github.com/nigels-com/glew.git', log_file)
    os.chdir('glew')
    os.chdir('auto')
    run_command('sed -i "s/PYTHON ?= python/PYTHON ?= python3/" Makefile', log_file)
    os.chdir('..')
    run_command('make extensions', log_file)
    os.makedirs('build', exist_ok=True)
    os.chdir('build')
    run_command('cmake -DCMAKE_INSTALL_PREFIX=../../sdk ./cmake', log_file)
    run_command('make -j16', log_file)
    run_command('make install', log_file)
    os.chdir('../../..')

    # Clone, build, and install Assimp
    run_command('git clone --recursive https://github.com/assimp/assimp.git', log_file)
    os.chdir('assimp')
    os.makedirs('build', exist_ok=True)
    os.chdir('build')
    run_command('cmake -DCMAKE_BUILD_TYPE=Release -DCMAKE_INSTALL_PREFIX=../../sdk ..', log_file)
    run_command('make -j 16', log_file)
    run_command('make install', log_file)
    os.chdir('../../..')

    # Clone, build, and install Box2D
    run_command('git clone --recursive https://github.com/erincatto/box2d.git', log_file)
    os.chdir('box2d')
    os.makedirs('build', exist_ok=True)
    os.chdir('build')
    run_command('cmake -DBOX2D_BUILD_DOCS=ON -DCMAKE_BUILD_TYPE=Release -DCMAKE_INSTALL_PREFIX=../../sdk ..', log_file)
    run_command('make -j 16', log_file)
    run_command('make install', log_file)
    os.chdir('../../..')

    # Clone, build, and install Bullet
    run_command('git clone --recursive https://github.com/bulletphysics/bullet3.git bullet', log_file)
    os.chdir('bullet')
    os.makedirs('build', exist_ok=True)
    os.chdir('build')
    run_command('cmake -DCMAKE_BUILD_TYPE=Release -DCMAKE_INSTALL_PREFIX=../../sdk ..', log_file)
    run_command('make -j 16', log_file)
    run_command('make install', log_file)
    os.chdir('../../..')

    # Clone, build, and install Chipmunk2D
    run_command('git clone --recursive https://github.com/slembcke/Chipmunk2D.git', log_file)
    os.chdir('Chipmunk2D')
    os.makedirs('build', exist_ok=True)
    os.chdir('build')
    run_command('cmake -DCMAKE_BUILD_TYPE=Release -DCMAKE_INSTALL_PREFIX=../../sdk ..', log_file)
    run_command('make -j 16', log_file)
    run_command('make install', log_file)
    os.chdir('../../..')

    # Clone, build, and install GLM
    run_command('git clone --recursive https://github.com/g-truc/glm.git', log_file)
    os.chdir('glm')
    os.makedirs('build', exist_ok=True)
    os.chdir('build')
    run_command('cmake -DCMAKE_BUILD_TYPE=Release -DCMAKE_INSTALL_PREFIX=../../sdk ..', log_file)
    run_command('make -j 16', log_file)
    run_command('make install', log_file)
    os.chdir('../../..')

    # Clone, build, and install Gli
    run_command('git clone --recursive https://github.com/g-truc/gli', log_file)
    os.chdir('gli')
    os.makedirs('build', exist_ok=True)
    os.chdir('build')
    run_command('cmake -DCMAKE_BUILD_TYPE=Release -DCMAKE_INSTALL_PREFIX=../../sdk ..', log_file)
    run_command('make -j 16', log_file)
    run_command('make install', log_file)
    os.chdir('../../..')

    # Clone and build Boost
    run_command('git clone --recursive https://github.com/boostorg/boost.git', log_file)
    os.chdir('boost')
    run_command('./bootstrap.sh', log_file)
    run_command('./b2 install --prefix=../sdk link=shared toolset=gcc', log_file)
    run_command('./b2 install --prefix=../sdk link=static toolset=gcc', log_file)
    os.chdir('..')

    # Clone and move stb
    run_command('git clone https://github.com/nothings/stb.git', log_file)
    shutil.move('stb', 'sdk/include')

    # Clone, build, and install FreeALUT
    run_command('git clone --recursive https://github.com/vancegroup/freealut.git', log_file)
    os.chdir('freealut')
    os.makedirs('build', exist_ok=True)
    os.chdir('build')
    run_command('cmake -DCMAKE_INSTALL_PREFIX:STRING="../../sdk" ..', log_file)
    run_command('make -j 16', log_file)
    run_command('make install', log_file)
    os.chdir('../../..')

    # Clone, build, and install OpenAL Soft
    run_command('git clone --recursive https://github.com/kcat/openal-soft.git', log_file)
    os.chdir('openal-soft')
    os.makedirs('build', exist_ok=True)
    os.chdir('build')
    run_command('cmake -DCMAKE_INSTALL_PREFIX:STRING="../../sdk" ..', log_file)
    run_command('make -j 16', log_file)
    run_command('make install', log_file)
    os.chdir('../../..')

    # Clone, build, and install FreeType
    run_command('git clone --recursive https://github.com/freetype/freetype.git', log_file)
    os.chdir('freetype')
    os.makedirs('build', exist_ok=True)
    os.chdir('build')
    run_command('cmake -DCMAKE_INSTALL_PREFIX:STRING="../../sdk" ..', log_file)
    run_command('make -j 16', log_file)
    run_command('make install', log_file)
    os.chdir('../../..')

    # Clone and clean ImGui
    run_command('git clone --recursive https://github.com/ocornut/imgui.git', log_file)
    shutil.move('imgui', 'sdk/include')
    os.chdir('sdk/include/imgui/backends')
    for impl in [
        'imgui_impl_allegro5.cpp', 'imgui_impl_allegro5.h', 'imgui_impl_android.cpp', 'imgui_impl_android.h',
        'imgui_impl_dx10.cpp', 'imgui_impl_dx10.h', 'imgui_impl_dx11.cpp', 'imgui_impl_dx11.h',
        'imgui_impl_dx12.cpp', 'imgui_impl_dx12.h', 'imgui_impl_dx9.cpp', 'imgui_impl_dx9.h',
        'imgui_impl_glut.cpp', 'imgui_impl_glut.h', 'imgui_impl_metal.h', 'imgui_impl_metal.mm',
        'imgui_impl_osx.h', 'imgui_impl_osx.mm', 'imgui_impl_sdl2.cpp', 'imgui_impl_sdl2.h',
        'imgui_impl_sdl3.cpp', 'imgui_impl_sdl3.h', 'imgui_impl_sdlrenderer2.cpp', 'imgui_impl_sdlrenderer2.h',
        'imgui_impl_sdlrenderer3.cpp', 'imgui_impl_sdlrenderer3.h', 'imgui_impl_wgpu.cpp', 'imgui_impl_wgpu.h',
        'imgui_impl_win32.cpp', 'imgui_impl_win32.h', 'imgui_impl_vulkan.h', 'imgui_impl_vulkan.cpp', 'vulkan'
    ]:
        try:
            os.remove(impl)
        except FileNotFoundError:
            pass
    os.chdir('../../../../')

    # Clean up and archive
    shutil.rmtree('frameworks')
    gcc_ver = subprocess.check_output('gcc --version', shell=True).decode().split()[2].split('-')[0]
    tar_file = f'sdk_gcc{gcc_ver}-{timestamp}.tar.xz'
    run_command(f'tar -cvJf {tar_file} sdk', log_file)
    shutil.move(tar_file, '../..')
    os.chdir('..')
    shutil.move('sdk', f'sdk-gcc{gcc_ver}')
    shutil.move(f'sdk-gcc{gcc_ver}', '..')

if __name__ == "__main__":
    gcc_version = input("Enter GCC version (e.g., 14): ")
    main(gcc_version)
