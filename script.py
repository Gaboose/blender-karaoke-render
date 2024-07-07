import bpy
import re
import datetime

def parse_time(s):
    tm = re.search(r'^(\d\d):(\d\d\.\d+)$', s.strip())
    return datetime.timedelta(minutes=int(tm.group(1)), seconds=float(tm.group(2)))

lrc = open("lyrics.lrc", "r").read().split("\n")
camera = bpy.data.objects['Camera']
scene = bpy.context.scene
text_offset = -2

# Read LRC file's header
header = {}
for i, line in enumerate(lrc):
    m = re.search(r'\[([a-z]+):(.*)\]', line)
    if not m:
        break
    header[m.group(1)] = m.group(2)
lrc = lrc[i:]

# Create a text object for every line
for i, line in enumerate(lrc):
    m = re.search(r'\[([0-9:.]+)\] (.*)', line)
    if not m:
        continue
    
    time = parse_time(m.group(1))
    line = m.group(2)
    
    font_curve = bpy.data.curves.new(type="FONT", name="Font Curve")
    font_curve.body = line
    font_curve.align_x = "CENTER"
    text = bpy.data.objects.new(name="Text", object_data=font_curve)
    text.location.y = -time.total_seconds() + text_offset
    bpy.context.scene.collection.objects.link(text)

# Animate camera
length = parse_time(header['length'])
frame_end = int(scene.render.fps*length.total_seconds())
camera.location.y = 0
camera.keyframe_insert(data_path='location', frame=1)
camera.location.y = -length.total_seconds()
camera.keyframe_insert(data_path='location', frame=frame_end)
scene.frame_end = frame_end

for fc in camera.animation_data.action.fcurves:
    if fc.data_path == 'location':
        for kfp in fc.keyframe_points:
            kfp.interpolation = 'LINEAR'

