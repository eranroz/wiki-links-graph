__author__ = 'eran'
import pandas as pd
import numpy as np
import scipy.sparse
import argparse


def create_orphan_pages(wikiname):
    pages = pd.read_csv('%s-page.csv.gz' % wikiname,
                        names=['pageid', 'namespace', 'title', 'page_is_redirect'],
                        usecols=[0, 1, 2, 5], compression='gzip')
    pages = pages.loc[pages.namespace == 0, ['pageid', 'title', 'page_is_redirect']]

    try:
        print('opening mainns')
        page_links = pd.read_csv('mainns-links-%s.csv' % wikiname)
    except:
        print('creating mainns links')
        page_links = pd.read_csv('%s-pagelinks.csv.gz' % wikiname,
                                 names=['from_page', 'ns', 'title', 'ns_from'],
                                 usecols=[0, 1, 2, 3], chunksize=100000, compression='gzip')
        only_main = (dt.loc[(dt.ns == 0) & (dt.ns_from == 0), ['from_page', 'title']] for dt in page_links)
        to_id = pd.concat([pd.merge(dt, pages, on='title', copy=False)[['from_page', 'pageid']] for dt in only_main])
        to_id.columns = ['from_page', 'to_page']
        page_links = to_id

        # resolve redirect
        redirects = page_links.loc[page_links.from_page.isin(pages.loc[pages.page_is_redirect == 1, 'pageid'])]
        redirects = redirects.groupby('from_page').filter(lambda x: len(x) == 1)  # only good redirects
        redirects.set_index('from_page', inplace=True)
        for i in range(3):
            page_links.loc[page_links.to_page.isin(redirects.index), 'to_page'] = page_links.loc[
                page_links.to_page.isin(redirects.index)].to_page.map(redirects.to_page)

        # remove redirect
        page_links = page_links.loc[~page_links.from_page.isin(redirects.index)]

        page_links.to_csv('mainns-links-%s.csv' % wikiname, index=False)

    # convert page_ids to series
    pages.set_index('pageid', inplace=True)
    pages = pages.loc[pages.page_is_redirect == 0]

    pageidmap = pd.Series(np.arange(pages.shape[0]), pages.index[pages.index.argsort()])

    page_links = page_links.loc[page_links.from_page.isin(pages.index)]
    page_links = page_links.loc[page_links.to_page.isin(pages.index)]
    print('Creating sparse graph')
    linkgraph = scipy.sparse.coo_matrix((np.ones(page_links.shape[0], dtype=bool),
                                         (page_links.from_page.map(pageidmap).values,
                                          page_links.to_page.map(pageidmap).values)),
                                        shape=(pages.shape[0], pages.shape[0]))
    print('Searching for connected components')
    n_components, labels = scipy.sparse.csgraph.connected_components(linkgraph, connection='strong')
    size_of_connected_components = np.bincount(labels)
    # skip the largest component
    connected_labels = np.argsort(size_of_connected_components)[-2::-1]
    connected_labels = connected_labels[size_of_connected_components[connected_labels] > 1]

    rows = []
    for i in connected_labels:
        connected_titles = pages[pages.index.isin(pageidmap[pageidmap.isin(np.where(labels == i)[0])].index)].title
        rows.append('<tr><td>%i</td><td>%s</td></tr>' % (len(connected_titles),
                                                         ', '.join(['<a href="%s">%s</a>' % (title, title) for title in
                                                                    connected_titles])))
    connected_table = '\n'.join(rows)
    with open('%s_components.html' % wikiname, 'w') as report:
        print('Wrote report')
        report.write(connected_table)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('wiki_name')
    args = parser.parse_args()
    print(args.wiki_name)
    create_orphan_pages(args.wiki_name)


if __name__ == '__main__':
    main()
