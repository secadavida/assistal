# Contributing

## Development

**Prerequisites**:

```sh
$ source ./venv/bin/activate # Linux/MacOS
$ venv\Scripts\activate      # Windows

$ deactivate # after finishing
```

**Running**:

```sh
$ python -m assistal
```

**Adding dependencies**:

```sh
$ pip install <deps>
$ pip freeze > requirements.txt
```

## Testing

**Generate random runtime data:**
```sh
python ./tests/conftest.py  # Linux/MacOS
python tests\conftest.py    # Windows
```
