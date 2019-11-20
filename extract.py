import pandas
from newspaper import Article
import numpy as np
import validators
import json
import argparse

# there are 239,677 pages

parser = argparse.ArgumentParser()

parser.add_argument('--start', type=int, required=True)
parser.add_argument('--end', type=int, required=True)
parser.add_argument('--out', type=str, required=True)

def main(args):
    articles = []
    iters = 0

    def parse_url(x):
        nonlocal iters
        try:
            article_url = x['source_url']
            iid = x['incident_id']
            if (validators.url(article_url)):
                article_dict = {}
                article = Article(article_url)
                article.download()
                if (article.html != ''):
                    article.parse()
                    article_dict['incident_id'] = iid
                    article_dict['title'] = article.title
                    if (article.publish_date):
                        article_dict['publish_date'] = article.publish_date.date().isoformat()
                    else:
                        article_dict['publish_date'] = ''
                    article_dict['text'] = article.text
                    article_dict['shooting_date'] = x['date']
                    article_dict['address'] = x['address']
                    article_dict['n_killed'] = x['n_killed']
                    article_dict['n_injured'] = x['n_injured']
                    articles.append(article_dict)
        except:
            pass 
        
        iters += 1
        if iters % 100 == 0:
            print(iters)

    df = pandas.read_csv('gun-violence-data_01-2013_03-2018.csv')
    df = df.replace(np.nan, '', regex=True)

    df_slice = df[['incident_id', 'source_url', 'address', 'n_killed', 'n_injured', 'date']][args.start:args.end]

    df_slice.apply(parse_url, axis=1)   

    #title = 'gv_data_2000.json'
    with open(args.out, 'w') as outfile:
        json.dump(articles, outfile)


if __name__ == '__main__':
    args = parser.parse_args()
    main(args)



