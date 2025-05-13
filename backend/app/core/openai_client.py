class OpenAIClient:
    def __init__(self, api_key: str):
        self.api_key = api_key

    def generate_summary(self, prompt: str) -> str:
        # import openai

        # openai.api_key = self.api_key
        # response = openai.ChatCompletion.create(
        #     model="gpt-3.5-turbo",
        #     messages=[
        #         {"role": "user", "content": prompt}
        #     ]
        # )
        # summary = response['choices'][0]['message']['content']
        # return summary
        
        from huggingface_hub import InferenceClient

        client = InferenceClient(
            provider="cerebras",
            api_key=self.api_key,
        )

        completion = client.chat.completions.create(
            model="meta-llama/Llama-4-Scout-17B-16E-Instruct",
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
        )
        result = completion.choices[0].message.content
        # result =   
        # print(result)
        if result.startswith("```html"):
            result = result[7:]  # Remove the first 7 characters (```html)
        if result.endswith("```"):
            result = result[:-3]  # Remove the last 3 characters (```)
        # print(result)
        return result
    
        # from openai import OpenAI

        # client = OpenAI( api_key= self.api_key)

        # response = client.responses.create(
        #     model="gpt-4.1",
        #     input=prompt
        # )


        # print(response.output_text)
        # return response.output_text

    # def stream_responses(self, prompt: str): 
    #     from openai import OpenAI
    #     client = OpenAI()
    #     stream = client.responses.create(
    #         model="gpt-4.1",
    #         input=[
    #             {
    #                 "role": "user",
    #                 "content": prompt,
    #             },
    #         ],
    #         stream=True,
    #     )

    #     for event in stream:
    #         print(event)