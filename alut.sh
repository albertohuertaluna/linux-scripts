git clone --recursive https://github.com/vancegroup/freealut.git
cd freealut
mkdir build
cd build
cmake -DCMAKE_INSTALL_PREFIX:STRING="../../sdk" ..
make -j 16
make install
cd ..
cd ..
