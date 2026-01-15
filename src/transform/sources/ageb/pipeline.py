from pathlib import Path
from pyspark.sql import DataFrame
from src.transform.core.pipelines.batch_transformer import BatchTransformerPipeline
from src.io.path_resolver import resolve_output_path
from src.transform.core.io.bronze_reader import resolve_bronze_leaf_paths
from src.transform.sources.ageb.templates.tabular_sheet import normalize_and_melt

from src.transform.sources.ageb.mappings.energy_sources import (
    ENERGY_SOURCE_MAP,
    STRUCTURE_ENERGY_CONS_MAP,
    RENEWABLE_TYPE_MAP,
    TRANSPORT_FEC_MAP,
    EFFICIENCY_INDICATOR_MAP,
    CHP_5_1_PJ_METRIC_MAP,
    CHP_5_1_TWH_METRIC_MAP,
)


class AgebTransformerPipeline(BatchTransformerPipeline):
    def read_bronze_paths(self) -> dict[str, list[Path | str]]:
        bronze_paths: dict[str, list[Path | str]] = {}

        # Rewrite this contract so it returns list of paths

        for ds_name, ds in self.source.datasets.items():
            if not ds.enabled:
                continue

            # Here we have to add still the subtables there is an extra level here
            bronze_paths[ds_name] = resolve_bronze_leaf_paths(
                resolve_output_path(self.project_config, ds, layer="bronze")
            )

        return bronze_paths

    # This is gonna throw an error it is all right
    def read_bronze(self, bronze_path: Path) -> DataFrame:
        return self.spark.read.parquet(str(bronze_path))

    def apply_steps(self, ds_name: str, df: DataFrame, verbose=False) -> DataFrame:
        if ds_name == "evaluation_tables":
            sheet_name = df.select("_sheet_name").distinct().collect()[0][0]

            if verbose:
                print(f"\n === Aplying steps for {sheet_name} ===")

            if sheet_name in (
                "1.1",
                "1.2",
                "1.3",
                "2.1",
                "4.1",
                "6.1",
                "6.2",
                "6.3",
                "6.4",
                "6.6",
            ):
                df = normalize_and_melt(
                    sheet_name,
                    df=df,
                    drop_cols=["Unnamed: 38"],
                    value_col="energy_source",
                    replace_map=ENERGY_SOURCE_MAP,
                    filter_total=True,
                    verbose=verbose,
                )

            elif sheet_name == "2.2":
                df = normalize_and_melt(
                    sheet_name,
                    df=df,
                    drop_cols=["Unnamed: 38"],
                    value_col="energy_source",
                    replace_map=STRUCTURE_ENERGY_CONS_MAP,
                    filter_total=True,
                    verbose=verbose,
                )

            elif sheet_name == "3.1":
                df = normalize_and_melt(
                    sheet_name,
                    df=df,
                    drop_cols=["Unnamed: 38"],
                    value_col="energy_source",
                    replace_map=RENEWABLE_TYPE_MAP,
                    filter_total=True,
                    verbose=verbose,
                )

            elif sheet_name == "5.1":
                unit = df.select("Unit").distinct().collect()[0][0].lower()

                if unit == "twh":
                    df = normalize_and_melt(
                        sheet_name,
                        df=df,
                        drop_cols=["Unnamed: 38"],
                        value_col="energy_source",
                        replace_map=CHP_5_1_TWH_METRIC_MAP,
                        filter_total=True,
                        verbose=verbose,
                    )

                elif unit == "pj":
                    df = normalize_and_melt(
                        sheet_name,
                        df=df,
                        drop_cols=["Unnamed: 38"],
                        value_col="energy_source",
                        replace_map=CHP_5_1_PJ_METRIC_MAP,
                        filter_total=True,
                        verbose=verbose,
                    )

            elif sheet_name == "6.7":
                df = normalize_and_melt(
                    sheet_name,
                    df=df,
                    drop_cols=["Unnamed: 38"],
                    value_col="energy_source",
                    replace_map=TRANSPORT_FEC_MAP,
                    filter_total=True,
                    verbose=verbose,
                )

            elif sheet_name == "7.1":
                df = normalize_and_melt(
                    sheet_name,
                    df=df,
                    drop_cols=["Unnamed: 38"],
                    value_col="indicator",
                    replace_map=EFFICIENCY_INDICATOR_MAP,
                    filter_total=True,
                    verbose=verbose,
                )

        return df

    def write_silver(self, ds_name: str, df: DataFrame) -> None:
        ds = self.source.datasets[ds_name]
        silver_path = resolve_output_path(self.project_config, ds, layer="silver")
        (df.write.mode("append").partitionBy("table_id").parquet(str(silver_path)))
