sudo apt -y install g*-9
sudo apt -y install g*-10
sudo apt -y install g*-11
sudo apt -y install g*-12
sudo apt -y install g*-13
sudo apt -y install g*-14
sudo apt -y install synaptic 
sudo apt -y install cmake git blender mm3d gimp nasm yasm geany* flex bison 
sudo apt -y install *boost*83* *assimp* *soil* *stb* freetype* *glm*dev *glew-dev mesa-utils *glfw3-dev *freeglut* *froga* *irrl* *sdl2* *sfml* *allegro*
sudo snap install code --classic
sudo apt -y install dotnet*8*
code --install-extension ms-dotnettools.csharp
dotnet new --install MonoGame.Templates.CSharp
dotnet new mgdesktopgl -o MyGame
cd MyGame
dotnet build
