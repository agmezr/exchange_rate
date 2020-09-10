# Exchange Rate

This is a simple app with a single endpoint that returns the
latest exchange rate from *USD* to *MXN* from different sources.

There are 3 different sources for now:
- Banxico
- Diario Oficial de la Federacion
- Fixer

To run locally you need to need an api key from [Fixer](https://fixer.io/) and a token from
[Banxico](https://www.banxico.org.mx/SieAPIRest/service/v1/token) once you have them
either export them or use it alongside the python server 

```bash

# create virtual env
python -m venv venv

# activate virtual env
source venv/bin/activate

# with the env vars declared run the server
BANXICO_TOKEN="<TOKEN>" FIXER_API_KEY="<API_KEY>" python server.py
```