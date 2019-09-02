#!/usr/bin/env python

import json
import os
import glob
import fire


def main(sumber):
    json_path = f'csv/{sumber}/*__*.json'

    berita_json = glob.glob(json_path)

    berita = []
    for file in berita_json:
        try:
            with open(file) as f:
                berita.append(json.load(f))
        except Exception as e:
            print(str(e))
            pass
    # check if path is available
    if not os.path.exists(f'hasil/{sumber}'):
        os.makedirs(f'hasil/{sumber}')

    berita = [sub for i in berita for sub in i]
    with open(f'hasil/{sumber}.json', "w+") as f:
        json.dump(berita, f,indent=4, sort_keys=True, default=str)

    for berita in berita_json:
        os.remove(berita)


if __name__ == "__main__":
    fire.Fire(main)