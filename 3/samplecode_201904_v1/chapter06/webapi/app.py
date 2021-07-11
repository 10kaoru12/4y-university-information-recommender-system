import hug
import pymongo 


def _build_mongodb_client():
    user = 'root'
    password = 'set_yours_credential'
    authority = "mongo:27017"
    client = pymongo.MongoClient(f"mongodb://{user}:{password}@{authority}")
    return client

        
def fetch_mongo_items():
    client = _build_mongodb_client()    
    
    db = client["mynavi"]    
    collection = db["books"]
    
    items = list(collection.aggregate([
        {"$project": {"_id": 1}},
        {"$sample": {"size": 3}},
    ]))                 
    return [item['_id'] for item in items]


def fetch_pickup_items():
    client = _build_mongodb_client()    
    
    db = client["mynavi"]    
    collection = db["pickup"]
    return [item["book_id"] for item in collection.find({}, {"_id": 0, "book_id": 1})]    


def merge_serieses_keeping_order(lhs_ids, rhs_ids):
    from itertools import chain
    seen = set()
    for item in chain(lhs_ids, rhs_ids):
        if item in seen:
            continue
        
        seen.add(item)
        yield item
           

@hug.get("/")
def api_example():
    return "WebAPIの開発"


@hug.get("/items", versions=1)
def api_random_ids():
    # 各自の実行環境のMongoDB上で存在するIDを指定する
    ids = fetch_mongo_items()
    ids = list(map(str, ids))
    return {
        "data": ids,
        "logic": "random"
    }


# 古いロジックにバージョン番号を与える
@hug.get("/items", versions=1)
def api_random_ids_with_pickup():
    # 各自の実行環境のMongoDB上で存在するIDを指定する
    ids = merge_serieses_keeping_order(
        fetch_pickup_items(),
        fetch_mongo_items(),        
    )
    ids = list(map(str, ids))
    return {
        "data": list(ids)[:3],
        "logic": "random w/ pickup"
    }


def fetch_ranked_items():
    client = _build_mongodb_client()        
    db = client["mynavi"]    
    collection = db["ranking_click"]
    
    items = list(collection.find().sort([
        ("date", pymongo.DESCENDING), 
        ("count", pymongo.DESCENDING)]
    ).limit(3))
    
    return [item["book_id"] for item in items]    


@hug.get("/items")
def api_ranking_by_click():
    # 各自の実行環境のMongoDB上で存在するIDを指定する
    ids = merge_serieses_keeping_order(
        fetch_ranked_items(),
        fetch_mongo_items(),        
    )
    ids = list(map(str, ids))
    return {
        "data": list(ids)[:3],
        "logic": "ranking-click"
    }


def fetch_ml_ranked_items():
    client = _build_mongodb_client()        
    db = client["mynavi"]    
    collection = db["ml_click"]
    
    items = list(collection.find().sort([
        ("date", pymongo.DESCENDING), 
        ("count", pymongo.DESCENDING)]
    ).limit(3))
    
    return [item["book_id"] for item in items]    


@hug.get("/items")
def api_ranking_by_ml_click():
    # 各自の実行環境のMongoDB上で存在するIDを指定する
    ids = merge_serieses_keeping_order(
        fetch_ml_ranked_items(),
        fetch_mongo_items(),        
    )
    ids = list(map(str, ids))
    return {
        "data": list(ids)[:3],
        "logic": "ml_click"
    }