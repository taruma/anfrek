import base64
import io
import pandas as pd
from dash import html


def parse_upload_data(content: str, filename: str):
    _, content_string = content.split(",")

    decoded = base64.b64decode(content_string)

    try:
        if filename.endswith(".csv"):
            dataframe = pd.read_csv(
                io.StringIO(decoded.decode("utf-8")), index_col=0, parse_dates=True
            )
        elif filename.endswith(".xlsx") or filename.endswith(".xls"):
            return (
                html.Div(
                    [
                        "Fitur pembacaan berkas excel masih dalam tahap pengembangan.",
                        " Template yang akan digunakan adalah hidrokit excel template.",
                    ],
                    className="text-center bg-danger text-white fs-4",
                ),
                None,
            )

        else:
            return (
                html.Div(
                    ["Hanya dapat membaca format .csv"],
                    className="text-center bg-danger text-white fs-4",
                ),
                None,
            )
    except Exception as e:
        print(e)
        return html.Div([f"There was an error processing this file. {e}"]), None

    return None, dataframe


def transform_to_dataframe(
    table_data,
    table_columns,
    multiindex: bool = False,
    apply_numeric: bool = True,
    parse_dates: list = None,
):

    if multiindex is True:
        dataframe = pd.DataFrame(table_data)
        dataframe.columns = pd.MultiIndex.from_tuples(
            [item["name"] for item in table_columns]
        )
    else:
        columns = pd.Index([item["name"] for item in table_columns])
        dataframe = pd.DataFrame(table_data, columns=columns)

    dataframe["DATE"] = pd.to_datetime(dataframe.DATE)
    dataframe = dataframe.set_index("DATE").sort_index()

    if multiindex is True:
        # removing date (index.name) from top level multiindex
        dataframe.columns = pd.MultiIndex.from_tuples(dataframe.columns.to_flat_index())

    if apply_numeric is True:
        dataframe = dataframe.apply(pd.to_numeric, errors="coerce")
    else:
        dataframe = dataframe.infer_objects()

    if parse_dates is not None:
        if multiindex:
            for col_dates in parse_dates:
                col_parsing = [
                    col_tuple
                    for col_tuple in dataframe.columns
                    if col_dates in col_tuple
                ]
                for col_dates in col_parsing:
                    dataframe[col_dates] = pd.to_datetime(
                        dataframe[col_dates], errors="coerce"
                    )
        else:
            for col_dates in parse_dates:
                dataframe[col_dates] = pd.to_datetime(
                    dataframe[col_dates], errors="coerce"
                )

    return dataframe
