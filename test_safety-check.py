import ollama

original_text = '''
AITA for telling my sister who can't have kids that she does not get to be a part of naming mine and my wife's babies?

My older sister (34F) was born without the reproductive organs required to have a biological child. Because of her condition she also has some other health problems which disqualify her from adopting due to the uncertainty around her quality and length of life. She was aware for most of her life that she couldn't have biological children. That was discovered when she was still very young but the rest came throughout her 20s. She had dreams of motherhood and had lists of baby names she wanted to use. But she will never be able to use them on children that are hers. What I (28M) did not know at the time was she had saved her baby names and was hoping she would get to name or help name my future children.

My wife (27F) and I are expecting our first child. We haven't announced the sex but my sister thinks we're having a girl and shared her girl names with us. We thanked her and said we (wife and I) would discuss what the name would be at some point. My sister looked upset by the response and she then shared her boy names thinking she got it wrong. We gave her the same response.

My mom suggested a couple of months ago that it would be generous and kind to let my sister have some input. I told her we felt it was better if we named our child ourselves.

My wife and I did look at the list, just to see if we liked any of the names. We did not. Names on the lists included Elizabeth, Hannah, Rosemary and Francesca for girls and James, Edward, Patrick and Michael for boys. Those just aren't to our preference. None of them were and there were more names.

My sister mentioned the names again recently and she said we should pick Elizabeth for a girl and Michael for a boy. She said that's what she'd do if she were having the baby. I told her we hadn't made our mind up yet but were still in discussions about it. She offered to help and I said no thanks, my wife and I want to figure it out between us. My sister said she wants to be a part of naming all our babies. That she would love to share all her endless thoughts on names that she'll never get to put into her own kid. I told her I understood she wanted that but my wife and I as parents would name our child and she does not get to be a part of that. I told her I understood that was hurtful to her but she does not get a say. I also asked her to please stop bringing it up. My sister told me I could let her have at least a little say in this and I said sorry but no.

She cried to mom, who thinks we should be more sensitive, while my dad told my sister I wasn't wrong and she needs to accept that she doesn't get to name our baby. My response has caused a divide among my parents and sister and me. It has been made clear my mom thinks I lack compassion and my sister believes I'm hurtful to her.

AITA?
'''

system_prompt = '''
Read the input text and look at the original text. The input text should be a subset of the original text, with some spelling mistakes / added words / missing words. 
Correct the mistakes and return the corrected text - the corrected text should still be the 'input text' but with the corrected mistakes.

For example:
input text: Etta for asking my dad to give me at least half of the money my mom owes me
original text: AITA for asking my dad to give me at least half of the money my mom owes me I (19F) live with my mom, dad and younger siblings, ever since I turned 18 I wanted to get a job because I wanted to have money to buy things for myself but my parents always said no. The little money I got from my dad or aunts/uncles I'd save but my mom always asks for it claiming to have some emergency and when it's time to pay back the money she forgets she ever borrowed money from me
OUTPUT: AITA for asking my dad to give me at least half of the money my mom owes me
Notice that the corrected text is still the 'input text' but with the corrected mistakes. It also did not add to the end of the text. 
DO NOT return anything else except for the corrected text. That means no additional text or comments.
'''

def correct_spelling(text):
  response = ollama.chat(
  model="llama3.1",
  messages=[
      {
        "role": "system", "content": system_prompt },
      {"role": "user", "content": f"original text: {original_text}\ninput text: {text}"},
    ]
  )
  return response["message"]["content"]


print(correct_spelling("name my future children. My wife, 27F, and I are expecting our first child. We haven't announced"))
