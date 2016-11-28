
import os
import json
from encryption_helper import dec_file, enc_file, generate_key

ignored_files = [
        ]


class CloudFS:
    def __init__(self, pwd, root=None):
        '''Create a new instance of CloudFS
        Set the current directory to the supplied path, and if 
        not path is supplied, use the current directory for the path
        '''
        self.key = generate_key(pwd)
        print("The key is %s and len is %s"%(self.key, len(self.key)))
        if root :
            self.cwd = root
        else :
            self.cwd = './'
        self.inode = self.load_inode()

    def load_inode(self, path=None):
        '''
        load_inode: load an encrypted inode and encrypt it and delete the original
        inode so that there is no way a malicious user can know anything
        '''
        if not path :
            path = self.cwd
        if not os.path.isfile(get_einode(path)):
            self.update_inode(path=path)
            return empty_inode(path)
        dec_file(self.key, get_einode(path))
        with open(get_inode(path), 'rb') as f:
            inode = json.load(f)
        os.remove(get_inode(path))
        return inode

    def update_inode(self, inode=None, path=None):
        '''
        Update the inode, and delete all the plain text files
        '''
        if not path:
            path = self.cwd
        if not inode:
            inode = empty_inode(path)
        with open(get_inode(path), 'w') as f:
            json.dump(inode, f)
        enc_and_del(get_inode(path), self.key)

    def inode_addfile(self, fname, efname):
        '''
        Add a new file to the inode
        '''
        self.inode["files"].append({"filename":fname, "filename_enc":efname})

    def encrypt(self, path=None):
        ''' 
        Encrypt all the files in the FS
        '''
        if not path:
            path = self.cwd
        enc_list = get_efnames(self.inode)
        newfiles = list()
        for f in os.listdir(path):
            if (not f in enc_list) and (not f in ignored_files) and (f != 'inode.dat.enc') and os.path.isfile(os.path.join(path, f)) :
                newfiles.append(f)
        for f in newfiles:
            rnd_name = get_random32(path)
            enc_and_del(os.path.join(path, f), self.key, os.path.join(path, rnd_name))
            self.inode_addfile(f, rnd_name)
        self.update_inode(self.inode, path)

    def fall_back(self, path=None, inode=None):
        if not path and not inode:
            path = self.cwd
            inode = self.inode
        elif(not path and inode) or (path and not inode):
            raise RuntimeError("Either pass both path, inode, or none")
        return path, inode
    
    def decrypt(self, path=None, inode=None, del_enc=True):
        '''
        decrypt all the files
        '''
        path, inode = self.fall_back(path, inode)
        for f in inode["files"]:
            dec_file(self.key, os.path.join(path, f["filename_enc"]), os.path.join(path, f["filename"]))
            if del_enc:
                os.remove(os.path.join(path, f["filename_enc"]))
        os.remove(os.path.join(path, 'inode.dat.enc'))
        inode["files"] = []



    def inode_clean(self, path=None, inode=None):
        '''
        remove the enc file names that are deleted from the main FS
        '''
        path, inode = self.fall_back(path, inode)

        for f in inode:
            enc_path = os.path.join(path, f["filename_enc"])
            if not os.path.isfile(enc_path):
                os.remove(enc_path)

def empty_inode(path):
    '''
    make an empty inode if none is present
    '''
    return {"files":[]}

def get_inode(dir):
    '''
    get the path of the un-encrypted inode
    '''
    return os.path.join(dir, 'inode.dat')

def get_einode(dir):
    '''
    get the path of the encrypted inode
    '''
    return os.path.join(dir, 'inode.dat.enc')

def get_efnames(inode):
    '''
    Get the list of encrypted file names from the inode
    '''
    fname_list = list()
    for name in inode["files"]:
        fname_list.append(name["filename_enc"])
    return fname_list

def enc_and_del(path, key, output=None):
    '''
    Encrypt all files and delete the plain text files
    '''
    enc_file(key, path, output)
    os.remove(path)

def get_random32(path=''):
    '''
    Get random names and also look for collisions in the current files in path
    '''
    names = os.listdir(path)
    while True:
        new_name = os.urandom(32).encode('hex')
        if new_name not in names:
            break
    return new_name


if __name__ == '__main__':
    print ("About to encrypt the folder test")
    a = raw_input('hello')
    #os.chdir('./test')
    encfs = CloudFS('hello','./test')

    encfs.encrypt()
    print ("Encrypted the files")
    a = raw_input('hello')
    encfs.decrypt()
    print("Decrypted the files")
    print("change some of  the files")
    a = raw_input('hello')
    encfs.encrypt()
    a = raw_input('hello')




