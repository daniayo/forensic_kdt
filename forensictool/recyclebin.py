import os
from datetime import datetime
from forensictool.ntfs_forensic import Extract_File
import hashlib

class ForensicTool:
    def __init__(self, window_ver, drive):
        self._drive = drive
        self._recycle_bin_link = drive + ':\\$Recycle.Bin'
        self._window_ver = window_ver
        self._recycle_bin_link = None
        self._NTFS_tool = Extract_File(drive + ':')

    def SetLink(self):
        if self._window_ver == "window 11":
            print(1)
            self._recycle_bin_link = 'C:\\$Recycle.Bin'
    
    def RecycleBinForensic(self): # 휴지통 포렌식
        result_file = open('휴지통 포렌식 결과.txt', 'w')
        if self._window_ver == "window 11":
            dirs = os.listdir(self._recycle_bin_link) # 휴지통 안의 폴더들
            for dir in dirs:
                try:
                    files = os.listdir(self._recycle_bin_link + '\\' + dir) # 내 진짜 휴지통 안의 삭제된 파일을
                    for file in files:
                        if file[1] == 'I': # 삭제된 파일의 정보를 담고있는 파일
                            
                            f = open(self._recycle_bin_link + '\\' + dir + '\\' + file, 'rb')
                            data = f.read()
                            print(int.from_bytes(data[16:24], 'little') / 1000)
                            result_file.write('파일명 : ' + file + '\n파일 헤더 : ' + str(int.from_bytes(data[:8], 'little')) + '\n원본 파일 크기 : ' + str(int.from_bytes(data[8:16], 'little')) + '\n삭제된 시간 : ' + str(datetime.fromtimestamp(int.from_bytes(data[16:24], 'little') / 1e9)) + '\n\n')
                            # 삭제된 시간 수정 필요함
                            f.close()

                except Exception as e:
                    print(e)
                    pass
        
        print('Recycle Bin Forensic Done.')
        result_file.close()

    def NTFSForensic(self): # NTFS 포렌식
        self._NTFS_tool.Extract('/$MFT','$MFT')
        self._NTFS_tool.Extract('/$LogFile','$LogFile')
        self._NTFS_tool.Extract_UsnJrnl()
        files = ['$MFT', '$LogFile', '$UsnJrnl']
        enc = hashlib.md5()
        for file in files:
            with open(file, 'rb') as f:
                text = f.read()
                enc.update(text)
