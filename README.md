# Cartogram Web Visualization Project

This project uses the cartogram generation algorithm written by Gastner et. al. to create an interactive cartogram-generating website.

## Layout

All of the website code is currenlty located in the `internal/` folder. 

## Basic Outline

This website uses the Flask Python web framework, along with SQLAlchemy to create a friendly user interface for the original cartogram generating program written in C. The Flask application takes input from a CSV file, transforms this into the area information format readable by the C code, and then uses the `subprocess` module to invoke the original cartogram generating executable. The .gen-formatted output is then transformed into JSON that is plottable by D3. All of these inputs and outputs are stored in a database (SQLAlchemy supports a variety of database backends, but we've had the most success with PostgreSQL), allowing generated cartograms to be shared on social media. HTTP Streaming is used to deliver real-time information about the progress in generating each cartogram.

## Cartogram Generation Process

The following is a rough outline of the cartogram generating process using this website.

1. The user selects a map and uploads a corresponding CSV file with data they want to visualize.
2. An AJAX request is made to `/cartogramui`. This returns an "areas string", which contains the area information found in the CSV file separated by semicolons and place in a certain order (e.g. "3;14;27..."). Information about colors and tooltips are also returned. All of this information is stored in a database and associated with a unique string key.
3. An AJAX request is made to `/cartogram` with the areas string, map name, and unique string key. The C code is invoked, and progress is calculated and sent to the user via HTTP streaming (the Oboe.js library is used on the client side to parse the HTTP streaming data). The .gen output from the C code is transformed into JSON by the module `gen2dict` and displayed using the D3 JavaScript library.

## Prerequisites

You need to have the following installed on your computer:

* Python 3
* Python Virtualenv (can be installed via `pip` by `sudo pip install virtualenv`)
* A database server (PostgreSQL recommended)

All other prerequisites will be installed by the `internal/setupenv.sh` shell script.

## Configuration and Installation

Before you run the server, you'll need to configure a few environment variables. Copy `internal/envsetting.sh.dist` to `internal/envsettings.sh` and change the following settings

**CARTOGRAM\_DATA\_DIR:** The path of the directory that contains the `cartogram` executable, as well as all original `.gen` files<br/>
**CARTOGRAM_COLOR**: HTML color that will be used to color the cartogram.<br/>
**CARTOGRAM_DEBUG**: Set to `TRUE` to run the Flask server in debug mode. Otherwise set to `FALSE`.<br/>
**CARTOGRAM_HOST**: Host (e.g. `127.0.0.1:5000`) for the Flask (development) and Gunicorn (production) servers.<br/>
**CARTOGRAM_PORT**: Port (e.g. `5000`) for the Flask (development) and Gunicorn (production) servers.
**CARTOGRAM_DATABASE_URI**: URI for the database server used by SQLAlchemy.

Once you have set these values, make the `internal/envsettings.sh` script executable. You can now set up the Python virtualenv. Change into the `internal` directory from the project root, and run `source ./setupenv.sh`.

## Running the Development Server

If you have not already activated the Python virtualenv, change into the `internal` directory from the project root, and run `source ./setupenv.sh`.

To start the development server, run `python web.py`. The server will bind to the address and port specified in `internal/setupenv.sh`.

## Running the Production Server

The server that comes with Flask is unsuitable for production. Instead, we use Gunicorn. If you have not already activated the Python virtualenv, change into the `internal` directory from the project root, and run `source ./setupenv.sh`.

To start the production server, run `./gunicorn.sh`. The server will run in daemon mode, and bind to the address and port specified in `internal/setupenv.sh`. The Gunicorn shell script also calculates automatically the number of workers using the information in `/proc/cpuinfo`, following the recommended formula in the Gunicorn documentation (`2 x num_cores + 1`).

## Adding an Additional Map

This section assumes that you have found an acceptable conventional map, and that you have converted your chosen projection of that map into the .gen file format.

Each map used in this website has an associated `CartogramHandler` class that extends `handlers.base_handler.BaseCartogramHandler`. To create a new map, create the file `internal/handlers/my_new_map.py`. You'll then need to implement the following methods in your `CartogramHandler` class:

    class CartogramHandler(handlers.base_handler.BaseCartogramHandler):

        def get_name(self):
            # Returns a string containg the map's display name (e.g. "China")

        def get_gen_file(self):
            # Returns a string containing the path to the conventional map's .gen file
        
        def validate_values(self, values):
            # Returns True if the array of area values supplied is valid, False if it is not.
            # We recommend you use the following template, replacing NUMBER_OF_REGIONS with the actual number of regions in your map:
            # At this point the areas string has been turned into an array of floats (hopefully they're all floats):
            # (i.e. "4;31;27..." has become [4.0, 31.0, 27.0,...])

            if len(values) != NUMBER_OF_REGIONS:
                return False
            
            for v in values:
                if type(v) != float:
                    return False

            return True
        
        def gen_area_data(self, values):
            # Returns a string containing the cartogram area format with the user-specified values filled in
            # See one of the existing maps for an example
            # At this point the areas string has been turned into an array of floats (hopefully they're all floats):
            # (i.e. "4;31;27..." has become [4.0, 31.0, 27.0,...])

        def csv_to_area_string_and_colors(self, csvfile)
            # Converts CSV input to the areas string that is fed to the cartogram generator. This function also generates color and tooltip
            # information. You'll probably want to use handlers.base_handler.BaseCartogramHandler.order_by_example to do this. See
            # internal/handlers/base_handler.py for more information.

Finally you'll need to edit `internal/web.py`. First, import your new map module:

    from handlers import usa, india, china, your_new_map

Then, add it to the variable `cartogram_handlers`:

    cartogram_handlers = {
        'usa': usa.CartogramHandler(),
        'india': india.CartogramHandler(),
        'china': china.CartogramHandler(),
        'your_new_map': your_new_map.CartogramHandler()
    }



