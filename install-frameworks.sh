sudo update-alternatives --set gcc /usr/bin/gcc-$1
sudo update-alternatives --set g++ /usr/bin/g++-$1

rm -rf frameworks
mkdir frameworks
cd frameworks

git clone --recursive https://github.com/boostorg/boost.git
cd boost
./bootstrap.sh
mkdir build
cd build
cmake -DCMAKE_INSTALL_PREFIX=../../sdk .. 
make -j 16
make install
# ./b2 -j16 install --prefix=../sdk link=shared toolset=gcc
# ./b2 -j16 install --prefix=../sdk link=static toolset=gcc
cd ..
cd ..

git clone --recursive https://github.com/assimp/assimp.git
cd assimp
mkdir build
cd build
cmake  -DBUILD_SHARED_LIBS=ON  -DASSIMP_WARNINGS_AS_ERRORS=OFF -DASSIMP_BUILD_TESTS=OFF -DCMAKE_INSTALL_PREFIX=../../sdk ..
make -j 16
make install
rm -rf * 
cmake  -DBUILD_SHARED_LIBS=OFF -DASSIMP_WARNINGS_AS_ERRORS=OFF -DASSIMP_BUILD_TESTS=OFF -DCMAKE_INSTALL_PREFIX=../../sdk ..
make -j 16
make install
cd ..
cd ..



git clone --recursive https://github.com/glfw/glfw.git 
cd glfw/
mkdir build
cd build
cmake  -DGLFW_BUILD_TESTS=OFF -DGLFW_BUILD_EXAMPLES=OFF -DCMAKE_INSTALL_PREFIX=../../sdk ..
make -j 16
make install
cd ..
cd ..

git clone --recursive https://github.com/nigels-com/glew.git
cd glew
cd auto
sed -i 's/PYTHON ?= python/PYTHON ?= python3/' Makefile
cd ..
make extensions
cd build
cmake -DCMAKE_INSTALL_PREFIX=../../sdk ./cmake
make -j16
make install
cd ..
cd ..




git clone --recursive https://github.com/erincatto/box2d.git
cd box2d
mkdir build
cd build
cmake -DBOX2D_SAMPLES=OFF -DBOX2D_BENCHMARKS=OFF -DBOX2D_DOCS=OFF -DBOX2D_PROFILE=OFF	-DBOX2D_VALIDATE=OFF -DBOX2D_UNIT_TESTS=OFF  -DCMAKE_INSTALL_PREFIX=../../sdk ..
	
make -j 16
make install
cd ..
cd ..

git clone --recursive https://github.com/bulletphysics/bullet3.git bullet
cd bullet
mkdir build
cd build
cmake  cmake  -DBUILD_SHARED_LIBS=ON -DBUILD_EXTRAS=OFF -DBUILD_UNIT_TESTS=OFF -DBUILD_BULLET2_DEMOS=OFF -DBUILD_OPENGL3_DEMOS=OFF -DBUILD_CPU_DEMOS=OFF -DBUILD_EXTRAS=OFF -DCMAKE_INSTALL_PREFIX=../../sdk ..
make -j 16
make install
cd ..
cd ..

git clone --recursive https://github.com/slembcke/Chipmunk2D.git
cd Chipmunk2D
mkdir build
cd build
cmake  -DBUILD_DEMOS=OFF -DCMAKE_INSTALL_PREFIX=../../sdk ..
make -j 16
make install
cd ..
cd ..

git clone --recursive  https://github.com/g-truc/glm.git
cd glm
mkdir build
cd build
#cmake  -DCMAKE_INSTALL_PREFIX=../../sdk ..
cmake -DGLM_ENABLE_SIMD_SSE2=ON \
      -DGLM_ENABLE_SIMD_SSE3=ON \
      -DGLM_ENABLE_SIMD_SSSE3=ON \
      -DGLM_ENABLE_SIMD_SSE4_1=ON \
      -DGLM_ENABLE_SIMD_SSE4_2=ON \
      -DGLM_ENABLE_SIMD_AVX=ON \
      -DGLM_ENABLE_SIMD_AVX2=ON \
      -DGLM_BUILD_LIBRARY=ON \
      -DGLM_BUILD_TESTS=OFF \
      -DGLM_ENABLE_CXX_20=ON \
      -DCMAKE_INSTALL_PREFIX=../../sdk ..
make -j 16
make install
cd ..
cd ..

git clone --recursive https://github.com/g-truc/gli
cd gli
mkdir build
cd build
cmake  -DGLI_TEST_ENABLE=OFF -DCMAKE_INSTALL_PREFIX=../../sdk ..
make -j 16
make install
cd ..
cd ..


git clone https://github.com/nothings/stb.git
mv stb sdk/include

git clone --recursive https://github.com/vancegroup/freealut.git
cd freealut
mkdir build
cd build
cmake -DCMAKE_INSTALL_PREFIX:STRING="../../sdk" ..
make -j 16
make install
cd ..
cd ..

git clone --recursive https://github.com/kcat/openal-soft.git
cd openal-soft
mkdir build
cd build
cmake -DCMAKE_INSTALL_PREFIX:STRING="../../sdk" ..
make -j 16
make install
cd ..
cd ..


git clone --recursive https://github.com/freetype/freetype.git
cd freetype
mkdir build
cd build
cmake -DCMAKE_INSTALL_PREFIX:STRING="../../sdk" ..
make -j 16
make install
cd ..
cd ..

git clone --recursive https://github.com/ocornut/imgui.git
cd imgui
cmake_content=$(cat <<'EOF'
cmake_minimum_required(VERSION 3.0)
project(ImGui)

# Source files for ImGui core
set(IMGUI_SRC
    imgui.cpp
    imgui_draw.cpp
    imgui_widgets.cpp
    imgui_tables.cpp
    imgui_demo.cpp
)

# Source files for OpenGL2, OpenGL3, and GLFW backends
set(IMGUI_BACKEND_SRC
    backends/imgui_impl_glfw.cpp
    backends/imgui_impl_opengl3.cpp
    backends/imgui_impl_opengl2.cpp
)

# Add static library
add_library(imgui STATIC ${IMGUI_SRC} ${IMGUI_BACKEND_SRC})

# Include directories for ImGui core and backends
target_include_directories(imgui PUBLIC
    ${CMAKE_CURRENT_SOURCE_DIR}
    ${CMAKE_CURRENT_SOURCE_DIR}/backends
)

# Link necessary libraries (GLFW, OpenGL)
find_package(OpenGL REQUIRED)
find_package(glfw3 REQUIRED)

target_link_libraries(imgui PUBLIC OpenGL::GL glfw)

# Installation configuration for the static library
install(TARGETS imgui
        ARCHIVE DESTINATION lib
)

# Installation of ImGui core and backend header files
install(FILES
    imconfig.h
    imgui.h
    imgui_internal.h
    imstb_rectpack.h
    imstb_textedit.h
    imstb_truetype.h
    backends/imgui_impl_glfw.h
    backends/imgui_impl_opengl3.h
    backends/imgui_impl_opengl2.h
    DESTINATION include/imgui
)
EOF
)
echo "$cmake_content" > CMakeLists.txt
mkdir build
cd build
cmake  -DCMAKE_INSTALL_PREFIX=../../sdk ..
make 
make install
cd ..
cd ..

find . -type d -name ".git" -exec rm -rf {} +
gccver=$(gcc --version | grep gcc | cut -d' ' -f3 | cut -d'-' -f1)
timestamp=$(date +%Y-%m-%d_%H-%M-%S) && tar -cvJf sdk_gcc$1-$timestamp.tar.xz .
mv -v *.tar.xz ../..
pwd
cd ..
mv sdk sdk-gcc$1
mv sdk-gcc$1 ..
cd ..
rm -rf frameworks

