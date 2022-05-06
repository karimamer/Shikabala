import pandas as pd


def readfromhtml(filepath):
    """
    x = readfromhtml(
        "https://fbref.com/en/comps/Big5/shooting/players/Big-5-European-Leagues-Stats"
    )
    main idead is to use df = pd.read_html(filepath)[0] 
    """

    df = pd.read_html(filepath)[0]
    column_lst = list(df.columns)
    for index in range(len(column_lst)):
        column_lst[index] = column_lst[index][1]

    df.columns = column_lst
    df.drop(df[df["Player"] == "Player"].index, inplace=True)
    df = df.fillna("0")
    df.set_index("Rk", drop=True, inplace=True)
    try:
        df["Comp"] = df["Comp"].apply(lambda x: " ".join(x.split()[1:]))
        df["Nation"] = df["Nation"].astype(str)
        df["Nation"] = df["Nation"].apply(lambda x: x.split()[-1])
    except ValueError:
        print("Error in uploading file:" + filepath)
    finally:
        df = df.apply(pd.to_numeric, errors="ignore")
        return df
