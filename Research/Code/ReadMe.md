# Code to replicate the Clayton 2025 article

### Tricks used :

1. Cut the transcript in 5 to ensure not to lose the attention of the LLM
   
2. Made sure to cut the text in parts that are coherent in terms of meaning to help the LLM to inder on sentiments as well as possible

3. Passed the prompt found in Clayton(2025) as a system prompt to force the LLM to respect the rules as much as possible


### Ideas for the next steps

1. Check the sentiments found by the llm match the original transcript (basic nlp libraries)


### Problems :

1. The algorithm often has timeouts from the server of the Ollama

2. garder le meme prompt mais peut etre voir ce que ca donne pour q2 Nvidia 2025

