if [ -d "./repos" ]; then
    find ./repos -type d -name ".git" -execdir sh -c 'echo "Updating $(dirname $(pwd))"; git pull' \;

else
    echo "Directory does not exist."
    mkdir repos
    cd repos
    git clone --recursive https://github.com/SpartanJ/SOIL2.git 
    git clone --recursive https://github.com/boostorg/boost.git 
    git clone --recursive https://github.com/assimp/assimp.git
    git clone --recursive https://github.com/glfw/glfw.git 
    git clone --recursive https://github.com/nigels-com/glew.git
    git clone --recursive https://github.com/erincatto/box2d.git
    git clone --recursive https://github.com/bulletphysics/bullet3.git bullet
    git clone --recursive https://github.com/slembcke/Chipmunk2D.git
    git clone --recursive https://github.com/g-truc/glm.git
    git clone --recursive https://github.com/g-truc/gli
    git clone             https://github.com/nothings/stb.git
    git clone --recursive https://github.com/vancegroup/freealut.git
    git clone --recursive https://github.com/kcat/openal-soft.git
    git clone --recursive https://github.com/freetype/freetype.git
    git clone --recursive https://github.com/ocornut/imgui.git
    cd ..
fi
sh linux-scripts/install-frameworks.sh 9
sh linux-scripts/install-frameworks.sh 10
sh linux-scripts/install-frameworks.sh 11
sh linux-scripts/install-frameworks.sh 12
sh linux-scripts/install-frameworks.sh 13
sh linux-scripts/install-frameworks.sh 14
sh linux-scripts/install-frameworks.sh 15
