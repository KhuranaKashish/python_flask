from flask import *
import pandas as pd
import sqlite3
import numpy as np
app = Flask(__name__)

@app.route("/")
def index():
           # ''' return the template file with user interface'''
     return render_template('view.html')

@app.route("/tables")
def show_tables_panda():
                   # ''' return the dataset stored in dataframe
    dfName = request.args.get('df')
    data = pd.read_csv(dfName + ".csv")
    return data.to_html()

@app.route("/tables1")
def show_tables_sqlite():
                        # ''' making connection to sqlite and returning the dataset stored in sqlite
     dfName = request.args.get('df')
     cnx = sqlite3.connect('Sqlitekashish.db')
     df1 = pd.read_sql_query("select * from " +dfName, cnx)
     return df1.to_html()

@app.route("/tables2")
def write_sqlite():
                  #''' writing the dataframe to sqlite
     dfName = request.args.get('df')
     cnx = sqlite3.connect('Sqlitekashish.db')
     data = pd.read_csv(dfName + ".csv")
     data.to_sql(dfName, cnx, if_exists='replace', index = False)
     df1 = pd.read_sql_query("select * from " +dfName, cnx)
    
     return df1.to_html()

@app.route("/tables3")
def delete_tables_sql():
               # '''Delete the selected file from sqlite
     dfName = request.args.get('df')
     cnx = sqlite3.connect('Sqlitekashish.db')
     cur = cnx.cursor()
     sql= "delete from " +dfName
     cur.execute(sql)
     cnx.commit()
     return render_template('message.html')

@app.route("/tables4")
def match_column():
                    #'''matching the column name of pandas dataframe to selected sqlite table
     dfName = request.args.get('df')
     dfName1 = request.args.get('df1')
     df3 = pd.read_csv(dfName + ".csv")
     cnx = sqlite3.connect('Sqlitekashish.db')
     df4 = pd.read_sql_query("select * from " +dfName1, cnx)
     
     match = np.intersect1d(df4.columns, df3.columns)
     match1 = pd.DataFrame(match)
     return match1.to_html()


@app.route("/tables5")
def nth_percentile():
                #''' returning the nth percentile of selected dataset with numerical data type
     dfName = request.args.get('df')
     dfName1 = request.args.get('df1')
     dfName1=int(dfName1)
     dfName1=dfName1/100
     df3 = pd.read_csv(dfName + ".csv")
     df4=df3.describe(percentiles=[dfName1], include=None, exclude=None)
     return df4.to_html()
   

if __name__ == "__main__":
    app.run(debug=True)
