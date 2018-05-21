json_ploy.py
============
Simple plotting of JSON lines from a file or stdin

Installation
------------
pip:
```
pip install -r requirements.txt
```

Debian/Ubuntu/etc:
```
apt-get install python-matplotlib python-numpy
```

Usage:
------
Data can be plotted using an `input` file:
```
python plot_json.py parents children --input JSON_FILE
```

Or piped from `stdin`:
```
echo <JSON_DATA> | python plot_json.py foo,bar a,b
```

Use the help message for additional arguments and information:
```
python plot_json.py --help
```

Example:
--------
This will plot random data points for parents `foo` and `bar` with children `a` and `b` on most *nix systems:
```
for x in {foo,bar}; do
  for y in {0..9}; do
    printf "{\"2000-01-01 12:34:0${y}\": {\"${x}\": {\"a\":$RANDOM,\"b\":$RANDOM}}}\n";
  done;
done | python plot_json.py foo,bar a,b
```
