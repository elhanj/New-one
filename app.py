from flask import Flask, render_template, request
import pandas as pd
import matplotlib
matplotlib.use('Agg')  # Use a non-interactive backend for matplotlib
import matplotlib.pyplot as plt
import io
import base64

app = Flask(__name__)

# Load the CSV file into a DataFrame
df = pd.read_csv("/Users/sophia/Downloads/IP_Project - IP project.csv")
# A copy of the original DataFrame to allow resetting
original_df = df.copy()

@app.route('/', methods=['GET', 'POST'])
def index():
    global df
    output = ""
    plot_url = ""

    if request.method == 'POST':
        action = request.form['action']

        if action == 'display_csv':
            output = df.to_html()
        
        elif action == 'count_countries':
            output = df['COUNTRY NAME'].count()
        
        elif action == 'loc_vietnam':
            if 9 in df.index:
                output = df.loc[9].to_frame().transpose().to_html()
            else:
                output = "<p>Index 9 does not exist in the DataFrame.</p>"
        
        elif action == 'filter_high_global_rate':
            df_filtered = df[df['GLOBAL RATE'] > 130]
            output = df_filtered.to_html()
        
        elif action == 'shape':
            output = f"<p>{df.shape}</p>"
        
        elif action == 'drop_column':
            df_dropped = df.drop('GLOBAL RATE', axis=1)
            output = df_dropped.to_html()
        
        elif action == 'insert_column':
            df['GDP GROWTH RATE (%)'] = [6.5, 5.6, 5.0, 6.1, 4.8, 6.0, 1.7, 2.6, 4.4, 6.8, 3.3, 5.5,
                                        3.5, 5.4, 2.5, 3.2, 3.5, 3.9, 5.5, 4.0, 0.8, 2.9, 4.2, 3.4, 6.1, 5.6, 4.8]
            output = df.to_html()
        
        elif action == 'plot_global_rate':
            plt.figure(figsize=(10,6))
            df.plot(kind='bar', x='COUNTRY NAME', y='GLOBAL RATE', color=['red'], ax=plt.gca())
            plt.xlabel('Country Name')
            plt.ylabel('Global Rate')
            plt.title('Global Rate by Country')
            plt.tight_layout()
            
            # Save plot to a bytes buffer
            buf = io.BytesIO()
            plt.savefig(buf, format='png')
            buf.seek(0)
            plot_data = base64.b64encode(buf.getvalue()).decode('ascii')
            plot_url = f"data:image/png;base64,{plot_data}"
            plt.close()
        
        elif action == 'plot_histogram':
            df4 = pd.DataFrame({"UNEMPLOYMENT RATE": [7.4, 6.6, 6.3, 4.7, 4.3, 2.8, 3.7, 2.2, 3.5, 3.0]},
                               index=["India", "Philippines", "Indonesia", "Pakistan", "Bangladesh", "Japan",
                                      "South Korea", "Singapore", "Australia", "Germany"])
            plt.figure(figsize=(10,6))
            df4.plot(kind='pie', y='UNEMPLOYMENT RATE', legend=False, autopct='%1.1f%%', ax=plt.gca())
            plt.title('Unemployment Rate Distribution')
            plt.tight_layout()

            # Save plot to a bytes buffer
            buf = io.BytesIO()
            plt.savefig(buf, format='png')
            buf.seek(0)
            plot_data = base64.b64encode(buf.getvalue()).decode('ascii')
            plot_url = f"data:image/png;base64,{plot_data}"
            plt.close()
        
        elif action == 'first_4_countries':
            output = df.head(4).to_html()
        
        elif action == 'reset':
            df = original_df.copy()
            output = "<p>DataFrame has been reset to its original state.</p>"

    return render_template('index.html', output=output, plot_url=plot_url)

if __name__ == '__main__':
    app.run(debug=True)
