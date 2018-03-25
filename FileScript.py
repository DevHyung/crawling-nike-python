import os
import shutil
if __name__=="__main__":
    fileList = os.listdir('./')
    jpgList = []
    idx = 0
    for file in fileList:
        try:
            if '(바탕)' in file:
                shutil.move(os.getcwd()+'\\'+file,os.getcwd()+'\\'+file.split('(바탕)')[0]+'\\'+file)
        except:
            print("확인필요 >>> ",file)
    print(">>> 파일 이동완료 !!!")
    input("아무키나누르시면 종료됩니다.")