import pytest
import duckdb

from datacontract.data_contract import DataContract
from datacontract.model.run import Run
from datacontract.lint import resolve
from datacontract.engines.soda.connections.duckdb_connection import get_duckdb_connection

def test_local_csv():
    data_contract_str = """dataContractSpecification: 0.9.3
id: my-data-contract-id
info:
  title: My Data Contract
  version: 0.0.1
servers:
  production:
    type: local
    format: csv
    path: ./fixtures/csv/data/sample_data.csv
    delimiter: ','
models:
  sample_data:
    description: Csv file with encoding ascii
    type: table
    fields:
      field_one:
        type: string
      field_two:
        type: integer
      field_three:
        type: string
"""
    data_contract = DataContract(data_contract_str=data_contract_str)
    run = data_contract.test()
    print(run)
    assert run.result == "passed"

def test_bad_names():
    data_contract_str = """dataContractSpecification: 1.1.0
id: my-data-contract-id
info:
  title: My Data Contract
  version: 0.0.1
servers:
  production:
    type: local
    format: csv
    path: ./fixtures/csv/data/{model}.csv
    delimiter: ','
models:
  3-bad-names:
    description: Csv file with encoding ascii
    type: table
    fields:
      field one:
        type: string
        required: true
        unique: true
      2 field:
        type: integer
        required: true
        unique: true
      field-3:
        type: string
        required: true
        unique: true
    """
    data_contract = DataContract(data_contract_str=data_contract_str)
    run = data_contract.test()
    print(run)
    assert run.result == "passed"

