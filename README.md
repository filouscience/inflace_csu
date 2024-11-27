# inflace_csu
Script to fetch latest data on inflation from ČSÚ (Czech Statistical Office)


The dataset is located at [data.gov.cz/...](https://data.gov.cz/datov%C3%A1-sada?iri=https%3A%2F%2Fdata.gov.cz%2Fzdroj%2Fdatov%C3%A9-sady%2F00025593%2F790624c7263aca615ce9ddd24e7db464)

The script finds and downloads the latest distribution in form of CSV from there:
```
csv = getCSV()
```
The data is loaded into a Pandas DataFrame:
```
df = InflaceData(csv)
```
and can be accessed as a whole:
```
df.get_data_all()
```
or filtered by sector `ucel` and comparison base type `casz`:
```
df.get_data(ucel, casz)
```


### Demo
See the `demo.ipynb` notebook for a basic usage example.
