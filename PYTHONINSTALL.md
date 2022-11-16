# Python Installation ![python-logo-evensmaller](https://user-images.githubusercontent.com/31383711/200034228-92eebe7f-ce3b-4bf9-a7b2-1e314d5683bb.png)
---
Alternatively: you can use [pyenv](https://github.com/pyenv/pyenv) to manage your Python installations. If you do, you can skip this 'Python Installation' section and go to ['Setup Virtual Environment'](https://github.com/jalnor/os_monitoring_tool/edit/main/README.md#setup-virtual-environment).

**Check if Python is installed and get version info:**
### Windows
Open a  command prompt and type python --version or python3 --version. This should give you something like this:
```
Microsoft Windows [Version 10.0.19044.2130]
(c) Microsoft Corporation. All rights reserved.

C:\Users\[current_user]>python --version
Python 3.10.4
```

If you have a lower version or Python isn't installed, you can go to [python.org](https://www.python.org/downloads/) to download and install it. They have a lot of useful guides to help with the process.

### Mac
Mac comes with Python 2.x which is outdated. If your system does not have a newer version you can use Homebrew to install it.
If you have Homebrew installed it is easy to install the latest version of Python. If not, you can install Homebrew by pasting this in your terminal:
```
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```
Per Homebrew home page, the script will explain what it is doing. If you need more information before installing it you can go the website [brew.sh](https://brew.sh/).
With Homebrew installed, type this in terminal:
```
brew install python3
```

### Linux
Most flavors of Linux come with Python; however, Ubuntu may not. You can find information at [Geeks for Geeks](https://www.geeksforgeeks.org/how-to-download-and-install-python-latest-version-on-linux/?ref=gcse) on how to install it on Linux.

## Setup Virtual Environment
---
Once you have Python installed, using the command prompt or the Linux or Mac terminal, navigate to the folder where you downloaded the application. Type the following replacing the <name_of_virtualenv> with an appropriate name without the angle brackets and press enter:
```
python3 -m venv <name_of_virtualenv>
```
This will create a virtual environment folder, venv, in the project directory.

<img src="https://user-images.githubusercontent.com/31383711/200119581-877c040b-3d7c-4c7b-8599-1efa4a4c6aba.png" width="80" />

Next, you will need to activate the environment. Your prompt will change indicating the venv is active with the name surrounded by parenthesis. To deactivate run same command with deactivate instead or simply type deactivate. 
```
c:\Users\Public\app_dir>python -m venv my_venv

c:\Users\Public\app_dir>dir
 Volume in drive C has no label.
 Volume Serial Number is C446-E6DE

 Directory of c:\Users\Public\app_dir

11/05/2022  08:14 AM    <DIR>          .
11/05/2022  08:14 AM    <DIR>          ..
11/05/2022  08:14 AM    <DIR>          my_venv
               0 File(s)              0 bytes
               3 Dir(s)  350,627,840,000 bytes free

c:\Users\Public\app_dir>my_venv\scripts\activate.bat

(my_venv) c:\Users\Public\app_dir>deactivate
c:\Users\Public\app_dir>
```

Note: the image above is using Windows Command Prompt. On Unix type systems or with Git Bash for Windows, you will need to use:
```
user@machine MINGW64 /c/Users/Public/app_dir
$ source my_venv/Scripts/activate
(my_venv)
user@machine MINGW64 /c/Users/Public/app_dir
$ deactivate

user@machine MINGW64 /c/Users/Public/app_dir
$
```


Simply type deactivate at the prompt to deactivate the virtual environment.

You can find a more detailed description at this [Gist](https://gist.github.com/djccnt15/55105dea001df6ce4eccb7d2a1c719e3). This Gist also has detailed instructions for installing requirements using pip.
