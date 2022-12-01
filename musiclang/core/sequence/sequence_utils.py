


def merge_and_update(left, right, on):
    """
    Merge two sequences by updating when it is possible
    If the right array does not have an entry for the left row, use the previous value of the column

    :param left: Sequence that should be updated
    :param right: Sequence acting as the updater
    :param on: str or list, on which columns to perform the left join
    :return:
    """
    if not hasattr(on, '__iter__'):
        on = [on]
    new_columns = list(set(right.columns) - set(on))
    final = left.merge(right, on=on, how='left')
    colsx = [col + '_x' for col in new_columns]
    colsy = [col + '_y' for col in new_columns]
    for col in new_columns:
        final[col] = final[col + '_y'].fillna(final[col + '_x'])
    final = final.drop(colsx + colsy, axis=1)
    return final


def find_markov_path(df, columns, n=2, output_name=""):
    """
    Find the markov distribution with word of size n
    :param df:
    :param columns:
    :param n:
    :return:
    """
    sequence = df[columns]
