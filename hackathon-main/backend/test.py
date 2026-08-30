# from chromadb import PersistentClient

# client = PersistentClient(path="./vector_store")

# collections = client.list_collections()

# for collection in collections:
#     print("COLLECTION:", collection.name)
#     print("COUNT:", collection.count())
from chromadb import PersistentClient

client = PersistentClient(path="./vector_store")

collection = client.get_collection(
    "policy_b083e3302abb4d05aaa010d737fc7750"
)

data = collection.get(
    include=["documents", "metadatas"]
)

print("TOTAL:", len(data["documents"]))

for i, (doc, metadata) in enumerate(
    zip(data["documents"], data["metadatas"])
):

    print("\n==============================")
    print("CHUNK:", i)
    print("METADATA:", metadata)
    print("TEXT:", doc[:200])