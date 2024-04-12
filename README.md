# Install Poetry

Poetry helps manage the python libraries used in this application. It can be installed on you system by following the instructions [here](https://python-poetry.org/docs/).

# Install necessary packets

Run the following command to install the necessary packets:

```bash
poetry install
```

# Setting up the environment

To use the geocoding api you need to set the environment variable `GEOCODE_API`. Get a key of your own from https://geocode.maps.co/. Copy the file `.env.template` to `.env` and set the value of the variable to the api key.

# Opening the notebook

Now you can open the notebook and execute the code. If you open it in vs code you will be asked to select which kernel to use. Select the one that was created by poetry.

![](img/select-kernel.png)

# Run the application

To run the application, run the following command:

```bash
poetry run python -m app
```
