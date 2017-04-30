### Windows Subsystem for Linux
If you are an experienced Linux user and you have a supported Windows platform, you can run the worker:
* enabling [Windows Subsystem for Linux](https://msdn.microsoft.com/en-us/commandline/wsl/install_guide), and
* simply following the [[Running the worker on Linux]].

Astonishingly Stockfish got a 3-4% speedup when running as Linux application in WSL respect to when running as Windows application.

If you are not a Linux user, please don't try this at home, and use the following instructions.

### Get username/password for Multi Variant Fishtest

Create an account on Multi Variant Fishtest choosing an username/password:

http://35.161.250.236:6543/signup

### Setup Python on Windows

Install Python 2.7.x (not 3.x series), choose 32 or 64 bit according your Windows version:
* [Python 2.7.13 32-bit](https://www.python.org/ftp/python/2.7.13/python-2.7.13.msi)
* [Python 2.7.13 64-bit](https://www.python.org/ftp/python/2.7.13/python-2.7.13.amd64.msi)

### Setup Fishtest

Download Fishtest directly from Github and unzip the archive:

https://github.com/ianfab/fishtest/archive/master.zip


### MinGW-w64 & MSYS2 install

MSYS2 is a collection of GNU utilities, based on modern Cygwin (POSIX compatibility layer) that uses *pacman* (from [Arch Linux](https://wiki.archlinux.org/index.php/pacman)) as packages manager to install and to update packages. MinGW-w64 is a project created to support the GCC compiler on Windows systems.

MSYS2 provides 3 different shells:
* *MSYS2 MinGW 64-bit*, used to build 64 bit applications. Use this if you have a 64 bit Windows
* *MSYS2 MinGW 32-bit*, used to build 32 bit applications. Use this if you have a 32 bit Windows
* *MSYS2 MSYS*, used to build MSYS2 core packages. Don't use this shell

The default setting installs MSYS2 in to *C:\msys64* folder, the user home is the folder *C:\msys64\home\<your_username>* 
 (*C:\msys32* for 32 bit Windows)

Warning: MSYS2 might not work with Windows XP and Windows Server 2003.

1. download and install [MSYS2](http://msys2.github.io/), use the 64 bit or 32 bit installer according your operating system and follow the official instruction to update the MSYS2 packages (simply: a. update the core packages executing `pacman -Syuu`, when requested close the windows pushing the top right X button b. open a *MSYS2 MinGW 64-bit* shell and update the others packages executing `pacman -Syuu`)

2. install *make* and *MinGW-w64* packages (64 bit or 32 bit according your operating system):
  * 64 bit: at prompt run `pacman -S make mingw-w64-x86_64-gcc`
  * 32 bit: at prompt run `pacman -S make mingw-w64-i686-gcc`


### Launching the worker
1. in *fishtest-master/worker* directory, create a text file named *fishtest.bat* and copy in it the text below (write the \<n_cores\> that you want dedicate to fishtest, and your fishtest's \<username\> and \<password\>)
  * 64 bit Windows:
  ```
  @echo off
  SET PATH=C:\msys64\mingw64\bin;C:\msys64\usr\bin;%PATH%
  cmd /k C:\Python27\python.exe -i C:\fishtest-master\worker\worker.py --concurrency <n_cores> <username> <password>
  ```
  * 32 bit Windows:
  ```
  @echo off
  SET PATH=C:\msys32\mingw32\bin;C:\msys32\usr\bin;%PATH%
  cmd /k C:\Python27\python.exe -i C:\fishtest-master\worker\worker.py --concurrency <n_cores> <username> <password>
  ```

2. you MUST override the default `mingw32-make` command (the non standard MSYS's make command used by the worker) writing a `custom_make.txt` file in *fishtest-master\worker* directory, according the architecture of your CPU (you can also add the flag `-j <n_jobs>` to lower the compile time, use all the cores to speedup the building process):
 * 32 bit Windows:

   ``
    make profile-build ARCH=x86-32 COMP=mingw -j <n_jobs>
   ``

 * old CPU:

   ``
    make profile-build ARCH=x86-64 COMP=mingw -j <n_jobs>
   ``

 * Sandy Bridge and Ivy Bridge CPU:

   ``
     make profile-build ARCH=x86-64-modern COMP=mingw -j <n_jobs>
   ``

 * Haswell and later CPU:

   ``
    make profile-build ARCH=x86-64-bmi2 COMP=mingw -j <n_jobs>
   ``
3. start the worker executing *fishtest.bat* (e.g double click on *fishtest.bat*)
