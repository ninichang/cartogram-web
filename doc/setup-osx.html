<h1>Setting Up the Web Application on Mac OS X</h1>

<p>This setup guide will help you get the go-cart web application up and running on Max OS X. This guide assumes that you already have Homebrew installed.</p>

<h2>Installing and Configuring Prerequisites</h2>

<p>First, you need to install some third-party software dependencies. Open a new terminal window, and run the following command:</p>

<pre><code>$ brew install python3 postgresql pkg-config
</code></pre>

<p>Now you'll need to configure the PostgreSQL database server. PostgreSQL is a robust SQL database server go-cart uses to store users' generated cartograms so they can be shared on social media. In order for go-cart to use PostgreSQL, you'll need to create an account and database:</p>

<pre><code>$ sudo su - postgres
...
$ createuser --interactive --pwprompt gocart
</code></pre>

<p>Enter a password when prompted, and answer no to all of the questions asked by typing <code>n</code> and pressing return each time:</p>

<pre><code>Enter password for new role: 
Enter it again: 
Shall the new role be a superuser? (y/n) n
Shall the new role be allowed to create databases? (y/n) n
Shall the new role be allowed to create more new roles? (y/n) n
</code></pre>

<p>Now, you can create the database and finish up:</p>

<pre><code>$ createdb -O gocart gocart
$ exit
</code></pre>

<p>Now, you need to download and compile the cartogram generator. You must use the cartogram generator from the repository below, <strong>not</strong> the one from <code>Flow-Based-Cartograms/go_cart</code>.</p>

<pre><code>$ git clone https://github.com/mgastner/cartogram.git
...
$ cd cartogram
$ chmod +x autobuild.sh
$ ./autobuild.sh
...
</code></pre>

<p>Remember the path to the root of this repository, as you'll need it when configuring the web application later.</p>

<h2>Installing and Configuring the Web Application</h2>

<p>First, clone the web application code from GitHub</p>

<pre><code>$ git clone https://github.com/jansky/cartogram-web
</code></pre>

<p>Now, you need to change some settings:</p>

<pre><code>$ cd cartogram-web/internal
$ cp envsettings.sh.dist envsettings.sh
$ open -a textedit envsettings.sh
</code></pre>

<p>In the third line, replace <code>/home/jansky/cartogram</code> in <code>CARTOGRAM_DATA_DIR</code> with the path to the folder containing the cartogram generator. Do not include a trailing slash.</p>

<p>In the ninth line, in <code>CARTOGRAM_DATABASE_URI</code>, replace <code>username</code> with <code>gocart</code>, <code>password</code> with the database password you created, and <code>database</code> with <code>gocart</code>. Save the file and quit TextEdit.</p>

<p>Finally, you need to initialize the database:</p>

<pre><code>$ source ./setupenv.sh
(venv) $ python3
&gt;&gt;&gt; import web
&gt;&gt;&gt; web.db.create_all()
&gt;&gt;&gt; exit()
(venv) $
</code></pre>

<h2>Running the Web Application</h2>

<p>When you want to run the web application, open a new terminal window and navigate to the root of the <code>cartogram-web</code> repository using <code>cd</code>. Then, run</p>

<pre><code>$ cd internal
$ source ./setupenv.sh
(venv) $ python web.py
...
</code></pre>

<p>Now, you can navigate to http://localhost:5000 in your web browser to access the go-cart web application. </p>

<p>When you are finished, you can go back to the terminal window and press Control-C to kill the web application process.</p>
