# Visual_Data

Python scripts to encode/decode text files from/to mp4 video.

- **encode_file_as_video.py**: encodes a text file into a video
- **decode_file_from_video.py**: decodes text file from the encoded video
- **config.json**
  - **BIT_SIZE**: number of pixels (NxN) to be used for each bit of data
  - **ONE_BIT_COLOR**: color used for the 1 bit
  - **ZERO_BIT_COLOR**: color used for the 0 bit
  - **DELIMITER_COLOR**: color used for delimiting the name and the start/end of the file in the video
  - **FRAME_WIDTH**: width of the video frame
  - **FRAME_HEIGHT**: height of the video frame
  - **FILE_TO_ENCODE**: text file to be encoded
  - **ENCODED_VIDEO**: path and name of the output encoded video file
  - **DECODED_VIDEO_OUTPUT**: path to the directory where decoded output is to be written

## Dependencies

- ffmpeg
- cv2
- numpy

## Example
- File: ![encode_thix.txt](https://github.com/Aedif/visual_data/blob/master/encode_this.txt)
- Video: ![video.mp4](https://github.com/Aedif/visual_data/blob/master/encoded/video.mp4)
