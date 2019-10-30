import cv2
import numpy as np

#################################################################
#  入力：動画のパス
#  動画をグレースケールかつ200*200にリサイズして
#  動画の最後から150フレームとることにより、
#　[N, 150, 200, 200]となるデータセットを作成し、npy形式で保存する
#################################################################
# (おそらく5秒 = 150フレーム)

def CutFivesec(paths, trans_dir_path, filename):

    videos = []

    for path in paths:
        #ビデオ読み込み
        cap = cv2.VideoCapture(path)
        one_video = []
        print(path)

        while True:
            #1フレーム分読み込み
            ret, frame = cap.read()

            if ret:
                #グレースケールに変換
                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                #200*200にリサイズ
                gray = cv2.resize(gray, (200,200))
                #one_videoに1フレームずつappend
                one_video.append(gray)

            else:
                break

        #動画の最後から150フレーム取ってappend
        videos.append(one_video[-150:])

    videos = np.array(videos)
    print(videos.shape)

    #[N, 150, 200, 200]の動画データセットを一つのnpyファイルにして保存
    np.save(trans_dir_path + "/" + filename, videos)


#CutFivesec("D:/VE/TRANS_DATA/1Q/wide", "D:/VE/TRANS_DATA/1Q", "test1")