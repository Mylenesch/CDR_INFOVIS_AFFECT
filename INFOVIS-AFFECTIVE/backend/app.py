from flask import Flask, jsonify, render_template, request
from flask_cors import CORS
from sqlalchemy import create_engine, text
import pandas as pd

app = Flask(__name__)
CORS(app) 


def _load_data_to_db():
    engine = create_engine("postgresql://myuser:mypassword@db/mydatabase")

    with engine.connect() as conn:
        conn.execute(text("DROP TABLE IF EXISTS od_matrix, sci CASCADE;"))

    od_df = pd.read_csv("modified_od_matrix.csv", delimiter=",")
    od_df.to_sql("od_matrix", engine, if_exists="replace", index=True)

    sci_df = pd.read_csv("sci.csv", delimiter=",")
    sci_df.to_sql("sci", engine, if_exists="replace", index=True)


def _fetch_od_data_from_db(query="SELECT * FROM od_matrix"):
    engine = create_engine("postgresql://myuser:mypassword@db/mydatabase")
    od_table = pd.read_sql_query(query, engine)
    if 'origin_centroid' in od_table.columns:
        od_table['origin_centroid'] = od_table['origin_centroid'].apply(coordify)
        od_table['origin_centroid'] = od_table['origin_centroid'].apply(tuple)
    if 'destination_centroid' in od_table.columns:
        od_table['destination_centroid'] = od_table['destination_centroid'].apply(coordify)
        od_table['destination_centroid'] = od_table['destination_centroid'].apply(tuple)
    return od_table


def coordify(x):
    x = x.replace('POINT (', '').replace(')', '').split()
    x = [float(value) for value in x]
    return x


def query_options(column_name):
    options = _fetch_od_data_from_db(f"SELECT DISTINCT {column_name} FROM od_matrix ORDER BY {column_name} ASC;")
    json_data = options.to_json(orient='records')
    return json_data


def _aggregate_flows(table):
    grouped = table.groupby(['origin_city', 'destination_city'])
    grouped_with_count = grouped.size().reset_index(name='count')
    merged_df = pd.merge(table, grouped_with_count, on=['origin_city', 'destination_city'], how='left')
    merged_df = merged_df.drop_duplicates(subset=['origin_city', 'destination_city'])
    return merged_df


def _aggregate_bars(table):
    grouped = table.groupby(['week', 'segment', 'origin_city'])['flow_count'].sum().reset_index()
    return grouped


def _create_bar_json_data(table):
        nested_dict = {}
        records = []
        for _, row in table.iterrows():
            record = {
                'week': row['week'],
                'segment': row['segment'],
                'flow_count': row['flow_count'],
                'origin_city': row['origin_city'],
            }
            records.append(record)

        nested_dict['records'] = records
        return nested_dict


def _create_od_json_data(table):
    nested_dict = {}
    records = []
    for _, row in table.iterrows():
        record = {
            'week': row['week'],
            'count': row['count'],
            'segment': row['segment'],
            'flow_count': row['flow_count'],
            'origin': {
                'city': row['origin_city'],
                'loc': row['origin_loc'],
                'centroid': row['origin_centroid']
            },
            'destination': {
                'city': row['destination_city'],
                'loc': row['destination_loc'],
                'centroid': row['destination_centroid']
            },
        }
        records.append(record)
    nested_dict['records'] = records
    return nested_dict


_load_data_to_db()



@app.route('/')
def home():
    return render_template('index.html')

@app.route('/get_options', methods=['GET'])
def get_options():
    origins = query_options('origin_city')
    destinations = query_options('destination_city')
    weeks = query_options('week')
    data = {
        'origins': origins,
        'destinations': destinations,
        'weeks': weeks
    }
    return jsonify(data)


@app.route('/get_query_results', methods=['GET'])
def get_query_results():
    query = "SELECT * FROM od_matrix WHERE destination_city = 'GAZIANTEP'"
    table = _fetch_od_data_from_db(query)
    table = _aggregate_flows(table)
    flows = _create_od_json_data(table)
    return jsonify(data=flows)


@app.route('/get_od', methods=['GET'])
def get_od():
    table = _fetch_od_data_from_db()
    table = _aggregate_flows(table)
    flows = _create_od_json_data(table)
    return jsonify(data=flows)


@app.route('/submit_filters', methods=['POST'])
def submit_filters():
    data = request.json
    selected_city = data.get('selectedCity')
    direction = data.get('direction')
    segments = data.get('selectedSegments')
    segments_str = ', '.join(f"'{segment}'" for segment in segments)
    weeks = data.get('selectedWeeks')
    weeks_str = ', '.join(f"'{week}'" for week in weeks)

    if selected_city != "All":
        if direction == 'to':
            if not segments:
                query = f"SELECT * FROM od_matrix WHERE destination_city = '{selected_city}' AND week IN ({weeks_str})"
            else:
                query = f"SELECT * FROM od_matrix WHERE destination_city = '{selected_city}' AND segment IN ({segments_str}) AND week IN ({weeks_str})"
        elif direction =='from':
            if not segments:
                query = f"SELECT * FROM od_matrix WHERE origin_city = '{selected_city}' AND week IN ({weeks_str})"
            else:
                query = f"SELECT * FROM od_matrix WHERE origin_city = '{selected_city}' AND segment IN ({segments_str}) AND week IN ({weeks_str})"
    else:
        if direction == 'to':
            if not segments:
                query = f"SELECT * FROM od_matrix WHERE week IN ({weeks_str})"
            else:
                query = f"SELECT * FROM od_matrix WHERE segment IN ({segments_str}) AND week IN ({weeks_str})"
        elif direction =='from':
            if not segments:
                query = f"SELECT * FROM od_matrix WHERE week IN ({weeks_str})"
            else:
                query = f"SELECT * FROM od_matrix WHERE segment IN ({segments_str}) AND week IN ({weeks_str})"

            
    fetched_data = _fetch_od_data_from_db(query)

    bar_table = _aggregate_bars(fetched_data)
    bar_data = _create_bar_json_data(bar_table)

    od_table = _aggregate_flows(fetched_data)
    flow_data = _create_od_json_data(od_table)
  

    response = {
        'barData': bar_data,
        'flowData': flow_data
    }
  
    return jsonify(response)


@app.route('/get_bar_data', methods=['GET'])
def get_bar_data():
    table = _fetch_od_data_from_db("SELECT * FROM od_matrix WHERE origin_city = 'Gaziantep'")
    table = _aggregate_bars(table)
    data = _create_bar_json_data(table)

    return jsonify(data)

if __name__ == '__main__':
    app.run(host='0.0.0.0')
