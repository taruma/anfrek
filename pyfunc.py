import base64
import io
import pandas as pd
import numpy as np
from dash import html


def parse_upload_data(content: str, filename: str):
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


def generate_report_statout(dataframe: pd.DataFrame) -> str:
    from hidrokit.contrib.taruma import hk158, hk151

    series = dataframe.iloc[:, 0]

    describe = series.describe()
    count, mean, std, smin, p25, p50, p75, smax = describe.to_list()
    Cv, Cs, Ck = hk158.calc_coef(series)
    std0 = series.std(ddof=0)
    Kn = hk151.find_Kn(count)
    mean_log = series.apply(np.log10).mean()
    std_log = series.apply(np.log10).std()
    lower_bound, upper_bound = hk151.calc_boundary(
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
        f"Cv = {Cv}\n"
        f"Cs = {Cs}\n"
        f"Ck = {Ck}\n\n"
        "[OUTLIER]\n"
        f"N = {count}\n"
        f"Kn = {Kn}\n"
        f"MEAN_LOG = {mean_log}\n"
        f"STD_LOG = {std_log}\n"
        f"LOWER_BOUND = {lower_bound}\n"
        f"UPPER_BOUND = {upper_bound}\n"
    )

    return report


def transform_return_period(return_period):
    result = []
    for period in return_period.split():
        try:
            num = abs(int(period))
            if num == 0:
                continue
            result.append(num)
        except Exception as e:
            print(e)

    return result


def generate_dataframe_freq(
    dataframe: pd.DataFrame,
    return_period: list[int],
    src_normal: str,
    src_lognormal: str,
    src_gumbel: str,
    src_logpearson3: str,
) -> pd.DataFrame:
    from hidrokit.contrib.taruma import anfrek

    dataframe = dataframe.iloc[:, 0].replace(0, np.nan).dropna().to_frame()

    df_normal = anfrek.freq_normal(
        dataframe,
        return_period=return_period,
        source=src_normal,
        index_name="Return Period",
    )

    df_lognormal = anfrek.freq_lognormal(
        dataframe,
        return_period=return_period,
        source=src_lognormal,
        index_name="Return Period",
    )

    df_gumbel = anfrek.freq_gumbel(
        dataframe,
        return_period=return_period,
        source=src_gumbel,
        index_name="Return Period",
    )

    df_logpearson3 = anfrek.freq_logpearson3(
        dataframe,
        return_period=return_period,
        source=src_logpearson3,
        index_name="Return Period",
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
    from hidrokit.contrib.taruma import hk140, hk141

    dist_name = "Normal,Log Normal,Gumbel,Log Pearson III".split(",")
    dist_name_lower = "normal,lognormal,gumbel,logpearson3".split(",")

    # KS

    ks_normal = hk140.kstest(
        dataframe,
        dist="normal",
        source_dist=src_normal,
        alpha=alpha,
        source_dcr=src_ks,
        show_stat=False,
        report="full",
    )
    ks_lognormal = hk140.kstest(
        dataframe,
        dist="lognormal",
        source_dist=src_lognormal,
        alpha=alpha,
        source_dcr=src_ks,
        show_stat=False,
        report="full",
    )
    ks_gumbel = hk140.kstest(
        dataframe,
        dist="gumbel",
        source_dist=src_gumbel,
        alpha=alpha,
        source_dcr=src_ks,
        show_stat=False,
        report="full",
    )
    ks_logpearson3 = hk140.kstest(
        dataframe,
        dist="logpearson3",
        source_dist=src_logpearson3,
        alpha=alpha,
        source_dcr=src_ks,
        show_stat=False,
        report="full",
    )

    ks_col = [ks_normal, ks_lognormal, ks_gumbel, ks_logpearson3]
    ks_frame = pd.concat(ks_col, keys=dist_name, axis=1)

    # CHI SQUARE

    chi_normal = hk141.chisquare(
        dataframe,
        dist="normal",
        source_dist=src_normal,
        alpha=alpha,
        source_xcr=src_chisquare,
        show_stat=False,
    ).rename({"batas_kelas": "classes"}, axis=1)
    chi_lognormal = hk141.chisquare(
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
