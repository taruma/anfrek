"""This module contains functions for processing data and generating reports."""

import base64
import io
import pandas as pd
import numpy as np
from dash import html
from hidrokit.contrib.taruma import hk158
from hidrokit.contrib.taruma import outlier_hydrology, statistical_coefficients
from hidrokit.contrib.taruma import gumbel, lognormal, normal, logpearson3

from hidrokit.contrib.taruma import hk140, hk141
from hidrokit.contrib.taruma import kolmogorov_smirnov, chi_square


def parse_upload_data(content: str, filename: str):
    """
    Parse and process uploaded data based on the file format.

    Args:
        content (str): The content of the uploaded file.
        filename (str): The name of the uploaded file.

    Returns:
        tuple or None: A tuple containing an HTML div element and a DataFrame object
            if the file format is supported. If the file format is not supported or
            there is an error, returns a tuple containing
            an HTML div element with an error message and None.

    Raises:
        UnicodeDecodeError: If the file is not valid UTF-8.
        pd.errors.ParserError: If the CSV file is not well-formed.
        ValueError: If the content string is not valid base64.
    """
    _, content_string = content.split(",")

    decoded = base64.b64decode(content_string)

    try:
        if filename.lower().endswith(".csv"):
            dataframe = pd.read_csv(
                io.StringIO(decoded.decode("utf-8")), index_col=0, parse_dates=True
            )
        elif filename.lower().endswith(".xlsx") or filename.lower().endswith(".xls"):
            return (
                html.Div(
                    [
                        "Fitur pembacaan berkas excel masih dalam tahap pengembangan.",
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
    except UnicodeDecodeError as e:
        print(e)
        return html.Div([f"File is not valid UTF-8. {e}"]), None
    except pd.errors.ParserError as e:
        print(e)
        return html.Div([f"CSV file is not well-formed. {e}"]), None
    except ValueError as e:
        print(e)
        return html.Div([f"Content string is not valid base64. {e}"]), None

    return None, dataframe


def transform_to_dataframe(
    table_data,
    table_columns,
    multiindex: bool = False,
    apply_numeric: bool = True,
    parse_dates: list = None,
):
    """
    Transform table data into a pandas DataFrame.

    Args:
        table_data (list): The table data to be transformed.
        table_columns (list): The columns of the table.
        multiindex (bool, optional): Whether to use a multi-index for the DataFrame. Defaults to False.
        apply_numeric (bool, optional): Whether to apply numeric conversion to the DataFrame. Defaults to True.
        parse_dates (list, optional): List of column names to parse as dates. Defaults to None.

    Returns:
        pandas.DataFrame: The transformed DataFrame.
    """

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


def generate_report_statout(dataframe: pd.DataFrame) -> str:
    """
    Generate a statistical report based on the given dataframe.

    Args:
        dataframe (pd.DataFrame): The input dataframe.

    Returns:
        str: The generated statistical report.

    """
    series = dataframe.iloc[:, 0]
    describe = series.describe()
    count, mean, std, smin, p25, p50, p75, smax = describe.to_list()
    coef_cv, coef_cs, coef_ck = hk158.calc_coef(series)
    std0 = series.std(ddof=0)
    kn_value = outlier_hydrology.find_Kn(count)
    mean_log = series.apply(np.log10).mean()
    std_log = series.apply(np.log10).std()
    lower_bound, upper_bound = outlier_hydrology.calc_boundary(
        series.replace(0, np.nan).dropna().to_frame()
    )

    report = (
        "[DESCRIPTIVE]\n"
        f"COUNT = {count}\n"
        f"MEAN = {mean}\n"
        f"STD = {std}\n"
        f"STD0 = {std0}\n"
        f"MIN = {smin}\n"
        f"25P = {p25}\n"
        f"50P = {p50}\n"
        f"75P = {p75}\n"
        f"MAX = {smax}\n\n"
        "[DISTRIBUTION]\n"
        f"Cv = {coef_cv}\n"
        f"Cs = {coef_cs}\n"
        f"Ck = {coef_ck}\n\n"
        "[OUTLIER]\n"
        f"N = {count}\n"
        f"Kn = {kn_value}\n"
        f"MEAN_LOG = {mean_log}\n"
        f"STD_LOG = {std_log}\n"
        f"LOWER_BOUND = {lower_bound}\n"
        f"UPPER_BOUND = {upper_bound}\n"
    )

    return report


def transform_return_period(return_period):
    """Transform return period string into a list of integers."""
    result = []
    for period in return_period.split():
        try:
            num = abs(int(period))
            if num == 0:
                continue
            result.append(num)
        except ValueError as e:
            print(e)

    return result


def generate_dataframe_freq(
    dataframe: pd.DataFrame,
    return_periods: list[int],
    src_normal: str,
    src_lognormal: str,
    src_gumbel: str,
    src_logpearson3: str,
) -> pd.DataFrame:
    """Generate a frequency analysis dataframe based on the given dataframe."""

    dataframe = dataframe.iloc[:, 0].replace(0, np.nan).dropna().to_frame()

    df_normal = normal.freq_normal(
        dataframe,
        return_periods=return_periods,
        source=src_normal,
        out_index_name="Return Period",
    )

    df_lognormal = lognormal.freq_lognormal(
        dataframe,
        return_periods=return_periods,
        source=src_lognormal,
        out_index_name="Return Period",
    )

    df_gumbel = gumbel.freq_gumbel(
        dataframe,
        return_periods=return_periods,
        source=src_gumbel,
        out_index_name="Return Period",
    )

    df_logpearson3 = logpearson3.freq_logpearson3(
        dataframe,
        return_periods=return_periods,
        source=src_logpearson3,
        out_index_name="Return Period",
    )

    result = pd.concat([df_normal, df_lognormal, df_gumbel, df_logpearson3], axis=1)

    return result


def generate_report_fit(
    dataframe: pd.DataFrame,
    alpha: float,
    src_ks: str,
    src_chisquare: str,
    src_normal: str,
    src_lognormal: str,
    src_gumbel: str,
    src_logpearson3: str,
) -> pd.DataFrame:
    """Generate a goodness of fit report based on the given dataframe."""

    dist_name = "Normal,Log Normal,Gumbel,Log Pearson III".split(",")
    dist_name_lower = "normal,lognormal,gumbel,logpearson3".split(",")

    # KS

    ks_normal = kolmogorov_smirnov.kolmogorov_smirnov_test(
        dataframe,
        distribution="normal",
        distribution_source=src_normal,
        significance_level=alpha,
        critical_value_source=src_ks,
        display_stat=False,
        report_type="full",
    )
    ks_lognormal = kolmogorov_smirnov.kolmogorov_smirnov_test(
        dataframe,
        distribution="lognormal",
        distribution_source=src_lognormal,
        significance_level=alpha,
        critical_value_source=src_ks,
        display_stat=False,
        report_type="full",
    )
    ks_gumbel = kolmogorov_smirnov.kolmogorov_smirnov_test(
        dataframe,
        distribution="gumbel",
        distribution_source=src_gumbel,
        significance_level=alpha,
        critical_value_source=src_ks,
        display_stat=False,
        report_type="full",
    )
    ks_logpearson3 = kolmogorov_smirnov.kolmogorov_smirnov_test(
        dataframe,
        distribution="logpearson3",
        distribution_source=src_logpearson3,
        significance_level=alpha,
        critical_value_source=src_ks,
        display_stat=False,
        report_type="full",
    )

    ks_col = [ks_normal, ks_lognormal, ks_gumbel, ks_logpearson3]
    ks_frame = pd.concat(ks_col, keys=dist_name, axis=1)


    chi_normal = chi_square.chisquare(
        dataframe,
        dist="normal",
        source_dist=src_normal,
        alpha=alpha,
        source_xcr=src_chisquare,
        show_stat=False,
    ).rename({"batas_kelas": "classes"}, axis=1)
    chi_lognormal = chi_square.chisquare(
        dataframe,
        dist="lognormal",
        source_dist=src_lognormal,
        alpha=alpha,
        source_xcr=src_chisquare,
        show_stat=False,
    ).rename({"batas_kelas": "classes"}, axis=1)
    chi_gumbel = hk141.chisquare(
        dataframe,
        dist="gumbel",
        source_dist=src_gumbel,
        alpha=alpha,
        source_xcr=src_chisquare,
        show_stat=False,
    ).rename({"batas_kelas": "classes"}, axis=1)
    chi_logpearson3 = hk141.chisquare(
        dataframe,
        dist="logpearson3",
        source_dist=src_logpearson3,
        alpha=alpha,
        source_xcr=src_chisquare,
        show_stat=False,
    ).rename({"batas_kelas": "classes"}, axis=1)

    chi_col = [chi_normal, chi_lognormal, chi_gumbel, chi_logpearson3]
    chi_frame = pd.concat(chi_col, keys=dist_name, axis=1)

    # REPORT
    series = dataframe.iloc[:, 0]

    # CHI REPORT
    n_class = hk141._calc_k(series.size)
    xcr = hk141.calc_xcr(alpha, dk=hk141._calc_dk(n_class, 2), source=src_chisquare)

    x2calc = []
    for _dist in chi_frame.columns.levels[0]:
        _chi = chi_frame[_dist]
        _x2 = np.sum(np.power(2, (_chi.fe - _chi.ft)) / _chi.ft)
        x2calc.append(_x2)

    x2calcs = pd.Series(x2calc, index=dist_name_lower)

    report_fit = (
        "[GOODNESS OF FIT]\n"
        f"N = {series.size}\n\n"
        "[KOLMOGOROV-SMIRNOV]\n"
        f"DELTA_CRITICAL = {hk140.calc_dcr(alpha, series.size, source=src_ks)}\n"
        f"DELTA_NORMAL = {ks_normal.d.max()}\n"
        f"DELTA_LOGNORMAL = {ks_lognormal.d.max()}\n"
        f"DELTA_GUMBEL = {ks_gumbel.d.max()}\n"
        f"DELTA_LOGPEARSON3 = {ks_logpearson3.d.max()}\n\n"
        "[CHI SQUARE]\n"
        f"X2_CRITICAL = {xcr}\n"
        f"X2_NORMAL = {x2calcs.normal}\n"
        f"X2_LOGNORMAL = {x2calcs.lognormal}\n"
        f"X2_GUMBEL = {x2calcs.gumbel}\n"
        f"X2_LOGPEARSON3 = {x2calcs.logpearson3}\n"
    )

    return (ks_frame, chi_frame, report_fit)
