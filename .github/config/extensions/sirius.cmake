duckdb_extension_load(sirius
    DONT_LINK LOAD_TESTS
    GIT_URL https://github.com/mbrobbel/sirius
    GIT_TAG e429e7ea80dddf84d1de53d8d39734e822d44248
    INCLUDE_DIR src
    TEST_DIR test/sql
    SUBMODULES "duckdb;cucascade;substrait"
)
