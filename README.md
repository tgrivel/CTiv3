"# CTiv3" 


# Getting started

Download en installeer Anaconda:
https://www.anaconda.com/download/

Open de Anaconda prompt en type:
```
conda env create -f environment.yml
```

# Running

```
conda activate ocido
flask run
```

Alternatief:
```
python applicatie.py
```

# Docker
docker build -t ctiv3 .
docker run ctiv3
