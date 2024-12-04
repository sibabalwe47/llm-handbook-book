from datetime import datetime as dt
from pathlib import Path as pt
import click

import sys
import os

# Add the project root directory to the system path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from zenml.logger import get_logger

logger = get_logger(__name__)

# pipelines 
from pipelines.digital_data_etl import digital_data_etl

@click.command(
    help="""
LLM Engineering project CLI v0.0.1. 

Main entry point for the pipeline execution. 
This entrypoint is where everything comes together.

Run the ZenML LLM Engineering project pipelines with various options.

Run a pipeline with the required parameters. This executes
all steps in the pipeline in the correct order using the orchestrator
stack component that is configured in your active ZenML stack.

Examples:

  \b
  # Run the pipeline with default options
  python run.py
               
  \b
  # Run the pipeline without cache
  python run.py --no-cache
  
  \b
  # Run only the ETL pipeline
  python run.py --only-etl

"""
)
@click.option(
    "--no-cache",
    is_flag=True,
    default=False,
    help="Disable caching for the pipeline run.",
)
@click.option(
    "--run-end-to-end-data",
    is_flag=True,
    default=False,
    help="Whether to run all the data pipelines in one go.",
)
@click.option(
    "--run-etl",
    is_flag=True,
    default=False,
    help="Whether to run the ETL pipeline.",
)
@click.option(
    "--run-export-artifact-to-json",
    is_flag=True,
    default=False,
    help="Whether to run the Artifact -> JSON pipeline",
)
@click.option(
    "--etl-config-filename",
    default="digital_data_etl_paul_iusztin.yaml",
    help="Filename of the ETL config file.",
)
@click.option(
    "--run-feature-engineering",
    is_flag=True,
    default=False,
    help="Whether to run the FE pipeline.",
)
@click.option(
    "--run-generate-instruct-datasets",
    is_flag=True,
    default=False,
    help="Whether to run the instruct dataset generation pipeline.",
)
@click.option(
    "--run-generate-preference-datasets",
    is_flag=True,
    default=False,
    help="Whether to run the preference dataset generation pipeline.",
)
@click.option(
    "--run-training",
    is_flag=True,
    default=False,
    help="Whether to run the training pipeline.",
)
@click.option(
    "--run-evaluation",
    is_flag=True,
    default=False,
    help="Whether to run the evaluation pipeline.",
)
@click.option(
    "--export-settings",
    is_flag=True,
    default=False,
    help="Whether to export your settings to ZenML or not.",
)
def main(
    no_cache: bool = False,
    run_end_to_end_data: bool = False,
    run_etl: bool = True,
    etl_config_filename: str = "digital_data_etl_paul_iusztin.yaml",
    run_export_artifact_to_json: bool = False,
    run_feature_engineering: bool = False,
    run_generate_instruct_datasets: bool = False,
    run_generate_preference_datasets: bool = False,
    run_training: bool = False,
    run_evaluation: bool = False,
    export_settings: bool = False,
) -> None:
    """"""
    # pipeline args configuration
    pipeline_args = {
        "enable_cache": not no_cache
    }

    root_dir = pt(__file__).resolve().parent.parent

    run_args_etl = {}
    pipeline_args["config_path"] = root_dir / "configs" / etl_config_filename
    pipeline_args["run_name"] = f"digital_data_etl_run_{dt.now().strftime('%Y_%m_%d_%H_%M_%S')}"
    digital_data_etl.with_options(**pipeline_args)(**run_args_etl)
        

if __name__ == "__main__":
    main()