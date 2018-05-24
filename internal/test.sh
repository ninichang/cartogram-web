#!/bin/bash

curl -X POST -s $HOST/cartogram -F handler=usa -F values="9;11;6;55;9;7;3;3;29;16;4;20;11;6;6;8;8;3;1;10;11;16;10;6;10;3;5;6;4;14;5;29;15;3;18;7;7;20;4;9;3;11;38;6;3;13;12;5;10;3" > test

python cmpjson.py test test_result.txt

if [ $? -eq 0 ]
then
    echo "Test passed."
else
    echo "Test failed."
fi