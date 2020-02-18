#!/bin/bash

ffmpeg -i figs_rel/%02d_100_avg_return.png -vf palettegen palette.png

ffmpeg -i figs_rel/%02d_100_avg_return.png -vf "drawtext=fontfile=Arial.ttf: text='Steals\: %{frame_num}': start_number=0: x=(w-tw)/2: y=h-(2*lh): fontcolor=black: fontsize=20: box=1: boxcolor=white: boxborderw=5" -c:a copy figs_frames/%03d.png

ffmpeg -i figs_frames/%03d.png -i palette.png -lavfi paletteuse output.gif