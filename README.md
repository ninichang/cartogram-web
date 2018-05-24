# Cartogram Web Visualization Project

This project uses the cartogram generation algorithm written by Gastner et. al. to create an interactive cartogram-generating website.

## Layout

This website is split into two component parts. First, there is the algorithm (or internal) side. This code is intended to be deployed on the Yale-NUS workstation, and will handle cartogram generation. All of this code is located in the `internal/` folder. Secondly, there is the user (or external) side. This code is inteded to be deployed on an external server, and serve as the public face of the website. All of this code will be located in the `external/` folder.

## Algorithm Side

The algorithm side uses Flask to create a simple web application that interfaces with a Python wrapper for the original C cartogram program.

### Prerequisites

You need to have the following installed on your computer:

* Python 3
* Python Virtualenv (can be installed via `pip` by `sudo pip install virtualenv`)

### Configuration and Installation

Before you run the server, you'll need to configure a few environment variables inside `internal/setupenv.sh`:

**CARTOGRAM\_DATA\_DIR:** The path of the directory that contains the `cartogram` executable, as well as all original `.gen` files<br/>
**CARTOGRAM_COLOR**: HTML color that will be used to color the cartogram.<br/>
**CARTOGRAM_DEBUG**: Set to `TRUE` to run the Flask server in debug mode. Otherwise set to `FALSE`.<br/>
**CARTOGRAM_HOST**: Host (e.g. `127.0.0.1:5000`) for the Flask (development) and Gunicorn (production) servers.<br/>
**CARTOGRAM_PORT**: Port (e.g. `5000`) for the Flask (development) and Gunicorn (production) servers.

Once you have set these values, you can set up the Python virtualenv. Change into the `internal` directory from the project root, and run `source ./setupenv.sh`.

**Note:** The `setupenv` script defaults to creating the virtualenv in `internal/venv`, and uses `/usr/bin/python3` as the path to the Python executable. If you do not like these defaults, you may change them by editing `setupenv.sh`, or running it as follows:

    $ VIRTUALENV_LOCATION=path/to/venv PYTHON=/path/to/python source ./setupenv.sh

### Running the Development Server

If you have not already activated the Python virtualenv, change into the `internal` directory from the project root, and run `source ./setupenv.sh`.

To start the development server, run `python web.py`. The server will bind to the address and port specified in `internal/setupenv.sh`.

### Running the Production Server

The server that comes with Flask is unsuitable for production. Instead, we use Gunicorn. If you have not already activated the Python virtualenv, change into the `internal` directory from the project root, and run `source ./setupenv.sh`.

To start the development server, run `./gunicorn.sh`. The server will bind to the address and port specified in `internal/setupenv.sh`.

### Testing

You can test that everything is up and running by running a sample request:

    curl -X POST -s YOUR_HOST_AND_PORT/cartogram -F handler=usa -F values="9;11;6;55;9;7;3;3;29;16;4;20;11;6;6;8;8;3;1;10;11;16;10;6;10;3;5;6;4;14;5;29;15;3;18;7;7;20;4;9;3;11;38;6;3;13;12;5;10;3" > test

You can then compare the `test` file against `internal/test_result.txt`. I have not yet found a satisfactory way to confirm that the results match. Simple `diff` does not work, because Python's `json.dump` has a tendency to change the order of the JSON values it outputs. However, the file is too large to be analyzed by a more specialized JSON diff tool like `jsondiff` in a reasonable amount of time.



