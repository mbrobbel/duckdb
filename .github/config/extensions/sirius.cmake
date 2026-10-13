duckdb_extension_load(sirius
    LOAD_TESTS
    GIT_URL https://github.com/mbrobbel/sirius
    GIT_TAG b917b0a3939d675a402089e2f6cda2961638cb2f
    SOURCE_DIR sirius-duckdb
    INCLUDE_DIR sirius-duckdb/src/include
    TEST_DIR sirius-duckdb/test/sql
    SUBMODULES "duckdb;cucascade;substrait"
)
