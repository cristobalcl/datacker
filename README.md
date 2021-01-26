# datacker

![Release](https://github.com/cristobalcl/datacker/workflows/Release/badge.svg)
[![Python 3.7](https://img.shields.io/badge/python-3.7-blue.svg)](https://www.python.org/downloads/release/python-370/)
[![Python 3.8](https://img.shields.io/badge/python-3.8-blue.svg)](https://www.python.org/downloads/release/python-380/)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black)

Convert your notebooks to runnable Docker images. The quickest way to bring Data Science work to production.

## Introduction

**Datacker** creates Docker images from one or more Jupyter Notebooks. You also can add a `requirements.txt` with the code dependencies. The result Docker image can execute the notebook by itself, and store the new notebook in a directory that can be bind mounted to a directory in the host machine for persisting (in next versions, the result can be stored in the cloud, in S3 for example). Parameters can be passed to the notebook dinamically.

## Usage

```
$ datacker --help
Usage: datacker [OPTIONS] IMAGE_NAME NOTEBOOKS...

Arguments:
  IMAGE_NAME    [required]
  NOTEBOOKS...  [required]

Options:
  -r, --requirements TEXT         Path to requirements file
  --install-completion [bash|zsh|fish|powershell|pwsh]
                                  Install completion for the specified shell.
  --show-completion [bash|zsh|fish|powershell|pwsh]
                                  Show completion for the specified shell, to
                                  copy it or customize the installation.

  --help                          Show this message and exit.
```

## Example

Using the example from `examples/parameters`:

Build the Docker image:

```
datacker datacker_parameters pie.ipynb -r requirements.txt
```

Run:

```
docker run --env NOTEBOOK_NAME=pie \
  --env PARAMETERS='{ "sizes": [40, 10, 20, 30], "explode": [0.1, 0, 0, 0] }' \
  --env PARAM_labels='["Cat", "Cactus", "Cattle", "Camel"]' \
  --mount type=bind,src=${PWD}/output,dst=/output \
  datacker_parameters
```

The name of the notebook is passed in the environment variable `NOTEBOOK_NAME`.

This example shows two ways for passing parameters to the notebooks: using the environment variable `PARAMETERS`, that accepts a JSON with the parameters; and the other way is using environment variables with a name like `PARAM_[var_name]`, that accepts values with a Python representation: float as `'3.1415'`, string as `'"Hello World!"'`, and so on. Variables defined with `PARAM_[var_name]` have priority.

The results will be stored in the `output` directory on the host.

## Parameterizing a Notebook

Before build a Datacker image you need to setup your notebook, if you want to use parameters when running. You need to mark a cell with the tag `parameters`. This cell will have the variables with its default values. Look at the notebooks in the `examples` directory.

To know how to add the tag to a cell check [How should I add cell tags and metadata to my notebooks?](https://jupyterbook.org/advanced/advanced.html#how-should-i-add-cell-tags-and-metadata-to-my-notebooks).

## Roadmap

* Store results in the cloud (S3, Azure,...).
* Examples of deploying in Kubernetes.
* Documentation.
