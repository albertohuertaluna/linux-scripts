import subprocess
import os
import shutil
import argparse
from datetime import datetime

def run_command(command, log_file, check=True, verbose=False):
    """Executes a shell command and logs all output to a specified file, with optional verbosity."""
    if verbose:
        print(f"Executing: {command}")

    try:
        with open(log_file, 'a') as log:
            process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            stdout, stderr = process.communicate()
            log.write(stdout)
            log.write(stderr)
            if verbose:
                print(stdout)
                print(stderr)
            if process.returncode != 0 and check:
                raise subprocess.CalledProcessError(process.returncode, command)
    except subprocess.CalledProcessError as e:
        with open(log_file, 'a') as log:
            log.write(f"Command failed: {command}\n")
            log.write(f"Return code: {e.returncode}\n")
            log.write(f"Stdout:\n{e.stdout}\n")
            log.write(f"Stderr:\n{e.stderr}\n")
            log.write("="*40 + "\n")
        if verbose:
            print(f"Error occurred while executing: {command}")
            print(f"Return code: {e.returncode}")
            print(f"Stdout:\n{e.stdout}")
            print(f"Stderr:\n{e.stderr}")

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

def clone_build_install(repo_url, build_dir_name, cmake_args=[], make_args=['-j 16'], install_args=[], log_file='build.log', verbose=False):
    """Clones, builds, and installs a library, saving logs to a specified file."""
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

def main(gcc_version, verbose):
    # Define log file
    timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    global_log_file = f'build_errors_{gcc_version}_{timestamp}.log'
    
    # Set GCC version
    run_command(f'sudo update-alternatives --set gcc /usr/bin/gcc-{gcc_version}', global_log_file, verbose=verbose)
    run_command(f'sudo update-alternatives --set g++ /usr/bin/g++-{gcc_version}', global_log_file, verbose=verbose)

    # Clean up and create directories
    if os.path.exists('frameworks'):
        shutil.rmtree('frameworks')
    os.makedirs('frameworks')
    os.chdir('frameworks')

    # Clone, build, and install GLEW
    glew_log_file = 'glew.log'
    clone_build_install_glew(glew_log_file, verbose)

    # Clone, build, and install other libraries
    clone_build_install(
        'https://github.com/glfw/glfw.git',
        'build',
        cmake_args=['-DCMAKE_BUILD_TYPE=Release', '-DCMAKE_INSTALL_PREFIX=../../sdk'],
        log_file='glfw.log',
        verbose=verbose
    )

    clone_build_install(
        'https://github.com/assimp/assimp.git',
        'build',
        cmake_args=['-DCMAKE_BUILD_TYPE=Release', '-DCMAKE_INSTALL_PREFIX=../../sdk'],
        log_file='assimp.log',
        verbose=verbose
    )

    clone_build_install(
        'https://github.com/erincatto/box2d.git',
        'build',
        cmake_args=['-DBOX2D_BUILD_DOCS=ON', '-DCMAKE_BUILD_TYPE=Release', '-DCMAKE_INSTALL_PREFIX=../../sdk'],
        log_file='box2d.log',
        verbose=verbose
    )

    clone_build_install(
        'https://github.com/bulletphysics/bullet3.git',
        'build',
        cmake_args=['-DCMAKE_BUILD_TYPE=Release', '-DCMAKE_INSTALL_PREFIX=../../sdk'],
        log_file='bullet.log',
        verbose=verbose
    )

    clone_build_install(
        'https://github.com/slembcke/Chipmunk2D.git',
        'build',
        cmake_args=['-DCMAKE_BUILD_TYPE=Release', '-DCMAKE_INSTALL_PREFIX=../../sdk'],
        log_file='chipmunk2d.log',
        verbose=verbose
    )

    clone_build_install(
        'https://github.com/g-truc/glm.git',
        'build',
        cmake_args=['-DCMAKE_BUILD_TYPE=Release', '-DCMAKE_INSTALL_PREFIX=../../sdk'],
        log_file='glm.log',
        verbose=verbose
    )

    clone_build_install(
        'https://github.com/g-truc/gli',
        'build',
        cmake_args=['-DCMAKE_BUILD_TYPE=Release', '-DCMAKE_INSTALL_PREFIX=../../sdk'],
        log_file='gli.log',
        verbose=verbose
    )

    # Clone and build Boost
    boost_log_file = 'boost.log'
    run_command('git clone --recursive https://github.com/boostorg/boost.git', boost_log_file, verbose=verbose)
    os.chdir('boost')
    run_command('./bootstrap.sh', boost_log_file, verbose=verbose)
    run_command('./b2 install --prefix=../sdk link=shared toolset=gcc', boost_log_file, verbose=verbose)
    run_command('./b2 install --prefix=../sdk link=static toolset=gcc', boost_log_file, verbose=verbose)
    os.chdir('..')

    # Clone and move stb
    stb_log_file = 'stb.log'
    run_command('git clone https://github.com/nothings/stb.git', stb_log_file, verbose=verbose)
    shutil.move('stb', 'sdk/include')

    # Clone and build FreeALUT
    freealut_log_file = 'freealut.log'
    clone_build_install(
        'https://github.com/vancegroup/freealut.git',
        'build',
        cmake_args=['-DCMAKE_INSTALL_PREFIX:STRING="../../sdk"'],
        log_file=freealut_log_file,
        verbose=verbose
    )

    # Clone and build OpenAL Soft
    openal_log_file = 'openal-soft.log'
    clone_build_install(
        'https://github.com/kcat/openal-soft.git',
        'build',
        cmake_args=['-DCMAKE_INSTALL_PREFIX:STRING="../../sdk"'],
        log_file=openal_log_file,
        verbose=verbose
    )

    # Clone and build FreeType
    freetype_log_file = 'freetype.log'
    clone_build_install(
        'https://github.com/freetype/freetype.git',
        'build',
        cmake_args=['-DCMAKE_INSTALL_PREFIX:STRING="../../sdk"'],
        log_file=freetype_log_file,
        verbose=verbose
    )

    # Clone and clean ImGui
    imgui_log_file = 'imgui.log'
    run_command('git clone --recursive https://github.com/ocornut/imgui.git', imgui_log_file, verbose=verbose)
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
    run_command(f'tar -cvJf {tar_filename} .', global_log_file, verbose=verbose)
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
