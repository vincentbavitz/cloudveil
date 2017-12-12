![alt text](https://image.ibb.co/mVqMxw/cloudveil_icon_sm.png "Cloud Veil")
# Cloud Veil 

This program simply encrypts your files (including filenames) and places them into your desired directory. The intended purpose of the program is to encrypt sensitive files and send them to a mounted [FUSE](https://en.wikipedia.org/wiki/Filesystem_in_Userspace) virtual disk which is connected to your cloud storage. Encrypting your files in this way adds another layer of security to cloud storage so you don't have to worry about the trustworthiness of their privacy claims. 

I wanted to avoid sending enormous [encrypted file containers](https://en.wikipedia.org/wiki/VeraCrypt) to cloud services because they have the
disadvantages of:
* using heaps of memory in the uploading process
* having to reupload the entire container after only minor changes to files within

Therefore, your individual files and their filenames are encrypted with AES256 in CBC mode.

## Security
The idea of Cloud Veil is to ensure that the cloud storage is self contained. This means that even if all of your drives were stolen, lost or damaged, you could still recover your files in their correct directories with your cloud login credentials and your encryption key.

No directory information is compromised because the filenames are encrypted as absolute paths and sent to a single directory on the cloud server.
Eg. */home/$USER/path/to/my/favourite/file.txt*
becomes
*/cloud-root/FGB387RFG134UYRTFBKUGVW8723KB789HITG14RTG34YWBN4T7GHVBDFJKGBGIEG*
The directory information is recovered upon decryption, allowing the program to place the files in the proper places upon recovery or downloading. This has the advantage of not revealing any information about the depth of your directories and also keeping the total directory length below the UNIX limit of 256 characters.

___
**NOTE**:
* If you decide to send files directly to your [FUSE](https://en.wikipedia.org/wiki/Filesystem_in_Userspace) volume, note that the program will only write to the disk as fast as your upload limit permits it.
* File sizes are not altered to any obfuscatory extent which may give hints to the types of files which are being stored.
* The same key is used for each file and again for each file-name (each using a different randomly generated [initialisation vector](https://en.wikipedia.org/wiki/Initialization_vector))

## Requirements
1. A UNIX based machine
2. [AesCrypt](https://www.aescrypt.com) (Linux)
3. PyCrypto (install with Pip)
4. [FUSE](https://en.wikipedia.org/wiki/Filesystem_in_Userspace) *optional*

## Future Improvements:
 * Add ability to select single files for encryption/decryption instead of just directories
 * Remove aescrypt dependency
 * Make multiplatform by using cross-platform tools
 * Improve security by replacing the depreciated PyCrypto library with the PyCa Cryptography library
 
 
