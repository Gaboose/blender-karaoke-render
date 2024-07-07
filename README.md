# Blender Karaoke Render

An experiment to render karaoke subtitles with headless Blender. The style could be improved but the concept works.

## How to use ##

Put your `lyrics.lrc` in the workdir.

Render a series of images.
```
blender -b project.blend -P script.py -x 1 -o //out/render -a
```

Convert the images to video.
```
ffmpeg -framerate 24 -pattern_type glob -i '*.png' -c:v libx264 -pix_fmt yuv420p out.mp4
```

Or convert the images to video with a blue background.
```
ffmpeg -f lavfi -i color=c=blue:s=1920x1080:r=24 -framerate 24 -pattern_type glob -i '*.png' -filter_complex "[0:v][1:v]overlay=shortest=1,format=yuv420p[out]" -map "[out]" -c:v libx264 -pix_fmt yuv420p out_blue.mp4
```

Chroma key blue back to transparent.
```
gst-launch-1.0 filesrc location='out_blue.mp4' ! decodebin ! videoconvert ! alpha method=blue ! videoconvert ! autovideosink
```