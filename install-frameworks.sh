sudo update-alternatives --set gcc /usr/bin/gcc-14
sudo update-alternatives --set g++ /usr/bin/g++-14

rm -rf frameworks
mkdir frameworks
cd frameworks


git clone --recursive https://github.com/glfw/glfw.git 
cd glfw/
mkdir build
cd build
cmake -DCMAKE_BUILD_TYPE=Release -DCMAKE_INSTALL_PREFIX=../../sdk ..
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

git clone --recursive https://github.com/assimp/assimp.git
cd assimp
mkdir build
cd build
cmake -DCMAKE_BUILD_TYPE=Release -DCMAKE_INSTALL_PREFIX=../../sdk ..
make -j 16
make install
cd ..
cd ..


git clone --recursive https://github.com/erincatto/box2d.git
cd box2d
mkdir build
cd build
cmake -DBOX2D_BUILD_DOCS=ON -DCMAKE_BUILD_TYPE=Release -DCMAKE_INSTALL_PREFIX=../../sdk ..
make -j 16
make install
cd ..
cd ..

git clone --recursive https://github.com/bulletphysics/bullet3.git bullet
cd bullet
mkdir build
cd build
cmake -DCMAKE_BUILD_TYPE=Release -DCMAKE_INSTALL_PREFIX=../../sdk ..
make -j 16
make install
cd ..
cd ..

git clone --recursive https://github.com/slembcke/Chipmunk2D.git
cd Chipmunk2D
mkdir build
cd build
cmake -DCMAKE_BUILD_TYPE=Release -DCMAKE_INSTALL_PREFIX=../../sdk ..
make -j 16
make install
cd ..
cd ..

git clone --recursive  https://github.com/g-truc/glm.git
cd glm
mkdir build
cd build
cmake -DCMAKE_BUILD_TYPE=Release -DCMAKE_INSTALL_PREFIX=../../sdk ..
make -j 16
make install
cd ..
cd ..

git clone --recursive https://github.com/g-truc/gli
cd gli
mkdir build
cd build
cmake -DCMAKE_BUILD_TYPE=Release -DCMAKE_INSTALL_PREFIX=../../sdk ..
make -j 16
make install
cd ..
cd ..

git clone https://github.com/boostorg/boost.git
cd boost
./bootstrap.sh
./b2 install --prefix=../sdk link=shared toolset=gcc
./b2 install --prefix=../sdk link=static toolset=gcc
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
mv imgui sdk/include
timestamp=$(date +%Y%m%d_%H%M%S) && tar -cvJf sdk_$timestamp.tar.xz sdk
mv -v *.tar.xz ..

cd ..

rm -rf frameworks
