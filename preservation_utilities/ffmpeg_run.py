import os
import ffmpeg
import errno
# requires installation of ffmpeg-python under pip. don't use python-ffmpeg as it won't work

def create_dir(filename):
    if not os.path.exists(os.path.dirname(filename)):
        try:
            os.makedirs(os.path.dirname(filename), exist_ok=True)
        except OSError as exc:
            if exc.errno != errno.EExist:
                raise

accept_list = ["avi", "wmv", "mpeg", "m4v", "mpg"]

for dirpath, dirnames, filenames in os.walk("."):
    for filename in filenames:
        filename_test = filename.split(".")[-1]
        if filename_test in accept_list:
            filename1 = os.path.join(dirpath, filename)
            source_dir = dirpath.split("/")[-1]
            target_dir = dirpath.replace(source_dir, "preservica_presentation2_lnk")
            new_filename = f"{filename[:-len(filename_test)]}mp4"
            filename2 = os.path.join(target_dir, new_filename)
            print(f"starting {filename1}")
            stream = ffmpeg.input(filename1)
            stream = ffmpeg.output(stream, filename2)
            ffmpeg.run(stream)
            print(f"{filename1} complete, moving on")
print("all done")