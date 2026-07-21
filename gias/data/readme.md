To get python code to run via wsl on windows:

Create file C:\Users\\<user_name\>\\.wslconfig

Add the below to the .wslconfig file and save 
```ubuntu
[wsl2]
networkingMode=mirrored
dnsTunneling=true
```

Open up a Poweshell instance (outside VS Code) and run

```ubuntu
wsl --shutdown
```

Reopen VS Code and Ubuntu wsl ternimal should work. 

Now activate venv, install requirements and run python script.

```ubuntu
   source .venv/bin/activate
   cd gias/data
   pip install -r requirements.txt
   python GIAS_ingestion.py
```

