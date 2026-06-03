import pandas as pd


def load_data(file_path: str):
    """
    Load Excel dataset and perform basic validation.
    """

    df = pd.read_excel(file_path)

    print("\nDataset Loaded Successfully!")

    print("\nShape:")
    print(df.shape)

    print("\nColumns:")
    print(df.columns.tolist())

    print("\nNull Values:")
    print(df.isnull().sum().sum())

    print("\nDuplicate Rows:")
    print(df.duplicated().sum())

    return df


if __name__ == "__main__":

    df = load_data("data/Visit_Charges_data.xlsx")

    print("\nDataset Info:")
    print(df.info())

