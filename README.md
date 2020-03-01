"# CTiv3" 


# Getting started

Download en installeer Anaconda:
https://www.anaconda.com/download/

```
conda create --file requirements.txt
pip install -r requirements-pip.txt
```

# Running

```
conda activate ctiv3
flask run
```

Alternatief:
```
python applicatie.py
```

# Docker
docker build -t ctiv3 .
docker run ctiv3
