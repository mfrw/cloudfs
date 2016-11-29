import cmd, os
import cloudfs 

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
        "Change directory"
        arg = [ a for a in line.split(' ') if len(a) > 0]
        if len(arg) > 1:
            print "Error: Check input"
            return
        if not os.path.isdir(arg[0]):
            print "%s : Not Found"%arg[0]
            return
        os.chdir(arg[0])
    
    def do_EOF(self, line):
        print ""
        return True

    def do_exit(self, line):
        "Exit from the shell"
        os.exit(0)



if __name__ == '__main__':
    c = CmdShell()
    c.cmdloop()

        






