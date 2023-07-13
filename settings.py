from pathlib import Path
import sys

# Get the absolute path of the current file
file_path = Path(__file__).resolve()

# Get the parent directory of the current file
root_path = file_path.parent

# Add the root path to the sys.path list if it is not already there
if root_path not in sys.path:
    sys.path.append(str(root_path))

# Get the relative path of the root directory with respect to the current working directory
ROOT = root_path.relative_to(Path.cwd())

# Sources
IMAGE = 'Image'
VIDEO = 'Video'
WEBCAM = 'Webcam'
RTSP = 'RTSP'
YOUTUBE = 'YouTube'

SOURCES_LIST = [IMAGE, VIDEO]#, WEBCAM, RTSP, YOUTUBE]

# Images config
IMAGES_DIR = ROOT / 'data/inference/image'
DEFAULT_IMAGE = IMAGES_DIR / 'office_4.jpg'
DEFAULT_DETECT_IMAGE = IMAGES_DIR / 'office_4_detected.jpg'
IMAGE_1_PATH = IMAGES_DIR / 'AbandonedAbandonedFurseal_mp4-1_jpg.rf.b58e5acde13cfc780a015d6bc0a6386d.jpg'
IMAGE_2_PATH = IMAGES_DIR / 'AbandonedAbsoluteGoldfinch_mp4-4_jpg.rf.ac988d297800cd8b322613668200a0ac.jpg'
IMAGE_3_PATH = IMAGES_DIR / 'AbandonedBackGnu_mp4-3_jpg.rf.ae9d35cc08343aa823415c0f6acec54b.jpg'
IMAGE_4_PATH = IMAGES_DIR / 'BarrenSecondhandAcornwoodpecker_mp4-3_jpg.rf.67b37225576d99878640023e9f72fc27.jpg'
IMAGE_5_PATH = IMAGES_DIR / 'ScalyPleasantAmazonparrot_mp4-0_jpg.rf.965787c98759006e494a540d83283073.jpg'
IMAGE_6_PATH = IMAGES_DIR / 'ShadowyLightheartedGuernseycow_mp4-4_jpg.rf.ba610fb6e34b9cedcab084e37ba3b4a1.jpg'
IMAGES_DICT = {
    'image_1': str(IMAGE_1_PATH),
    'image_2': str(IMAGE_2_PATH),
    'image_3': str(IMAGE_3_PATH),
    'image_4': str(IMAGE_4_PATH),
    'image_5': str(IMAGE_5_PATH),
    'image_6': str(IMAGE_6_PATH),
}



# Videos config
VIDEO_DIR = ROOT / 'data/inference/video'
VIDEO_1_PATH = VIDEO_DIR / 'AbandonedCandidAfricanporcupine.mp4'
VIDEO_2_PATH = VIDEO_DIR / 'BarrenSecondhandAcornwoodpecker-mobile.mp4'
VIDEO_3_PATH = VIDEO_DIR / 'SlimyDependentIbadanmalimbe-mobile.mp4'
#VIDEO_4_PATH = VIDEO_DIR / 'video_4.mp4'
#VIDEO_5_PATH = VIDEO_DIR / 'video_5.mp4'
VIDEOS_DICT = {
    'video_1': VIDEO_1_PATH,
    'video_2': VIDEO_2_PATH,
    'video_3': VIDEO_3_PATH,
    #'video_4': VIDEO_4_PATH,
    #'video_5': VIDEO_5_PATH,
}

# ML Model config
MODEL_DIR = ROOT / 'weights'
DETECTION_MODEL = MODEL_DIR / 'best.pt'
SEGMENTATION_MODEL = MODEL_DIR / 'best.pt'

# Webcam
WEBCAM_PATH = 0
