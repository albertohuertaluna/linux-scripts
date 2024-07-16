sudo update-alternatives --set gcc /usr/bin/gcc-11
sudo update-alternatives --set g++ /usr/bin/g++-11
rm -rf tutorials
mkdir tutorials
cd tutorials
#=======================================================================
#GET REPOS!!
#=======================================================================
git clone --recursive https://github.com/RayTracing/raytracing.github.io.git
git clone --recursive https://github.com/capnramses/antons_opengl_tutorials_book.git anton_gl
git clone --recursive https://github.com/opengl-tutorials/ogl.git opengl-tutorial
git clone --recursive https://github.com/JoeyDeVries/LearnOpenGL.git learn-opengl
git clone --recursive https://github.com/emeiri/ogldev.git ogldev
git clone --recursive https://github.com/PacktPublishing/OpenGL-4-Shading-Language-Cookbook-Third-Edition.git opengl-shading-book
git clone --recursive https://github.com/mmp/pbrt-v4 
git clone --recursive https://github.com/SaschaWillems/Vulkan.git vulkan-examples
git clone --recursive https://github.com/openglsuperbible/sb7code.git super-bible-7
#=======================================================================
#RAYTRACING ON THE WEEKEND!
#=======================================================================
cd raytracing.github.io/
mkdir build
cd build
cmake ..
make -j 16
cd ..
cd ..
#=======================================================================
#ANTON'S TUTORIALS
#=======================================================================
cd anton_gl
./build_all_linux_osx.sh
cd ..
#=======================================================================
#OPENGL SUPERBIBLE
#=======================================================================
cd super-bible-7
sed -i 's/set(COMMON_LIBS sb7 glfw3 X11 Xrandr Xinerama Xi Xxf86vm Xcursor GL rt dl)/set(COMMON_LIBS sb7 glfw X11 Xrandr Xinerama Xi Xxf86vm Xcursor GL rt dl)/' CMakeLists.txt
mkdir build
cd build
cmake ..
make -j 16
cd ..
cd bin
rm -rf media
git clone https://github.com/albertohuertaluna/sb7media.git media
cd media
mkdir textures
mkdir objects
mkdir shaders
tar xvf textures.tar.xz -C textures
tar xvf ladybug_co.tar.xz -C textures
tar xvf ladybug_nm.tar.xz -C textures
tar xvf terragen1.tar.xz -C textures
tar xvf treelights_2k.tar.xz -C textures
tar xvf objects.tar.xz -C objects
tar xvf shaders.tar.xz -C shaders
cd .. 
cd .. 
cd ..
#=======================================================================
#LEARN OPENGL
#=======================================================================
cd learn-opengl
mkdir build
cd build
cmake ..
make -j 16
cd ..
cd ..
#=======================================================================
#OPENGL TUTORIALS!
#=======================================================================
cd opengl-tutorial
mkdir build
cd build
cmake ..
make -j 16
cd ..
cd ..
#=======================================================================
#PACKT SHADING BOOK!
#=======================================================================
cd opengl-shading-book
mkdir build
cd build
cmake ..
make -j 16
cd ..
cd ..
#=======================================================================
#VULKAN!
#=======================================================================
cd vulkan-examples
mkdir build
cd build
cmake ..
make -j 16
cd ..
cd ..
#=======================================================================
#PBRT4!
#=======================================================================
cd pbrt-v4
mkdir build
cd build
cmake -DPBRT_BUILD_GPU_RENDERER=ON ..
make -j 16
cd ..
cd ..
sudo update-alternatives --set gcc /usr/bin/gcc-14
