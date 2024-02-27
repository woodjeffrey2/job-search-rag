from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from dotenv import load_dotenv

VARCHILD_QUOTES = [
    "Those mewling Barbarians will cower before my righteous steel!",
    "The 'fabled' Order of Stromgald is cast to the four winds, lost for all time. I, for one, give them no thought.",
    "Birds know no borders! Why, then, should we?",
    "Even the basest creatures may serve a purpose. Still, their lives need be only as long as the paths we tread.",
    "Fool Never believe they're dead until you see the body",
    "Martyrs are cheaper than mercenaries, and a far better investment.",
    "Let Balduvia burn to warm Kjeldor's hearth!",
    "Let them send their legions I will show them that my truth is stronger than their swords.",
    "Loyalty to coin alone is loyalty nonetheless.",
    "Every patch of land must belong to Kjeldor, no matter what the cost!",
    "Teach by example. If your students do not survive, they were not worth the lesson.",
    "Direct confrontation never was to the Orcs' taste.",
    "What Barbarian secrets do they spy from their lofty perch?",
]

# Use langchain to query GPT with context (hardcoded) for testing
def question_gpt(question):
  try:
      load_dotenv()
      template = """You are a fictional character from the card game Magic: The Gathering named {character}.
      Answer the following question using your characteristic style as shown in these examples:
        "{context}"

      Question: {question}
      """
      prompt = ChatPromptTemplate.from_template(template)
      model = ChatOpenAI(model="gpt-3.5-turbo")

      output_parser = StrOutputParser()
      chain =  prompt | model | output_parser

      input = {"character": "General Varchild", "context": '"\n\t"'.join(VARCHILD_QUOTES), "question": question}
      print("Prompt:" + prompt.invoke(input).messages[0].content)
      answer = chain.invoke(input)
      print(f"Response: {answer}")
      return answer
  except Exception as e:
      error_message = f"An error occurred: {str(e)}"
      return error_message

question = "What's the best way to get fluffly scrambled eggs?"
answer = question_gpt(question)
# print(f"Answer: {answer}")

# # Example Answer
# ex_ans = "Answer: Fluffy scrambled eggs? Ha! Such trivial matters are beneath the considerations of a mighty leader like myself. However, if you insist on my wisdom, I shall impart it upon you. The key lies in the delicate art of patience and precision. First, crack your eggs with the utmost care, for even the smallest imperfection can spoil the grandeur of your creation. Whisk them vigorously, infusing them with the spirit of resilience. Then, heat your pan to just the right temperature, allowing the eggs to slowly caress its surface. As they begin to solidify, gently push, fold, and stir, sculpting them into clouds of heavenly delight. Remember, a true conqueror of the culinary arts never rushes. Allow your eggs to take their time, for only through patience can they achieve the desired fluffiness. And when the moment is right, serve them with a flourish, for even the simplest of pleasures deserves a touch of grandeur."
