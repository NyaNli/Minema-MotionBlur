import os
import sys
import subprocess
import numpy as np

def get_ffmpeg():
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(os.path.dirname(os.path.abspath(sys.executable)), 'ffmpeg.exe')
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), 'ffmpeg.exe')

def get_arg(args, arg, default=None):
    if arg in args:
        return args[args.index(arg) + 1]
    else:
        if default:
            return default
        raise Exception('No such argument: %s' % str(arg))

def reset_arg(args, arg, value):
    if arg in args:
        args[args.index(arg) + 1] = value
    else:
        raise Exception('No such argument: %s' % str(arg))

def remove_arg(args, arg):
    if arg in args:
        args.remove(args[args.index(arg) + 1])
        args.remove(arg)

def calc_size(s):
    ss = s.split('x')
    return int(ss[0]) * int(ss[1])

# -mb_frames 10
# -f rawvideo -pix_fmt bgr24 -s %WIDTH%x%HEIGHT% -r %FPS% -i - -vf vflip -c:v libx264 -preset ultrafast -tune zerolatency -qp 18 -pix_fmt yuv420p %NAME%.mp4
if __name__ == "__main__":
    args = list(sys.argv)
    args.remove(args[0])

    blur_frames = float(get_arg(args, '-mb_frames', '10'))
    remove_arg(args, '-mb_frames')

    frame_size = get_arg(args, '-s')
    frame_rate = float(get_arg(args, '-r'))
    pixel_format = get_arg(args, '-pix_fmt')
    reset_arg(args, '-r', str(frame_rate // blur_frames))

    ffmpeg = subprocess.Popen([get_ffmpeg()] + args, stdin=subprocess.PIPE, universal_newlines=False, encoding=None, errors=None)

    pixels = calc_size(frame_size)
    if pixel_format == 'bgr24':
        pixel_size = 3
    else: # rgba32
        pixel_size = 4
    size = pixels * pixel_size

    done = False

    while not done:
        for i in range(int(blur_frames) + 1):
            if i == int(blur_frames):
                break
            data = sys.stdin.buffer.read(size)
            if not data or len(data) < size:
                done = True
                break

            if i == 0:
                buffer = np.frombuffer(data, dtype=np.uint8).astype(np.int)
            else:
                buffer += np.frombuffer(data, dtype=np.uint8).astype(np.int)

        if i > 0:
            buffer = (buffer / i + .5).astype(np.uint8)
            ffmpeg.stdin.write(buffer.tobytes())

    ffmpeg.stdin.close()
    ffmpeg.wait()