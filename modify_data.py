import json
import pandas


def main():

    main_df = pandas.read_json('data/gun_data.json')

    df = pandas.read_json('test.json')

    print(len(main_df))

    main_df = main_df.merge(df, on=["incident_id"])

    with open('data/gun_data_new.json', 'w') as outfile:
        main_df.to_json(outfile, orient='records')


if __name__ == "__main__":
    main()

    
    