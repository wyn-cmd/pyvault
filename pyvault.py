import os,sys,hashlib,getpass,pyAesCrypt
#data buffer
buff=1024*1024*64
#help message for seed
os.system('touch .help.txt')
seed_help=open('.help.txt','r').read()
#self-destruct password
self_password='passwordhack' 
#vault's logo
vault_logo='''
         __
      __|  |__            
  /\/##########\/\               
  \/#####/\#####\/         <The Vault encryption program>
 _/#####|##|#####\_              <Made by wyn-cmd>
|_###<#{-==-}#>###_|
  \#####|##|#####/
  /\#####\/#####/\ 
  \/\##########/\/
      ""|  |""
         ""
'''
def cli(txt): #create the CLI interface
    os.system('clear')
    print(f'{vault_logo}\n***{txt}***')

def delete(file): #securely erase files
    os.system(f'rm -rf {file}')
    txt='.'
    open('forenstic.dat','w').write(txt)
    num=0
    while True:
        txt+='............................................................................................................................................................'
        open('forenstic.dat','a').write(txt) #writes data to a file to remove traces of the deleted file
        if num>7599:
            os.system('rm -rf forenstic.dat')
            break
        num+=1

def auth(): #wuthenticate the password in case of self-destruct
    key=getpass.getpass(prompt='Password:',stream=None) #gets password
    keyc=len(key)
    if keyc<9:
        print('password is minimum of 9 characters')
        sys.exit()
    elif key==self_password: #self-destruct password
        return(False)
    return(key)

def seed(): #get the seed for the hashing algorithm
    while True:
        seed=getpass.getpass(prompt='Seed:',stream=None) #gets seed
        if seed=='help':
            print(seed_help)
            i=input('>')
        else:
            return(seed)
            
def hashing_algorithm(key,seed):
    key=f'*%)|(E#{seed}(0{key}^f#bw$'
    key=hashlib.md5(key.encode('utf8')).hexdigest()
    key=hashlib.sha224(key.encode('utf8')).hexdigest()
    key=hashlib.sha256(key.encode('utf8')).hexdigest()
    return(key)
    


def decrypt(key,seed): #decypt data
    cli('decrypting data...')
    encryption_keys=hashing_algorithm(key,seed)
    pyAesCrypt.decryptFile('.vault.encrypt','vault.zip',encryption_keys,1024*1024*128) #decrypt with AES-256 to get zip file
    os.system('rm -rf .vault.encrypt')
    os.system('unzip vault')
    os.system('rm -rf vault.zip')

def encrypt(key):
    cli('encrypting data...')
    os.system('mkdir vault')
    os.system('zip vault -r vault')
    delete('vault')
    pyAesCrypt.encryptFile('vault.zip','.vault.encrypt',key,1024*1024*128) #decrypt with AES-256 to get zip file
    delete('vault')
    delete('vault.zip')

def setup():
    cli('creating file...')
    os.system('mkdir vault')
    cli('Creating file...***\n***Input password to lock the Vault')
    while True:
        key=getpass.getpass(prompt='Password:',stream=None) #gets password
        keyc=len(key)
        if keyc<9:
            print('password is minimum of 9 characters')
            sys.exit()
        elif key==self_password: #self-destruct password
            cli('This password cannot be used as it is the self destruct password')
            print('input seed as double confirmation')
        else:
            break
    key=hashing_algorithm(key,seed())
    encrypt(key)
    cli('file successfully encrypted!')
    i=input('>')
    cli('input help for remembering the seed')
    seed_help=input('>')
    open('.help.txt','w').write(seed_help)
    cli('run the program again to decrypt the Vault')
    return

attempt=4
vault_file=os.path.exists('.vault.encrypt') #checks if the vault is already encrypted
vault_vulnerable=os.path.exists('vault/') #checks if the vault is decrypted
if vault_file==True:
    while True:
        cli('Vault is locked')
        lock=auth() #get password
        if lock==False:
            delete('.vault.encrypt') #erase file
            cli('Vault erased') 
            break
        else:
            try:
                decrypt(lock,seed()) #try to unlock the vault
                cli('Vault unlocked') 
                break
            except Exception: #if wrong password then warn
                attempt-=1 
                if attempt<1:
                    delete('.vault.encrypt')
                    cli('Vault erased') #erase after max tries
                    break
                if attempt<2:
                    cli(f'Vault is locked***\n***{attempt} attempt remaining')
                elif attempt>1:
                    cli(f'Vault is locked***\n***{attempt} attempts remaining')
                i=input('>')
elif vault_vulnerable==True:
    cli('Input password to lock the Vault')
    while True:
        key=getpass.getpass(prompt='Password:',stream=None) #gets password
        keyc=len(key)
        if keyc<9:
            print('password must be minimum of 9 characters')
            sys.exit()
        elif key==self_password: #self-destruct password
            cli('This password cannot be used as it is the self destruct password')
        else:
            break
    print('Input seed as double confirmation')
    key=hashing_algorithm(key,seed())
    encrypt(key)
    cli('Vault successfully encrypted!')
    
else:
    setup()
    
    
    
