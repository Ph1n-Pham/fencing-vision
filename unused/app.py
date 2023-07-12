# code based on: https://github.com/xugaoxiang/yolov5-streamlit

import streamlit as st #web app and camera
import numpy as np # for image processing 
from PIL import Image #Image processing 
import cv2 #computer vision 
import torch
from io import *
import glob
from datetime import datetime
import os
import wget
from video_predict import runVideo
from ultralytics import YOLO
import subprocess
from utils import get_detection_folder, check_folders
import redirect as rd

# This will check if we have all the folders to save our files for inference
check_folders()

# Configurations
CFG_MODEL_PATH = "trained_models/best.pt"
CFG_ENABLE_URL_DOWNLOAD = False
CFG_ENABLE_VIDEO_PREDICTION = True
if CFG_ENABLE_URL_DOWNLOAD:
    # Configure this if you set cfg_enable_url_download to True
    url = "https://archive.org/download/yoloTrained/yoloTrained.pt"
# End of Configurations

def imageInput(model, src):

    if src == 'Upload your own data.':
        image_file = st.file_uploader(
            "Upload An Image", type=['png', 'jpeg', 'jpg'])
        col1, col2 = st.columns(2)
        if image_file is not None:
            img = Image.open(image_file)
            with col1:
                st.image(img, caption='Uploaded Image',
                         use_column_width='always')
            ts = datetime.timestamp(datetime.now())
            imgpath = os.path.join('data/uploads', str(ts)+image_file.name)
            outputpath = os.path.join(
                'data/outputs', os.path.basename(imgpath))
            with open(imgpath, mode="wb") as f:
                f.write(image_file.getbuffer())

            with st.spinner(text="Predicting..."):
                # Load model
                pred = model(imgpath)
                pred.render()
                # save output to file
                for im in pred.ims:
                    im_base64 = Image.fromarray(im)
                    im_base64.save(outputpath)

            # Predictions
            img_ = Image.open(outputpath)
            with col2:
                st.image(img_, caption='Model Prediction(s)',
                         use_column_width='always')

    elif src == 'From example data.':
        # Image selector slider
        imgpaths = glob.glob('dataset/inference/image/*')
        if len(imgpaths) == 0:
            st.write(".")
            st.error(
                'No images found, Please upload example images in data/example_images', icon="")
            return
        imgsel = st.slider('Select random images from example data.',
                           min_value=1, max_value=len(imgpaths), step=1)
        image_file = imgpaths[imgsel-1]
        submit = st.button("Predict!")
        col1, col2 = st.columns(2)
        with col1:
            img = Image.open(image_file) #image_file is path
            st.image(img, caption='Selected Image', use_column_width='always')
        with col2:
            if image_file is not None and submit:
                #with st.spinner(text="Predicting..."):
                    # # Load model
                    # model = loadmodel()
                    # pred = model(image_file, stream=True)
                    # pred.render()
                    # # save output to file
                    # for im in pred.ims:
                    #     im_base64 = Image.fromarray(im)
                    #     im_base64.save(os.path.join(
                    #         'data/outputs', os.path.basename(image_file)))
                with rd.stderr(format='markdown', to=st.sidebar), st.spinner('Wait for it...'):
                    print(subprocess.run(['yolo', 'task=segment', 'mode=predict', 'model=trained_models/best.pt', 'conf=0.25', 'source={}'.format(image_file)],capture_output=True, universal_newlines=True).stderr)


                # Display predicton
                img_ = Image.open(os.path.join(
                    'data/images', os.path.basename(image_file)))
                st.image(img_, caption='Model Prediction(s)')
                st.balloons()


def videoInput(model, src):
    if src == 'Upload your own data.':
        uploaded_video = st.file_uploader(
            "Upload A Video", type=['mp4', 'mpeg', 'mov'])
        pred_view = st.empty()
        warning = st.empty()
        if uploaded_video != None:

            # Save video to disk
            ts = datetime.timestamp(datetime.now())  # timestamp a upload
            uploaded_video_path = os.path.join(
                'data/uploads', str(ts)+uploaded_video.name)
            with open(uploaded_video_path, mode='wb') as f:
                f.write(uploaded_video.read())

            # Display uploaded video
            with open(uploaded_video_path, 'rb') as f:
                video_bytes = f.read()
            st.video(video_bytes)
            st.write("Uploaded Video")
            submit = st.button("Run Prediction")
            if submit:
                runVideo(model, uploaded_video_path, pred_view)#, warning)##############

    elif src == 'From example data.':
        # Image selector slider
        videopaths = glob.glob('dataset/inference/video/*')
        if len(videopaths) == 0:
            st.error(
                'No videos found, Please upload example videos in data/example_videos', icon="⚠️")
            return
        imgsel = st.slider('Select random video from example data.',
                           min_value=1, max_value=len(videopaths), step=1)
        pred_view = st.empty()
        video = videopaths[imgsel-1]
        submit = st.button("Predict!")
        model = loadmodel()
        if submit:
            runVideo(model, video, pred_view)#, warning)


def instance_segmentation(uploaded_vid): #input is a video BytesIO object
    pass
    return uploaded_vid

def segmentation(uploaded_vid):
    return uploaded_vid

def get_cap(uploaded_file):
    return cv2.VideoCapture(uploaded_file)

st.title("📷 Fencing with Segmentation")
st.write("This Web App is to equip your fencing videos with instance segmentation.")

# collect the user input 

#file_image = st.sidebar.file_uploader("Upload your Photos", type=['jpeg','jpg','png'])

file_video = st.sidebar.file_uploader("Upload your Videos", type=['mp4','avi','mov'])

def main():
    CFG_MODEL_PATH = "trained_models/best.pt"
    if CFG_ENABLE_URL_DOWNLOAD:
        downloadModel()
        
    else:
        if not os.path.exists(CFG_MODEL_PATH):
            st.error(
                'Model not found, please config if you wish to download model from url set `cfg_enable_url_download = True`  ', icon="⚠️")

    # -- Sidebar
    st.sidebar.title('⚙️ Options')
    datasrc = st.sidebar.radio("Select input source.", [
                               'From example data.', 'Upload your own data.'])

    if CFG_ENABLE_VIDEO_PREDICTION:
        option = st.sidebar.radio("Select input type.", ['Image', 'Video'])
    else:
        option = st.sidebar.radio("Select input type.", ['Image'])
    if torch.cuda.is_available():
        deviceoption = st.sidebar.radio("Select compute Device.", [
                                        'cpu', 'cuda'], disabled=False, index=1)
    else:
        deviceoption = st.sidebar.radio("Select compute Device.", [
                                        'cpu', 'cuda'], disabled=True, index=0)
    # -- End of Sidebar

    if option == "Image":
        imageInput(loadmodel(deviceoption), datasrc)
    elif option == "Video":
        videoInput(loadmodel(deviceoption), datasrc)

    # if file_video:
    #     input_vid = file_video
    #     output_vid = segmentation(input_vid)
    #     one, two = st.columns(2)
    #     with one:
    #         st.write("**Input Video**")
    #         st.video(input_vid)
    #     with two:
    #         st.write("**Output Video**")
    #         st.video(output_vid)
    #     ## Download the output video 
    #     if st.button("Download Instance Segmented Video"):
    #         # im_pil = Image.fromarray(output_vid)
    #         # im_pil.save('final_image.jpeg')
    #         st.write('Download completed')
    

    else:
        st.write("You haven't uploaded any image file")

# Downlaod Model from url.
@st.cache_resource
def downloadModel():
    if not os.path.exists(CFG_MODEL_PATH):
        wget.download(url, out="models/")
    
@st.cache_resource
def loadmodel(device='cpu'):
    if CFG_ENABLE_URL_DOWNLOAD:
        CFG_MODEL_PATH = f"models/{url.split('/')[-1:][0]}"
    # model = torch.hub.load('ultralytics/yolov8', 'custom',
    #                        path="trained_models/best.pt", force_reload=True, device=device)
    model = YOLO('trained_models/best.pt')
    return model


if __name__ == '__main__':
    main()
#st.write("Courtesy: 1littlecoder Youtube Channel - [Sketch Code](https://github.com/amrrs/youtube-r-snippets/blob/master/Create_a_Pencil_Sketch_Portrait_with_Python_OpenCV.ipynb)")

#st.markdown("![](https://mms.businesswire.com/media/20200616005364/en/798639/23/Streamlit_Logo_%281%29.jpg=200x200)")