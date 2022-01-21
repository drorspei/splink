def iterrows(df):
    if str(type(df)) == "<class 'pandas.core.frame.DataFrame'>":
        return (row for _, row in df.iterrows())
    else:
        return df


def row_to_dict(row):
    try:
        return row.asDict()
    except AttributeError:
        return row.to_dict()