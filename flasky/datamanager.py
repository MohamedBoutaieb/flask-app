import redis
from redis.commands.search.query import Query
import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler, OrdinalEncoder
import pickle
import mysql.connector

def list_to_binary_floats(float_list):
    """Converts a list of floats into a packed binary representation."""
    return np.array(float_list, dtype=np.float32).tobytes()

class DataManager:
    def __init__(self,host : str = "localhost", port : int = 6379) -> None:
        with open('models/scaler.pkl','rb') as f:
            self.sc : StandardScaler = pickle.load(f)
        with open('models/ordinal.pkl','rb') as f:
            self.oe : OrdinalEncoder = pickle.load(f)

        self.r = redis.Redis(
            host=host,
            port=port)
        
        # MySQL connection parameters
        config = {
            'user': 'root',
            'password': '1234',
            'host': 'localhost',
            'database': 'veh',
            'raise_on_warnings': True
        }

        self.conn = mysql.connector.connect(**config)
        self.cursor = self.conn.cursor()
    
    def query(self,query_dict : dict):
        res_list = self.redis_search(query_dict)
        return self.db_result_query(res_list)
    
    def preprocess(self, query : dict):
        qq = pd.DataFrame([query])
        columns_to_categorize = ['fuel','seller_type','transmission']
        columns_to_scale = ['year', 'selling_price', 'km_driven', 'fuel','mileage','engine','max_power','seats','fuel','seller_type','transmission']
        qq[columns_to_categorize] = self.oe.transform(qq[columns_to_categorize])
        qq[columns_to_scale] = self.sc.transform(qq[columns_to_scale])
        return qq.iloc[0,:]
    
    # function to perform a redis search, taking in a list of floats as input
    def redis_search(self,query : dict):
        float_list = list_to_binary_floats(self.preprocess(query))

        query = (
            Query("*=>[KNN 5 @vector $vec as score]")
            .sort_by("score")
            .return_fields("score")
            .paging(0, 5)
            .dialect(2)
        )

        query_params = {
            "vec": float_list
        }
        
        return self.r.ft("idx1").search(query, query_params).docs
        

    def db_result_query(self,redis_response_list):
        res = []
        for vid in redis_response_list:
            # Parameterized query to prevent SQL injection
            sql = "SELECT * FROM vehicule WHERE id = %s"
            id_value = vid['id'].split(':')[1]
            
            self.cursor.execute(sql, (id_value,))
            
            # Fetching the result
            res.append(self.cursor.fetchone())
        return res
