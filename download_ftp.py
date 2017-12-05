# -*- encoding: utf8 -*-
import os
import sys
import ftplib
import multiprocessing
def wrap(inst, experiment_name, img_type):
    inst.run(experiment_name, img_type)

class FTPSync(object):
    def __init__(self):
        self.conn = ftplib.FTP('10.10.30.91', 'dingchenwei', 'Dcw1995996987')
        self.conn.cwd('/dingchenwei/matting_feathering/experiment/4x+feather+guidedFilter/label/')        # 远端FTP目录
    def get_dirs_files(self):
        u''' 得到当前目录和文件, 放入dir_res列表 '''
        dir_res = []
        self.conn.dir('.', dir_res.append)
        files = [f.split(None, 8)[-1] for f in dir_res if f.startswith('-')]
        dirs = [f.split(None, 8)[-1] for f in dir_res if f.startswith('d')]
        return (files, dirs)
    def walk(self, next_dir):
        print ('Walking to', next_dir)
        self.conn.cwd(next_dir)
        try:
            os.mkdir(next_dir)
        except OSError:
            pass
        os.chdir(next_dir)
        ftp_curr_dir = self.conn.pwd()
        local_curr_dir = os.getcwd()
        files, dirs = self.get_dirs_files()
        print ("FILES: ", files)
        print ("DIRS: ", dirs)
        for f in files:
            print (next_dir, ':', f)
            outf = open(f, 'wb')
            try:
                self.conn.retrbinary('RETR %s' % f, outf.write)
            finally:
                outf.close()
        for d in dirs:
            os.chdir(local_curr_dir)
            self.conn.cwd(ftp_curr_dir)
            self.walk(d)
    def run(self, experiment_name, img_type):
        os.chdir('./'+experiment_name+img_type)        # 本地下载目录
        self.walk('.')
def main():
    parent_path = '/dingchenwei/matting_feathering/experiment/'
    experiment_name = '4x+feather+guidedFilter/'
    if not os.path.exists(experiment_name):
        os.system('mkdir '+experiment_name)
    #img_types = ['matte/', 'label/', 'temp_matte/', 'guided_result/', 'add/']
    #pool = multiprocessing.Pool(processes=10)
    f = FTPSync()
    f.conn.cwd(parent_path+experiment_name+sys.argv[1]+'/')
    if(not os.path.exists(experiment_name+sys.argv[1]+'/')):
        os.system('mkdir '+experiment_name+sys.argv[1])
    f.run(experiment_name, sys.argv[1]+'/')
    #pool.apply_async(wrap, (f, experiment_name, img_types[1],))
    #for img_type in img_types:
    #    if not os.path.exists(experiment_name+img_type):
    #        os.system('mkdir '+experiment_name+img_type)
    #    f.conn.cwd(parent_path+experiment_name+img_type)
    #    pool.apply_async(f.run, (experiment_name, img_type,))
    #pool.close()
    #pool.join()
if __name__ == '__main__':
    main()
