import os
from os import listdir
from os.path import isfile, join

from pathlib import Path
import getpass

import base64
import hashlib
from Crypto import Random
from Crypto.Cipher import AES
from Crypto.PublicKey import RSA

from config import *

'''
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ CLOUD VEIL ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
  A simple tool to add an extra layer of security to your cloud uploads
'''


class AESCipher(object):

    def __init__(self, key): 
        self.bs = 16
        self.key = hashlib.sha256(key.encode()).digest()

    def encrypt(self, raw):
        raw = self._pad(raw)
        iv = Random.new().read(AES.block_size)
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        return base64.b64encode(iv + cipher.encrypt(raw))

    def decrypt(self, enc):
        enc = base64.b64decode(enc)
        iv = enc[:AES.block_size]
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        return self._unpad(cipher.decrypt(enc[AES.block_size:])).decode('utf-8')

    def _pad(self, s):
        return s + (self.bs - len(s) % self.bs) * chr(self.bs - len(s) % self.bs)

    @staticmethod
    def _unpad(s):
        return s[:-ord(s[len(s)-1:])]
def b32_AES_encrypt(plaintext, key):
    '''
    Encrypts data into base64.base32 to be alphanumeric and
    filesystem friendly (avoiding '.' and '/', etc)
    Key will be padded (hashed) so don't worry about making
    it a clean mutliple of 16/32 characters.
    
    Returns base32 encoded ciphertext
    '''
    cipher = AESCipher(key)    
    return base64.b32encode(cipher.encrypt(plaintext))
def b32_AES_decrypt(ciphertext, key):
    '''
    Decrypts data from base64.base32 to plaintext.
    '''
    cipher = AESCipher(key)
    return cipher.decrypt(base64.b32decode(ciphertext))

    
    
def dir_name(input_directory):
	#get input_directory name. eg "/path/to/elephants/" returns "elephants"
    #REPLACE FUNCTIONALITY WITH pathlib LIBRARY FUNCTIONS/CLASSES
	if input_directory[-1] == "/":
		input_directory = input_directory[:-1]
	
	i = len(input_directory) - 1
	while i >= 0:
		if input_directory[i] == "/":
			dir_name = input_directory[i:]
			break
		i -= 1
		
	return dir_name[1:]
    
    
        

    
def encrypt_n_push(sync_directory, input_directory, key):
    '''
    Encrypts files & filenames and sends them to the sync directory
    '''
    
    #set input directory location if config file has no value
    if not input_directory:
        input_directory = input("Input directory (absolute path): ")

    #fix /structure/
    if input_directory[-1] != "/":
        input_directory += "/"
    if input_directory[0] != "/":
        input_directory = "/" + input_directory

    if not os.path.isdir(input_directory):
        print("ERROR: Input directory does not exist!")
        exit()
    
    fileSet = set()
    for root, dirs, files in os.walk(input_directory):
        for fileName in files:
            fileSet.add((os.path.join( root[len(input_directory):], fileName ), fileName))    

    for item in fileSet:
        #encrypt filenames
        mydir = dir_name(input_directory) + "/" + item[0]
        sec_dir = b32_AES_encrypt(mydir, key)
        
        #in-file absolute path
        in_f = input_directory + item[0]
        #out-file absolute path
        out_f = sync_directory + sec_dir.decode("utf-8")

        print("AES256: " + out_f)
        print("        Output Path:    " + str(mydir))
        print("        Encrypted Path: " + out_f[:30] + "...")

        #now we encrypt the files with our encrypted path into the sync directory
        #note that aescrypt is a placeholder for a python-only approach
        command = "aescrypt -e -p '" + key + "' -o '" + out_f + "' '" + in_f + "'"
        os.system(command)
        
        

        
def decrypt_n_pull(sync_directory, landing_directory, key):
    '''
    Takes files whose 
    '''
    #get a list of all files in sync directory - NON RECURSIVELY
    #decrypt them into their original string values: REL_PATH
    #decrypt files and place them in their landing directory + REL_PATH
    #??? profit
    
    #set landing_directory location if config file has no value
    if not landing_directory:
        landing_directory = input("Landing directory (absolute path): ")

    #fix /structure/
    if landing_directory[-1] != "/":
        landing_directory += "/"
    if landing_directory[0] != "/":
        landing_directory = "/" + landing_directory

    if not os.path.isdir(landing_directory):
        print("ERROR: Landing directory does not exist!")
        exit()
     
    #2-list of filenames: item 0 is encrypted filename and item 1 is the decrypted
    files = [[f, ""] for f in listdir(sync_directory) if isfile(join(sync_directory, f))]       
    
    for item in files:
        #decrypt filename
        item[1] = b32_AES_decrypt(item[0], key)
        
        enc_file = sync_directory + item[0]
        out_dir = landing_directory + item[1]
        #print("enc_file: ", enc_file)     
        #print("out_dir:  ", out_dir)     

        #make subdirectory if it doesn't exist
        tmp_path = Path(os.path.dirname(out_dir))
        tmp_path.parent.mkdir(parents=True, exist_ok=True) 
        
        
        
        #decrypt file in landing directory
        print("AES256: " + out_dir)
        command = "aescrypt -d -p '" + key + "' -o '" + out_dir + "' '" + enc_file + "'"
        os.system(command)

        
        

        
def main(sync_directory, input_directory, landing_directory):
    MINPASSLEN = 10
    
    #set sync location if config file has no value
    if not sync_directory:
        sync_directory = input("Sync directory (absolute path): ")

    mode = ""
    while mode.upper() not in ['E','D']:
        mode = input("Are you [E]ncrypting or [D]ecrypting? ")
    
    #encrypt files
    password = getpass.getpass()
    while len(password) < MINPASSLEN:
        print("Please ensure that your password is above " + 
              str(MINPASSLEN) + " characters.")
        password = getpass.getpass()
    
    #encryption mode
    if mode.upper() == 'E':
        encrypt_n_push(sync_directory, input_directory, password)
    elif mode.upper() == 'D':
        decrypt_n_pull(sync_directory, landing_directory, password)
           
    
        
if __name__ == "__main__":
    main(sync_directory, input_directory, landing_directory)
    