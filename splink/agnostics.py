def iterrows(df):
    if str(type(df)) == "<class 'pyarrow.lib.Table'>":
        return (row for _, row in df.iterrows())
    else:
        return df


def row_to_dict(row):
    try:
        return row.asDict()
    except AttributeError:
        return row.to_dict()