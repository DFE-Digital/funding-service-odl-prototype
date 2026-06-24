import requests
import pandas as pd
import polars as pl

def do_something():
    return pd.DataFrame()

if __name__ == '__main__':
    print(do_something.__dict__)
    print(vars(do_something))

print()