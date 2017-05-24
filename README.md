# OPDSS: Open Platform Digital Signage System

High-quality digital signage generation system that can be customized by user

## Development

 - Language: Python 3.6.1
 - Other requirements: Specified in requirements.txt

### Development Environment Setting

#### Using pyenv & Ubuntu
 - Tested in Ubuntu 16.04.2 LTS
 1. Install dependencies
 ```bash
 ~$ sudo apt-get install -y make build-essential libssl-dev zlib1g-dev libbz2-dev libreadline-dev
 libsqlite3-dev wget curl llvm libncurses5-dev libncursesw5-dev xz-utils tk-dev
 ~$ sudo apt-get install git #If git is not installed
 ```
 2. Install pyenv using pyenv-installer
 ```bash
 ~$ curl -L https://raw.githubusercontent.com/pyenv/pyenv-installer/master/bin/pyenv-installer | bash
 ```
 3. If warning occurs, add presented commands in `~/.bashrc` and restart the shell
 4. Update pyenv
 ```bash
 ~$ pyenv update
 ```
 5. Install Python 3.6.1 in pyenv
 ```bash
 ~$ pyenv install 3.6.1
 ```
 6. Create virtual environment for development with Python 3.6.1
 ```bash
 ~$ pyenv virtualenv 3.6.1 venv
 ```
 7. Activate virtual environment
 ```bash
 ~$ pyenv activate venv
 ```
 8. Clone the repository and move the directory into it
 ```bash
 ~$ git clone https://github.com/limgit/guess
 #If credential is required, enter it.
 ~$ cd guess
 ```
 9. Install the requirements
 ```bash
 ~/guess$ pip install -r requirements.txt
 ```
 10. **PROFIT!**

Everytime you work on the repository, activate virtualenv with `$ pyenv activate venv`

To deactivate, `$ pyenv deactivate` is used
