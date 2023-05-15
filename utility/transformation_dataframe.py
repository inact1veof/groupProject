import pandas as pd
import datetime


def transform(filenames_input, analyzer_names, pdk_level):

    frames = []
    for i in range(0, len(filenames_input)):
        df = pd.read_csv(filenames_input[i], sep=',', header=0)

        result_df = pd.DataFrame(columns=['Measurement', 'Value', 'Time'])

        result_df['Value'] = df[1] / pdk_level
        result_df['Time'] = df[0]
        result_df['Measurement'] = analyzer_names[i]
        result_df["Time"] = pd.to_datetime(result_df['Time']).dt.strftime('%Y-%m-%dT%H:%M:%SZ')

        frames.append(result_df)

    result = pd.concat(frames)

    return result
