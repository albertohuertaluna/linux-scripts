import subprocess
import os
import shutil
import argparse
from datetime import datetime

def run_command(command, log_file, check=True, verbose=False):
    """Executes a shell command and logs errors if any, with optional verbosity."""
    if verbose:
        print(f"Executing: {command}")
        
    try:
        result = subprocess.run(command, shell=True, check=check, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if verbose:
            print(result.stdout.decode())
    except subprocess.CalledProcessError as e:
        with open(log_file, 'a') as log:
            log.write(f"Command failed: {command}\n")
            log.write(f"Return code: {e.returncode}\n")
            log.write(f"Stdout:\n{e.stdout.decode()}\n")
            log.write(f"Stderr:\n{e.stderr.decode()}\n")
            log.write("="*40 + "\n")
        if verbose:
            print(f"Error occurred while executing: {command}")
            print(f"Return code: {e.returncode}")
            print(f"Stdout:\n{e.stdout.decode()}")
            print(f"Stderr:\n{e.stderr.decode()}")

def clone_build_install_glew(log_file, verbose):
    """Clones, builds, and installs GLEW."""
    # Clone GLEW repository
    run_command('git clone --recursive https://github.com/nigels-com/glew.git', log_file, verbose=verbose)
    
    # Change to the GLEW directory
    os.chdir('glew')
    
    # Change to the auto directory and update Makefile
    os.chdir('auto')
    run_command('sed -i "s/PYTHON ?= python/PYTHON ?= python3/" Makefile', log_file, verbose=verbose)
    
    # Change back to the root of the GLEW directory
    os.chdir('..')
    
    # Build extensions
    run_command('make extensions', log_file, verbose=verbose)
    
    # Change to the build directory
    os.makedirs('build', exist_ok=True)
    os.chdir('build')
    
    # Run CMake and Make
    run_command('cmake -DCMAKE_INSTALL_PREFIX=../../sdk ./cmake', log_file, verbose=verbose)
    run_command('make -j16', log_file, verbose=verbose)
    
    # Install GLEW
    run_command('make install', log_file, verbose=verbose)
    
    # Change back to the previous directory
    os.chdir('../..')

def main(gcc_version, verbose):
    # Define log file
    timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    log_file = f'build_errors_{gcc_version}_{timestamp}.log'
    
    # Set GCC version
    run_command(f'sudo update-alternatives --set gcc /usr/bin/gcc-{gcc_version}', log_file, verbose=verbose)
    run_command(f'sudo update-alternatives --set g++ /usr/bin/g++-{gcc_version}', log_file, verbose=verbose)

    # Clean up and create directories
    if os.path.exists('frameworks'):
        shutil.rmtree('frameworks')
    os.makedirs('frameworks')
    os.chdir('frameworks')

    # Clone, build, and install GLEW
    clone_build_install_glew(log_file, verbose)

    # Function to clone, build, and install other libraries
    def clone_build_install(repo_url, build_dir_name, cmake_args=[], make_args=['-j 16'], install_args=[]):
        repo_name = repo_url.split('/')[-1].replace('.git', '')
        run_command(f'git clone --recursive {repo_url}', log_file, verbose=verbose)
        os.chdir(repo_name)
        os.makedirs(build_dir_name, exist_ok=True)
        os.chdir(build_dir_name)
        cmake_command = f'cmake {" ".join(cmake_args)} ..'
        run_command(cmake_command, log_file, verbose=verbose)
        run_command(f'make {" ".join(make_args)}', log_file, verbose=verbose)
        run_command(f'make install {" ".join(install_args)}', log_file, verbose=verbose)
        os.chdir('..')
        os.chdir('..')

    # Clone and build other libraries
    clone_build_install(
        'https://github.com/glfw/glfw.git',
        'build',
        cmake_args=['-DCMAKE_BUILD_TYPE=Release', '-DCMAKE_INSTALL_PREFIX=../../sdk']
    )

    clone_build_install(
        'https://github.com/assimp/assimp.git',
        'build',
        cmake_args=['-DCMAKE_BUILD_TYPE=Release', '-DCMAKE_INSTALL_PREFIX=../../sdk']
    )

    clone_build_install(
        'https://github.com/erincatto/box2d.git',
        'build',
        cmake_args=['-DBOX2D_BUILD_DOCS=ON', '-DCMAKE_BUILD_TYPE=Release', '-DCMAKE_INSTALL_PREFIX=../../sdk']
    )

    clone_build_install(
        'https://github.com/bulletphysics/bullet3.git',
        'build',
        cmake_args=['-DCMAKE_BUILD_TYPE=Release', '-DCMAKE_INSTALL_PREFIX=../../sdk']
    )

    clone_build_install(
        'https://github.com/slembcke/Chipmunk2D.git',
        'build',
        cmake_args=['-DCMAKE_BUILD_TYPE=Release', '-DCMAKE_INSTALL_PREFIX=../../sdk']
    )

    clone_build_install(
        'https://github.com/g-truc/glm.git',
        'build',
        cmake_args=['-DCMAKE_BUILD_TYPE=Release', '-DCMAKE_INSTALL_PREFIX=../../sdk']
    )

    clone_build_install(
        'https://github.com/g-truc/gli',
        'build',
        cmake_args=['-DCMAKE_BUILD_TYPE=Release', '-DCMAKE_INSTALL_PREFIX=../../sdk']
    )

    # Clone and build Boost
    run_command('git clone --recursive https://github.com/boostorg/boost.git', log_file, verbose=verbose)
    os.chdir('boost')
    run_command('./bootstrap.sh', log_file, verbose=verbose)
    run_command('./b2 install --prefix=../sdk link=shared toolset=gcc', log_file, verbose=verbose)
    run_command('./b2 install --prefix=../sdk link=static toolset=gcc', log_file, verbose=verbose)
    os.chdir('..')

    # Clone and move stb
    run_command('git clone https://github.com/nothings/stb.git', log_file, verbose=verbose)
    shutil.move('stb', 'sdk/include')

    # Clone and build FreeALUT
    clone_build_install(
        'https://github.com/vancegroup/freealut.git',
        'build',
        cmake_args=['-DCMAKE_INSTALL_PREFIX:STRING="../../sdk"']
    )

    # Clone and build OpenAL Soft
    clone_build_install(
        'https://github.com/kcat/openal-soft.git',
        'build',
        cmake_args=['-DCMAKE_INSTALL_PREFIX:STRING="../../sdk"']
    )

    # Clone and build FreeType
    clone_build_install(
        'https://github.com/freetype/freetype.git',
        'build',
        cmake_args=['-DCMAKE_INSTALL_PREFIX:STRING="../../sdk"']
    )

    # Clone and clean ImGui
    run_command('git clone --recursive https://github.com/ocornut/imgui.git', log_file, verbose=verbose)
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
        'imgui_impl_win32.cpp', 'imgui_impl_win32.h', 'imgui_impl_vulkan.h', 'imgui_impl_vulkan.cpp'
    ]:
        os.remove(impl)
    os.chdir('../../../..')

    # Package and move the SDK
    tar_filename = f'sdk_gcc{gcc_version}-{timestamp}.tar.xz'
    run_command(f'tar -cvJf {tar_filename} .', log_file, verbose=verbose)
    shutil.move(tar_filename, '../..')
    shutil.move('sdk', f'sdk-gcc{gcc_version}')
    shutil.move(f'sdk-gcc{gcc_version}', '..')

    # Cleanup
    shutil.rmtree('frameworks')

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Build libraries with a specific GCC version.')
    parser.add_argument('gcc_version', type=str, help='The GCC version to use.')
    parser.add_argument('--verbose', action='store_true', help='Enable verbose output.')
    args = parser.parse_args()
    
    main(args.gcc_version, args.verbose)
