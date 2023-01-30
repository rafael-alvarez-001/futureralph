# futureralph
Demo Project for Ralph

# Pre-requisites
- A *nix system. It "may" work with Windows, but this was not tested
- Python (tested with 3.11, but any fairly modern 3.x version should work) with `pip` and `virtualenv`
- A local file system location where you can read/write files locally
- Internet connection

# How to run

1. Clone repo

2. Create a python virtual environment and activate it
```shell
> python -m venv venv

> source env/bin/activate
```
3. Install additional required libraries in the virtual environment
```shell
> pip install -r requirements.txt
```
4. Run the application
```shell
> python main.py
```

# Important Files
`config.yml` - YAML file containing 