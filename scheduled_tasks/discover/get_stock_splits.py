import os
import sys
import yaml
import requests
import pandas as pd
sys.path.append(os.path.join(os.path.dirname(__file__), '../..'))
from helpers import connect_mysql_database

cnx, engine = connect_mysql_database()
cur = cnx.cursor()

with open("config.yaml") as config_file:
    config_keys = yaml.load(config_file, Loader=yaml.Loader)


def main():
    final_df = pd.DataFrame()
    url = f"https://api.polygon.io/v3/reference/splits?limit=999&s" \
          f"ort=execution_date&apiKey={config_keys['POLYGON_KEY']}&reverse_split="
    for i in ["true", "false"]:
        df = pd.DataFrame(requests.get(url+i).json()["results"])
        df["Reverse"] = i.title()
        final_df = final_df.append(df)

    final_df.drop_duplicates(inplace=True)
    print(final_df)
    cur.executemany("INSERT IGNORE INTO stock_splits VALUES (%s ,%s ,%s ,%s, %s)", final_df.values.tolist())
    cnx.commit()


if __name__ == '__main__':
    main()