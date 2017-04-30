### Get username/password for Multi Variant Fishtest

Create an account on Multi Variant Fishtest choosing an username/password:

http://35.161.250.236:6543/signup

### Debian/Ubuntu

Install the required packages:
```
sudo apt update -y
sudo apt install -y build-essential unzip
```
Ubuntu 16.04 is not suggested, the Stockfish tuning branch triggers a gcc bug. As workaround write a custom_make.txt with  `make build (...)` instead of `make profile-build (...)` but this slow down a bit the worker.

### Setup fishtest

It is recommended for security reasons to create a separate user for the fishtest worker since you are essentially running arbitrary code/instructions. This way testing multi variant stockfish can have no impact on your primary accounts and configuration.
```
sudo useradd -m mvfishtest
```
Download fishtest:
```
sudo -i -u mvfishtest wget https://github.com/ianfab/fishtest/archive/master.zip
sudo -i -u mvfishtest unzip master.zip
```

### Launching the worker

Use this script to run the worker with the output in console: 

```bash
#!/bin/bash
# usage: mvfishtest.sh  [<n_cores> <username> <password>]
# <n_cores>: number of cores to be used in fishtest. Suggested max value = n. physical cores-1
# <username>: username on fishtest (to be enclosed in quote if contains special characters)
# <password>: password on fishtest (to be enclosed in quote if contains special characters)
# The three parameters are mandatory only for the first execution

if [ $# -gt 0 ]; then
  sudo -i -u mvfishtest python fishtest-master/worker/worker.py --concurrency $1 $2 $3
else
  sudo -i -u mvfishtest python fishtest-master/worker/worker.py
fi
```

For the first execution the three parameters are mandatory:

```
bash mvfishtest.sh <n_cores> <username> <password>
```

Starting from the second execution simply run the script or without parameters or with a different number of cores:
```
bash mvfishtest.sh [<n_cores>]
```


### RHEL/CentOS
The default version of GCC does not support C++11, you must install the developer toolset, which adds a newer version of GCC. Follow the instructions for your Linux distribution:

https://www.softwarecollections.org/en/scls/rhscl/devtoolset-6/

Use this script to run the worker with the output in console: 
```bash
#!/bin/bash
# usage: mvfishtest.sh  [<n_cores> <username> <password>]
# <n_cores>: number of cores to be used in fishtest. Suggested max value = n. physical cores-1
# <username>: username on fishtest (to be enclosed in quote if contains special characters)
# <password>: password on fishtest (to be enclosed in quote if contains special characters)
# The three parameters are mandatory only for the first execution

if [ $# -gt 0 ]; then
  sudo -i -u mvfishtest << EOF
source scl_source enable devtoolset-6
python fishtest-master/worker/worker.py --concurrency $1 "$2" "$3"
EOF
else
  sudo -i -u mvfishtest << EOF
source scl_source enable devtoolset-6
python fishtest-master/worker/worker.py
EOF
fi
```

### Override the default make command

If default make command is not suitable for you, you can create a `custom_make.txt` file in *fishtest-master/worker* directory, containing a single line command that fishtest will run to compile the sources (you can also add the flag -j <n_jobs> to lower the compile time, use all the cores to speedup the building process). View below some examples:

 * 32 bit Windows:

   ``
    make profile-build ARCH=x86-32 COMP=gcc -j <n_jobs>
   ``

 * old CPU:

   ``
    make profile-build ARCH=x86-64 COMP=gcc -j <n_jobs>
   ``

 * Sandy Bridge and Ivy Bridge CPU:

   ``
     make profile-build ARCH=x86-64-modern COMP=gcc -j <n_jobs>
   ``

 * Haswell and later CPU:

   ``
    make profile-build ARCH=x86-64-bmi2 COMP=gcc -j <n_jobs>
   ``