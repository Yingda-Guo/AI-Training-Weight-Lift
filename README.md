# Deep Learning AI Trainer: Weight Lift Counter

Combining Computer Vision with Deep Learning Algorithm, the python application can detect human arms in real-time. Based on the angle changes, the application can detect weight lift movement and count the number of lifts for each arm. The applicaiton supports real-time streaming with low hardware requirement, even without a GPU.

![demo1](https://user-images.githubusercontent.com/13625416/128560715-efa8d10a-57b8-4c55-8d61-2365d552de35.gif)
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

   ![demo1](https://user-images.githubusercontent.com/13625416/128560715-efa8d10a-57b8-4c55-8d61-2365d552de35.gif)



Video2:


   ![demo2](https://user-images.githubusercontent.com/13625416/128560725-5d787f61-0bb5-4ee0-a4b0-fe66333ef295.gif)


Live-Streaming:


   ![demo3](https://user-images.githubusercontent.com/13625416/128560751-6c760a8a-b717-458b-8c5c-d3ed19b0c9a4.gif)

