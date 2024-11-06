import urllib.request
import html.parser
import pandas as pd
import io

class DownloadLinkParser(html.parser.HTMLParser):
    def reset(self):
        super().reset() # call reset() method of the parent class
        self.link = ""
        self.flag = False
    
    def handle_starttag(self, tag, attrs):
        if tag == 'li':
            for (name, value) in attrs:
                if name == 'class' and value == 'download': # switch flag to True on <li class="download">
                    self.flag = True
        
        if tag == 'a' and self.flag == True:
            for (name, value) in attrs:
                if name == 'href':
                    self.link = value # save the download link
    
    def handle_endtag(self, tag):
        if tag == 'li': # switch flag to False on </li>
            self.flag = False
    
    def get_link(self):
        return self.link

def get_CSV_link():
    # Český statistický úřad -- dataset: Indexy spotřebitelských cen
    dataset_url = 'https://data.gov.cz/datov%C3%A1-sada?iri=https%3A%2F%2Fdata.gov.cz%2Fzdroj%2Fdatov%C3%A9-sady%2F00025593%2F790624c7263aca615ce9ddd24e7db464'
    dataset_obj = urllib.request.urlopen(dataset_url, data=None)
    text_bytes = dataset_obj.read()
    dataset_obj.close()
    text_str = text_bytes.decode('UTF-8') # HTML string
    parser = DownloadLinkParser()
    parser.feed(text_str)
    return parser.get_link() # return download link to the dataset distribution
    
def get_CSV(url=''):
    if url=='':
        csv_url = get_CSV_link() # unless specified (e.g. link to older distribution), get link to latest data from ČSÚ
    print('request CSV from: "' + csv_url + '"\n')
    csv_obj = urllib.request.urlopen(csv_url, data=None)
    csv_bytes = csv_obj.read()
    csv_obj.close()
    csv_str = csv_bytes.decode('UTF-8')
    return csv_str # return CSV as string

class InflaceData(): # composition of Pandas DataFrame and specific methods to extract relevant data
    def __init__(self, CSV_string):
        self.df = pd.read_csv(io.StringIO(CSV_string))         # load CSV to dataframe
        self.df.loc[self.df.ucel_kod.isnull(),'ucel_kod'] = 0  # ('ucel_kod' == NaN) refers to non-sector-specific data. Set NaN --> 0 for convenience.
        self.df.sort_values(by = 'obdobido', inplace = True)   # Sort by timestamp

    def list_ucel(self):
        print(self.df.drop_duplicates('ucel_kod',inplace=False).sort_values(by='ucel_kod').reset_index(drop=True)[['ucel_kod','ucel_txt']].astype({'ucel_kod': int}) )
        #    ucel_kod                                      ucel_txt
        #0          0                                           NaN
        #1          1              Potraviny a nealkoholické nápoje
        #2          2         Alkoholické nápoje, tabák a narkotika
        #3          3                                Odívání a obuv
        #4          4                Bydlení, voda, energie, paliva
        #5          5  Bytové vybavení, zařízení domácnosti; opravy
        #6          6                                        Zdraví
        #7          7                                       Doprava
        #8          8                                    Komunikace
        #9          9                            Rekreace a kultura
        #10        10                                    Vzdělávání
        #11        11                        Stravování a ubytování
        #12        12                      Ostatní výrobky a služby

    def list_casz(self):
        print(self.df.drop_duplicates('casz_kod',inplace=False).reset_index(drop=True)[['casz_kod','casz_txt']])
        #  casz_kod                             casz_txt
        #0        B                     předchozí období (meziměsíční)
        #1        Z                průměr bazického roku (bazický index, oproti průměru 2015)
        #2        C       stejné období předchozího roku (meziroční, oproti stejnému měsíci před rokem)
        #3        K  stejných 12 měsíců předchozího roku (průměrná meziroční)

    def get_data(self, ucel=0, casz='C'): # return selected data
        return self.df.loc[self.df.ucel_kod == ucel].loc[self.df.casz_kod == casz][['rok','mesic','hodnota']]
    
    def get_data_all(self):
        return self.df # return the entire dataframe














