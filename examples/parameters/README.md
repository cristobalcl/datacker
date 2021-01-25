Example: parameters
===================

Build:

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

This example shows two ways for passing parameters to the notebooks: using the environment variable `PARAMETERS`, that accepts a JSON with the parameters; and the other way is using environment variables with a name like `PARAM_[var_name]`, that accepts values with a Python representation: float as `'3.1415'`, string as `'"Hello World!"'`, and so on.

The results will be stored in the `output` directory.
