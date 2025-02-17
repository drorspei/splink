# https://stackoverflow.com/questions/52556798/spark-iterative-recursive-algorithms-breaking-spark-lineage
# From https://github.com/high-performance-spark/high-performance-spark-examples/blob/f02142bebf528437702ec8fa689c9c0263e96fe7/high_performance_pyspark/SQLLineage.py#L20



def cutLineage(df):
    """
    Cut the lineage of a DataFrame - used for iterative algorithms

    .. Note: This uses internal members and may break between versions
    >>> df = rdd.toDF()
    >>> cutDf = cutLineage(df)
    >>> cutDf.count()
    3
    """
    try:
        jRDD = df._jdf.toJavaRDD()
        jSchema = df._jdf.schema()
        jRDD.cache()
        sqlCtx = df.sql_ctx
        try:
            javaSqlCtx = sqlCtx._jsqlContext
        except:
            javaSqlCtx = sqlCtx._ssql_ctx
        newJavaDF = javaSqlCtx.createDataFrame(jRDD, jSchema)
        newDF = DataFrame(newJavaDF, sqlCtx)
        return newDF
    except AttributeError:
        return df


def default_break_lineage_blocked_comparisons(df_gammas, spark):
    df_gammas = cutLineage(df_gammas)
    df_gammas.persist()
    return df_gammas
