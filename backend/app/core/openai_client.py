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
        from openai import OpenAI

        client = OpenAI( api_key= self.api_key)

        response = client.responses.create(
            model="gpt-4.1",
            input=prompt
        )

        print(response.output_text)
        return response.output_text

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