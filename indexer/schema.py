import weaviate
import weaviate.classes as wvc

CLASS_NAME = "Experience"


def create_collection_schema(client):
    """Create schema for professional experience in Weaviate

    :param client: Weaviate client to use to create the collection schema
    :type client: WeaviateClient (V4)
    """
    client.collections.create(
        name=CLASS_NAME,
        vectorizer_config=wvc.config.Configure.Vectorizer.text2vec_openai(
            vectorize_collection_name=False
        ),
        generative_config=wvc.config.Configure.Generative.openai(),
        properties=[
            wvc.config.Property(
                name="description",
                description="description of the professional experience",
                data_type=wvc.config.DataType.TEXT,
                vectorize_property_name=False,
                tokenization=wvc.config.Tokenization.WORD,
            ),
            wvc.config.Property(
                name="job",
                data_type=wvc.config.DataType.TEXT,
                vectorize_property_name=False,
                tokenization=wvc.config.Tokenization.WORD,
            ),
        ],
    )


client = weaviate.connect_to_local()
try:
    create_collection_schema(client)
    print("Schema created successfully")

except Exception as e:
    print("Error: " + e)

finally:
    client.close()
