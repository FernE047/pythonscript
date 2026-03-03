from turn_video_into_frames import turn_video_into_frames
from convert_frames_to_bw import convert_frames_to_bw
from display_video_as_ascii import display_video

def main() -> None:
    turn_video_into_frames()
    convert_frames_to_bw()
    display_video()

if __name__ == "__main__":
    main()