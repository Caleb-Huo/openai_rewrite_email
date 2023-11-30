from shiny import App, reactive, render, ui
from openai import OpenAI

class Myemail:
    
    def __init__(self):
        self.before = ""
        self.after = ""
        self.system = {"role": "system", 
                   "content": "My name is Alex. I am a grad student in Department of Biostatistics. Please help me rewrite my email in a polite, professional and concise way."}
        self.user = {"role": "user", 
                 "content": self.before}
    
    def get_input(self, input):
        self.before = input
        self.user.update({"content": self.before})
    
    def rewrite(self):
        completion = client.chat.completions.create(  
            model="gpt-3.5-turbo",
            messages=[
                self.system,
                self.user
            ]
        )
        self.after = completion.choices[0].message.content
        #print(self.after)

client = OpenAI(api_key='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')        
myemail = Myemail()

app_ui = ui.page_fluid(
    ui.panel_title("Hi Alex, welcome to use your personalized email rewriter"),
    ui.input_text_area("x2", "", placeholder="Enter text"),
    ui.input_action_button("compute", "Rewrite!"),    
    ui.output_text_verbatim("result", placeholder=True),
)

def server(input, output, session):

    @output
    @render.text
    @reactive.event(input.compute) # Take a dependency on the button
    def result():
        myemail.get_input(input.x2())
        myemail.rewrite()
        # Because of the @reactive.event(), everything in this function is
        # ignored until reactive dependencies are triggered.
        return myemail.after

app = App(app_ui, server)
