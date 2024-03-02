from dotenv import load_dotenv
import pandas as pd
import weaviate
import weaviate.classes as wvc
import yaml

MAX_EXPERIENCES = 5
COLLECTION_NAME = "Experience"
JOB_FILE = "./indexer/data/job.yml"


def generate_cover_letter(client, job):
    """use Weaviate's generative-openai module to prompt GPT to generate a cover letter

    :param client: Weaviate client to use for generative search
    :type client: WeaviateClient (V4)
    :param job: information about the job the cover letter is for
    :type job: panda dataframe row object (4 columns: 'company', 'position', 'role_description', 'requirements')
    """
    try:
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
        print(f"Response: {response}")
        for o in response.objects:
            print(o.generated)
            print(o.properties)

    except Exception as e:
        error_message = f"An error occurred: {str(e)}"
        return error_message


def vector_search(client, query):
    exps = client.collections.get(COLLECTION_NAME)
    result = exps.query.near_text(
        query=query,
        limit=MAX_EXPERIENCES,
        return_metadata=wvc.query.MetadataQuery(distance=True),
    )
    return result


load_dotenv()
wev = weaviate.connect_to_local()
question = "What's the best way to get fluffly scrambled eggs?"
try:
    with open(JOB_FILE, "r") as file:
        yaml_data = yaml.safe_load(file)

    job = pd.DataFrame(yaml_data, index=[0])
    answer = generate_cover_letter(wev, job.iloc[0])

    # Uncomment to test vector search results w/o GPT prompting
    # query = """
    # Help lead major projects and take new products from 0->1
    # Identify the hardest technical and/or quality problems holding us back, and then build solutions
    # Chart high level technical direction and follow up to make sure those projects come together to deliver on results
    # Mentor and develop new senior engineers to help grow the team
    # Ship new features and build infrastructure using: TypeScript, React, CSS, GraphQL, Node.js, and Postgres
    # At least 6 years of professional software development experience
    # Experience in a technical leadership role, working cross functionally
    # Working experience building full stack applications with TypeScript
    # Working experience building directly for users
    # You're excited about the future of programming and have experience working with IDEs, terminals, or other common developer tools
    # You've had previous experience working at a startup in a cross-functional engineering role
    # """
    # vecs = vector_search(wev, query)
    # print(f"Top {MAX_EXPERIENCES} results:")
    # for o in vecs.objects:
    #     print(o.properties)
    #     print(o.metadata.distance)
finally:
    wev.close()
