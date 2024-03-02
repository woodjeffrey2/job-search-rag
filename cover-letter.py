from dotenv import load_dotenv
import pandas as pd
import weaviate
import weaviate.classes as wvc
import yaml

MAX_EXPERIENCES = 5
COLLECTION_NAME = "Experience"
JOB_FILE = "./indexer/data/job.yml"
OUTPUT_DIR = "./indexer/data"


def generate_cover_letter(client, job):
    """use Weaviate's generative-openai module to prompt GPT to generate a cover letter

    :param client: Weaviate client to use for generative search
    :type client: WeaviateClient (V4)
    :param job: information about the job the cover letter is for
    :type job: panda dataframe row object (4 columns: 'company', 'position', 'role_description', 'requirements')
    """
    job_description = f"""
      job description:
      {job["role_description"]}
      {job["requirements"]}
      """
    vector_placeholder = """
      professional experience:
      {job} - {description}
      """
    instructions = f"""
      I am an experienced software engineer applying for the {job["position"]} position at {job["company"]} detailed in the job description above.
      Please write a cover letter for my application that highlights any of my professional experience that seems relevant to the job description.
      """
    prompt_template = job_description + vector_placeholder + instructions
    print(f"Prompt Template: {prompt_template}")

    experiences = client.collections.get(COLLECTION_NAME)
    response = experiences.generate.near_text(
        query=job["requirements"],
        grouped_task=prompt_template,
        limit=MAX_EXPERIENCES,
    )

    for o in response.objects:
        print(o.generated)
        print(o.properties)
    print(f"Response: {response.generated}")

    # write GPT completion to file
    fname = (job["company"] + "-" + job["position"]).replace(" ", "_")
    with open(f"{OUTPUT_DIR}/{fname}.txt", "w") as f:
        f.write(response.generated)

    return response.generated


def vector_search(client, query):
    """use Weaviate's generative-openai module to prompt GPT to generate a cover letter

    :param client: Weaviate client to use for generative search
    :type client: WeaviateClient (V4)
    :param query: job context to compare against stored vectors
    :type query: string
    """
    exps = client.collections.get(COLLECTION_NAME)
    result = exps.query.near_text(
        query=query,
        limit=MAX_EXPERIENCES,
        return_metadata=wvc.query.MetadataQuery(distance=True),
    )
    return result


load_dotenv()
wev = weaviate.connect_to_local()
try:
    with open(JOB_FILE, "r") as file:
        yaml_data = yaml.safe_load(file)

    job = pd.DataFrame(yaml_data, index=[0])
    letter = generate_cover_letter(wev, job.iloc[0])

    # # Uncomment to test vector search results w/o GPT prompting
    # job = job.iloc[0]
    # vecs = vector_search(wev, job["requirements"])
    # print(f"Top {MAX_EXPERIENCES} results:")
    # for o in vecs.objects:
    #     print(o.properties)
    #     print(o.metadata.distance)
finally:
    wev.close()
