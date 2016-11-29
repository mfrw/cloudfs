#!/usr/bin/env python

import cmd, os
import cloudfs 
import cloud_upload
import sys
import zipfile
import base64

class CmdShell(cmd.Cmd):
    prompt = 'cloudfs> '

    def do_encrypt(self, line):
        "encrypt $password [ $path ]"
        "Encrypts path (default current dir) with password"
        err_msg = "usage: encrypt $password [ $path ]" 
        args = [a for a in line.split(' ') if len(a) > 0]
        if len(args) < 1 or len(args) > 2:
            print err_msg
            return
        passphrase = args[0]
        path = os.getcwd()
        if len(args) == 2:
            path = args[1]
        if not os.path.exists(os.path.join(os.getcwd(), path)) and os.path.isdir(os.path.join(os.getcwd(), path)):
            print "Please enter a valid path"
            return
        fs = cloudfs.CloudFS(passphrase, path)
        fs.encrypt()
        print "Encrypted %s"%path
        del fs
    
    def do_decrypt(self, line):
        "decrypt $password [ $path ]"
        "Decrypts path (default current dir) with password"
        err_msg = "usage: decrypt $password [ $path ]" 
        args = [a for a in line.split(' ') if len(a) > 0]
        if len(args) < 1 or len(args) > 2:
            print err_msg
            return
        passphrase = args[0]
        path = os.getcwd()
        if len(args) == 2:
            path = args[1]
        if not os.path.exists(os.path.join(os.getcwd(), path)) and os.path.isdir(os.path.join(os.getcwd(), path)):
            print "Please enter a valid path"
            return
        fs = cloudfs.CloudFS(passphrase, path)
        fs.decrypt()
        print "Decrypted %s"%path
        del fs

    def do_shell(self, line):
        "shell cmd"
        "Run a Shell command"
        output = os.popen(line).read()
        print output

    def do_ls(self, line):
       "List directories"
       output = os.popen('ls').read()
       print output

    def do_cd(self, line):
        '''
        Change directory
        '''
        arg = [ a for a in line.split(' ') if len(a) > 0]
        if len(arg) > 1:
            print "Error: Check input"
            return
        if not os.path.isdir(arg[0]):
            print "%s : Not Found"%arg[0]
            return
        os.chdir(arg[0])

    def do_uploadfile(self, line):
        '''
        uploadfile filename
        Uploads a single file to the cloud (GDrive) 
        '''
        arg = [a for a in line.split(' ') if len(a) > 0]
        if not os.path.exists(arg[0]):
            print "File does not exits"
            return
        upload = cloud_upload.DriveUpload()
        upload.upload_file(arg)
        del upload
    
    def do_uploadall(self, line):
        '''
        uploadfile path
        Uploads all  file to the cloud (GDrive) 
        '''
        arg = [a for a in line.split(' ') if len(a) > 0]
        if not os.path.exists(arg[0]):
            print "File does not exits"
            return
        fnames = []
        for i in os.listdir(arg[0]):
            if not i.startswith('.'):
                fnames.append(i)
        upload = cloud_upload.DriveUpload()
        upload.upload_file(fnames)
        del upload

    def do_uploadzdir(self, line):
        '''
        uploadzdir [$dir] 
        upload a dir and all the contents there in a tar.gz
        '''
        err_msg = 'Bad Arguments'
        arg = [ a for a in line.split(' ') if len(a) > 0]
        if len(arg) == 0:
            path = os.getcwd()
        elif len(arg) == 1:
            path = arg[0]
        if len(arg) > 1:
            print err_msg
            return
        if not os.path.exists(os.path.join(os.getcwd(), path)) and os.path.isdir(os.path.join(os.getcwd(), path)):
            print "Directory Not found"
            return
        zipf = zipfile.ZipFile('inode.dat.enc.zip', 'w', zipfile.ZIP_DEFLATED)
        zipdir(path, zipf)
        zipf.close()
        upload = cloud_upload.DriveUpload()
        upload.upload_file('inode.dat.enc.zip')
        del upload
        os.remove('inode.dat.enc.zip')

    def do_EOF(self, line):
        print ""
        return True

    def do_exit(self, line):
        "Exit from the shell"
        sys.exit(0)


def zipdir(path, ziph):
    '''
    ziph is zipfile handle
    '''
    for root, dirs, files in os.walk(path):
        for f in files:
            ziph.write(os.path.join(root, f))


if __name__ == '__main__':
    c = CmdShell()
    c.cmdloop()
