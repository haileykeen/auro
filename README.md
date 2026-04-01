# auro

cd ~/ros2_ws
# Install any missing Python dependencies for OWL-ViT
pip install transformers torch torchvision timm
# Build your custom nodes
colcon build --symlink-install
source install/setup.bash
