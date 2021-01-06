from gql import Client, gql
from gql.transport.requests import RequestsHTTPTransport
import pandas as pd
from datetime import datetime

class MeshClient():
    def __init__(self):
        self._transport = RequestsHTTPTransport(url="https://merfi.xyz/graphql",verify=True, retries=3)
        self._gql_client = Client(transport=self._transport, fetch_schema_from_transport=True)
        self._engine_query = gql('''
        query getEngineResult ($expr: String!, $tstart: String, $tend: String, $interval_unit: intervalUnit!, $n: Int) {
          engine(expr: $expr, range: { from: $tstart, to: $tend}, interval: { unit: $interval_unit, n: $n}) {
            __typename,
            ...on DSLScalar {
              value
            }
            ...on DSLTimeseries {
              values {
                timestamp,
                value
              }
            }
            ...on DSLError {
              message
            }
          }
        }
        ''')
        self._search_query = gql('''
        query search($search_str: String!) {
          search(searchStr: $search_str) {
            ...on basicToken {
              symbol
              name
              address
            }
            ...on optionToken {
              premium {
                symbol
              }
              name
              address
            }
            ...on virtualToken {
              symbol
              name
            }
            ...on uniswapPair {
              name
              address
              token0Price {
                symbol
              }
            }
            ...on aggregatePair {
              name
            }
          }
        }
        ''')
    
    def engine(self,mesh_string,time_start=None,time_end=None,unit="MINUTE",number=15):
        if time_start is None:
            time_start = str(int((datetime.now().timestamp() - 3*86400)))
        if time_end is None:
            time_end = str(int(datetime.now().timestamp()))
        params = {
            "expr":mesh_string,
            "tstart":time_start,
            "tend":time_end,
            "interval_unit": unit,
            "n":number
        }
        result = self._gql_client.execute(self._engine_query,variable_values=params)
        df = pd.DataFrame.from_records(result["engine"]["values"])
        df["timestamp"] = pd.to_datetime(df["timestamp"],unit="s")
        return df
    
    def search(self,search_string):
        if search_string == "":
            return None
        else:
            result = self._gql_client.execute(self._search_query,variable_values={"search_str":search_string})
            return result
        