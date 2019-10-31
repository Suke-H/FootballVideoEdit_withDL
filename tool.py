import os
from glob import glob

def MakeDir(source_dir_path, trans_dir_path):
    # source/長県戦, source/九産戦, ...のようなパスを取得
    paths = glob(source_dir_path + "/**")
    print(paths)

    # trans/長県戦, trans/九産戦, ...となるようフォルダ作成
    for path in paths:
        os.mkdir(trans_dir_path + "/" + os.path.basename(path))

    # source/長県戦/1Q,  source/長県戦/2Qのようなパスを取得
    paths = glob(source_dir_path + "/**/**")
    print(paths)

    # trans/長県戦/1Q, trans/九産戦/1Q, ...となるようフォルダ作成
    for path in paths:
        Q = os.path.basename(path)
        dir = os.path.dirname(path)
        match = os.path.basename(dir)
        make_path = trans_dir_path + "/" + match + "/" + Q
        print(make_path)
        os.mkdir(make_path)

MakeDir("D:/2018data", "D:/2018mp4")


