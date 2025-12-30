from pyspark.sql import DataFrame
from pyspark.sql import functions as sf
from src.transform.core.pipelines.batch_transformer import BatchTransformerPipeline
from src.transform.core.steps.base_step import (
    remove_cols,
    change_order_cols,
    strip_prefix_before_delimiter,
    rename_cols,
    add_mapped_column,
)


class EeaTransformerPipeline(BatchTransformerPipeline):
    def apply_steps(self, ds_name: str, df: DataFrame, verbose=False) -> DataFrame:
        # Define cols to remove as list[str]
        cols_to_remove = [
            "Country_code",
            "Country",
            "Format_name",
            "Pollutant_name",
            "Notation",
            "DataSource",
            "PublicationDate",
            "Country_code_3",
            "Unit",
        ]

        # Cols new order
        cols_new_order = [
            "Sector_code",
            "Sector_name",
            "sector_label",
            "Parent_sector_code",
            "Year",
            "emissions",
        ]

        # Cols naming map
        cols_map = {
            "Sector_code": "sector_code",
            "Sector_name": "sector_name",
            "sector_label": "sector_label",
            "Parent_sector_code": "parent_sector_code",
            "Year": "year",
            "emissions": "emissions",
        }

        # Value names for a new col
        sector_name_to_label = {
            "Energy": "Energy",
            "Energy Industries": "Energy ind.",
            "Public Electricity and Heat Production": "Elec. & heat",
            "Petroleum Refining": "Refining",
            "Manufacturing Industries and Construction": "Manufacturing",
            "Manufacture of Solid Fuels and Other Energy Industries": "Solid fuels",
            "Fuel combustion activities (sectoral approach)": "Combustion",
        }

        if verbose:
            print("1. Raw dataframe:")
            df.show(n=5, truncate=False)

        df = remove_cols(df, cols_to_remove)

        if verbose:
            print(f"2. Removing cols: {cols_to_remove}")
            df.show(n=5, truncate=False)

        df = strip_prefix_before_delimiter(df, "Sector_name", delimiter="-")

        if verbose:
            print(
                "3. Stripping prefix before delimiter of 'Sector_name' before - character"
            )
            df.show(n=5, truncate=False)

        df = add_mapped_column(df, "sector_label", "sector_name", sector_name_to_label)

        if verbose:
            print("4. Add a new mapped column to enhance human readability")
            df.show(n=5, truncate=False)

        df = change_order_cols(df, cols_new_order)

        if verbose:
            print(
                f"5. Change the order of cols to follow this new order {cols_new_order}"
            )
            df.show(n=5, truncate=False)

        df = rename_cols(df, cols_map)

        if verbose:
            print("6. Renaming cols to follow snake_case convention")
            df.show(n=5, truncate=False)

        df = df.sort(sf.col("year"))

        if verbose:
            print("7. Sorting out the DataFrame by year")
            df.show(n=5, truncate=False)

        if verbose:
            print("Final result")
            df.show(n=20, truncate=False)

        return df
