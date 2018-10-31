Generating the docs
----------

### Install requirements:

```bash
$ pipenv install --dev
$ pipenv shell
```

### Build the docs

```bash
$ make docs
```

### Serve docs locally
```bash
$ make serve-docs
```


### deploy docs using `gh-pages`

```bash
$ make releasedocs
```

**Note**:

1. Never edit the the gh-pages git branch by hand. Only use via the `mkdocs gh-deploy` command. 
2. Never edit the generated site by hand because using `gh-deploy` blows away the `gh-pages` branch and you'll lose your edits.
