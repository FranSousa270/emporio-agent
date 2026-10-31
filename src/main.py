from src.repositories.csv_repository import load_all_csv


def main():
    datasets = load_all_csv()

    for name, dataframe in datasets.items():
        print(f"\nDataset: {name}")
        print(f"Registros: {len(dataframe)}")
        print(f"Colunas: {list(dataframe.columns)}")


if __name__ == "__main__":
    main()