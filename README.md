[![Build Status](https://travis-ci.org/akhoroshev/redis-tools.svg?branch=master)](https://travis-ci.org/akhoroshev/redis-tools)

# Redis-tools
## Rdf loader

Loads RDF graph in ReddisGraph

##### Example of usage

``` 
$ ./rdf_loader.py examples/pizza.xml
```

##### Help 

``` 
$ ./rdf_loader.py -h 
```

## CFPQ query runner

Runs a cfpq query and collect statistics and results

##### Example of usage

``` 
$ ./cfpq_runner.py --algo ALGO_NAME --repeat 3 --port 6380 --prof gpu SUITE_PATH
```
##### Help 

``` 
$ ./cfpq_runner.py -h 
```