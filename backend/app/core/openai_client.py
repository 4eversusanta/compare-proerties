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
        
        # from huggingface_hub import InferenceClient

        # client = InferenceClient(
        #     provider="cerebras",
        #     api_key=self.api_key,
        # )

        # completion = client.chat.completions.create(
        #     model="meta-llama/Llama-4-Scout-17B-16E-Instruct",
        #     messages=[
        #         {
        #             "role": "user",
        #             "content": prompt,
        #         }
        #     ],
        # )
        # result = completion.choices[0].message.content
        result = '''
                <!DOCTYPE html>
                <html lang="en">
                <head>
                <meta charset="UTF-8">
                <title>Property Comparison</title>
                <style>
                    body {
                    font-family: sans-serif;
                    padding: 20px;
                    }
                    .comparison-section {
                    max-width: 700px;
                    margin: auto;
                    }
                    .property-cards {
                    display: flex;
                    justify-content: space-between;
                    margin-bottom: 40px;
                    }
                    .property-card {
                    border: 1px solid #ccc;
                    border-radius: 8px;
                    padding: 15px;
                    width: 30%;
                    box-shadow: 0 2px 5px rgba(0,0,0,0.1);
                    }
                    .property-card h3 {
                    margin-top: 0;
                    }

                    .bar-chart {
                    display: flex;
                    flex-direction: column;
                    gap: 20px;
                    }
                    .bar-group {
                    display: flex;
                    align-items: center;
                    }
                    .bar-label {
                    width: 100px;
                    }
                    .bar {
                    height: 20px;
                    border-radius: 5px;
                    margin-right: 10px;
                    }
                    .bar-a {
                    background-color: #ff6384;
                    width: 60%;
                    }
                    .bar-b {
                    background-color: #36a2eb;
                    width: 80%;
                    }
                    .bar-c {
                    background-color: #4bc0c0;
                    width: 70%;
                    }
                </style>
                </head>
                <body>

                <div class="comparison-section">
                <h2>Real Estate Property Comparison</h2>

                <div class="property-cards">
                    <div class="property-card">
                    <h3>Property A</h3>
                    <p>Price: $450,000</p>
                    <p>Size: 1,800 sqft</p>
                    <p>Bedrooms: 3</p>
                    </div>
                    <div class="property-card">
                    <h3>Property B</h3>
                    <p>Price: $520,000</p>
                    <p>Size: 2,000 sqft</p>
                    <p>Bedrooms: 4</p>
                    </div>
                    <div class="property-card">
                    <h3>Property C</h3>
                    <p>Price: $490,000</p>
                    <p>Size: 1,900 sqft</p>
                    <p>Bedrooms: 3</p>
                    </div>
                </div>

                <div class="bar-chart">
                    <div class="bar-group">
                    <div class="bar-label">Price</div>
                    <div class="bar bar-a" title="Property A: $450K"></div>
                    <div class="bar bar-b" title="Property B: $520K"></div>
                    <div class="bar bar-c" title="Property C: $490K"></div>
                    </div>
                    <div class="bar-group">
                    <div class="bar-label">Size</div>
                    <div class="bar bar-a" style="width: 60%" title="1,800 sqft"></div>
                    <div class="bar bar-b" style="width: 80%" title="2,000 sqft"></div>
                    <div class="bar bar-c" style="width: 70%" title="1,900 sqft"></div>
                    </div>
                    <div class="bar-group">
                    <div class="bar-label">Bedrooms</div>
                    <div class="bar bar-a" style="width: 60%" title="3 Bedrooms"></div>
                    <div class="bar bar-b" style="width: 80%" title="4 Bedrooms"></div>
                    <div class="bar bar-c" style="width: 60%" title="3 Bedrooms"></div>
                    </div>
                </div>
                </div>

                </body>
                </html>
    
        '''    
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