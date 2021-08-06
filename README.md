# AI-Training-Weight-Lift

AI Training Project #1: Weight Lift Counter. The app supports video load and live-camera-streaming. 

## Environment Setup

    conda create -n AI-Training python=3.7 
    conda install -n AI-Training tensorflow # Install tensorflow 
    conda install -n AI-Training -c conda-forge opencv # Install opencv
    conda activate AI-Training # Activate virtual environment
    pip install mediapipe # Install mediapipe # install mediapipe
    python -c 'import tensorflow as tf; print(tf.__version__)' # Check setup

## Run App
   

For video file import:
    
    python run.py -v resource/weight_lift3.mp4
For live-camera-streaming:

    python live_streaming.py

## Demo

Video1:
![480pgif1](https://user-images.githubusercontent.com/13625416/128559429-6073b878-4b42-4d65-a829-0f9eb9417e9b.gif)

Video2:
https://user-images.githubusercontent.com/13625416/128559015-80353398-9982-456b-b913-2bb0e5205563.mov


Live-Streaming:
https://user-images.githubusercontent.com/13625416/128559295-94d3914d-832d-4918-902d-47380b3daa06.mov

