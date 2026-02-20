from dash import Dash, html, dcc, Output, Input
import plotly.express as px
import pandas as pd

# داده نمونه (می‌توانی با API جایگزین کنی)
data = {
    "date": pd.date_range(end=pd.Timestamp.today(), periods=7).tolist()*6,
    "parameter": ["pm25","pm10","no2","co","o3","so2"]*7,
    "value": [120,95,40,12,30,10,110,90,42,14,28,11,
              130,100,38,15,32,9,125,92,41,13,31,10,
              118,89,39,12,29,11,112,85,36,10,25,8,
              110,80,34,11,27,9],
    "location": ["Test"]*42
}
df = pd.DataFrame(data)

# تحلیل کوتاه فارسی
analysis_texts = {
    "pm25":"ذرات ریز PM2.5 برای ریه‌ها خطرناک است.",
    "pm10":"ذرات درشت PM10 باعث تحریک تنفسی می‌شوند.",
    "no2":"گاز NO2 از خودرو و صنعت منتشر می‌شود.",
    "co":"گاز CO در سطح بالا بسیار خطرناک است.",
    "o3":"ازن O3 باعث تحریک تنفسی می‌شود.",
    "so2":"SO2 باعث مشکلات تنفسی و آلرژی می‌شود."
}

parameters = sorted(df['parameter'].unique())
dropdown_options = [{"label": p.upper(), "value": p} for p in parameters]

# اپ Dash
app = Dash(__name__)
app.layout = html.Div([
    html.H1("داشبورد آلودگی هوای اردکان", style={"textAlign":"center"}),
    dcc.Dropdown(id="param-dropdown", options=dropdown_options, value=parameters[0], clearable=False, style={"width":"200px","margin":"0 auto"}),
    html.Div([
        dcc.Graph(id="bar-graph", style={"display":"inline-block","width":"45%"}),
        dcc.Graph(id="line-graph", style={"display":"inline-block","width":"45%"})
    ], style={"textAlign":"center"}),
    html.Div(id="analysis-box", style={"border":"1px solid #ccc","padding":"10px","width":"60%","margin":"20px auto","backgroundColor":"#f9f9f9","textAlign":"justify"}),
    html.P("تهیه شده توسط غزل امیدواری، دانشجوی ارشد رشته مدیریت صنعتی، دانشگاه یزد", style={"textAlign":"center","fontStyle":"italic"})
])

@app.callback(
    Output("bar-graph","figure"),
    Output("line-graph","figure"),
    Output("analysis-box","children"),
    Input("param-dropdown","value")
)
def update_graph(param):
    df_bar = df[df.parameter==param].groupby("location")["value"].mean().reset_index()
    fig_bar = px.bar(df_bar, x="location", y="value", color="value", color_continuous_scale=px.colors.sequential.Viridis, title=f"{param.upper()} میانگین مکان‌ها")
    df_line = df[df.parameter==param].groupby("date")["value"].mean().reset_index()
    fig_line = px.line(df_line, x="date", y="value", markers=True, title=f"روند {param.upper()} در زمان", color_discrete_sequence=["crimson"])
    return fig_bar, fig_line, analysis_texts.get(param,"")

if __name__ == "__main__":
    app.run(debug=True)
