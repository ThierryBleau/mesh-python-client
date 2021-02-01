import requests as r
import pandas as pd
from datetime import datetime
import json, time, base64

class MeshClient():
    def __init__(self,username=None,password=None):
        if not username:
            print("[ERROR] Username required")
        elif not password:
            print("[Error] Password required")
        else:
            encoded_auth = base64.b64encode(f"{username}:{password}".encode())
            self.auth = f"Basic {encoded_auth.decode()}"
            self.rest_url = "https://api.merfi.xyz/api/"
            self.graphql_url = "https://api.merfi.xyz/graphql"
            self.search_query = '''
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
            '''
    
    def engine(self,mesh_string,time_start=None,time_end=None,unit="MINUTE",number=15,display='raw'):

        if time_start is None:
            time_start = int((datetime.now().timestamp() - 3*86400))
        if time_end is None:
            time_end = int(datetime.now().timestamp())

        headers = {
          "Authorization":self.auth,
          "Content-Type":"application/json"
        }

        params = {
            "expr":mesh_string,
            "range":{"tstart":time_start,"tend":time_end},
            "interval":{"unit": unit,"n":number}
        }

        identifier = r.post(self.rest_url + "engine",json=params,headers=headers)

        result = None
        while not result:
            status = r.get(self.rest_url + "status",params={"id":identifier.content.decode()},headers=headers)
            #print(status.content.decode())
            if status.content.decode() != 'DONE':
                time.sleep(4)
            else:
                result = r.get(self.rest_url + "fetch", params={"id":identifier.content.decode()},headers=headers).json()

        if display == "raw":
            df = result
        elif display == "dataframe":
            if result[0] == 'DSLScalar':
                df = result['engine']['value']
            else:
                df = pd.DataFrame.from_records(result["DSLTimeseries"]["values"])
                df["timestamp"] = pd.to_datetime(df["timestamp"],unit="s")
        else:
            df = None

        return df

    
    
    def search(self,search_string):
        if search_string == "":
            return None
        else:
            return r.post(self.graphql_url,json={"query":self.search_query,"variables":{"search_str":search_string}})
        